#pyuic5 -o ui.py bus_direct.ui

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QStatusBar, QPlainTextEdit
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QTextDocument, QTextCursor, QTextCharFormat, QFont
from TreeVisual import gen_huff_tree
import webbrowser
from Structure import *
from NLPModule import *
from queue import Queue


class Text_Editor(QMainWindow):
    def __init__(self, parent=None):
        self.openfile = list()  # single file
        self.path_list = list()     # multiple file
        self.binary_code = ""
        self.huff_a = HuffmanTree
        self.inv_index = dict()     # inverted_index
        self.highlight = False  # high light or not
        window_icon = QIcon("./icon/text_editor.png")
        window_icon.addPixmap(QtGui.QPixmap("my.ico"), QIcon.Normal, QIcon.Off)

        # MainWindow
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
        self.editor_font = self.plainTextEdit.font()
        self.editor_font.setPointSize(20)
        self.plainTextEdit.setFont(self.editor_font)
        self.setCentralWidget(self.plainTextEdit)   # set it as central widget
        self.plainTextEdit.close()      # close, make it invisible
        self.plainTextEdit.textChanged.connect(lambda: self.text_changed())
        self.plainTextEdit.cursorPositionChanged.connect(lambda: self.cursor_pos_changed())
        #Cursor
        # self.text_cursor = self.plainTextEdit.textCursor()

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
        m_remove_highlight = QAction(QIcon("./icon/remove_tag.png"), "Remove Highlight", self)
        m_remove_highlight.setObjectName("M_Remove_Highlight")
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
        menu_edit.addAction(m_remove_highlight)
        menu_coding.addAction(m_encode)
        menu_coding.addAction(m_decode)
        menu_advanced.addAction(m_mul_search)
        menu_advanced.addAction(m_statistic)

        # toolBar
        self.toolBar = self.addToolBar("File")
        self.toolBar.setObjectName("toolBar")
        self.font_size = QComboBox()
        combo_font = self.font_size.font()
        combo_font.setPointSize(13)
        font_label = QLabel()
        font_label.setText("Font Size:")
        temp_font = font_label.font()
        temp_font.setBold(True)
        font_label.setFont(temp_font)
        self.font_size.setFont(combo_font)
        font_size_list = [10, 11, 12, 13, 15, 17, 20, 23, 26, 30]
        for i in range(10):
            self.font_size.addItem(str(font_size_list[i]))
            temp_font = combo_font
            temp_font.setPointSize(font_size_list[i])
            self.font_size.setItemData(i, temp_font, Qt.FontRole)
        self.font_size.setCurrentIndex(6)   # default value (3+1)*5 = 20
        self.font_size.setEditable(True)
        self.font_size.setMinimumWidth(100)
        self.font_size.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.font_size.currentTextChanged[str].connect(lambda: self.change_font_size())    # send content
        # add QAction to toolBar
        self.toolBar.addAction(m_new)
        self.toolBar.addAction(m_open)
        self.toolBar.addAction(m_save)
        self.toolBar.addSeparator()
        self.toolBar.addAction(m_find)
        self.toolBar.addAction(m_replace)
        self.toolBar.addAction(m_remove_highlight)
        self.toolBar.addSeparator()
        self.toolBar.addAction(m_encode)
        self.toolBar.addAction(m_decode)
        self.toolBar.addSeparator()
        self.toolBar.addAction(m_mul_search)
        self.toolBar.addAction(m_statistic)
        self.toolBar.addSeparator()
        self.toolBar.addWidget(font_label)
        self.toolBar.addWidget(self.font_size)

        # statusbar
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        # init component
        self.courser_pos = QLabel()
        self.courser_pos.setMinimumWidth(200)
        self.courser_pos.setAlignment(Qt.AlignCenter)
        self.courser_pos.setText("Bl:1 \t Col:1")
        self.sb_message = QLabel()
        self.sb_message.setMinimumWidth(200)
        self.sb_message.setAlignment(Qt.AlignCenter)
        self.word_count = QLabel()
        self.word_count.setMinimumWidth(100)
        self.word_count.setAlignment(Qt.AlignCenter)
        self.word_count.setText("0 Char")
        self.file_name = QLabel()
        self.file_name.setMinimumWidth(150)
        self.file_name.setAlignment(Qt.AlignCenter)
        self.file_name.setText("File:")
        self.statusbar.addPermanentWidget(self.sb_message)
        self.statusbar.addPermanentWidget(self.courser_pos)
        self.statusbar.addPermanentWidget(self.word_count)
        self.statusbar.addPermanentWidget(self.file_name)

        # connect
        m_new.triggered.connect(self.new_pressed)
        m_open.triggered.connect(self.open_pressed)
        m_save.triggered.connect(self.save_pressed)
        m_find.triggered.connect(self.find_pressed)
        m_replace.triggered.connect(self.replace_pressed)
        m_remove_highlight.triggered.connect(self.rem_hl_pressed)
        m_encode.triggered.connect(self.encode_pressed)
        m_decode.triggered.connect(self.decode_pressed)
        m_mul_search.triggered.connect(self.mul_search_pressed)
        m_statistic.triggered.connect(self.statistic_pressed)

        # testing
        # self.inverted_index()

    # BASIC FUNCTION: NEW, OPEN, SAVE
    def new_pressed(self):
        print("inside func new_pressed")
        if self.plainTextEdit.isHidden():
            # plain_text_edit not visible, creat new file
            pass
        elif self.plainTextEdit.toPlainText() != '':
            print("plain text content:")
            if self.check_if_saved() == "Cancel":
                return
        self.openfile = []  # new file, clear current file path
        self.plainTextEdit.setPlainText("")  # clear content
        self.plainTextEdit.show()
        self.statusbar.showMessage("New File")
        self.file_name.setText("File:New")

    def open_pressed(self):
        print("inside func open_pressed")
        if self.check_if_saved() == "Cancel":
            return
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
            self.file_name.setText("File:" + get_file_name(openfile_name[0]))
        else:
            print("open fail")
            self.statusbar.showMessage("Open Failed")

    def open_mul_file(self):
        # file path stored in self.path_list
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
            self.file_name.setText("File:" + get_file_name(filename_save[0]))
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

    def content_unsaved(self):
        # Handle Exception: content unsaved, check if saved etc
        print("inside func content_unsaved")
        unsaved = QMessageBox.information(self, "Save?", "Current content unsaved. Do you wish to save it?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Yes)
        if unsaved == QMessageBox.Yes:
            print("Save unsaved File")
            self.save_pressed()
            print("file saved, closing plainTextEdit")
            self.plainTextEdit.clear()
            self.plainTextEdit.close()
            # update status bar
            self.word_count.setText("0 Char")
            self.courser_pos.setText("Bl:0 \t Col:0")
            print("hidden:", self.plainTextEdit.isHidden())
            print("plaintextedit hidden")
        elif unsaved == QMessageBox.No:
            print("discard unsaved file")
            self.statusbar.showMessage("Discard Unsaved File")
            self.plainTextEdit.clear()
            self.plainTextEdit.close()
            self.word_count.setText("0 Char")
            self.courser_pos.setText("Bl:0 \t Col:0")
        elif unsaved == QMessageBox.Cancel:
            return "Cancel"
            # what to do if cancel?

    def content_empty(self):
        print("inside func content_empty")
        QMessageBox.warning(self, "Empty", "Content Empty!", QMessageBox.Ok, QMessageBox.Ok)

    def check_if_saved(self):
        print("inside func check_if_saved")
        if self.plainTextEdit.isHidden():
            return
        if self.openfile == []:
            # No file has been opened/Not initialized
            if self.plainTextEdit.isVisible():
                if self.plainTextEdit.toPlainText() != '':
                    # if plaintext not empty
                    # Save New File
                    return self.content_unsaved()
        else:
            # openfile exist
            file_a = open(self.openfile, mode='r')
            str_f = file_a.read()
            str_e = self.plainTextEdit.toPlainText()
            if str_e != str_f:
                return self.content_unsaved()

    # FUNCTION: FIND & REPLACE
    # TODO: bug in highlight
    def find_pressed(self):
        print("inside func find_pressed")
        if self.plainTextEdit.isHidden():
            self.content_empty()
        else:
            dialog = QDialog()
            layout = QGridLayout(dialog)
            dialog.setWindowTitle("Find")
            print("set title")

            find_label = QLabel("Find: ")
            label_font = find_label.font()
            label_font.setPointSize(13)
            find_label.setFont(label_font)
            find_text = QLineEdit()

            sensitive = QCheckBox()
            sensitive.setText("Case Sensitive")

            button_box = QDialogButtonBox()
            find_button = QPushButton("Find")
            cancel_button = QPushButton("Cancel")
            button_box.addButton(find_button, QDialogButtonBox.AcceptRole)
            button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)
            button_box.accepted.connect(lambda: self.find_process(dialog, find_text.text(), sensitive.isChecked()))
            button_box.rejected.connect(lambda: self.replace_close(dialog))

            print("init widget")
            layout.addWidget(find_label, 0, 0)
            layout.addWidget(find_text, 0, 1)
            layout.addWidget(sensitive, 1, 0, 1, 2)
            layout.addWidget(button_box, 2, 0, 1, 2)
            print("done layout")
            dialog.setLayout(layout)
            dialog.exec()

    def find_process(self, dialog, str_pattern, sensitive):
        self.rem_hl_pressed()
        if str_pattern == '':
            self.content_empty()
            return
        str_target = self.plainTextEdit.toPlainText()
        if not sensitive:
            str_pattern = str_pattern.lower()
            str_target = str_target.lower()
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
            self.highlight = True
        else:
            self.target_not_find()
        # dialog.destroy()

    def replace_pressed(self):
        print("inside func replace_pressed")
        if self.plainTextEdit.isHidden():
            self.content_empty()
        else:
            dialog = QDialog()
            layout = QGridLayout(dialog)
            # replace_input = QDialog()
            dialog.setWindowTitle("Replace")
            print("set title")

            old_label = QLabel("Old: ")
            new_label = QLabel("New: ")
            label_font = old_label.font()
            label_font.setPointSize(13)
            old_label.setFont(label_font)
            new_label.setFont(label_font)
            old_text = QLineEdit()
            new_text = QLineEdit()

            button_box = QDialogButtonBox()
            replace_button = QPushButton("Replace")
            cancel_button = QPushButton("Cancel")
            button_box.addButton(replace_button, QDialogButtonBox.AcceptRole)
            button_box.addButton(cancel_button, QDialogButtonBox.RejectRole)
            button_box.accepted.connect(lambda: self.replace_process(dialog, old_text.text(), new_text.text()))
            button_box.rejected.connect(lambda: self.replace_close(dialog))

            print("init widget")
            layout.addWidget(old_label, 0, 0)
            layout.addWidget(old_text, 0, 1)
            layout.addWidget(new_label, 1, 0)
            layout.addWidget(new_text, 1, 1)
            layout.addWidget(button_box, 2, 0, 1, 2)
            print("done layout")
            dialog.setLayout(layout)
            dialog.exec()

    def target_not_find(self):
        print("inside func target_not_find")
        not_found = QMessageBox.information(self, "Not Found", "Target Not Found.",
                                            QMessageBox.Yes, QMessageBox.Yes)

    def replace_process(self, dialog, old, new):
        print("inside func replace_process")
        str_a = kmp_replace(self.plainTextEdit.toPlainText(), old, new)
        self.plainTextEdit.setPlainText(str_a)
        dialog.destroy()

    def replace_close(self, dialog):
        print("inside func replace_close")
        dialog.destroy()
        self.rem_hl_pressed()

    def rem_hl_pressed(self):
        # remove high-light
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
        self.highlight = False

    # FUNCTION: ENCODE & DECODE
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
            """file_b = open("binary.txt", mode='w+')
            file_b.write(str_a)
            file_b.close()
            webbrowser.open(r".\binary.txt")"""
            self.huff_code_present(dict_count, dict_code, sorted_key, self.binary_code)
        else:
            self.content_empty()

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
            decode_pre = QDialog()
            s_layout = QVBoxLayout()
            prompt_text = QLabel("Decode Result:")
            prompt_text.setFont(QFont("Roman times", 17, QFont.Bold))
            s_layout.addWidget(prompt_text)
            print("prompt_text init")
            decode_text = QPlainTextEdit(str_a)
            s_layout.addWidget(decode_text)
            decode_text.setReadOnly(True)
            decode_text.resize(400, 300)
            text_font = decode_text.font()
            text_font.setPointSize(15)
            decode_text.setFont(text_font)
            decode_pre.setLayout(s_layout)
            decode_pre.resize(400, 300)
            decode_pre.exec()

    def huff_code_present(self, dict_count, dict_code, sorted_key, binary_code):
        print("inside func huff_code_table")
        # dict_code: Huffman code
        # dic_count: Word Count
        # sorted_kay: sequence for words
        dialog = QDialog()
        grid_layout = QGridLayout()
        prompt_font = QFont("Roman times", 13, QFont.Bold)
        left_prompt_text = QLabel("Word Count:")
        left_prompt_text.setFont(prompt_font)
        grid_layout.addWidget(left_prompt_text, 0, 0)
        right_prompt_text = QLabel("Binary Huff Code:")
        right_prompt_text.setFont(prompt_font)
        grid_layout.addWidget(right_prompt_text, 0, 1)
        sta_table = QTableWidget(len(dict_code), 3, dialog)
        grid_layout.addWidget(sta_table, 1, 0)
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
        binary = QPlainTextEdit(binary_code)
        binary.setReadOnly(True)
        grid_layout.addWidget(binary, 1, 1)
        dialog.setLayout(grid_layout)
        print("table shown")
        dialog.resize(600, 600)
        dialog.exec()

    # ADV FUNCTION
    def mul_search_pressed(self):
        print("inside func mul_search_pressed")
        # check if saved. Close it if saved
        if self.check_if_saved() == "Cancel":
            return
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.close()
        # update status bar
        self.word_count.setText("0 Char")
        self.courser_pos.setText("Bl:0 \t Col:0")
        self.file_name.setText("File:")

        self.open_mul_file()
        result_exist = True     # take it as default that result exist
        if not self.path_list:
            print("mul_search open fail")
        else:
            self.inv_index, sentence_index = self.inverted_index()
            inv_sen_no_index = pos_to_sentence_no(self.inv_index, sentence_index)
            # Input dialog
            find_input = QInputDialog()
            find_input.setWindowTitle("Inverted Index Find")
            find_input.setLabelText("Find:")
            find_input.setInputMode(QInputDialog.TextInput)
            str_pattern = ''
            if find_input.exec() == QInputDialog.Accepted:
                str_pattern = find_input.textValue()
            elif find_input.exec() == QInputDialog.Rejected:
                pass
            print("str_pattern:", str_pattern)
            word_list = []
            if str_pattern != '':
                queue = infix_to_postfix(str_pattern)
                stack_a = SStack()
                while not queue.empty():
                    temp_str = queue.get()
                    if temp_str == '&' or temp_str == '|':
                        index1 = stack_a.pop()
                        index2 = stack_a.pop()
                        result = expression_calculation(index1, index2, temp_str)
                        print("expression calculation finished")
                        stack_a.push(result)
                    elif temp_str in inv_sen_no_index or temp_str[0] == '~':
                        print("in marker", temp_str)
                        # into stack
                        if temp_str[0] == '~':
                            temp_index = invert_select(temp_str, sentence_index, inv_sen_no_index)
                        else:
                            temp_index = inv_sen_no_index[temp_str]
                            print(temp_str, "temp_index:", temp_index)
                            word_list.append(temp_str)
                        print(temp_str, "temp_index:", temp_index)
                        stack_a.push(temp_index)
                        print(temp_index)
                    else:
                        # fault here
                        # In expression 'a|b', when b doesn't exist
                        # result_exist is marked as False
                        # thoughts on solving this: remove break; push an empty index into stack
                        print("dont exist")
                        stack_a.push({})
                        # result_exist = False
                        # break
                result = None
                if not stack_a.is_empty():
                    result = stack_a.top()
                    count = 0
                    for path in result.keys():
                        count += len(result[path])
                    if count == 0:
                        result_exist = False
                else:
                    # what to do if stack is empty
                    pass
                print('final:', result)
                # DONE?: fault in result_exist
                self.search_result_present(result, word_list, sentence_index, result_exist, str_pattern)
            else:
                self.content_empty()

    def statistic_pressed(self):
        print("inside func statistic_pressed")
        # check if saved. Close it if saved.
        if self.check_if_saved() == "Cancel":
            return
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.close()
        # update status bar
        self.word_count.setText("0 Char")
        self.courser_pos.setText("Bl:0 \t Col:0")
        self.file_name.setText("File:")

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
                word_num = []
                filtered_words = token_filter(str_a, word_num)
                # print("word_num:", word_num[0])
                # print("OG: ", filtered_words, "\n")
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

    # improve the data structure of inverted index
    # sentence dict{'file_path':{'1': [start pos, end pos], '2': [start pos, end pos]}, 'second file_path':{}}
    # inv_index: {'word':{"path1":[pos1, pos3], "path2":[pos3, pos4]}, 'word2':{'path': [pos]}}
    def inverted_index(self):
        print("inside func inverted_index")
        # get file path from self.path_list
        inv_index = dict()  # inverted_index
        # Abandoned: inv_index[word] = [[file_path, word_pos],[]]
        file_path = self.path_list
        sentence_dict = {}
        for path_a in file_path:
            # open a single file and convert it to string
            file_a = open(path_a, mode='r')
            str_a = file_a.read()
            # Case insensitive
            str_a = str_a.lower()
            # list of sentence
            # sentence dict{'file_path':{file}, 'second file_path':{}}
            # file:{'1': [start pos, end pos], '2': [start pos, end pos]}
            # indexing sentence
            pos = 0
            sentence_no = 1
            sentence_temp_dict = {}
            while pos < len(str_a):
                temp_list = locate_sentence([path_a, pos])
                # print(temp_list)
                sentence_temp_dict[sentence_no] = temp_list[1:]
                # print(sentence_no, temp_list[1:])
                pos = temp_list[2] + 1
                sentence_no += 1
            # print("temp_dict:", temp_dict)
            sentence_dict[path_a] = sentence_temp_dict
            # indexing word in this file
            # inv_index: {'word':{"path1":[pos1, pos3], "path2":[pos3, pos4]}, 'word2':{'path': [pos]}}
            # inv_index[word] = {"path1":[pos1, pos3], "path2":[pos3, pos4]}
            print("done sentence")
            j = 0
            for i in range(len(str_a)):
                if not str_a[i].isalpha():
                    if str_a[j].isalpha():
                        temp_str = str_a[j:i]
                        if temp_str not in inv_index:
                            # inv_index[temp_str] = {}
                            word_temp_dict = {}
                            pos_list = [j]
                            word_temp_dict[path_a] = pos_list
                            inv_index[temp_str] = word_temp_dict
                        else:
                            if path_a in inv_index[temp_str]:
                                inv_index[temp_str][path_a].append(j)
                            else:
                                inv_index[temp_str][path_a] = [j]
                            # inv_index[temp_str] = [[path_a, j]]
                        j = i
                elif not str_a[j].isalpha():
                    # find the starting pos of the next word
                    j = i
            file_a.close()
        print("inverted_dict: ", inv_index)
        return inv_index, sentence_dict

    def search_result_present(self, result, word_list, sentence_index, exist, search_str):
        print("Inside func search_result_present")
        print("result:", result)
        # sentence_index described the pos of each sentences
        # set the font for label and plain text editor
        label_font = QLabel().font()
        label_font.setPointSize(10)
        label_font.setBold(True)
        text_font = QLabel().font()
        text_font.setPointSize(15)
        print("font done")
        # Init QDialog
        search_result = QDialog()
        search_result.setWindowTitle("Inverted search result")
        result_count = 0
        print("init window")
        # Init Layout
        saw_content = QWidget()
        v_layout = QVBoxLayout(saw_content)
        # result string
        search_string = QLabel()
        search_string.setText("Result of: " + search_str)
        print(1)
        temp_font = search_string.font()
        temp_font.setBold(True)
        temp_font.setPointSize(15)
        print(2)
        search_string.setFont(temp_font)
        print(3)
        v_layout.addWidget(search_string)
        print("exist:", exist)
        if exist:
            for key in result.keys():
                # get the number of result
                result_count += len(result[key])
            print("result count")
            rank_dict = {}
            for key in result.keys():
                # key is the path of the file
                print("key:", key)
                i = 0
                # thoughts on implementing TF-IDF ranking
                # init & calculate the TDF-ID value of each result.
                # store QWidgets in list
                # use this list as key, TDF-ID as value
                # sort this dict. Output by TDF-ID value

                while i < len(result[key]):
                    widgets_list = []
                    temp_label = QLabel()
                    temp_label.setText(key)
                    temp_label.setFont(label_font)
                    # v_layout.addWidget(temp_label)
                    widgets_list.append(temp_label)
                    temp_text = QPlainTextEdit()
                    temp_text.setReadOnly(True)
                    temp_text.setFont(text_font)
                    temp_text.setMaximumHeight(90)
                    # temp_text.sizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                    # print(sentence_index[key][result[key][i]])
                    sentence_pos = sentence_index[key][result[key][i]]  # return [start_pos, end_pos]
                    temp_file = open(key, mode='r')
                    temp_str = temp_file.read()
                    show_str = temp_str[sentence_pos[0]: sentence_pos[1]]
                    temp_text.setPlainText(show_str)
                    print(show_str)
                    # set high light
                    word_pos = []
                    print("word_list:", word_list)
                    value_str = ""
                    rank_value = 0
                    for word in word_list:
                        print("get pos for word:", word)
                        # get pos of target
                        kmp_temp_result = kmp_matching(show_str.lower(), word)
                        print(kmp_temp_result)
                        if kmp_temp_result == -1:
                            continue
                        kmp_result = []
                        # THIS LINE IS FOR TESTING ONLY!!!!!
                        # kmp_result = kmp_temp_result.copy()
                        # kmp_result = kmp_temp_result
                        # check if pos correct
                        # TODO:correct this, when word is at the end of the sentence
                        for j in range(len(kmp_temp_result)):
                            if kmp_temp_result[j] == 0 and \
                                    kmp_temp_result[j] + len(word) - 1 == len(show_str) - 1:
                                # "word"
                                kmp_result.append(kmp_temp_result[j])
                            elif kmp_temp_result[j] == 0 and \
                                    not show_str[kmp_temp_result[j] + len(word)].isalpha():
                                # "word_"
                                kmp_result.append(kmp_temp_result[j])
                            elif kmp_temp_result[j] + len(word) - 1 == len(show_str) - 1 and \
                                    not show_str[kmp_temp_result[j] - 1].isalpha():
                                # "_word"
                                kmp_result.append(kmp_temp_result[j])
                            elif not show_str[kmp_temp_result[j] - 1].isalpha() and \
                                    not show_str[kmp_temp_result[j] + len(word)].isalpha():
                                kmp_result.append(kmp_temp_result[j])
                        print("kmp_result:", kmp_result)
                        if kmp_result != -1:
                            print("inside kmp_result")
                            # word exist in this result
                            word_pos.extend(kmp_result)
                            # calculating tf-idf
                            tf_idf_value = tf_idf_cal(token_word_count(temp_str), len(self.path_list), key,
                                                      self.inv_index[word])
                            rank_value += (tf_idf_value * len(kmp_result))
                            value_str += (word + '(' + ('%.3f' % tf_idf_value) + ') ')
                        print(word_pos)
                    print("outside for word")
                    # print(value_str)
                    tf_idf_label = QLabel()
                    tf_idf_label.setText("TF-IDF: " + ('%.3f' % rank_value) + '\n' + value_str)
                    # v_layout.addWidget(tf_idf_label)
                    widgets_list.append(tf_idf_label)
                    # implementing highlight
                    document = temp_text.document()
                    highlight_cursor = QTextCursor(document)
                    cursor = QTextCursor(document)
                    print("before high light")
                    cursor.beginEditBlock()
                    color_format = QTextCharFormat(highlight_cursor.charFormat())
                    color_format.setBackground(Qt.yellow)
                    for i_alter in range(0, len(word_pos)):
                        pos = len(word_pos) - 1 - i_alter
                        QTextCursor.setPosition(highlight_cursor, word_pos[pos])
                        highlight_cursor.select(QTextCursor.WordUnderCursor)
                        highlight_cursor.mergeCharFormat(color_format)
                    cursor.endEditBlock()
                    print("done high light")
                    temp_file.close()
                    # v_layout.addWidget(temp_text)
                    widgets_list.append(temp_text)
                    widgets_tuple = tuple(widgets_list)
                    # print(widgets_list)
                    rank_dict[widgets_tuple] = rank_value
                    i += 1
            # print("sorting dict")
            # sorted_list = sorted_dict(rank_dict, rank_dict.keys(), True)
            aux = [(rank_dict[k], k) for k in rank_dict.keys()]
            aux.sort(key=takeFirst, reverse=True)
            sorted_list = [k for v, k in aux]
            # print("done dict")
            # print(len(sorted_list))
            scroll_area = QScrollArea(search_result)
            for key in sorted_list:
                for i in key:
                    v_layout.addWidget(i)
            scroll_area.setWidget(saw_content)
            scroll_area.setFixedSize(800, 500)
            # search_result.sizePolicy(QSizePolicy.Preferred)
            search_result.exec()
        else:
            self.target_not_find()

    # FUNC RELATED TO STATUS BAR
    def text_changed(self):
        print("in func text_changed")
        self.word_count.setText(len(self.plainTextEdit.toPlainText()).__str__() + " Char")
        self.statusbar.clearMessage()

    def cursor_pos_changed(self):
        # Ln is actually block num
        print("In func cursor_pos_changed")
        # col = self.text_cursor.columnNumber()
        # row = self.text_cursor.blockNumber()
        temp_cursor = self.plainTextEdit.textCursor()
        col = temp_cursor.columnNumber()
        row = temp_cursor.blockNumber()
        print(self.plainTextEdit.textCursor().positionInBlock())
        print(self.plainTextEdit.textCursor().position())
        str_a = "Bl:" + str(row+1) + " \t "+"Col:" + str(col+1)
        self.courser_pos.setText(str_a)
        # remove highlight
        # if self.highlight:
            # self.rem_hl_pressed()   # remove high light

    def change_font_size(self):
        print("In func change_font_size")
        size = self.font_size.currentText()
        if size.isdigit():
            self.editor_font.setPointSize(int(size))
            self.plainTextEdit.setFont(self.editor_font)
        # elif size == "":
        #     pass    # do nothing if it's blank
        else:
            # if not digit, set to default size
            self.font_size.setCurrentIndex(6)
            self.editor_font.setPointSize(20)
            self.plainTextEdit.setFont(self.editor_font)

# TODO: check if saved when closing window
# TODO: different arrangement for & and |
# DONE: consider move some of the func to Structure.py
