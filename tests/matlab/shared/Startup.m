% Copyright 2022-2024 The MathWorks, Inc.

classdef Startup < matlab.unittest.TestCase
    % STARTUP is developed for the MATLAB Docker images.
    % Startup checks that the startup.m script is functioning correctly.
    % It checks that the environment variables for the proxy host, port,
    % username and password are correctly set in MATLAB Docker image container
    % when specified using the docker -e command.
    
    properties
        WebSettings;
    end
    
    methods (TestMethodSetup)
        
        function getWebSettings(testCase)
            s = settings;
            testCase.WebSettings = s.matlab.web;
        end
        
    end
    
    methods (Test)
        
        function testHostIsSet(testCase)
            expectedHost = getenv('MW_PROXY_HOST');
            testCase.assertNotEmpty(expectedHost);
            actualHost = testCase.WebSettings.ProxyHost.ActiveValue;
            testCase.verifyEqual(expectedHost, actualHost)
        end
        
        function testPortIsSet(testCase)
            expectedPort = getenv('MW_PROXY_PORT');
            testCase.assertNotEmpty(expectedPort);
            actualPort = testCase.WebSettings.ProxyPort.ActiveValue;
            testCase.verifyEqual(expectedPort, actualPort);
        end
        
        function testProxyUsernameIsSet(testCase)
            expectedUserName = getenv('MW_PROXY_USERNAME');
            testCase.assertNotEmpty(expectedUserName);
            actualUserName = testCase.WebSettings.ProxyUsername.ActiveValue;
            testCase.verifyEqual(expectedUserName, actualUserName);
        end
        
        function testProxyPasswordIsSet(testCase)
            expectedPassword = getenv('MW_PROXY_PASSWORD');
            testCase.assertNotEmpty(expectedPassword);
            actualPassword = testCase.WebSettings.ProxyPassword.ActiveValue;
            testCase.verifyEqual(expectedPassword, actualPassword);
        end
        
    end
    
end
