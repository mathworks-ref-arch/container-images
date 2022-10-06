#!/bin/sh
#
# Makes the file (passed as 1st arg) executable and runs it
#
# This script uses the following environment variables set by the submit MATLAB code:
# PARALLEL_SERVER_S3_BUCKET       - The S3 Bucket.
# PARALLEL_SERVER_S3_PREFIX       - The prefix under which the job's files are stored in the S3 bucket.
# PARALLEL_SERVER_JOB_LOCATION    - The job's storage location.
# PARALLEL_SERVER_TASK_ID_OFFSET  - The offset of the Task's ID relative to the value of AWS_BATCH_JOB_ARRAY_INDEX.

# Copyright 2020 The MathWorks, Inc.

# The first argument is the path to the job wrapper.
JOB_WRAPPER=${1}

if [ -n "${AWS_BATCH_JOB_ARRAY_INDEX}" ]; then
    # This is an array job.
    # The Task ID is equal to AWS_BATCH_JOB_ARRAY_INDEX + PARALLEL_SERVER_TASK_ID_OFFSET.
    TASK_ID=`expr ${AWS_BATCH_JOB_ARRAY_INDEX} + ${PARALLEL_SERVER_TASK_ID_OFFSET}`
else
    # This is not an array job.
    # The Task ID is equal to PARALLEL_SERVER_TASK_ID_OFFSET.
    TASK_ID=${PARALLEL_SERVER_TASK_ID_OFFSET}
fi
echo "Task ID is ${TASK_ID}"

# Export PARALLEL_SERVER_TASK_LOCATION because parallel.cluster.generic.independentDecodeFcn requires it.
export PARALLEL_SERVER_TASK_LOCATION="${PARALLEL_SERVER_JOB_LOCATION}/Task${TASK_ID}";

# Determine which input file to copy from S3 for this task.
LIST_INPUT_FILES_CMD="aws s3api list-objects-v2 --bucket ${PARALLEL_SERVER_S3_BUCKET} --prefix ${PARALLEL_SERVER_S3_PREFIX}/stageIn/${PARALLEL_SERVER_JOB_LOCATION}/Task --query 'Contents[].{Key: Key}' --output text"
echo "Listing all the task input files for this MATLAB job using the command ${LIST_INPUT_FILES_CMD}"
LIST_INPUT_FILES_OUTPUT=`eval ${LIST_INPUT_FILES_CMD}`

LIST_INPUT_FILES_EXIT_CODE=${?}
if [ ${LIST_INPUT_FILES_EXIT_CODE} -ne 0 ] ; then
    echo "Listing the task input files failed.  Exiting with code ${LIST_INPUT_FILES_EXIT_CODE}"
    exit ${LIST_INPUT_FILES_EXIT_CODE}
fi

GROUPED_TASK_INPUT_FILES=`echo ${LIST_INPUT_FILES_OUTPUT} | grep -e "Task[0-9]\+-[0-9]\+.in.mat" --only-matching`
SINGLE_TASK_INPUT_FILES=`echo ${LIST_INPUT_FILES_OUTPUT} | grep -e "Task[0-9]\+.in.mat" --only-matching`

for FILE in ${SINGLE_TASK_INPUT_FILES}
do
    if [ ${FILE} = "Task${TASK_ID}.in.mat" ] ; then
        INPUT_FILE_TO_DOWNLOAD=${FILE}
        break
    fi
done

if [ -z ${INPUT_FILE_TO_DOWNLOAD} ] ; then
    for FILE in ${GROUPED_TASK_INPUT_FILES}
    do
        # Extract the start and end ranges
        START_RANGE=`echo ${FILE} | grep -e "[0-9]\+" --only-matching | head -n 1`
        END_RANGE=`echo ${FILE} | grep -e "[0-9]\+" --only-matching  | tail -n 1`

        if [ ${TASK_ID} -ge ${START_RANGE} ] && [ ${TASK_ID} -le ${END_RANGE} ]; then
            INPUT_FILE_TO_DOWNLOAD=${FILE}
            break
        fi
    done
fi

if [ -z ${INPUT_FILE_TO_DOWNLOAD} ] ; then
    echo "We could not find an input file for this Task in S3.  Exiting with code 1"
    exit 1;
fi

echo "Determined the task input file for this task to be ${INPUT_FILE_TO_DOWNLOAD}."

# Copy input files from S3 to JobStorageLocation.
JOB_STORAGE_LOCATION="/usr/local/JobStorageLocation"
S3_COPY_CMD="aws s3 cp s3://${PARALLEL_SERVER_S3_BUCKET}/${PARALLEL_SERVER_S3_PREFIX}/stageIn ${JOB_STORAGE_LOCATION}/ \
--recursive \
--exclude \"${PARALLEL_SERVER_JOB_LOCATION}/Task*.*\" \
--include \"${PARALLEL_SERVER_JOB_LOCATION}/${INPUT_FILE_TO_DOWNLOAD}\""

echo "Copying files from S3 to JobStorageLocation using command: ${S3_COPY_CMD}"
eval ${S3_COPY_CMD}

S3_COPY_EXIT_CODE=${?}
if [ ${S3_COPY_EXIT_CODE} -ne 0 ] ; then
    echo "Copy of input files from S3 to JobStorageLocation failed.  Exiting with code ${S3_COPY_EXIT_CODE}"
    exit ${S3_COPY_EXIT_CODE}
fi

chmod +x ${JOB_WRAPPER}

echo "Executing the job wrapper script ${JOB_WRAPPER}"
$JOB_WRAPPER

# Store the exit code from the JobWrapper so we can exit with it later.
JOB_WRAPPER_EXIT_CODE=${?}

# Zip files up to transfer to S3.
ZIP_CMD="zip -jr ${JOB_STORAGE_LOCATION}/${PARALLEL_SERVER_TASK_LOCATION}.zip ${JOB_STORAGE_LOCATION}/${PARALLEL_SERVER_JOB_LOCATION}/* \
    -x \\*.in.mat \
    -x \\*independentJobWrapper.sh"
echo "Zipping task output files using command: ${ZIP_CMD}"
eval ${ZIP_CMD}

ZIP_CMD_EXIT_CODE=${?}
if [ ${ZIP_CMD_EXIT_CODE} -ne 0 ] ; then
    echo "Zipping task output files failed.  Exiting with exit code ${ZIP_CMD_EXIT_CODE}"
    exit ${ZIP_CMD_EXIT_CODE}
fi

# Copy zipped job output files to S3
S3_COPY_CMD="aws s3 cp ${JOB_STORAGE_LOCATION}/${PARALLEL_SERVER_TASK_LOCATION}.zip s3://${PARALLEL_SERVER_S3_BUCKET}/${PARALLEL_SERVER_S3_PREFIX}/stageOut/${PARALLEL_SERVER_TASK_LOCATION}.zip"
echo "Copying zipped output files from JobStorageLocation to S3 using command: ${S3_COPY_CMD}"
eval ${S3_COPY_CMD}

S3_COPY_EXIT_CODE=${?}
if [ ${S3_COPY_EXIT_CODE} -ne 0 ] ; then
    echo "Copy of output files from JobStorageLocation to S3 failed.  Exiting with exit code ${S3_COPY_EXIT_CODE}"
    exit ${S3_COPY_EXIT_CODE}
fi

echo "Exiting with the exit code received from the JobWrapper: ${JOB_WRAPPER_EXIT_CODE}"
exit ${JOB_WRAPPER_EXIT_CODE}
