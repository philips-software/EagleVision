"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import os
import sys
import unittest
from unittest import mock
from io import StringIO
from test.test_support import TestResource
import pandas as pd
from pandas.util.testing import assert_frame_equal
from eagleeye.similarity_eagle import SimilarityEagle


class SimilarityEagleTestCase(unittest.TestCase):
    """ Class to test the Similarity_eagle.py"""

    @classmethod
    def tearDown(cls):
        filelist = [temp_f for temp_f in os.listdir(os.path.join(TestResource.report, "pattern_and_similarity_report"))]
        for temp_f in filelist:
            os.remove(os.path.join(TestResource.report, "pattern_and_similarity_report", temp_f))

    def setUp(self):
        """ Function used to setup the read the console out """
        self.held, sys.stdout = sys.stdout, StringIO()

    @staticmethod
    def dummy_dataf():
        """ Function which creates a dummy data frame for testing"""
        data_f = {
            "Uniq ID": [".cpp_BrowserProcessHandler", "cpp_BrowserProcessHandler"],
            "Code": ["BrowserProcessHandler::BrowserProcessHandler(jobject app_handler) \n{\n\
                    assertequal = app_handler\n}", "BrowserProcessHandler::~BrowserProcessHandler() {\
            base::AutoLock\
            lock_scope(router_cfg_lock_)\
            router_cfg_.clear()}"]
        }
        dataf = pd.DataFrame(data_f, columns=['Uniq ID', 'Code'])
        return dataf

    @staticmethod
    def empty_dataf():
        """ Function for testing purpose returns an empty dataframe"""
        return pd.DataFrame()

    def test__code_extraction__empty_dataframe_path(self):
        """ Function to test the report folder creation, empty extraction handling """
        similarityobj = SimilarityEagle()
        self.assertEqual(similarityobj.dataframe, None)
        self.assertEqual(similarityobj.report_path, None)

        TestResource.input_json["run_similarity"] = False
        mocked_class = mock.Mock()
        mocked_class.return_value = self.empty_dataf()

        with mock.patch('functiondefextractor.core_extractor.extractor', mocked_class):
            similarityobj.orchestrate_similarity(TestResource.input_json)
            out_str = (sys.stdout.getvalue().split('\n'))
            matches = [c for c in out_str if c in 'No functions are extracted. Data frame is empty. Recheck your ' \
                                                  'input arguments']
            if len(list(filter(None, matches))):  # pylint: disable= C1801
                self.assertEqual(list(filter(None, matches))[0], 'No functions are extracted. Data frame is empty. '
                                                                 'Recheck your input arguments')
            else:
                self.assertTrue(len(list(filter(None, matches))),
                                "mock is not called, no print seen")  # pylint: disable= C1801
            self.assertEqual(similarityobj.report_path, os.path.join(TestResource.report,
                                                                     "pattern_and_similarity_report"))
            self.assertTrue(mocked_class.called)

    def test__code_extraction_non_empty_df(self):
        """ Function to test the report folder creation, report file creation, non empty extraction handling """
        similarityobj = SimilarityEagle()
        TestResource.input_json["run_similarity"] = False
        mocked_class = mock.Mock()
        mocked_class.return_value = self.dummy_dataf()
        with mock.patch('functiondefextractor.core_extractor.extractor', mocked_class):
            similarityobj.orchestrate_similarity(TestResource.input_json)
            out_str = (sys.stdout.getvalue().split('\n'))
            matches = [c for c in out_str if
                       c in 'No functions are extracted. Data frame is empty. Recheck your input arguments']
            self.assertEqual(len(list(filter(None, matches))), 0)
            self.assertTrue(mocked_class.called)
            self.assertEqual(similarityobj.report_path,
                             os.path.join(TestResource.report, "pattern_and_similarity_report"))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "assertPivot")))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "assert_pattern")))
        actual_dataframe = pd.read_html(TestResource.get_result_file_name(
            "pattern_and_similarity_report", "assertPivot"))
        expected_dataframe = pd.read_html(os.path.join(TestResource.tst_resource_folder, "golden_assertPivot.html"))
        assert_frame_equal(actual_dataframe[0], expected_dataframe[0], "check  the assertion on html")
        actual_dataframe = pd.read_excel(TestResource.get_result_file_name(
            "pattern_and_similarity_report", "assert_pattern"), index_col=0)
        expected_dataframe = pd.read_excel(os.path.join(TestResource.tst_resource_folder,
                                                        "golden_assert_pattern.xlsx"), index_col=0)

        self.assertTrue(actual_dataframe['Uniq ID'].equals(expected_dataframe['Uniq ID']))
        self.assertTrue(actual_dataframe['Code'].equals(expected_dataframe['Code']))
        self.assertTrue(actual_dataframe['Count of assert in function'].
                        equals(expected_dataframe['Count of assert in function']))
        actual_dataframe['assert Statements'].replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"],
                                                      value=["", ""], regex=True, inplace=True)

        expected_dataframe['assert Statements'].replace(to_replace=[r"\\t|\\n|\\r", "\t|\n|\r"],
                                                        value=["", ""], regex=True, inplace=True)
        self.assertTrue(actual_dataframe['assert Statements'].equals(expected_dataframe['assert Statements']))

    def test__code_extraction_non_empty_df_no_pattern(self):
        """ Function to test the non empty extraction handling with out pattern an no similarity check"""
        similarityobj = SimilarityEagle()
        mocked_class = mock.Mock()
        mocked_class.return_value = self.dummy_dataf()
        with mock.patch('functiondefextractor.core_extractor.extractor', mocked_class):
            TestResource.input_json["pattern_match"] = None
            TestResource.input_json["run_similarity"] = False
            similarityobj.orchestrate_similarity(TestResource.input_json)
            out_str = (sys.stdout.getvalue().split('\n'))
            matches = [c for c in out_str if
                       c in 'The pattern input is expected to be list and should be of same length as pattern ' \
                            'separators']
            self.assertEqual(len(list(filter(None, matches))), 1)
            self.assertTrue(mocked_class.called)
            self.assertFalse(os.path.isfile(os.path.join(TestResource.report, "pattern_and_similarity_report",
                                                         "assertPivot.html")))
            self.assertFalse(os.path.isfile(os.path.join(TestResource.report, "pattern_and_similarity_report",
                                                         "assert_pattern.xlsx")))

    def test__code_extraction_non_empty_df_pattern_and_separator(self):
        """ Function to test the non empty extraction handling with out pattern and pattern separator and no similarity
        check"""
        similarityobj = SimilarityEagle()
        mocked_class = mock.Mock()
        mocked_class.return_value = self.dummy_dataf()
        with mock.patch('functiondefextractor.core_extractor.extractor', mocked_class):
            TestResource.input_json["pattern_match"] = ["assert", "print"]
            TestResource.input_json["pattern_seperator"] = ["(", None]
            TestResource.input_json["run_similarity"] = False
            similarityobj.orchestrate_similarity(TestResource.input_json)
            self.assertTrue(mocked_class.called)
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "assertPivot")))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "printPivot")))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "assert_pattern")))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "print_pattern")))

    def test_similarity_check_with_mock_extraction(self):
        """ Function to test the similarity check"""
        similarityobj = SimilarityEagle()
        mocked_class = mock.Mock()
        mocked_class.return_value = self.dummy_dataf()
        with mock.patch('functiondefextractor.core_extractor.extractor', mocked_class):
            TestResource.input_json["pattern_match"] = None
            TestResource.input_json["run_similarity"] = True
            TestResource.input_json["similarity_range"] = "0,100"
            similarityobj.orchestrate_similarity(TestResource.input_json)
            self.assertTrue(mocked_class.called)
            self.assertEqual(similarityobj.report_path, os.path.join(TestResource.report,
                                                                     "pattern_and_similarity_report"))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "similarity_recommendation_0")))
            self.assertTrue(os.path.isfile(TestResource.get_result_file_name(
                "pattern_and_similarity_report",
                "similarity_brief_report")))
            actual_dataframe = pd.read_excel(TestResource.get_result_file_name(
                "pattern_and_similarity_report", "similarity_recommendation_0"), index_col=0)
            expected_dataframe = pd.read_excel(os.path.join(TestResource.tst_resource_folder,
                                                            "golden_similarity_recommendation_0.xlsx"), index_col=0)
            self.assertTrue(actual_dataframe.equals(expected_dataframe))
            actual_dataframe = pd.read_html(TestResource.get_result_file_name("pattern_and_similarity_report",
                                                                              "similarity_brief_report"))
            expected_dataframe = pd.read_html(os.path.join(TestResource.tst_resource_folder,
                                                           "golden_similarity_brief_report.html"))
            assert_frame_equal(actual_dataframe[0], expected_dataframe[0])


if __name__ == '__main__':
    unittest.main()
