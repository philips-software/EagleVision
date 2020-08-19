"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import os
import sys
import unittest
from unittest import mock
from io import StringIO
from pathlib import Path
from test.test_support import TestResource
import pandas as pd
from eagleeye.cloc_eagle import ClocEagle


class ClocEagleTestCase(unittest.TestCase):
    """ Class to unit test the cloc_eagle.py"""

    @classmethod
    def tearDown(cls):
        """Deletes the generated files """
        if os.path.exists(os.path.join(TestResource.report, "cloc_report", "cloc.csv")):
            os.remove(os.path.join(TestResource.report, "cloc_report", "cloc.csv"))
        if os.path.exists(os.path.join(TestResource.report, "cloc_report", "cloc.cmd")):
            os.remove(os.path.join(TestResource.report, "cloc_report", "cloc.cmd"))
        if os.path.exists(os.path.join(TestResource.report, "cloc_report", "cloc-report.html")):
            os.remove(os.path.join(TestResource.report, "cloc_report", "cloc-report.html"))
        if os.path.exists(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json")):
            os.remove(os.path.join(Path(__file__).parent.parent, "test_resource", "populate.json"))

    def setUp(self):
        """ Function used to setup the read the console out """
        self.held, sys.stdout = sys.stdout, StringIO()

    @staticmethod
    def dummy_dataf():
        """ Function which creates a dummy data frame for testing"""
        data_f = {'files': [12, 2, 1, 1, 16],
                  'language': ["Python", "JSON", "C++", "DOS Batch", "SUM"],
                  'blank': [140, 0, 5, 0, 145],
                  'comment': [195, 0, 4, 0, 199],
                  'code': [714, 53, 32, 1, 800],
                  'TEST': ""
                  }
        dataf = pd.DataFrame(data_f, columns=['files', 'language', 'blank', 'comment', 'code', 'TEST'])
        Path(os.path.join(TestResource.report, "cloc_report")).mkdir(parents=True, exist_ok=True)
        dataf.to_csv(os.path.join(TestResource.report, "cloc_report", "cloc.csv"), index=False)
        return dataf

    @mock.patch('subprocess.call', autospec=True)
    def test_path(self, mock_subproc_call):
        """ Function to test the path setting """
        mock_subproc_call.return_value = True
        cloceagleobj = ClocEagle()
        cloceagleobj.orchestrate_cloc(TestResource.input_json)
        self.assertEqual(cloceagleobj.report_path, os.path.join(TestResource.report, "cloc_report"))

    @mock.patch('subprocess.call', autospec=True)
    def test_init_cmd_path(self, mock_subproc_call):
        """ Function to test the default init , command forming, and path creation"""
        mock_subproc_call.return_value = False
        self.dummy_dataf()
        cloceagleobj = ClocEagle()
        self.assertEqual(cloceagleobj.cmd, "")
        self.assertEqual(cloceagleobj.report_path, None)

        cloceagleobj.orchestrate_cloc(TestResource.input_json)

        self.assertEqual(cloceagleobj.cmd.replace("/", os.sep),
                         'cloc "%s" --csv --out="%s" --exclude-dir=src --exclude-ext=*.cpp,*.java' %
                         (TestResource.tst_resource_folder, os.path.join(TestResource.report,
                                                                         "cloc_report", "cloc.csv")))
        self.assertEqual(cloceagleobj.report_path, os.path.join(TestResource.report, "cloc_report"))
        self.assertTrue(mock_subproc_call.called)

    @mock.patch('subprocess.call', autospec=True)
    def test_cmd_file_generation_and_content(self, mock_subproc_call):
        """ Function to test the command file generation and the content verification"""
        mock_subproc_call.return_value = False
        cloceagleobj = ClocEagle()
        self.dummy_dataf()
        cloceagleobj.orchestrate_cloc(TestResource.input_json)
        f_cmd = open(os.path.join(TestResource.report, "cloc_report", "cloc.cmd"), "r")
        cmd_out = (f_cmd.readline())

        self.assertEqual(cmd_out.replace("/", os.sep).rstrip(),
                         'cloc "%s" --csv --out="%s" --exclude-dir=src --exclude-ext=*.cpp,*.java' %
                         (TestResource.tst_resource_folder, os.path.join(TestResource.report,
                                                                         "cloc_report", "cloc.csv")))
        self.assertTrue(mock_subproc_call.called)

    @mock.patch('subprocess.call', autospec=True)
    def test_report_file_generation_content(self, mock_subproc_call):
        """ Function to test the report file generation from the csv generated from command out """
        from pandas.util.testing import assert_frame_equal
        mock_subproc_call.return_value = False
        cloceagleobj = ClocEagle()
        self.dummy_dataf()
        cloceagleobj.orchestrate_cloc(TestResource.input_json)
        dataframe = pd.read_html(os.path.join(TestResource.report, "cloc_report", "cloc-report.html"))
        dataframe = pd.concat(dataframe)
        dataframe.drop(dataframe.columns[0], axis=1, inplace=True)
        dataframe_out = self.dummy_dataf()
        dataframe_out.drop(dataframe_out.columns[5], axis=1, inplace=True)
        assert_frame_equal(dataframe, dataframe_out)
        self.assertTrue(mock_subproc_call.called)
        self.assertEqual(True, os.path.isfile(os.path.join(TestResource.report, "cloc_report", "cloc.cmd")))
        self.assertEqual(True, os.path.isfile(os.path.join(TestResource.report, "cloc_report", "cloc-report.html")))
        self.assertEqual(True, os.path.isfile(os.path.join(TestResource.report, "cloc_report", "cloc.csv")))

    @mock.patch('subprocess.call', autospec=True)
    def test_cmd_with_no_arg_to_cmd(self, mock_subproc_call):
        """ Function to test the command when optional arguments are not passed """
        mock_subproc_call.return_value = False
        cloceagleobj = ClocEagle()
        self.dummy_dataf()
        data = {**TestResource.input_json, 'cloc_args': None, }
        cloceagleobj.orchestrate_cloc(data)
        f_cmd = open(os.path.join(TestResource.report, "cloc_report", "cloc.cmd"), "r")
        self.assertEqual(f_cmd.readline().replace("/", os.sep).rstrip(), 'cloc "%s" --csv --out="%s"' %
                         (TestResource.tst_resource_folder, os.path.join(TestResource.report, "cloc_report",
                                                                         "cloc.csv")))
        self.assertTrue(mock_subproc_call.called)

    @mock.patch('subprocess.call', autospec=True)
    def test_fail(self, mock_subproc_call):
        """ Function to test when the subprocess call fails"""
        mock_subproc_call.return_value = True
        cloceagleobj = ClocEagle()
        self.dummy_dataf()
        cloceagleobj.orchestrate_cloc(TestResource.input_json)
        out_str = (sys.stdout.getvalue().split('\n'))
        matches = [c for c in out_str if c in 'There was error while processing the sub process command']
        self.assertEqual(len(list(filter(None, matches))), 1)
        self.assertEqual(matches[0], 'There was error while processing the sub process command')
        self.assertEqual(False, os.path.isfile(os.path.join(TestResource.report, "cloc_report", "cloc-report.html")))


if __name__ == '__main__':
    unittest.main()
