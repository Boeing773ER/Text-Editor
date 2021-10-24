import ctypes
import sys
import nltk
import webbrowser
from Structure import *
from TreeVisual import *
from NLPModule import *
from QTGUI import *
from queue import Queue
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

if __name__ == '__main__':
    """app = QtWidgets.QApplication(sys.argv)
    text_editor = Text_Editor()
    text_editor.show()
    sys.exit(app.exec_())"""

    str_a = "   ~ ~ aaa | bbb  &ccc"
    queue_a = nifix_to_postfix(str_a)
    while not queue_a.empty():
        print(queue_a.get())
