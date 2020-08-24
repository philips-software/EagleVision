"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import os
import json
from pathlib import Path
import unittest
from unittest.mock import mock_open, Mock, patch
from test.test_support import TestResource
from eagleeye.base_eagle import BaseEagle


class EagleBaseTestCase(unittest.TestCase):
    """ Class to test the base_eagle.py """

    @classmethod
    def tearDown(cls):
        """"Deletes the generated files """
        if os.path.exists(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json")):
            os.remove(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))

    @staticmethod
    def test_validate_wrong_inputs_path__():
        """ Function to validate wrong path in json"""
        baseobj = BaseEagle()
        baseobj._proj_path = "random_path"
        with patch('sys.exit') as exit_mock:
            baseobj.__validate_inputs_path__()
            assert exit_mock.called

    @staticmethod
    def test_validate_inputs_path__():
        """ Function to validate right path in json"""
        baseobj = BaseEagle()
        baseobj._proj_path = Path(__file__).parent
        with patch('sys.exit') as exit_mock:
            baseobj.__validate_inputs_path__()
            assert not exit_mock.called

    def test_base_init(self):
        """ Function to test the base class default init """
        baseobj = BaseEagle()
        self.assertEqual(baseobj.input_dict, dict())
        self.assertEqual(baseobj._proj_path, None)
        self.assertEqual(baseobj._run_extraction, None)
        self.assertEqual(baseobj._run_similarity, None)
        self.assertEqual(baseobj._run_cloc_metric, None)
        self.assertEqual(baseobj._run_cyclomatic_complexity, None)
        self.assertEqual(baseobj._annotation, None)
        self.assertEqual(baseobj._pattern, None)
        self.assertEqual(baseobj._pattern_seperator, None)
        self.assertEqual(baseobj._delta, None)
        self.assertEqual(baseobj._exclude_extraction, None)
        self.assertEqual(baseobj._cyclo_exclude, None)
        self.assertEqual(baseobj._report_path, None)
        self.assertEqual(baseobj._cloc_args, None)
        self.assertEqual(baseobj._cyclo_args, None)
        self.assertEqual(baseobj._similarity_range, None)

    def test_set_get_class_var(self):
        """ Function to test the base class with a set init values """
        baseobj = BaseEagle()
        baseobj._proj_path = "random_path"
        self.assertEqual(baseobj.get_proj_path(), "random_path")
        baseobj._run_extraction = "_run_extraction"
        self.assertEqual(baseobj.get_run_extraction(), "SIMEXE")
        baseobj._run_similarity = "_run_similarity"
        self.assertEqual(baseobj.get_run_similarity(), "SIMEXE")
        baseobj._run_cloc_metric = "_run_cloc_metric"
        self.assertEqual(baseobj.get_run_cloc_metric(), "CLOCEXE")
        baseobj._run_cyclomatic_complexity = "_run_cyclomatic_complexity"
        self.assertEqual(baseobj.get_run_cyclomatic_complexity(), "CYCLOEXE")
        baseobj._annotation = "_annotation"
        self.assertEqual(baseobj.get_annotation(), "_annotation")
        baseobj._pattern = "_pattern"
        self.assertEqual(baseobj.get_pattern(), "_pattern")
        baseobj._pattern_seperator = "_pattern_seperator"
        self.assertEqual(baseobj.get_pattern_seperator(), "_pattern_seperator")
        baseobj._delta = "_delta"
        self.assertEqual(baseobj.get_delta(), "_delta")
        baseobj._exclude_extraction = "_exclude_extraction"
        self.assertEqual(baseobj.get_exclude_extraction(), "_exclude_extraction")
        baseobj._cyclo_exclude = "_cyclo_exclude"
        self.assertEqual(baseobj.get_cyclo_exclude(), "_cyclo_exclude")
        baseobj._report_path = "report_path"
        self.assertEqual(baseobj.get_report_path(), os.path.join("random_path", "EagleEyeReport"))
        baseobj._cloc_args = "_cloc_args"
        self.assertEqual(baseobj.get_cloc_args(), "_cloc_args")
        baseobj._cyclo_args = "_cyclo_args"
        self.assertEqual(baseobj.get_cyclo_args(), "_cyclo_args")
        baseobj._similarity_range = "_similarity_range"
        self.assertEqual(baseobj.get_similarity_range(), "_similarity_range")
        baseobj._run_similarity = None
        baseobj._run_cloc_metric = None
        baseobj._run_cyclomatic_complexity = None
        self.assertEqual(baseobj.get_run_similarity(), "")
        self.assertEqual(baseobj.get_run_cloc_metric(), "")
        self.assertEqual(baseobj.get_run_cyclomatic_complexity(), "")

    @staticmethod
    def test_validate_wrong_json_path__():
        """ Function to validate a wrong json path """
        baseobj = BaseEagle()
        with patch('sys.exit') as exit_mock:
            baseobj.validate_path_json("random_path")
            assert exit_mock.called

    @staticmethod
    def test_validate_json_path__():
        """ Function to validate a right json path """
        baseobj = BaseEagle()
        with patch('sys.exit') as exit_mock:
            baseobj.validate_path_json(Path(__file__))
            assert not exit_mock.called

    @patch("builtins.open", new_callable=mock_open,
           read_data=json.dumps({'name': 'John', 'shares': 100,
                                 'price': 1230.23}))
    def test_read_file_data(self, mock_file):
        """ Function to validate a json read """
        baseobj = BaseEagle()
        expected_output = {
            'name': 'John',
            'shares': 100,
            'price': 1230.23
        }

        baseobj.validate_path_json = Mock(return_value=True)
        actual_output = baseobj.read_json(os.path.join(Path(__file__).parent.parent, "test_resource", 'example.json'))
        mock_file.assert_called_with(os.path.join(Path(__file__).parent.parent, "test_resource", 'example.json'))
        self.assertEqual(expected_output, actual_output)

    def test_populate_data(self):
        """ Function to validate populate json data """
        TestResource.write_json("populate.json", TestResource.json_in)
        baseobj = BaseEagle()
        json_data = baseobj.read_json(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))
        baseobj.populate_data(json_data[0])
        self.assertEqual(os.path.normpath(baseobj._proj_path),
                         os.path.normpath(os.path.join(Path(__file__).parent.parent, "test_resource")))
        self.assertEqual(baseobj._run_extraction, True)
        self.assertEqual(baseobj._run_similarity, True)
        self.assertEqual(baseobj._run_cloc_metric, True)
        self.assertEqual(baseobj._run_cyclomatic_complexity, True)
        self.assertEqual(baseobj._annotation, "@test")
        self.assertEqual(baseobj._pattern, ['assert'])
        self.assertEqual(baseobj._pattern_seperator, ["("])
        self.assertEqual(baseobj._delta, 5)
        self.assertEqual(baseobj._exclude_extraction, "*.cpp")
        self.assertEqual(baseobj._cyclo_exclude, ["*.cpp", "*.java"])
        self.assertEqual(baseobj._cloc_args, "--exclude-dir=src --exclude-ext=*.cpp,*.java")
        self.assertEqual(baseobj._cyclo_args, "-l java  -l python")
        self.assertEqual(baseobj._similarity_range, "70,100")

    def test_specific_string_getters(self):
        """ Function to validate few json items when the input json is null """
        TestResource.write_json("populate.json", TestResource.json_in)
        baseobj = BaseEagle()
        json_data = baseobj.read_json(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))
        json_data[0]["run_similarity"] = None
        json_data[0]["run_extraction"] = None
        json_data[0]["run_cloc_metric"] = None
        json_data[0]["run_cyclomatic_complexity"] = None
        baseobj.populate_data(json_data[0])
        self.assertEqual(baseobj.get_run_similarity(), "")
        self.assertEqual(baseobj.get_run_extraction(), "")
        self.assertEqual(baseobj.get_run_cloc_metric(), "")
        self.assertEqual(baseobj.get_run_cyclomatic_complexity(), "")


if __name__ == '__main__':
    unittest.main()
