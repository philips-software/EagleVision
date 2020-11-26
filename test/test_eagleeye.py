"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import os
import unittest
from unittest import mock
from pathlib import Path
from test.test_support import TestResource
from eaglevision.eaglevision import EagleVision
from eaglevision.eaglevision import create_parser


def check_create_parser(option, value):
    """ create a parser for command line input and return handle"""
    return create_parser([option, value])


class EagleVisionTestCase(unittest.TestCase):
    """ Class to test the eaglevision.py"""

    @classmethod
    def tearDown(cls):
        """"Deletes the generated files """
        if os.path.exists(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json")):
            os.remove(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))

    def test_cloc_eagle_orchestrate_cloc(self):
        """ Function to test the orchestrate_cloc """
        file = open(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"), "w")
        file.write(TestResource.json_in.replace('"run_cloc_metric":true', '"run_cloc_metric": true').
                   replace('"run_similarity":true', '"run_similarity":false').
                   replace('"run_extraction":true', '"run_extraction":false').
                   replace('"run_cyclomatic_complexity":true', '"run_cyclomatic_complexity":false'))
        file.close()
        eaglevisionobj = EagleVision(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))
        self.assertEqual(eaglevisionobj.json_path, os.path.join(Path(__file__).parent.parent,
                                                                "test_resource", "populate.json"))
        mocked_class = mock.Mock()
        with mock.patch('eaglevision.cloc_eagle.ClocEagle.orchestrate_cloc', mocked_class):
            eaglevisionobj.eaglewatch()
            self.assertTrue(mocked_class.called)

    def test_cyclomatic_eagle_orchestrate_cyclomatic(self):
        """ Function to test the orchestrate_cyclomatic """
        file = open(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"), "w")
        file.write(TestResource.json_in.replace('"run_cloc_metric":true', '"run_cloc_metric": false').
                   replace('"run_similarity":true', '"run_similarity":false').
                   replace('"run_extraction":true', '"run_extraction":false').
                   replace('"run_cyclomatic_complexity":true', '"run_cyclomatic_complexity":true'))
        file.close()
        eaglevisionobj = EagleVision(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))
        self.assertEqual(eaglevisionobj.json_path, os.path.join(Path(__file__).parent.parent,
                                                                "test_resource", "populate.json"))
        mocked_class = mock.Mock()
        with mock.patch('eaglevision.cyclomatic_eagle.CyclomaticEagle.orchestrate_cyclomatic', mocked_class):
            eaglevisionobj.eaglewatch()
            self.assertTrue(mocked_class.called)

    def test_similarity_eagle_orchestrate_similarity(self):
        """ Function to test the orchestrate_similarity """
        file = open(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"), "w")
        file.write(TestResource.json_in.replace('"run_cloc_metric":true', '"run_cloc_metric": false').
                   replace('"run_similarity":true', '"run_similarity":true').
                   replace('"run_extraction":true', '"run_extraction":false').
                   replace('"run_cyclomatic_complexity":true', '"run_cyclomatic_complexity":false'))
        file.close()
        eaglevisionobj = EagleVision(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))
        self.assertEqual(eaglevisionobj.json_path, os.path.join(Path(__file__).parent.parent,
                                                                "test_resource", "populate.json"))
        mocked_class = mock.Mock()
        with mock.patch('eaglevision.similarity_eagle.SimilarityEagle.orchestrate_similarity', mocked_class):
            eaglevisionobj.eaglewatch()
            self.assertTrue(mocked_class.called)

    def test_similarity_eagle_orchestrate_similarity_extraction(self):
        """ Function to test the orchestrate_similarity  only with extraction"""
        file = open(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"), "w")
        file.write(TestResource.json_in.replace('"run_cloc_metric":true', '"run_cloc_metric": false').
                   replace('"run_similarity":true', '"run_similarity":false').
                   replace('"run_extraction":true', '"run_extraction":true').
                   replace('"run_cyclomatic_complexity":true', '"run_cyclomatic_complexity":false'))
        file.close()

        eaglevisionobj = EagleVision(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))
        self.assertEqual(eaglevisionobj.json_path, os.path.join(Path(__file__).parent.parent,
                                                                "test_resource", "populate.json"))
        mocked_class = mock.Mock()
        with mock.patch('eaglevision.similarity_eagle.SimilarityEagle.orchestrate_similarity', mocked_class):
            eaglevisionobj.eaglewatch()
            self.assertTrue(mocked_class.called)

    def test_path(self):
        """ Function to test the path variable in the command line
        correct and incorrect """
        with self.assertRaises(SystemExit):
            check_create_parser("-p", "path_test")
        parsed = check_create_parser("--p", "path_test")
        self.assertEqual(parsed.path, "path_test")


if __name__ == '__main__':
    unittest.main()
