import os
import secrets
from robot.parsing.model import TestData
from robot.parsing.populators import NoTestsFound
import ConfigurationHelper


class GetSuiteInfo:
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TESTS_DIR = os.path.join(PROJECT_DIR, ConfigurationHelper.parse_configuration_file())

    SUITE_NAME = "SuiteName"
    SUITE_ID = "SuiteID"
    SUITE_PATH = "SuitePath"
    SUITE_SHORT_PATH = "SuiteShortPath"
    SUITE_VARIABLES = "SuiteVariables"
    SUITE_TEST_NUMBERS = "SuiteTestNumbers"
    SUITE_TESTS = "Tests"
    TEST_NAME = "TestName"
    TEST_TAGS = "TestTags"
    TEST_DOCUMENTS = "TestDocs"
    TEST_STEPS = "TestSteps"
    TEST_ID = "TestID"

    @staticmethod
    def retrieve_all_tests():
        suites_data = []
        suites = [os.path.join(GetSuiteInfo.TESTS_DIR, f) for f in os.listdir(GetSuiteInfo.TESTS_DIR) if
                  f.endswith(".robot")]
        for suite_path in suites:
            try:
                suite_data = TestData(parent=None, source=suite_path)
            except NoTestsFound:
                data = {GetSuiteInfo.SUITE_PATH: suite_path,
                        GetSuiteInfo.SUITE_SHORT_PATH: GetSuiteInfo.get_short_path(suite_path)}
            else:
                variables = [{"VarName": v.name, "VarValue": v.value} for v in suite_data.variable_table.variables]
                tests, children = GetSuiteInfo.get_tests_for_suite(suite_path)
                data = {GetSuiteInfo.SUITE_NAME: suite_data.name,
                        GetSuiteInfo.SUITE_ID: secrets.token_hex(8),
                        GetSuiteInfo.SUITE_PATH: os.path.abspath(suite_data.source),
                        GetSuiteInfo.SUITE_SHORT_PATH: GetSuiteInfo.get_short_path(suite_path),
                        GetSuiteInfo.SUITE_VARIABLES: variables,
                        GetSuiteInfo.SUITE_TESTS: tests,
                        GetSuiteInfo.SUITE_TEST_NUMBERS: len(tests) if tests else 0}
            if data.get(GetSuiteInfo.SUITE_NAME) is not None:
                suites_data.append(data)
        return suites_data

    @staticmethod
    def get_tests_for_suite(path_to_suite: str = None, parent: TestData = None):
        """
        Args:
            path_to_suite: the string representation of path to x.robot file
            parent: suite type, used for children to recursively find all children
        Returns:
            list of all test cases in the suite and its children
        """
        try:
            tests_data = TestData(parent=parent, source=path_to_suite)
        except NoTestsFound:
            return [], []
        else:
            tests = []
            text_index = 0
            for test_case in tests_data.testcase_table:
                steps = getattr(tests_data.testcase_table.tests[text_index], "steps")
                steps = [{'step': step.name, "args": step.args} for step in steps if getattr(step, "name", None)]
                tests.append({GetSuiteInfo.TEST_NAME: test_case.name,
                              GetSuiteInfo.TEST_TAGS: test_case.tags.as_list()[1:],
                              GetSuiteInfo.TEST_DOCUMENTS: str(test_case.doc),
                              GetSuiteInfo.TEST_STEPS: steps,
                              GetSuiteInfo.TEST_ID: secrets.token_hex(nbytes=8)})
                text_index += 1
            children = [child.name for child in tests_data.children]
            return tests, children

    @staticmethod
    def get_short_path(abs_path_):
        parent = os.path.basename(os.path.dirname(abs_path_))
        child = os.path.basename(abs_path_)
        return f"../{parent}/{child}"


if __name__ == "__main__":
    from pprint import pprint
    GetSuiteInfo.TESTS_DIR = "../../Tests"
    suites_ = GetSuiteInfo.retrieve_all_tests()
    for suite_ in suites_:
        pprint(suite_)
        print("====================================================================")
        print("====================================================================")
