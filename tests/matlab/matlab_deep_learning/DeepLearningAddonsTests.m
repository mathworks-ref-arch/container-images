%   Copyright 2021-2024 The MathWorks, Inc.

classdef DeepLearningAddonsTests < matlab.unittest.TestCase
    % DEEPLEARNINGADDONSTESTS is developed for the MATLAB Deep Learning
    % Docker image.
    % DeepLearningAddonsTests checks that there are no extra toolboxes
    % available in the MATLAB Deep Learning Docker image.
    
    
    methods(Test)
        function testInstalledToolboxesMatchExpected( testCase )
            import matlab.unittest.constraints.IsSameSetAs
            
            % identifiers of the expected  toolboxes and support packages
            expectedIdentifier = ["DM",... % Parallel Computing Toolbox
                "GC",... % GPU Coder Toolbox
                "IP",... % Image Processing Toolbox
                "ME",... % MATLAB Coder Toolbox
                "NN",... % Deep Learning Toolbox
                "SG",... % Signal Processing Toolbox
                "ST",... % Statistic and Machine Learning Toolbox
                "TA",... % Text Analytics Toolbox
                "VP"];   % Computer Vision Toolbox
            
            if string(version('-release')) >= "2025a"
                expectedIdentifier = [expectedIdentifier, ...
                    "INCEPTIONRESNETV2", ... % "Deep Learning Toolbox Model for Inception-ResNet-v2 Network"
                    "CAFFEIMPORTER", ... % "Deep Learning Toolbox Importer for Caffe Models"
                    "INCEPTIONV3", ... % "Deep Learning Toolbox Model for Inception-v3 Network"
                    "RESNET101", ... % "Deep Learning Toolbox Model for ResNet-101 Network"
                    "ONNXCONVERTER", ... % "Deep Learning Toolbox Converter for ONNX Model Format"
                    "KERASIMPORTER", ... % "Deep Learning Toolbox Converter for TensorFlow models"
                    "GOOGLENET", ... % "Deep Learning Toolbox Model for GoogLeNet Network"
                    "ALEXNET", ... % "Deep Learning Toolbox Model for AlexNet Network"
                    "GPU_DEEPLEARNING_LIB", ... % "GPU Coder Interface for Deep Learning Libraries"
                    "RESNET18", ... % "Deep Learning Toolbox Model for ResNet-18 Network"
                    "RESNET50", ... % "Deep Learning Toolbox Model for ResNet-50 Network"
                    "ML_DEEPLEARNING_LIB", ... % "MATLAB Coder Interface for Deep Learning Libraries"
                    "AIVNV"]; % "Deep Learning Toolbox Verification Library"
            end

            installedToolboxIdentifiers = matlab.addons.installedAddons().Identifier;
            testCase.verifyThat(installedToolboxIdentifiers, IsSameSetAs(expectedIdentifier));
        end % testDesiredToolboxesAreInstalled
        
        function testInstalledSupportPackagesMatchExpected( testCase )
            import matlab.unittest.constraints.IsSameSetAs
            
            expectedSupportPackage = {
                'Deep Learning Toolbox Model for Inception-ResNet-v2 Network', ... % "INCEPTIONRESNETV2"
                'Deep Learning Toolbox Importer for Caffe Models', ... % "CAFFEIMPORTER"
                'Deep Learning Toolbox Model for Inception-v3 Network', ... % "INCEPTIONV3"
                'Deep Learning Toolbox Model for ResNet-101 Network', ... % "RESNET101"
                'Deep Learning Toolbox Converter for ONNX Model Format', ... % "ONNXCONVERTER"
                'Deep Learning Toolbox Converter for TensorFlow models', ... % "KERASIMPORTER"
                'Deep Learning Toolbox Model for GoogLeNet Network', ... % "GOOGLENET"
                'Deep Learning Toolbox Model for AlexNet Network', ... % "ALEXNET"
                'GPU Coder Interface for Deep Learning Libraries', ... % "GPU_DEEPLEARNING_LIB"
                'Deep Learning Toolbox Model for ResNet-18 Network', ... % "RESNET18"
                'Deep Learning Toolbox Model for ResNet-50 Network', ... % "RESNET50"
                'MATLAB Coder Interface for Deep Learning Libraries', ... % "ML_DEEPLEARNING_LIB"
                'Deep Learning Toolbox Verification Library', ... % "AIVNV"
                };
            
            installedSupportPackages = matlabshared.supportpkg.getInstalled();
            testCase.assertNotEmpty(installedSupportPackages)
            installedSupportPackageNames = {installedSupportPackages.Name};
            testCase.verifyThat(installedSupportPackageNames, ...
                IsSameSetAs(expectedSupportPackage));
        end % testInstalledSupportPackagesMatchExpected
    end % methods(Test)
end % classdef
