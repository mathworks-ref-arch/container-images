# !/bin/bash

# MATLAB_LICENSE_FILE is set by the action

# write the license file
mkdir -p $(dirname $LICENSE_FILE_PATH)
echo "# BEGIN--------------BEGIN--------------BEGIN" > $LICENSE_FILE_PATH
echo "SERVER ${HOSTNAME} ${MAC_ADDRESS//:} ${PORT}" >> $LICENSE_FILE_PATH
echo "DAEMON MLM ./MLM PORT=27100" >> $LICENSE_FILE_PATH
echo "${MATLAB_LICENSE_FILE}" >> $LICENSE_FILE_PATH
echo "# END-----------------END-----------------END" >> $LICENSE_FILE_PATH
