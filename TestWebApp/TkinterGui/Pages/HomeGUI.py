import tkinter as tk
import tkinter.ttk as ttk
from TkinterGui.Pages.PageName import PAGE


class RobotMainFrame(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent)
        self._controller = controller
        self._suites_data = kwargs.get("suites_data", [])
        self._dh = 0.02
        self._h = 0.15

        self._suite_canvas = tk.Canvas(self, bg="black")
        self._suite_canvas.place(bordermode=tk.INSIDE, relx=0, rely=0, relwidth=0.5, relheight=1.0)
        self._tests_canvas = tk.Canvas(self, bg="black")
        self._tests_canvas.place(bordermode=tk.INSIDE, relx=0.5, rely=0, relwidth=0.5, relheight=1.0)

        self.suites_widgets = {}
        self.tests_widgets = {}
        self._build()

    def _build(self):
        ind = 0
        for suite in self._suites_data:
            number_of_tests = len(suite.get('Tests', []))
            text = "{:<30}".format(suite['SuiteName']) + f"--{number_of_tests} Tests"
            suite_id = suite['SuiteID']
            btn = ttk.Button(self._suite_canvas, text=text,  style="TButton",
                             command=lambda t=suite_id: self._suite_btn_clicked(t))
            btn.place(bordermode=tk.INSIDE, relx=0.15, rely=(ind * (self._dh + self._h) + self._dh), relwidth=0.7, relheight=self._h)
            self.suites_widgets[suite_id] = btn
            ind += 1

    def _suite_btn_clicked(self, suite_id):
        for id_, btn in self.suites_widgets.items():
            if id_ == suite_id:
                self.suites_widgets[id_].config(state=tk.DISABLED)
                self.tests_widgets = {}
                for widget in self._tests_canvas.winfo_children():
                    widget.destroy()

                tests = next(filter(lambda s: s['SuiteID'] == id_, self._suites_data))['Tests']
                ind = 0
                for test in tests:
                    number_of_steps = len(test.get('TestSteps', []))
                    text = "{:<30}".format(test['TestName']) + f"--{number_of_steps} Steps"
                    test_id = test['TestID']
                    btn = ttk.Button(self._tests_canvas, text=text, style="TButton",
                                     command=lambda t=test_id: self._test_btn_clicked(t))
                    btn.place(bordermode=tk.INSIDE, relx=0.15, rely=(ind * (self._dh + self._h) + self._dh), relwidth=0.7, relheight=self._h)
                    self.tests_widgets[test_id] = btn
                    ind += 1
                self.master.update()
            else:
                self.suites_widgets[id_].config(state=tk.NORMAL)

    def _test_btn_clicked(self, test_id):
        for suite_id, btn in self.suites_widgets.items():
            if str(btn['state']) == str(tk.DISABLED):
                suite = next(filter(lambda s: s['SuiteID'] == suite_id, self._suites_data))
                tests = suite['Tests']
                test = next(filter(lambda t: t['TestID'] == test_id, tests))
                test['SuiteName'] = suite['SuiteName']
                self._controller.show_page(PAGE.ROBOT_TEST_PAGE, test_data=test)
                return
