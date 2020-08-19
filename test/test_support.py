"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file holds the test resources for testing """

import os
from pathlib import Path


class TestResource:
    """This test class stores data required to test the functionality """
    tst_resource_folder = os.path.join(os.path.dirname(__file__), os.pardir, "test_resource")
    par_dir = os.path.join(os.path.dirname(__file__), os.pardir)
    input_json = {
        "path": "%s" % tst_resource_folder,
        "run_extraction": True,
        "run_similarity": True,
        "extraction_annotation": None,
        "extraction_delta": None,
        "extraction_exclude": "*.cpp",
        "pattern_match": ["assert"],
        "pattern_seperator": ["("],
        "similarity_range": "70,100",
        "run_cloc_metric": True,
        "cloc_args": "--exclude-dir=src --exclude-ext=*.cpp,*.java",
        "run_cyclomatic_complexity": True,
        "cyclo_args": "-l java  -l python",
        "cyclo_exclude": ["*.cpp", "*.java"]
    }

    report = os.path.join(tst_resource_folder, "EagleEyeReport")
    json_path = os.path.join(Path(__file__).parent.parent, "test_resource").replace("\\", "/")
    json_in = '[{\
                    "path": "%s",\
                    "run_extraction":true,\
                    "run_similarity":true,\
                    "extraction_annotation":"@test",\
                    "extraction_delta":5,\
                    "extraction_exclude":"*.cpp",\
                    "pattern_match":["assert"],\
                    "pattern_seperator":["("],\
                    "similarity_range":"70,100",\
                    "run_cloc_metric":true,\
                    "cloc_args":"--exclude-dir=src --exclude-ext=*.cpp,*.java",\
                    "run_cyclomatic_complexity":true,\
                    "cyclo_args":"-l java  -l python",\
                    "cyclo_exclude":["*.cpp","*.java"]\
                    }]' % json_path

    @staticmethod
    def write_json(name, json_in):
        """ Function to write a json file"""
        file = open(os.path.join(Path(__file__).parent.parent, "test_resource", name), "w")
        file.write(json_in)
        file.close()
