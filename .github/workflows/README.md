# Workflows in container-images

This repository uses workflows to build the Dockerfiles hosted in this repository and publish them to container registries. 

## Overview

There are 2 kinds of YML files used here:
1. `build-and-publish-docker-image.yml`, which specifies a reusable workflow, which MUST be called from a workflow configuration file.
2. Other YML files in the `.github/workflows` directory call this reusable-workflow.

Each of these workflows:
  a. Monitors a specific directory. For example, the file `matlab-deps-r2023a-ubuntu20.04.yml` monitors the directory `container-images/matlab-deps/r2023a/ubuntu20.04`
  b. Is triggered when changes are made to the directory it monitors. This should build and publish to the configured registries.

## Triggers and Scheduled Jobs

All workflows are scheduled to run on Monday at 00:00.
Workflows are also triggered when you push any changes to the directories with Dockerfiles.
Workflows can be manually triggered from the "Actions" tab.

## Directory structure

The container-images repository has the following folder structure:

The root folder lists the hosted container images, each of which is called the `BASE_IMAGE`:

1. matlab-deps
2. polyspace-deps
3. matlab-runtime-deps (From R2023b)

These folders list various releases of MATLAB, each of which is called the `MATLAB_RELEASE`:

1. r2019b
2. r2020a ... and so on

Each folder may list one or more OS flavours, each of which is called the `OS`:
1. aws-batch
2. ubi8 / ubi9
3. ubuntu20.04 / ubuntu22.04

Each of these folders should have a `Dockerfile` and some accompanying files:

1. Dockerfile
2. base-dependencies.txt
3. *.sh `(scripts)`

## Images Pushed to DockerHub:

### Tags created
The `MATLAB_RELEASE` is used to create two tags.
One starting with lower case `r` and another with upper case `R`:
1. The letter `r` in lower case in `MATLAB_RELEASE`. Here after called: `r_MATLAB_RELEASE`
2. The letter `R` is upper case in `MATLAB_RELEASE`. Here after called: `R_MATLAB_RELEASE`

The images pushed for each Dockerfile will use the following naming schema:
` mathworks/${BASE_IMAGE}:${r_MATLAB_RELEASE}-${OS} `
` mathworks/${BASE_IMAGE}:${R_MATLAB_RELEASE}-${OS} `

### Latest Tag
Every `BASE_IMAGE` needs a `MATLAB_RELEASE` & `OS` flavor that marks its `latest` image.
Set the variable `should_add_latest_tag` to `true` in the workflow file to specify which image should carry the `latest` tag.
**Note: Remember to set the variable to `false` when marking a new image as the `latest` one. **

Setting the `should_add_latest_tag` field to `true` in a workflow will push images without the OS specified in the tag:
` mathworks/${BASE_IMAGE}:${r_MATLAB_RELEASE} `
` mathworks/${BASE_IMAGE}:${R_MATLAB_RELEASE} `

For example: 
```yml
#matlab-deps-r2023a-ubuntu20.04.yml
...
    with:
        docker_build_context: './matlab-deps/r2023a/ubuntu20.04'
        base_image_name: mathworks/matlab-deps
        matlab_release_tag: 'r2023a'
        os_info_tag: 'ubuntu20.04'
        should_add_latest_tag: true
...
```
Will generate the following tags:
1. r2023a
1. R2023a
1. r2023a-ubuntu20.04
1. R2023a-ubuntu20.04
1. latest

## Workflow Description

Each workflow must set the following `inputs` to the `reusable-workflow`:
```YML
      docker_build_context:
        description: 'Relative path to folder with Dockerfile. Ex: ./matlab-deps/r2023a/ubuntu20.04 '
        required: true
        type: string
      base_image_name:
        description: 'Name of base image. Example: mathworks/matlab-deps'
        required: true
        type: string
      matlab_release_tag:
        description: 'Name of matlab release. Example: r2023a'
        required: true
        type: string
      os_info_tag:
        description: 'Allowed values: aws-batch, ubi8, ubi9, ubuntu20.04 ubuntu22.04'
        required: true
        type: string
      should_add_latest_tag:
        description: 'Specify if this image should also be tagged as latest'
        required: true
        type: boolean
```


Each `reusable-workflow` job consists of the following steps:

1. Check-out the repository into a GitHub Actions runner.
1. Setup Image Tags: Configures tags to have both Pascal & camel case tags (R2023a, r2023a)
1. Login to DockerHub Container Registry
1. Build the image & push 
1. If the variable "should_add_latest_tag" is present that an additional "latest" tag is added to the image.

----
Copyright 2023 The MathWorks, Inc.
----
