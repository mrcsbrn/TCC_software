# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer/pure_substance_calculations_ui.ui',
# licensing of 'designer/pure_substance_calculations_ui.ui' applies.
#
# Created: Thu Feb  7 00:26:32 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PureSubstanceCalculationsWindow(object):
    def setupUi(self, PureSubstanceCalculationsWindow):
        PureSubstanceCalculationsWindow.setObjectName("PureSubstanceCalculationsWindow")
        PureSubstanceCalculationsWindow.resize(974, 648)
        self.gridLayout_3 = QtWidgets.QGridLayout(PureSubstanceCalculationsWindow)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_searchSubstance = QtWidgets.QGroupBox(PureSubstanceCalculationsWindow)
        self.groupBox_searchSubstance.setObjectName("groupBox_searchSubstance")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_searchSubstance)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btn_searchSubstance = QtWidgets.QPushButton(self.groupBox_searchSubstance)
        self.btn_searchSubstance.setObjectName("btn_searchSubstance")
        self.gridLayout_4.addWidget(self.btn_searchSubstance, 0, 0, 1, 1)
        self.le_searchSubstance = QtWidgets.QLineEdit(self.groupBox_searchSubstance)
        self.le_searchSubstance.setObjectName("le_searchSubstance")
        self.gridLayout_4.addWidget(self.le_searchSubstance, 0, 1, 1, 1)
        self.tableWidget_searchSubstance = QtWidgets.QTableWidget(self.groupBox_searchSubstance)
        self.tableWidget_searchSubstance.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_searchSubstance.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget_searchSubstance.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_searchSubstance.setAlternatingRowColors(True)
        self.tableWidget_searchSubstance.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget_searchSubstance.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_searchSubstance.setShowGrid(False)
        self.tableWidget_searchSubstance.setRowCount(0)
        self.tableWidget_searchSubstance.setColumnCount(26)
        self.tableWidget_searchSubstance.setObjectName("tableWidget_searchSubstance")
        self.tableWidget_searchSubstance.setColumnCount(26)
        self.tableWidget_searchSubstance.setRowCount(0)
        self.gridLayout_4.addWidget(self.tableWidget_searchSubstance, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox_searchSubstance, 0, 0, 1, 1)
        self.groupBox_EOS = QtWidgets.QGroupBox(PureSubstanceCalculationsWindow)
        self.groupBox_EOS.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_EOS.setObjectName("groupBox_EOS")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_EOS)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidget_eos_options = QtWidgets.QListWidget(self.groupBox_EOS)
        self.listWidget_eos_options.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_eos_options.setAlternatingRowColors(True)
        self.listWidget_eos_options.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget_eos_options.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget_eos_options.setObjectName("listWidget_eos_options")
        self.gridLayout.addWidget(self.listWidget_eos_options, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_EOS, 1, 0, 1, 1)
        self.groupBox_processVariables = QtWidgets.QGroupBox(PureSubstanceCalculationsWindow)
        self.groupBox_processVariables.setMinimumSize(QtCore.QSize(0, 50))
        self.groupBox_processVariables.setObjectName("groupBox_processVariables")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_processVariables)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_processVariables)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_procT = QtWidgets.QLineEdit(self.groupBox_processVariables)
        self.le_procT.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.le_procT.setObjectName("le_procT")
        self.horizontalLayout.addWidget(self.le_procT)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_processVariables)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.le_procP = QtWidgets.QLineEdit(self.groupBox_processVariables)
        self.le_procP.setObjectName("le_procP")
        self.horizontalLayout_2.addWidget(self.le_procP)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_processVariables, 2, 0, 1, 1)
        self.btn_calculate = QtWidgets.QPushButton(PureSubstanceCalculationsWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_calculate.sizePolicy().hasHeightForWidth())
        self.btn_calculate.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.btn_calculate.setFont(font)
        self.btn_calculate.setObjectName("btn_calculate")
        self.gridLayout_3.addWidget(self.btn_calculate, 3, 0, 1, 1)
        self.groupBox_results = QtWidgets.QGroupBox(PureSubstanceCalculationsWindow)
        self.groupBox_results.setObjectName("groupBox_results")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_results)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget_results = QtWidgets.QTableWidget(self.groupBox_results)
        self.tableWidget_results.setRowCount(2)
        self.tableWidget_results.setColumnCount(2)
        self.tableWidget_results.setObjectName("tableWidget_results")
        self.tableWidget_results.setColumnCount(2)
        self.tableWidget_results.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_results.setHorizontalHeaderItem(1, item)
        self.gridLayout_2.addWidget(self.tableWidget_results, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_results, 0, 1, 4, 1)

        self.retranslateUi(PureSubstanceCalculationsWindow)
        QtCore.QObject.connect(self.le_searchSubstance, QtCore.SIGNAL("returnPressed()"), self.btn_searchSubstance.click)
        QtCore.QMetaObject.connectSlotsByName(PureSubstanceCalculationsWindow)

    def retranslateUi(self, PureSubstanceCalculationsWindow):
        PureSubstanceCalculationsWindow.setWindowTitle(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Pure Substance Calculations", None, -1))
        self.groupBox_searchSubstance.setTitle(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Search substance", None, -1))
        self.btn_searchSubstance.setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Search", None, -1))
        self.groupBox_EOS.setTitle(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Equation of state", None, -1))
        self.groupBox_processVariables.setTitle(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Process variables", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "T [K]", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "P [bar]", None, -1))
        self.btn_calculate.setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Calculate", None, -1))
        self.groupBox_results.setTitle(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Results", None, -1))
        self.tableWidget_results.verticalHeaderItem(0).setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Molar volume (m3/mol)", None, -1))
        self.tableWidget_results.verticalHeaderItem(1).setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Z", None, -1))
        self.tableWidget_results.horizontalHeaderItem(0).setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Liquid", None, -1))
        self.tableWidget_results.horizontalHeaderItem(1).setText(QtWidgets.QApplication.translate("PureSubstanceCalculationsWindow", "Vapor", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PureSubstanceCalculationsWindow = QtWidgets.QWidget()
    ui = Ui_PureSubstanceCalculationsWindow()
    ui.setupUi(PureSubstanceCalculationsWindow)
    PureSubstanceCalculationsWindow.show()
    sys.exit(app.exec_())

