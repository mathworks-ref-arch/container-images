# Copyright 2021-2024 The MathWorks, Inc.

"""Run the tests for Docker images which can run in -vnc mode"""

import unittest

import docker
import testinfra
from pytools import helper


class TestVncMode(unittest.TestCase):
    """Test a Docker container when running in -vnc mode.

    Running a Docker container in -vnc mode will run the vnc and noVNC
    applications and connect them to the sockets 5901 and 6080.
    """

    @classmethod
    def setUpClass(cls):
        """Run the Docker container specifying the '-vnc' mode in command"""
        cls.client = docker.from_env()
        image_name = helper.get_image_name()
        cls.client.images.get(image_name)

        cls.container = cls.client.containers.run(
            image=image_name,
            detach=True,
            stdin_open=True,
            publish_all_ports=True,
            environment={"PASSWORD": "8charspw"},
            command="-vnc",
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)
        helper.wait_for_cmd_cont(cls.container, "vnc", 30)
        helper.wait_for_cmd_cont(cls.container, "noVNC", 30)

    @classmethod
    def tearDownClass(cls):
        """Stop and remove the Docker container"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ##################################################################################

    def test_sockets_active(self):
        """Test that the sockets are listening"""
        for socket in ["tcp://0.0.0.0:6080", "tcp://0.0.0.0:5901"]:
            with self.subTest(socketAddress=socket):
                self.assertTrue(self.host.socket(socket).is_listening)

    def test_password_is_set(self):
        """Test that the custom VNC password has been set correctly.

        We check that the (encrypted) content of ~/.vnc/passwd equals the output
        of
        `echo $CUSTOM_PASSWORD | vncpasswd -f`
        """

        self.assertEqual(
            self.host.run("echo '8charspw' | vncpasswd -f").stdout_bytes,
            self.host.file("/home/matlab/.vnc/passwd").content,
        )

    def test_vnc_active(self):
        """Test that there is an active VNC session"""
        vnc_port = str(5901)
        vnc_list_cmd = f"/usr/bin/vncserver -list -rbfport {vnc_port}"
        # run "vncserver -list -rbfport 5901" in the Docker container
        vnc_list_output = self.host.check_output(vnc_list_cmd)
        # the output of "vncserver -list -rbfport 5901" is a text containing a
        # tab-separated table, e.g.
        #
        # TigerVNC server sessions:
        #
        # X DISPLAY #     RFB PORT #      RFB UNIX PATH   PROCESS ID #    SERVER
        # 1               5901                            34              Xtigervnc
        #
        # table_lines will extract the lines in the table above (including the title line)
        table_lines = list(
            filter(lambda line: "\t" in line, vnc_list_output.split("\n"))
        )
        self.assertRegex(
            table_lines[-1],
            vnc_port,
            f"command {vnc_list_cmd} returned:\n{vnc_list_output}",
        )


##################################################################################

if __name__ == "__main__":
    unittest.main()
