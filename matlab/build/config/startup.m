% Copyright 2024 The MathWorks, Inc.

function startup

% Setup default proxy settings based on the environment variables that
% are set in the run.sh script.
host = getenv('MW_PROXY_HOST');
port = getenv('MW_PROXY_PORT');
if ~isempty(host) && ~isempty(port)
    matlab.net.internal.copyProxySettingsFromEnvironment();
end

end
