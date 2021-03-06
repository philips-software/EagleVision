"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import sys
import xml.etree.ElementTree as ETree
import argparse


def create_parser(args):
    """ Function which add the command line arguments required for the cyclomatic complexity report parser"""
    # Create the parser
    cyclo_parser = argparse.ArgumentParser(description="cyclomatic complexity gate Parser")

    # Add the arguments
    cyclo_parser.add_argument("--cyclo", metavar="--c", type=int, help="cyclo benchmark")
    return cyclo_parser.parse_args(args)


class CycloGate():
    """ Class to gate the cyclomatic complexity"""

    @staticmethod
    def get_index_cnn(root):
        """
        Function to parse the xml file generated by lizard for cyclomatic complexity to identify the index of CNN

        Parameters:
          root (etree node): root node of the parsed xml

        Returns:
        (int) index of CNN in the xml
        """
        count = 0
        val = None
        try:
            labels = root.find("labels")
            for label in labels.iter("label"):
                if str(label.text).upper() == str("CCN"):
                    val = count
                else:
                    count += 1
            return val
        except AttributeError:
            print("Guardrail unable to find the tag CCN in the report ")  # pragma: no mutate
            sys.exit(1)

    def get_all_func_cnn(self, root):
        """
        Function which create a dictionary with all functions in the parsed files/source with their CNN

        Parameters:
          root (etree node): root node of the parsed xml

        Returns:
        (dictionary) with list of function names and its Cyclomatic complexity

        """
        temp_val = []
        cyclo_dict = dict()
        index = self.get_index_cnn(root)
        try:
            functions = root.findall("item")
            for item in functions:
                for cnn in item.iter("value"):
                    temp_val.append(cnn)
                cyclo_dict[str(item.attrib["name"])] = temp_val[index].text
                temp_val = []
            if not cyclo_dict:
                print("Guardrail unable to find the tags item/value/name in the report file ")  # pragma: no mutate
                sys.exit(1)
            else:
                return cyclo_dict
        except KeyError:
            print("Guardrail unable to find the tags item/value/name in the report ")  # pragma: no mutate
            sys.exit(1)

    def parse_cyclo_report_xml(self, xml_file):
        """ Function used to fetch the necessary data from the xml output - lizard

        Parameters:
          xml_file (string): path to the xml file to be parsed

        Returns:
        (dictionary) with list of function names and its Cyclomatic complexity or None

        """
        try:
            root = ETree.parse(xml_file).getroot()
            for functions in root.iter("measure"):
                if functions.attrib['type'] == "Function":
                    print("successfully found functions with CNN")  # pragma: no mutate
                    return self.get_all_func_cnn(functions)
            return None

        except IOError:
            print("cc.xml report file path")  # pragma: no mutate
            sys.exit(1)
        except KeyError:
            print("tags required are not found in cc.xml report file path")  # pragma: no mutate
            sys.exit(1)

    @staticmethod
    def validate_return(val, message):
        """
        Function to validate the returns from subprocess

        Parameters:
          val (int): return value from subprocess
          message (string): message to be printed.

        Returns:
        sub-process return value.
        """

        if val:
            msg = "Guardrail, failed {}.".format(message)
            print(msg)  # pragma: no mutate
            sys.exit(val)
        else:
            msg = "Guardrail, passed {}.".format(message)
            print(msg)  # pragma: no mutate
            return


if __name__ == "__main__":
    ARGS = create_parser(sys.argv[1:])
    CYCLOGATEOBJ = CycloGate()
    COMPLEXITY = CYCLOGATEOBJ.parse_cyclo_report_xml("CC.xml")
    CYCLOCOMPLEX = [CYCLOCOMPLEX for CYCLOCOMPLEX in COMPLEXITY if int(COMPLEXITY.get(CYCLOCOMPLEX)) > ARGS.cyclo]
    CYCLOGATEOBJ.validate_return(len(CYCLOCOMPLEX), "Cyclomatic complexity")
