import tkinter as tk
import tkinter.ttk as ttk
from TkinterGui.Pages.PageName import PAGE


class RobotTestFrame(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent)
        self._controller = controller
        self._test_data = kwargs.get("test_data", {})
        self._dh = 0.02
        self._h = 0.15
        self._build()

    def _build(self):
        ind = 0
        label = ttk.Label(self, text=f"Test: {self._test_data['SuiteName']}/{self._test_data['TestName']}")
        label.place(bordermode=tk.INSIDE, relx=0.15, rely=(ind * (self._dh + self._h) + self._dh), relwidth=0.7, relheight=self._h)
        ind += 1

        for test_step in self._test_data['TestSteps']:
            text = f"STEP {ind}:  {test_step['step']} => {', '.join(test_step['args'])}"
            label = ttk.Label(self, text=text)
            label.place(bordermode=tk.INSIDE, relx=0.15, rely=(ind * (self._dh + self._h) + self._dh), relwidth=0.7, relheight=self._h)
            ind += 1
        btn = ttk.Button(self, text="BACK", style="TButton", command=self._back)
        btn.place(bordermode=tk.INSIDE, relx=0.15, rely=(ind * (self._dh + self._h) + self._dh), relwidth=0.15, relheight=self._h * 0.5)

    def _back(self):
        self._controller.show_page(PAGE.ROBOT_HOME_PAGE)
