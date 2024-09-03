%   Copyright 2021-2024 The MathWorks, Inc.

classdef AvailableProductsTest < matlab.unittest.TestCase
    % AVAILABLEPRODUCTSTEST is developed for the MATLAB Docker images.
    % AvailableProductsTest checks that there are no extra toolboxes available in
    % the MATLAB Docker image distribution.
    
    methods(Test)
        function testOnlyMATLABisInstalled( testCase )
            installedAddons= matlab.addons.installedAddons();
            testCase.verifyEmpty(installedAddons);
        end % testOnlyMATLABisInstalled


    end % methods(Test)
end % classdef
