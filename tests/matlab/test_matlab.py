# Copyright 2021-2024 The MathWorks, Inc.

"""Run the tests for the mathworks/matlab image"""

from .matlab.run_AvailableProductsTest import Run_AvailableProductsTest
from .matlab.test_ddux import TestDDUX
from .shared.run_startup import Run_Startup_Test
from .shared.test_matlab_docker_batch import TestBatchMode
from .shared.test_matlab_docker_shell import TestBasicFeatures
from .shared.test_matlab_docker_vnc import TestVncMode
from .shared.test_matlab_proxy_integration import (
    TestMatlabProxyInteg,
    TestMatlabProxyIntegAdvanced,
    TestMatlabProxyIntegNoLic,
)
from .shared.test_msh_integration import TestMSHIntegration
from pytools.test_suite_launcher import TestSuite

################################################################################

if __name__ == "__main__":
    TestSuite(
        TestDDUX,
        TestMSHIntegration,
        TestBatchMode,
        TestBasicFeatures,
        TestVncMode,
        TestMatlabProxyInteg,
        TestMatlabProxyIntegAdvanced,
        TestMatlabProxyIntegNoLic,
        Run_AvailableProductsTest,
        Run_Startup_Test,
    ).run()
