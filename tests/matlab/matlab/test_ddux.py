# Copyright 2021-2024 The MathWorks, Inc.

"""Run the tests to check for DDUX information set in the image"""

import unittest

from shared import test_ddux


class TestDDUX(test_ddux.TestDDUX):
    """Test the DDUX information set when running the container"""

    def get_tag_value_pairs(self):
        """Override this method in subclasses to provide different tag-value pairs"""
        return {
            "MW_CONTEXT_TAGS": "MATLAB:DOCKERHUB:V1",
            "MHLM_CONTEXT": "MATLAB_DOCKERHUB",
        }


################################################################################


if __name__ == "__main__":
    unittest.main()
