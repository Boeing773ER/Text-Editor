from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMouseTracking(False)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        MainWindow.setToolTip("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 50, 691, 411))
        self.plainTextEdit.setObjectName("plainTextEdit")
        MainWindow.setCentralWidget(self.centralwidget)
        # menubar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        #File: QMenu
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuCoding = QtWidgets.QMenu(self.menubar)
        self.menuCoding.setObjectName("menuCoding")
        self.menuAdvanced = QtWidgets.QMenu(self.menubar)
        self.menuAdvanced.setObjectName("menuAdvanced")
        MainWindow.setMenuBar(self.menubar)

        # statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # toolBar
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # QAction within menuBar
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionFind = QtWidgets.QAction(MainWindow)
        self.actionFind.setObjectName("actionFind")
        self.actionReplace = QtWidgets.QAction(MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionOpen_2 = QtWidgets.QAction(MainWindow)
        self.actionOpen_2.setObjectName("actionOpen_2")
        self.actionSave_2 = QtWidgets.QAction(MainWindow)
        self.actionSave_2.setObjectName("actionSave_2")
        self.actionEncode = QtWidgets.QAction(MainWindow)
        self.actionEncode.setObjectName("actionEncode")
        self.actionDecode = QtWidgets.QAction(MainWindow)
        self.actionDecode.setObjectName("actionDecode")
        self.actionAdvanced_Search = QtWidgets.QAction(MainWindow)
        self.actionAdvanced_Search.setObjectName("actionAdvanced_Search")
        self.actionStatistic = QtWidgets.QAction(MainWindow)
        self.actionStatistic.setObjectName("actionStatistic")

        # QAction for toolbar
        self.tb_New = QtWidgets.QAction(MainWindow)
        self.tb_New.setObjectName("tb_New")

        # add action to menuBar
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen_2)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_2)
        self.menuEdit.addAction(self.actionFind)
        self.menuEdit.addAction(self.actionReplace)
        self.menuCoding.addAction(self.actionEncode)
        self.menuCoding.addAction(self.actionDecode)
        self.menuAdvanced.addAction(self.actionAdvanced_Search)
        self.menuAdvanced.addAction(self.actionStatistic)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuCoding.menuAction())
        self.menubar.addAction(self.menuAdvanced.menuAction())
        # toolBar
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # for multi language
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuCoding.setTitle(_translate("MainWindow", "Coding"))
        self.menuAdvanced.setTitle(_translate("MainWindow", "Advanced"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionFind.setText(_translate("MainWindow", "Find"))
        self.actionReplace.setText(_translate("MainWindow", "Replace"))
        self.actionOpen_2.setText(_translate("MainWindow", "Open"))
        self.actionSave_2.setText(_translate("MainWindow", "Save"))
        self.actionEncode.setText(_translate("MainWindow", "Encode"))
        self.actionDecode.setText(_translate("MainWindow", "Decode"))
        self.actionAdvanced_Search.setText(_translate("MainWindow", "Advanced Search"))
        self.actionStatistic.setText(_translate("MainWindow", "Statistic"))
