from flask import Flask, render_template, request, jsonify, send_from_directory
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


@app.route("/_execution_start", methods=["POST"])
def _execution_start():
    global tests_to_execute, execution_manager, execution_thread
    tests_to_execute = {"Tests": request.json['tests'], "parallel": request.json['tests'], "log": request.json['log']}
    execution_manager = ExecutionManager(tests=tests_to_execute, suites=suites)
    execution_thread = Thread(target=execution_manager.start)
    execution_thread.start()
    return jsonify(status="OK", tests=execution_manager.prepared_tests, redirect="/result")


@app.route("/result")
def result():
    global execution_manager
    return render_template("result.html", tests=execution_manager.prepared_tests)


@app.route("/_execution_status", methods=["GET"])
def _execution_status():
    global execution_manager, execution_thread
    if execution_thread.isAlive():
        return jsonify(tests=execution_manager.status, execution="running")
    else:
        execution_thread.join()
        return jsonify(tests=execution_manager.status, execution="done", log=execution_manager.log)


@app.route("/view-report/<log>")
def view_html_report(log):
    return send_from_directory("../RobotReports", log)


if __name__ == '__main__':
    app.run(debug=True)
