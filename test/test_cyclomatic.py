"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import os
import sys
import unittest
from unittest import mock
from io import StringIO
from pathlib import Path
from test.test_support import TestResource
import pandas as pd
import numpy as np
from eagleeye.cyclomatic_eagle import CyclomaticEagle


class CycloEagleTestCase(unittest.TestCase):
    """ Class to unit test the cyclomatic_eagle.py"""

    @classmethod
    def tearDown(cls):
        """"Deletes the generated files """
        if os.path.exists(os.path.join(TestResource.report, "cyclomatic_report", "cyclomatic-complexity.csv")):
            os.remove(os.path.join(TestResource.report, "cyclomatic_report", "cyclomatic-complexity.csv"))
        if os.path.exists(os.path.join(TestResource.report, "cyclomatic_report", "cyclomatic-complexity-report.html")):
            os.remove(os.path.join(TestResource.report, "cyclomatic_report", "cyclomatic-complexity-report.html"))
        if os.path.exists(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json")):
            os.remove(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))

    def setUp(self):
        """ Function used to setup the read the console out """
        self.held, sys.stdout = sys.stdout, StringIO()

    @staticmethod
    def dummy_dataf():
        """ Function which creates a dummy data frame for testing"""
        data_f = {
            'NLOC': [3, 13, 19, 5],
            'CCN': [1, 3, 5, 1],
            'Token': [20, 115, 161, 30],
            'Param': [1, 3, 2, 1],
            'Length': [3, 18, 24, 5],
            'Location': ['PhoenixTestApplication::main@9-11PhoenixTestApplication.java',
                         'ExtentReporterNG::generateReport@24-41@ExtentReporterNG.java',
                         'ExtentReporterNG::buildTestNodes@43-66@ExtentReporterNG.java',
                         'ExtentReporterNG::getTime@68-72@ExtentReporterNG.java'],
            'Path': ['Random path', 'Random path', 'Random path', 'Random path'],
            'Function': ['Random function', 'Random function', 'Random function', 'Random function'],
            'Args': ['Random arg', 'Random arg', 'Random arg', 'Random arg'],
            'Row': [3, 13, 19, 5],
            'Col': [1, 3, 5, 1]
        }
        dataf = pd.DataFrame(data_f, columns=["NLOC", "CCN", "Token", "Param", "Length", "Location",
                                              "Path", "Function", "Args", "Row", "Col"])
        Path(os.path.join(TestResource.report, "cyclomatic_report")).mkdir(parents=True, exist_ok=True)
        dataf.to_csv(os.path.join(TestResource.report, "cyclomatic_report",
                                  "cyclomatic-complexity.csv"), index=False, header=None)
        return dataf

    @mock.patch('subprocess.call', autospec=True)
    def test_path(self, mock_subproc_call):
        """ Function to test the path setting """
        mock_subproc_call.return_value = True
        cycloeagleobj = CyclomaticEagle()
        cycloeagleobj.orchestrate_cyclomatic(TestResource.input_json)
        cycloeagleobj.orchestrate_cyclomatic(TestResource.input_json)
        self.assertEqual(cycloeagleobj.report_path, os.path.join(TestResource.report, "cyclomatic_report"))
        self.assertTrue(mock_subproc_call.called)

    @mock.patch('subprocess.call', autospec=True)
    def test__init_cmd_path(self, mock_subproc_call):
        """ Function to test the default init , command forming, and path creation"""
        mock_subproc_call.return_value = False
        self.dummy_dataf()
        cycloeagleobj = CyclomaticEagle()

        self.assertEqual(cycloeagleobj.cmd, "")
        self.assertEqual(cycloeagleobj.report_path, None)

        cycloeagleobj.orchestrate_cyclomatic(TestResource.input_json)

        self.assertEqual(cycloeagleobj.cmd.replace("/", os.sep),
                         'python -m lizard "%s" -l java  -l python  -x "*.cpp", -x "*.java" --csv' %
                         TestResource.tst_resource_folder)
        self.assertEqual(cycloeagleobj.report_path, os.path.join(TestResource.report, "cyclomatic_report"))
        self.assertTrue(mock_subproc_call.called)

    def test_report_file_generation_content(self):
        """ Function to test the report file generation from the csv generated from command out """
        cycloeagleobj = CyclomaticEagle()
        self.dummy_dataf()
        with mock.patch.object(CyclomaticEagle, '_CyclomaticEagle__subprocess_out', return_value=False):
            mock.return_value = False
            cycloeagleobj.orchestrate_cyclomatic(TestResource.input_json)

            self.assertEqual(True, os.path.isfile(os.path.join
                                                  (TestResource.report, "cyclomatic_report",
                                                   "cyclomatic-complexity-report.html")))
            self.assertEqual(True, os.path.isfile(os.path.join
                                                  (TestResource.report, "cyclomatic_report",
                                                   "cyclomatic-complexity.csv")))
            data_frame = pd.read_html(
                os.path.join(TestResource.report, "cyclomatic_report", "cyclomatic-complexity-report.html"))
            data_frame = pd.concat(data_frame)
            data_frame.drop(data_frame.columns[0], axis=1, inplace=True)
            data_frame_report = self.dummy_dataf()
            data_frame_report.columns = ["NLOC", "CCN", "Token", "Param", "Length", "Location",
                                         "Path", "Function", "Args", "Row", "Col"]
            data_frame_report.sort_values('CCN', ascending=False, inplace=True)
            data_frame_report.drop(['Path', 'Function', 'Row', 'Col'], axis=1, inplace=True)
            self.assertTrue(np.array_equal(data_frame.values, data_frame_report.values))

    @mock.patch('subprocess.call', autospec=True)
    def test_cmd_no_exclude(self, mock_subproc_call):
        """ Function to verify the command generation with out excludes """
        mock_subproc_call.return_value = False
        cycloeagleobj = CyclomaticEagle()
        data = {**TestResource.input_json, 'cyclo_exclude': [None]}
        cycloeagleobj.orchestrate_cyclomatic(data)
        self.assertTrue(mock_subproc_call.called)
        self.assertEqual(cycloeagleobj.cmd.replace("/", os.sep),
                         'python -m lizard "%s" -l java  -l python  --csv' %
                         TestResource.tst_resource_folder)

    @mock.patch('subprocess.call', autospec=True)
    def test_cmd_no_args(self, mock_subproc_call):
        """ Function to verify the command generation with out arguments """
        mock_subproc_call.return_value = False
        cycloeagleobj = CyclomaticEagle()
        data = {**TestResource.input_json, 'cyclo_args': None, }
        cycloeagleobj.orchestrate_cyclomatic(data)
        self.assertTrue(mock_subproc_call.called)
        self.assertEqual(cycloeagleobj.cmd.replace("/", os.sep),
                         'python -m lizard "%s"   -x "*.cpp", -x "*.java" --csv' %
                         TestResource.tst_resource_folder)

    @mock.patch('subprocess.call', autospec=True)
    def test_fail(self, mock_subproc_call):
        """ Function to test the  subprocess command fail """
        mock_subproc_call.return_value = True
        cycloeagleobj = CyclomaticEagle()
        cycloeagleobj.orchestrate_cyclomatic(TestResource.input_json)
        out_str = (sys.stdout.getvalue().split('\n'))
        matches = [c for c in out_str if c in 'There was error while processing the sub process command']
        self.assertEqual(matches[0], 'There was error while processing the sub process command')
        self.assertEqual(False, os.path.isfile(os.path.join(TestResource.report,
                                                            "cyclomatic_report", "cyclomatic-complexity-report.html")))


if __name__ == '__main__':
    unittest.main()
