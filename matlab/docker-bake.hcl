# Copyright 2024 The MathWorks, Inc.

# General Configuration variables

variable "LATEST_RELEASE" {
  default = "R2024a"
}

variable "MATLAB_RELEASE" {
  default = "${LATEST_RELEASE}"
}

variable "MPM_ADDITIONAL_FLAGS" {
  default = ""
}

variable "MATLAB_DEPS_IMAGE" {
  default = "mathworks/matlab-deps"
}

variable "APT_ADDITIONAL_PACKAGES" {
  default = ""
}

variable "MATHWORKS_SERVICE_HOST_INSTALL_URL" {
  default = "https://www.mathworks.com/MathWorksServiceHost/glnxa64/install_managed_msh.sh"
}

variable "common_args" {
  default = {
    MATLAB_DEPS_IMAGE = "${MATLAB_DEPS_IMAGE}"
    MATLAB_RELEASE = "${MATLAB_RELEASE}"
    MPM_ADDITIONAL_FLAGS = "${MPM_ADDITIONAL_FLAGS}"
    APT_ADDITIONAL_PACKAGES = "${APT_ADDITIONAL_PACKAGES}"
    MATHWORKS_SERVICE_HOST_INSTALL_URL = "${MATHWORKS_SERVICE_HOST_INSTALL_URL}"
  }
}

# Deep learning specific configuration

variable "DEEP_LEARNING_TOOLBOXES" {
  default = "Computer_Vision_Toolbox GPU_Coder Image_Processing_Toolbox MATLAB_Coder Deep_Learning_Toolbox Parallel_Computing_Toolbox Signal_Processing_Toolbox Statistics_and_Machine_Learning_Toolbox Text_Analytics_Toolbox"
}

variable "DEEP_LEARNING_SPKGS" {
  default = "Deep_Learning_Toolbox_Model_for_AlexNet_Network Deep_Learning_Toolbox_Model_for_GoogLeNet_Network Deep_Learning_Toolbox_Model_for_Inception-ResNet-v2_Network Deep_Learning_Toolbox_Model_for_Inception-v3_Network Deep_Learning_Toolbox_Model_for_ResNet-101_Network Deep_Learning_Toolbox_Model_for_ResNet-18_Network Deep_Learning_Toolbox_Model_for_ResNet-50_Network Deep_Learning_Toolbox_Verification_Library Deep_Learning_Toolbox_Importer_for_Caffe_Models Deep_Learning_Toolbox_Converter_for_TensorFlow_models GPU_Coder_Interface_for_Deep_Learning_Libraries MATLAB_Coder_Interface_for_Deep_Learning_Libraries Deep_Learning_Toolbox_Converter_for_ONNX_Model_Format"
}

# Metadata overrides

variable "REPOSITORY" {
  default = "mathworks"
}

variable "CUSTOM_TAG" {
  default = ""
}

# Set up auto tagging

function "with_custom_tags" {
  params = [image, release]
  result = [
    "${REPOSITORY}/${image}:${release}-${CUSTOM_TAG}",
    "${REPOSITORY}/${image}:${lower("${release}")}-${CUSTOM_TAG}",
  ]
}

function "standard_tags" {
  params = [image, release]
  result = [
    "${REPOSITORY}/${image}:${release}",
    "${REPOSITORY}/${image}:${lower("${release}")}",
    equal("${release}","${LATEST_RELEASE}") ? "${REPOSITORY}/${image}:latest": "",
  ]
}

function "tags" {
  params = [image, release]
  result = equal("${CUSTOM_TAG}", "") ? standard_tags(image, release) : with_custom_tags(image, release)
}

group "default" {
  targets = ["matlab"]
}

group "all" {
  targets = [
    "matlab",
    "matlab-deep-learning",
    ]
}

# Target for mathworks/matlab
target "matlab" {
  context = "."
  dockerfile = "Dockerfile"
  target = "matlab"
  args = common_args
  tags = tags("matlab", "${MATLAB_RELEASE}")
  platforms = ["linux/amd64"]
}

# Target for mathworks/matlab-deep-learning
target "matlab-deep-learning" {
  context = "."
  dockerfile = "Dockerfile"
  target = "matlab-deep-learning"
  tags = tags("${"matlab-deep-learning"}", "${MATLAB_RELEASE}")
  args = merge(common_args, {
    ADDITIONAL_PRODUCTS = "${DEEP_LEARNING_TOOLBOXES} ${DEEP_LEARNING_SPKGS}"
  })
   platforms = ["linux/amd64"]
}
