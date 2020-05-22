import os
import sys
import json
sys.path.append(os.path.abspath(".."))
import configuration
from ExecuteTests import ExecuteRobotTests
from RobotListeners.TestOverviewListener import RobotOverviewListener


class GetSuiteInfoByDryrun:
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TESTS_DIR = os.path.join(PROJECT_DIR, configuration.SUITES_DIR)

    @staticmethod
    def retrieve_all_tests():
        suites_paths = [os.path.join(GetSuiteInfoByDryrun.TESTS_DIR, f) for f in
                        os.listdir(GetSuiteInfoByDryrun.TESTS_DIR) if f.endswith(".robot")]

        listener = RobotOverviewListener()
        runner = ExecuteRobotTests()
        options = {"listener": listener, "dryrun": "yes", "log": None, "output": None, "report": None}
        runner.execute(suites_paths, options=options)
        return listener.suites


if __name__ == "__main__":
    data = GetSuiteInfoByDryrun.retrieve_all_tests()
    with open("gettests.json", "w") as jf:
        json.dump(data, jf)
