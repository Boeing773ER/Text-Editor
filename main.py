import ctypes
import sys
import nltk
import webbrowser
from Structure import *
from TreeVisual import *
from NLPModule import *
from QTGUI import *
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    text_editor = Text_Editor()
    text_editor.show()
    sys.exit(app.exec_())

    """s = ", but as an adaptation, it    fails from every angle.<br /><br />The harrowing novel about the reality"
    print("OG: ", s)
    s = token_filter(s)
    print("tokenize: ", s)"""

    """str_1 = "abcdabcdabab"
    str_2 = "ab"
    text_pos = kmp_matching(str_1, str_2)
    print(text_pos)
    for i in range(0, len(text_pos)):
        print(i, text_pos[len(text_pos)-1-i], " ")"""
