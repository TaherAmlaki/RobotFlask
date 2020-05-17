from flask import Flask, render_template, request, jsonify
from threading import Thread
from MyRobotRunners.GetTests import GetSuiteInfo
from MyRobotRunners.ExecuteTestArray import ExecutionManager


app = Flask(__name__)
suites = None
tests_to_execute = None
execution_manager = None
execution_thread = None


@app.route("/")
@app.route("/home")
def home():
    global suites
    suites = GetSuiteInfo.retrieve_all_tests()
    suite_test_numbers = sum([suite["SuiteTestNumbers"] for suite in suites])
    return render_template('home.html', suites=suites, test_numbers=suite_test_numbers)


@app.route("/execute", methods=["GET", "POST"])
def execute_page():
    global tests_to_execute, execution_manager, execution_thread
    if request.method == "POST":
        tests_to_execute = {'Tests': request.json['Tests']}
        execution_manager = ExecutionManager(tests=tests_to_execute, suites=suites)
        execution_thread = Thread(target=execution_manager.start)
        execution_thread.start()
    return render_template("execute.html", tests=tests_to_execute)


@app.route("/_execution_python", methods=["GET"])
def _execution_python():
    global execution_manager, execution_thread
    if execution_thread.isAlive():
        return jsonify(execution_manager.get_status())
    else:
        execution_thread.join()
        res = execution_manager.get_status().copy()
        res['execution'] = 'done'
        return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
