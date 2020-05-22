import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import logging
from TkinterGui.Pages.PageName import PAGE
from MyRobotRunners.GetTests import GetSuiteInfo
from TkinterGui.Pages.HomeGUI import RobotMainFrame
from TkinterGui.Pages.TestGUI import RobotTestFrame


def set_ttk_styles():
    style = ttk.Style()
    style.configure('TButton', relief='flat', background='#0275d8', font=("Arial", 12), padding=5)
    style.configure('TLabel', relief='RAISED', background='#95ed93', font=("Arial", 11), anchor=tk.CENTER)
    style.configure('TFrame', relief='RAISED', background='#e6e8ed', font=("Arial", 11), anchor=tk.CENTER)
    style.configure("TFrame", background="#000000")


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_ttk_styles()

        self.suites_data = GetSuiteInfo.retrieve_all_tests()
        self._container = ttk.Frame(self)
        self._container.pack(side="top", fill="both", expand=True)
        self._container.grid_rowconfigure(0, weight=1)
        self._container.grid_columnconfigure(0, weight=1)
        self.title('Robot Framework Tests Overview')
        self.geometry('{}x{}'.format(1000, 600))
        self.wm_minsize(width=1000, height=600)
        self.resizable(width=True, height=True)
        self.configure(bg="black")
        try:
            self.wm_iconbitmap(bitmap="my_icon.ico")
        except tk.TclError:
            pass
        self.frames = {}
        self._page_dict = {PAGE.ROBOT_HOME_PAGE: RobotMainFrame, PAGE.ROBOT_TEST_PAGE: RobotTestFrame}
        self.show_page(PAGE.ROBOT_HOME_PAGE, suites_data=self.suites_data)

    def show_page(self, page: PAGE, **kwargs):
        if self.frames.get(page) is None:
            p = self._page_dict.get(page)(parent=self._container, controller=self, **kwargs)
            self.frames[page] = p
            p.grid(row=0, column=0, sticky='nsew')
        frame = self.frames.get(page)
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("CLOSE", "Do you want to close?"):
            self.destroy()


if __name__ == "__main__":
    try:
        app = MainWindow()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
    except Exception as ex:
        res = messagebox.showinfo("Critical Error",
                                  f"A critical exception occurred and we cannot continue. {type(ex).__name__}"
                                  f", {str(ex)}")
        logging.error("Critical Error",
                      f"A critical exception occurred and we cannot continue. {type(ex).__name__}"
                      f", {str(ex)}")
