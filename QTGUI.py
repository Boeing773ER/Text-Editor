#pyuic5 -o ui.py bus_direct.ui
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QStatusBar, QPlainTextEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QTextDocument, QTextCursor, QTextCharFormat
from TreeVisual import gen_huff_tree
import webbrowser
from Structure import *
from NLPModule import *


class Text_Editor(QMainWindow):
    def __init__(self, parent=None):
        self.openfile = list()  # single file
        self.path_list = list() # multiple file
        self.binary_code = ""
        self.huff_a = HuffmanTree
        window_icon = QIcon("./icon/text_editor.png")
        window_icon.addPixmap(QtGui.QPixmap("my.ico"), QIcon.Normal, QIcon.Off)

        super(Text_Editor, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Text Editor")
        self.setWindowIcon(window_icon)
        self.resize(800, 600)
        self.setMouseTracking(False)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setToolTip("")
        # plainTextEdit
        self.plainTextEdit = QPlainTextEdit()
        editor_font = self.plainTextEdit.font()
        editor_font.setPointSize(20)
        self.plainTextEdit.setFont(editor_font)
        self.setCentralWidget(self.plainTextEdit)   # set it as central widget
        self.plainTextEdit.close()      # close, make it invisible
        self.plainTextEdit.textChanged.connect(lambda: self.text_changed())

        # menubar
        self.menubar = self.menuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        # menu
        menu_file = self.menubar.addMenu("File(&F)")
        menu_edit = self.menubar.addMenu("Edit(&E)")
        menu_coding = self.menubar.addMenu("Coding(&C)")
        menu_advanced = self.menubar.addMenu("Advanced(&A)")
        # QAction within menuBar
        m_save = QAction(QIcon("./icon/save.png"), "Save", self)
        m_save.setObjectName("M_Save")
        m_save.setShortcut("Ctrl+S")
        m_open = QAction(QIcon("./icon/open.png"), "Open", self)
        m_open.setObjectName("M_Open")
        m_open.setShortcut("Ctrl+O")
        m_new = QAction(QIcon("./icon/new file.png"), "New File", self)
        m_new.setObjectName("M_New")
        m_new.setShortcut("Ctrl+N")
        m_find = QAction(QIcon("./icon/find.png"), "Find", self)
        m_find.setObjectName("M_Find")
        m_find.setShortcut("Ctrl+F")
        m_replace = QAction(QIcon("./icon/replace.png"), "Replace", self)
        m_replace.setObjectName("M_Replace")
        m_replace.setShortcut("Ctrl+R")
        m_remove_hightlight = QAction(QIcon("./icon/remove_tag.png"), "Remove Highlight", self)
        m_remove_hightlight.setObjectName("M_Remove_Highlight")
        m_encode = QAction(QIcon("./icon/encode.png"), "Encode", self)
        m_encode.setObjectName("M_Encode")
        m_decode = QAction(QIcon("./icon/decode.png"), "Decode", self)
        m_decode.setObjectName("M_Decode")
        m_mul_search = QAction(QIcon("./icon/adv_search.png"), "Multi File Search", self)
        m_mul_search.setObjectName("M_Mul_Search")
        m_statistic = QAction(QIcon("./icon/statistic.png"), "Statistic", self)
        m_statistic.setObjectName("M_Statistic")
        # add action to menuBar
        menu_file.addAction(m_new)
        menu_file.addAction(m_open)
        menu_file.addSeparator()
        menu_file.addAction(m_save)
        menu_edit.addAction(m_find)
        menu_edit.addAction(m_replace)
        menu_edit.addSeparator()
        menu_edit.addAction(m_remove_hightlight)
        menu_coding.addAction(m_encode)
        menu_coding.addAction(m_decode)
        menu_advanced.addAction(m_mul_search)
        menu_advanced.addAction(m_statistic)

        # toolBar
        self.toolBar = self.addToolBar("File")
        self.toolBar.setObjectName("toolBar")
        # add QAction to toolBar
        self.toolBar.addAction(m_new)
        self.toolBar.addAction(m_open)
        self.toolBar.addAction(m_save)
        self.toolBar.addSeparator()
        self.toolBar.addAction(m_find)
        self.toolBar.addAction(m_replace)
        self.toolBar.addAction(m_remove_hightlight)
        self.toolBar.addSeparator()
        self.toolBar.addAction(m_encode)
        self.toolBar.addAction(m_decode)
        self.toolBar.addSeparator()
        self.toolBar.addAction(m_mul_search)
        self.toolBar.addAction(m_statistic)

        # statusbar
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        # init component
        self.courser_pos = QLabel()
        self.courser_pos.setMinimumWidth(200)
        self.courser_pos.setAlignment(Qt.AlignCenter)
        self.courser_pos.setText("Ln:1 \t Col:1")
        self.sb_message = QLabel()
        self.sb_message.setMinimumWidth(200)
        self.sb_message.setAlignment(Qt.AlignCenter)
        self.word_count = QLabel()
        self.word_count.setMinimumWidth(100)
        self.word_count.setAlignment(Qt.AlignCenter)
        self.word_count.setText("0 Char")
        self.statusbar.addPermanentWidget(self.sb_message)
        self.statusbar.addPermanentWidget(self.courser_pos)
        self.statusbar.addPermanentWidget(self.word_count)
        """QLabel* label = new QLabel("TQSilence");

    if( label != NULL )
    {
        statusLbl.setMinimumWidth(200);
        statusLbl.setAlignment(Qt::AlignCenter);
        statusLbl.setText("Ln: 1    Col: 1");

        label->setMinimumWidth(200);
        label->setAlignment(Qt::AlignCenter);

        sb->addPermanentWidget(new QLabel());
        sb->addPermanentWidget(&statusLbl);
        sb->addPermanentWidget(label);
    }
    else
    {
        ret = false;
    }

    return ret;
}"""

        # connect
        m_new.triggered.connect(self.new_pressed)
        m_open.triggered.connect(self.open_pressed)
        m_save.triggered.connect(self.save_pressed)
        m_find.triggered.connect(self.find_pressed)
        m_replace.triggered.connect(self.replace_pressed)
        m_remove_hightlight.triggered.connect(self.rem_hl_pressed)
        m_encode.triggered.connect(self.encode_pressed)
        m_decode.triggered.connect(self.decode_pressed)
        m_mul_search.triggered.connect(self.mul_search_pressed)
        m_statistic.triggered.connect(self.statistic_pressed)
        # for test

    # BASIC FUNCTION: NEW, OPEN, SAVE
    def new_pressed(self):
        print("inside func new_pressed")
        if self.plainTextEdit.isHidden():
            # plain_text_edit not visible, creat new file
            self.openfile = []
            # self.setCentralWidget(self.plainTextEdit)
            self.plainTextEdit.show()
            self.statusbar.showMessage("New File")
        elif self.plainTextEdit.toPlainText() != '':
            self.check_if_saved()
            self.plainTextEdit.show()

    def open_pressed(self):
        print("inside func open_pressed")
        self.check_if_saved()
        openfile_name = QFileDialog.getOpenFileName(self, caption='Open File', filter='*.txt')
        if openfile_name != ('', ''):
            self.openfile = openfile_name[0]
            print("open"+self.openfile)
            file_a = open(self.openfile, mode='r+')
            print("file opened")
            str_a = file_a.read()
            print("done reading")
            """if self.centralWidget() is None:
                self.setCentralWidget(self.plainTextEdit)"""
            # if plain text edit not visible, show it
            if self.plainTextEdit.isHidden():
                self.plainTextEdit.show()
            self.plainTextEdit.setPlainText(str_a)
        else:
            print("open fail")
            self.statusbar.showMessage("Open Failed")

    # file path stored in self.path_list
    def open_mul_file(self):
        print("inside func open_mul_file")
        file_path = QFileDialog.getOpenFileNames(self, caption="Open Mul Files", filter="*.txt")
        # getOpenFileNames return in format ([path],"*.txt")
        self.path_list = file_path[0]
        print(type(self.path_list), "\n", self.path_list)
        return self.path_list

    def save_pressed(self):
        print("inside func save_pressed")
        # if self.centralWidget() is None:
        if self.plainTextEdit.isHidden():
            self.content_empty()
        else:
            if not self.openfile:
                # save as new file
                self.save_new_file()
            else:
                # write it back to the original file
                self.save_to_exist()

    def save_new_file(self):
        print("inside func save_new_file")
        filename_save = QFileDialog.getSaveFileName(self, caption="Save New File", filter="*.txt")
        print(filename_save)
        if filename_save != ('', ''):
            print("Save_path:", filename_save)
            file_a = open(filename_save[0], mode='w+')
            edit_str = self.plainTextEdit.toPlainText()
            file_a.write(edit_str)
            file_a.close()
            self.openfile = filename_save[0]
            self.statusbar.showMessage("Saved")
        else:
            print("Save fail")
            self.statusbar.showMessage("Save Failed")

    def save_to_exist(self):
        print("inside func save_to_exist")
        print("save to existing file")
        print("openfile:" + self.openfile)
        edit_str = self.plainTextEdit.toPlainText()
        print("text:" + edit_str)
        file_a = open(self.openfile, mode='w+')
        file_a.write(edit_str)
        file_a.close()
        self.statusbar.showMessage("Saved")

    # Handle Exception: content unsaved, check if saved etc
    def content_unsaved(self):
        print("inside func content_unsaved")
        unsaved = QMessageBox.information(self, "Save?", "Current content unsaved. Do you wish to save it?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
        if unsaved == QMessageBox.Yes:
            print("save unsaved file")
            self.save_pressed()
            print("file saved, closing plainTextEdit")
            self.plainTextEdit.clear()
            self.plainTextEdit.close()
            print("hidden:", self.plainTextEdit.isHidden())
            print("plaintextedit hidden")
        elif unsaved == QMessageBox.No:
            print("discard unsaved file")
            self.statusbar.showMessage("Discard Unsaved File")
            self.plainTextEdit.clear()
            self.plainTextEdit.close()

    def content_empty(self):
        print("inside func content_empty")
        QMessageBox.warning(self, "Empty", "Content Empty!", QMessageBox.Ok, QMessageBox.Ok)

    def check_if_saved(self):
        print("inside func check_if_saved")
        if self.plainTextEdit.isHidden():
            return
        if not self.openfile:
            # No file has been opened/Not initialized
            if self.plainTextEdit.isVisible():
                # Save New File
                self.content_unsaved()
        else:
            # openfile exist
            file_a = open(self.openfile, mode='r')
            str_f = file_a.read()
            str_e = self.plainTextEdit.toPlainText()
            if str_e != str_f:
                self.content_unsaved()

    # FUNCTION: FIND & REPLACE
    # TODO: bug in highlight
    def find_pressed(self):
        print("inside func find_pressed")
        if self.plainTextEdit.isHidden():
            self.content_empty()
        else:
            print("in find")
            find_input = QInputDialog()
            find_input.setWindowTitle("Find")
            find_input.setLabelText("Find:")
            find_input.setInputMode(QInputDialog.TextInput)
            if find_input.exec() == QInputDialog.Accepted:
                str_pattern = find_input.textValue()
            print("QInputDialog show")
            str_target = self.plainTextEdit.toPlainText()
            text_pos = kmp_matching(str_target, str_pattern)
            if (text_pos != -1) and (text_pos is not None):
                print("text_pos:", text_pos)
                document = self.plainTextEdit.document()
                highlight_cursor = QTextCursor(document)
                cursor = QTextCursor(document)
                cursor.beginEditBlock()
                color_format = QTextCharFormat(highlight_cursor.charFormat())
                color_format.setBackground(Qt.yellow)
                for i in range(0, len(text_pos)):
                    pos = len(text_pos) - 1 - i
                    print(pos, text_pos[pos])
                    QTextCursor.setPosition(highlight_cursor, text_pos[pos])
                    highlight_cursor.select(QTextCursor.WordUnderCursor)
                    print(highlight_cursor.position())
                    highlight_cursor.mergeCharFormat(color_format)
                cursor.endEditBlock()
            else:
                self.target_not_find()

    # TODO: complete func replace_pressed, connect pushbutton
    def replace_pressed(self):
        print("inside func replace_pressed")
        if self.plainTextEdit.isHidden():
            self.content_empty()
        else:
            dialog = QDialog()
            layout = QGridLayout(dialog)
            replace_input = QDialog()
            replace_input.setWindowTitle("Replace")
            print("set title")
            old_label = QLabel("Old")
            new_label = QLabel("New")
            old_text = QLineEdit()
            new_text = QLineEdit()
            replace_button = QPushButton("Replace")
            cancel_button = QPushButton("Cancel")
            print("init widget")
            layout.addWidget(old_label, 0, 0)
            layout.addWidget(old_text, 0, 1)
            layout.addWidget(new_label, 1, 0)
            layout.addWidget(new_text, 1, 1)
            layout.addWidget(replace_button, 2, 0)
            layout.addWidget(cancel_button, 2, 1)
            print("done layout")
            dialog.setLayout(layout)
            # replace_button.customContextMenuRequested.connect(self.replace_process())
            # replace_button.click.connect(self.replace_process())
            # cancel_button.clicked.connect()
            dialog.exec()

    def target_not_find(self):
        print("inside func target_not_find")

    # remove high-light
    def rem_hl_pressed(self):
        print("inside func rem_hl_pressed")
        document = self.plainTextEdit.document()
        highlight_cursor = QTextCursor(document)
        cursor = QTextCursor(document)
        cursor.beginEditBlock()
        color_format = QTextCharFormat(highlight_cursor.charFormat())
        color_format.setBackground(Qt.white)
        highlight_cursor.select(QTextCursor.Document)
        highlight_cursor.mergeCharFormat(color_format)
        cursor.endEditBlock()

    # FUNCTION: ENCODE & DECODE
    # TODO: output binary to QDialog
    def encode_pressed(self):
        print("inside func encode_pressed")
        if self.plainTextEdit.isVisible():
            # gen tree
            edit_str = self.plainTextEdit.toPlainText()
            dict_count = dict()
            count_element(edit_str, dict_count)  # dict:['symbol':count]
            sorted_key = sorted_dict(dict_count, dict_count.keys(), reverse=True)
            self.huff_a = HuffmanTree(dict_count, len(dict_count))  # generate HuffTree using dict
            dict_code = gen_huff_tree(self.huff_a)
            webbrowser.open(r".\tree_base.html")
            # gen huff_dict
            """file_a = open("huff_dict.txt", mode='w+')
            dict_ref = dict_code.__str__()
            file_a.write(dict_ref)
            file_a.close()
            webbrowser.open(r".\huff_dict.txt")"""
            # gen binary
            str_a = ""
            for i in range(len(edit_str)):
                str_a += dict_code[edit_str[i]]
            self.binary_code = str_a
            file_b = open("binary.txt", mode='w+')
            file_b.write(str_a)
            file_b.close()
            webbrowser.open(r".\binary.txt")
            self.huff_code_table(dict_count, dict_code, sorted_key)
        else:
            self.content_empty()

    # TODO: output Decode to QDialog
    def decode_pressed(self):
        print("inside func decode_pressed")
        if self.binary_code == "":
            print("binary not generate yet")
        else:
            temp_root = self.huff_a.root
            str_a = ""
            for i in self.binary_code:
                # print("i:", i)
                if i == '0':
                    # print(temp_root.value, "right:", temp_root.right.value)
                    temp_root = temp_root.right
                elif i == '1':
                    # print(temp_root.value, "left:", temp_root.left.value)
                    temp_root = temp_root.left
                if temp_root.is_leaf():
                    str_a += temp_root.name
                    # print(str_a)
                    temp_root = self.huff_a.root
                    # print("complete assignment")
            print(str_a)

    def huff_code_table(self, dict_count, dict_code, sorted_key):
        print("inside func huff_code_table")
        # dict_code: Huffman code
        # dic_count: Word Count
        # sorted_kay: sequence for words
        dialog = QDialog()
        print("sorted_key:", len(sorted_key))
        print("dict_code:", len(dict_code))
        sta_table = QTableWidget(len(dict_code), 3, dialog)
        print("huff_code_table creat")
        dialog.setWindowTitle("Huffman Tree")
        header = ["Word", "Count", "Huffman Code"]
        sta_table.setHorizontalHeaderLabels(header)
        sta_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for i in range(len(dict_code)):
            sta_table.setItem(i, 0, QTableWidgetItem(sorted_key[i]))
            sta_table.setItem(i, 1, QTableWidgetItem(str(dict_count[sorted_key[i]])))
            sta_table.setItem(i, 2, QTableWidgetItem(str(dict_code[sorted_key[i]])))
        print("table init complete")
        sta_table.show()
        sta_table.resize(300, 600)
        print("table shown")
        dialog.exec()

    # ADV FUNCTION
    # TODO: complete func mul_search_pressed
    def mul_search_pressed(self):
        print("inside func mul_search_pressed")
        # check if saved. Close it if saved
        self.check_if_saved()
        self.plainTextEdit.close()
        self.open_mul_file()
        if not self.path_list:
            print("mul_search open fail")
        else:
            inv_index = self.inverted_index()
            print(inv_index)
            find_input = QInputDialog()
            find_input.setWindowTitle("Inverted Index Find")
            find_input.setLabelText("Find:")
            find_input.setInputMode(QInputDialog.TextInput)
            if find_input.exec() == QInputDialog.Accepted:
                str_pattern = find_input.textValue()
            str_pattern = str_pattern.lstrip()  # remove space on the left
            temp_pos = 0
            word_list = []
            for i in range(len(str_pattern)):
                if str_pattern[i] == ' ':
                    word_list.append(str_pattern[temp_pos:i])
                    temp_pos = i + 1
            word_list.append(str_pattern[temp_pos:len(str_pattern)])    # add last word
            print(word_list)
            # not finished
            result_list = []
            if len(word_list) == 1:
                # wrong
                pos_list = inv_index[word_list[0]]  # pos_list:[[path, pos], [path, pos]]
                for j in pos_list:
                    result_list.append(self.locate_sentence(j))
                # repetition in result_list
                print(result_list)
            else:
                for i in word_list:
                    pos_list = inv_index[i]  # pos_list:[[path, pos], [path, pos]]
                    for j in pos_list:
                        print(self.locate_sentence(j))

    def statistic_pressed(self):
        print("inside func statistic_pressed")
        # check if saved. Close it if saved.
        self.check_if_saved()
        self.plainTextEdit.close()
        dict_b = dict()
        self.open_mul_file()
        if not self.path_list:
            print("statistic open fail")
        else:
            for path_a in self.path_list:
                file_a = open(path_a, mode='r')
                str_a = file_a.read()
                str_a = str_a.lower()
                # tokenize + filter
                filtered_words = token_filter(str_a)
                print("OG: ", filtered_words, "\n")
                # stemming
                stem_words = stemming(filtered_words)
                # simple counting, result in dict_b
                count_element(stem_words, dict_b)
                file_a.close()
            sorted_key = sorted_dict(dict_b, dict_b.keys(), reverse=True)
            for i in range(10):
                print(sorted_key[i], dict_b[sorted_key[i]])
            self.gen_sta_table(dict_b, sorted_key)

    def gen_sta_table(self, dict_b, sorted_key):
        print("inside func gen_sta_table")
        # dict_b: word count
        # sorted_kay: sequence for words
        dialog = QDialog()
        sta_table = QTableWidget(30, 2, dialog)
        print("sta_table creat")
        dialog.setWindowTitle("Statistic")
        header = ["Word", "Count"]
        sta_table.setHorizontalHeaderLabels(header)
        sta_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        for i in range(30):
            sta_table.setItem(i, 0, QTableWidgetItem(sorted_key[i]))
            sta_table.setItem(i, 1, QTableWidgetItem(str(dict_b[sorted_key[i]])))
        print("table init complete")
        sta_table.show()
        sta_table.resize(300, 600)
        print("table shown")
        dialog.exec()

    def inverted_index(self):
        print("inside func inverted_index")
        # get file path from self.path_list
        inv_index = dict()  # inverted_index
        # inv_index[word] = [[file_path, word_pos],[]]
        file_path = self.path_list
        # file_path = ["D:/University Courses/Data Structure Design/Source Code/test data/0_3.txt",
        #               "D:/University Courses/Data Structure Design/Source Code/test data/1_1.txt"]  # testing
        for path_a in file_path:
            # open a single file and convert it to string
            file_a = open(path_a, mode='r')
            str_a = file_a.read()
            # Case insensitive
            str_a = str_a.lower()
            j = 0
            # indexing word in this file
            for i in range(len(str_a)):
                if not str_a[i].isalpha():
                    if str_a[j].isalpha():
                        temp_str = str_a[j:i]
                        if temp_str in inv_index:
                            inv_index[temp_str].append([path_a, j])
                        else:
                            inv_index[temp_str] = [[path_a, j]]
                        j = i
                elif not str_a[j].isalpha():
                    # find the starting pos of the next word
                    j = i
            file_a.close()
        return inv_index

    def replace_process(self):
        print("inside func replace_process")

    def text_changed(self):
        print("in func text_changed")
        self.word_count.setText(len(self.plainTextEdit.toPlainText()).__str__() + " Char")
        # self.rem_hl_pressed()

    def locate_sentence(self, list_a):
        file_a = open(list_a[0], mode='r')
        str_a = file_a.read()
        w_pos = list_a[1]
        s_pos = 0   # start pos
        e_pos = 0   # end pos
        for i in range(w_pos, len(str_a)):
            if str_a[i] == '.' or str_a[i] == '!' or str_a[i] == '?' or str_a[i] == '>' or str_a[i] == '<':
                e_pos = i
                break
        s_pos = w_pos
        while s_pos >= 0:
            if str_a[s_pos] == '.' or str_a[s_pos] == '!' or str_a[s_pos] == '?' or str_a[s_pos] == '>' \
                    or str_a[s_pos] == '<':
                print(s_pos, str_a[s_pos])
                break
            s_pos -= 1
        return [list_a[0], s_pos, e_pos]

# TODO: 高级搜索用表达式求值
# TODO: TDF-ID