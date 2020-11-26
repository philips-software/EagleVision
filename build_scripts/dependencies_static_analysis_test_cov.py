"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
build script to building the similarity tool"""
import os
import sys
import platform
import subprocess
from subprocess_calls import call_subprocess
from install_dependencies import install_pip


def install_aspell():
    """
    Installs Aspell and configure for english
    """
    if str(platform.system()).upper() == "LINUX":
        call_subprocess("sudo apt-get update -qq")
        call_subprocess("sudo apt-get install --assume-yes aspell aspell-en")
        print("Stage Install aspell -- COMPLETED & PASSED --")
    else:
        print("Please install and configure Aspell for english")


def install_npm_packages():
    """
    Installs jscpd and configure for english
    """
    if str(platform.system()).upper() == "LINUX":
        call_subprocess("sudo npm install")
        call_subprocess("sudo npm install -g jscpd@3.2.1")
        call_subprocess("sudo npm i -g yaml-lint@1.2.4")
        call_subprocess("sudo npm i -g markdownlint-cli@0.23.1")
        call_subprocess("sudo npm i -g stylelint@13.6.1")
        call_subprocess("sudo npm i -g stylelint-config-standard@20.0.0")
        call_subprocess("sudo npm i -g cloc@2.6.0")
        print("Stage Install jscpd, markdownlint, stylelint & ymllint -- COMPLETED & PASSED --")
    else:
        print("Please install and configure jscpd, stylelint, markdownlint & ymllint")


def check_stylelint():
    """
    function check the repo for any python linting errors on css
    """
    call_subprocess("npx stylelint eaglevision/*.css")
    print("Stage linting CSS (stylelint)- -- COMPLETED & PASSED  --")


def check_lint():
    """
    function check the repo for any python linting errors
    """
    call_subprocess("python -m pylint eaglevision/ test/ build_scripts/ ")
    print("Stage linting -- COMPLETED & PASSED  --")


def check_yml_linting():
    """
    function check the repo for any yml linting errors
    """
    call_subprocess("yamllint -d relaxed .github/workflows/*.yml ")
    print("Stage linting yml -- COMPLETED & PASSED  --")


def check_md_linting():
    """
    function check the repo for any yml linting errors
    """
    call_subprocess("markdownlint *.md ")
    print("Stage linting md files -- COMPLETED & PASSED  --")


def check_code_duplication():
    """
    checks the repo for any duplicate or code code with 20 token and 10% allowed duplicate
    """
    call_subprocess('jscpd --min-tokens 20 --reporters "json" --mode "strict" --format "python" -o . .')
    call_subprocess("python build_scripts/jscpd_parser.py --j 10 ")
    print("Stage duplicate detection -- COMPLETED & PASSED  --")


def check_cyclomatic_complexity():
    """
    checks the repo for function with cyclomatic complexity , fails if value is greater than 6
    """
    call_subprocess("python -m lizard eaglevision test build_scripts -X> CC.xml")
    call_subprocess("python build_scripts/cyclo_gate.py --c 7")
    print("Stage cyclomatic complexity detection -- COMPLETED & PASSED  --")


def check_dead_code():
    """
    checks the repo for dead code with minimum confidence 70
    """
    call_subprocess("python -m vulture --min-confidence 70 "
                    "eaglevision test build_scripts whitelist.py")
    print("Stage dead code detection -- COMPLETED & PASSED  --")


def check_spelling():
    """
    check the repo for spelling errors
    """
    call_subprocess("python -m pyspelling")
    print("Stage spell checking -- COMPLETED & PASSED  --")


def test_coverage():
    """
    executes the tests and gates the coverage for greater than 95
    """
    call_subprocess('python -m pytest test --capture=sys --cov-config=.coveragerc --cov-report "html" '
                    '--cov=eaglevision')
    call_subprocess("coverage report --fail-under=95")
    call_subprocess("codecov")
    print("Stage test & coverage -- COMPLETED & PASSED --")


def mutation_pass_fail_check():
    """ Gates mutation test for 20 percentage """
    call_subprocess("mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut.xml")
    call_subprocess("python build_scripts/mutmut_parse.py --m 20")
    print("Stage mutation testing -- COMPLETED & PASSED  --")


def mutation_testing():
    """
    executes the mutation tests
    """
    working_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))
    retval = subprocess.call("python -m mutmut run ", shell=True, cwd=working_dir)
    if retval:
        if retval & 14:
            mutation_pass_fail_check()
        else:
            print("un expected error occurred while mutation test")
            sys.exit(1)
    else:
        mutation_pass_fail_check()


if __name__ == "__main__":
    install_pip()
    install_aspell()
    install_npm_packages()
    check_lint()
    check_stylelint()
    check_yml_linting()
    check_md_linting()
    check_code_duplication()
    check_cyclomatic_complexity()
    check_dead_code()
    check_spelling()
    test_coverage()
    mutation_testing()
