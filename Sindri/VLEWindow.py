import numpy as np
from PySide2 import QtWidgets

from Factories.EOSMixFactory import createEOSMix, getEOSMixOptions
from EOSMixture import calc_options
from ui.vle_ui import Ui_FormVLE
from units import conv_unit, temperature_options, pressure_options

diagram_types = ["isothermal", "isobaric"]


class Window_VLE(QtWidgets.QWidget, Ui_FormVLE):
    def __init__(
        self, subsInSystem, initialMolarFraction, k, t, tunit, p, punit, parent=None
    ):
        super(Window_VLE, self).__init__(parent)
        self.setupUi(self)

        self.subsInSystem = subsInSystem
        self.k = k
        self.n = len(self.subsInSystem)
        self.initialMolarFraction = initialMolarFraction
        self.eosname = ""
        self.calctype = ""

        self.molarFractions_headers = ["Name", "Formula", "Molar fraction"]
        self.initialP = p
        self.initialT = t
        self.initialPunit = punit
        self.initialTunit = tunit

        self.diagtype = diagram_types[0]
        self.expfilename = ""

        # connections
        self.comboBox_EOS.currentTextChanged.connect(self._setEOSname)
        self.comboBox_CalcType.currentTextChanged.connect(self._setCalculationChanges)
        self.comboBox_Punit.currentTextChanged.connect(self._setCalculationChanges)
        self.comboBox_Tunit.currentTextChanged.connect(self._setCalculationChanges)
        self.btn_calculate.clicked.connect(self.calculate)
        self.comboBox_diagramType.currentTextChanged.connect(self._setDiagType)
        self.btn_openExpData.clicked.connect(self._openExpDataFile)
        self.btn_plot.clicked.connect(self._plot)
        self.btn_saveToTxtBinaryMixData.clicked.connect(
            self._saveToTxtBinaryMixtureData
        )
        self._connectPlotCheckBox()

        self._initialSetup()
        self.label_VarAnswerUnits.setText("[bar]")

    def _initialSetup(self):
        # initialize tablewidget of molar fractions
        self.tableWidget_MolarFractions.setRowCount(self.n)
        self.tableWidget_MolarFractions.setColumnCount(3)

        self.tableWidget_MolarFractions.setHorizontalHeaderLabels(
            self.molarFractions_headers
        )
        self.tableWidget_Results.setRowCount(self.n)
        self.results_col_count = 6
        self.tableWidget_Results.setColumnCount(self.results_col_count)

        for i in range(self.n):
            n = QtWidgets.QTableWidgetItem(self.subsInSystem[i].Name)
            f = QtWidgets.QTableWidgetItem(self.subsInSystem[i].Formula)
            fraction = QtWidgets.QTableWidgetItem(
                "{:.5f}".format(self.initialMolarFraction[i])
            )

            self.tableWidget_MolarFractions.setItem(i, 0, n)
            self.tableWidget_MolarFractions.setItem(i, 1, f)
            self.tableWidget_MolarFractions.setItem(i, 2, fraction)
            self.tableWidget_Results.setItem(
                i, 0, QtWidgets.QTableWidgetItem(self.subsInSystem[i].Name)
            )
            self.tableWidget_Results.setItem(
                i, 1, QtWidgets.QTableWidgetItem(self.subsInSystem[i].Formula)
            )

        mixeosoptions = getEOSMixOptions()
        # self.comboBox_EOS.addItems(list(vle_options.keys()))
        self.comboBox_EOS.addItems(mixeosoptions)
        self.comboBox_CalcType.addItems(list(calc_options.keys()))
        self.comboBox_Tunit.addItems(temperature_options)
        self.comboBox_Punit.addItems(pressure_options)

        self.le_Tvalue.setText(self.initialT)
        self.le_Pvalue.setText(self.initialP)
        self.comboBox_Tunit.setCurrentText(self.initialTunit)
        self.comboBox_Punit.setCurrentText(self.initialPunit)

        if self.n > 2:
            self.tabWidget_VLE.setTabEnabled(1, False)
        else:
            self.comboBox_diagramType.addItems(diagram_types)

    def calculate(self):

        # self.VLEeq = VLE(self.subsInSystem, self.eosname, self.k)
        self.VLEeq = createEOSMix(self.subsInSystem, self.eosname, self.k)

        # check if P and T are numbers
        if not self._PandTareValidNumbers():
            title = "P and T error"
            msg = "P and/or T are not valid numbers"
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

        # get molar fractions values
        if not self._areMolarFractonsValidNumbers():
            title = "Molar fraction error"
            msg = "Molar fraction have one or more invalid numbers"
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

        p = conv_unit(
            float(self.le_Pvalue.text()), self.comboBox_Punit.currentText(), "Pa"
        )
        t = conv_unit(
            float(self.le_Tvalue.text()), self.comboBox_Tunit.currentText(), "K"
        )

        z = np.empty(self.n, dtype=np.float64)
        rn = 2
        for i in range(self.n):
            z[i] = float(self.tableWidget_MolarFractions.item(i, rn).text())

        if self.calctype == "bubbleP":
            y, p, pv, pl, k, ite = self.VLEeq.getBubblePointPressure(z, t)
            p = conv_unit(p, "Pa", self.comboBox_Punit.currentText())
            self.le_scalarAnswer.setText("{:.5e}".format(p))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(self.n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(y[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.tableWidget_Results.setItem(i, 2, sy)
                self.tableWidget_Results.setItem(i, 3, spv)
                self.tableWidget_Results.setItem(i, 4, spl)
                self.tableWidget_Results.setItem(i, 5, sk)

        elif self.calctype == "dewP":
            x, p, pv, pl, k, ite = self.VLEeq.getDewPointPressure(z, t)
            p = conv_unit(p, "Pa", self.comboBox_Punit.currentText())
            self.le_scalarAnswer.setText("{:.5e}".format(p))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(self.n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(x[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.tableWidget_Results.setItem(i, 2, sy)
                self.tableWidget_Results.setItem(i, 3, spv)
                self.tableWidget_Results.setItem(i, 4, spl)
                self.tableWidget_Results.setItem(i, 5, sk)

        elif self.calctype == "bubbleT":
            y, t, pv, pl, k, ite = self.VLEeq.getBubblePointTemperature(z, p)
            t = conv_unit(t, "K", self.comboBox_Tunit.currentText())
            self.le_scalarAnswer.setText("{:.5e}".format(t))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(self.n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(y[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.tableWidget_Results.setItem(i, 2, sy)
                self.tableWidget_Results.setItem(i, 3, spv)
                self.tableWidget_Results.setItem(i, 4, spl)
                self.tableWidget_Results.setItem(i, 5, sk)

        elif self.calctype == "dewT":
            x, t, pv, pl, k, ite = self.VLEeq.getDewPointTemperature(z, p)
            t = conv_unit(t, "K", self.comboBox_Tunit.currentText())
            self.le_scalarAnswer.setText("{:.5e}".format(t))
            # col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            for i in range(self.n):
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(x[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.tableWidget_Results.setItem(i, 2, sy)
                self.tableWidget_Results.setItem(i, 3, spv)
                self.tableWidget_Results.setItem(i, 4, spl)
                self.tableWidget_Results.setItem(i, 5, sk)

        else:
            try:
                x, y, v, pv, pl, k, ite = self.VLEeq.getFlash(z, p, t)
            except Exception as e:
                title = "Error calculating flash"
                msg = str(e)
                QtWidgets.QMessageBox.about(self, title, msg)
                return -1
            self.le_scalarAnswer.setText("{:.7f}".format(v))
            col_headers = ["Name", "Formula", "x", "y", "Phivap", "Philiq", "K"]
            for i in range(self.n):
                sx = QtWidgets.QTableWidgetItem("{:.5f}".format(x[i]))
                sy = QtWidgets.QTableWidgetItem("{:.5f}".format(y[i]))
                spv = QtWidgets.QTableWidgetItem("{:.5f}".format(pv[i]))
                spl = QtWidgets.QTableWidgetItem("{:.5f}".format(pl[i]))
                sk = QtWidgets.QTableWidgetItem("{:.5f}".format(k[i]))
                self.tableWidget_Results.setItem(i, 2, sx)
                self.tableWidget_Results.setItem(i, 3, sy)
                self.tableWidget_Results.setItem(i, 4, spv)
                self.tableWidget_Results.setItem(i, 5, spl)
                self.tableWidget_Results.setItem(i, 6, sk)

    def _areMolarFractonsValidNumbers(self):

        s = 0.0
        try:
            for i in range(self.n):
                v = float(self.tableWidget_MolarFractions.item(i, 2).text())
                t = v * 1.0 + 1.0
                s += v
            if abs(s - 1.0) < 1e-6:
                return True
            else:
                return False
        except:
            return False

    def _setDiagType(self):
        self.diagtype = self.comboBox_diagramType.currentText()
        self.comboBox_varUnit.clear()

        if self.diagtype == diagram_types[0]:  # isothermal
            self.label_var.setText("T")
            self.comboBox_varUnit.addItems(temperature_options)
        else:
            self.label_var.setText("P")
            self.comboBox_varUnit.addItems(pressure_options)

    def _plot(self):

        if not self._isGenDataVarValid():
            title = "Variable not valid"
            msg = "Variable is not a valid number"
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

        gendata_header = ["{} [{}]", "x1", "y1"]

        try:
            # self.VLEeq = VLE(self.subsInSystem, self.eosname, self.k)
            self.VLEeq = createEOSMix(self.subsInSystem, self.eosname, self.k)
            if self.diagtype == diagram_types[0]:  # isothermal
                _v = conv_unit(
                    float(self.le_varValue.text()),
                    self.comboBox_varUnit.currentText(),
                    "K",
                )
                x, y, var = self.VLEeq.isothermalBinaryMixtureGenData(
                    _v,
                    Tunit=self.comboBox_varUnit.currentText(),
                    Punit=self.comboBox_Punit.currentText(),
                )
                gendata_header[0] = "{} [{}]".format(
                    "P", self.comboBox_Punit.currentText()
                )
            else:
                _v = conv_unit(
                    float(self.le_varValue.text()),
                    self.comboBox_varUnit.currentText(),
                    "Pa",
                )
                x, y, var = self.VLEeq.isobaricBinaryMixtureGenData(
                    _v,
                    Tunit=self.comboBox_Tunit.currentText(),
                    Punit=self.comboBox_varUnit.currentText(),
                )
                gendata_header[0] = "{} [{}]".format(
                    "T", self.comboBox_Tunit.currentText()
                )
        except Exception as e:
            title = "Error generating data to plot"
            msg = str(e)
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

        # populate table
        n = len(x)
        self.tableWidget_DataResult.setRowCount(n)
        self.tableWidget_DataResult.setColumnCount(3)
        self.tableWidget_DataResult.setHorizontalHeaderLabels(gendata_header)

        for i in range(n):
            item_var = QtWidgets.QTableWidgetItem("{:3.5e}".format(var[i]))
            item_x = QtWidgets.QTableWidgetItem("{:0.5f}".format(x[i]))
            item_y = QtWidgets.QTableWidgetItem("{:0.5f}".format(y[i]))
            self.tableWidget_DataResult.setItem(i, 0, item_var)
            self.tableWidget_DataResult.setItem(i, 1, item_x)
            self.tableWidget_DataResult.setItem(i, 2, item_y)

        if self.checkBox_plotExpData.isChecked():
            expfilename = self.expfilename
        else:
            expfilename = ""

        if self.checkBox_plotx.isChecked():
            plottype = "x"
        elif self.checkBox_ploty.isChecked():
            plottype = "y"
        else:
            plottype = "both"

        try:

            if self.diagtype == diagram_types[0]:  # isothermal
                self.VLEeq.isothermalBinaryMixturePlot(
                    _v,
                    Tunit=self.comboBox_varUnit.currentText(),
                    Punit=self.comboBox_Punit.currentText(),
                    expfilename=expfilename,
                    plottype=plottype,
                )
            else:
                self.VLEeq.isobaricBinaryMixturePlot(
                    _v,
                    Tunit=self.comboBox_Tunit.currentText(),
                    Punit=self.comboBox_varUnit.currentText(),
                    expfilename=expfilename,
                    plottype=plottype,
                )
        except Exception as e:
            title = "Error plotting"
            msg = str(e)
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

    def _saveToTxtBinaryMixtureData(self):

        try:
            extension = ".txt"
            subs1 = self.subsInSystem[0].Name
            subs2 = self.subsInSystem[1].Name
            var = float(self.le_varValue.text())
            varunit = self.comboBox_varUnit.currentText()
            name_suggestion = "{}-{}_at_{:.5f}_{}{}".format(
                subs1, subs2, var, varunit, extension
            )
            txt_file_name = QtWidgets.QFileDialog.getSaveFileName(
                self,
                "Save binary mixture data",
                name_suggestion,
                "Files (*{})".format(extension),
            )[0]
            if not txt_file_name:
                return 0

        except Exception as e:
            title = "Error getting filename"
            msg = str(e)
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

        try:
            i_n = self.tableWidget_DataResult.rowCount()
            j_n = self.tableWidget_DataResult.columnCount()

            content = ""

            # header
            if self.diagtype == diagram_types[0]:
                content += "{}\t".format(self.comboBox_Punit.currentText())
            else:
                content += "{}\t".format(self.comboBox_Tunit.currentText())
            content += "{}\t{}\n".format("x1", "y1")

            # data
            for i in range(i_n):
                content += "{}\t{}\t{}\n".format(
                    self.tableWidget_DataResult.item(i, 0).text(),
                    self.tableWidget_DataResult.item(i, 1).text(),
                    self.tableWidget_DataResult.item(i, 2).text(),
                )

            with open(txt_file_name, "w") as file:
                file.write(content)

            title = "Successfully"
            msg = "The file has been saved"
            QtWidgets.QMessageBox.about(self, title, msg)

        except Exception as e:
            title = "Error saving data to file"
            msg = str(e)
            QtWidgets.QMessageBox.about(self, title, msg)
            return -1

    def _uncheckX_and_Y(self):
        self._disconnectPlotCheckBox()
        self.checkBox_plotx.setChecked(False)
        self.checkBox_ploty.setChecked(False)
        self._connectPlotCheckBox()

    def _uncheckX_and_XY(self):
        self._disconnectPlotCheckBox()
        self.checkBox_plotx.setChecked(False)
        self.checkBox_plotxy.setChecked(False)
        self._connectPlotCheckBox()

    def _uncheckY_and_XY(self):
        self._disconnectPlotCheckBox()
        self.checkBox_plotxy.setChecked(False)
        self.checkBox_ploty.setChecked(False)
        self._connectPlotCheckBox()

    def _isGenDataVarValid(self):
        try:
            v = float(self.le_varValue.text()) * 1.0 + 1.0
            return True
        except:
            return False

    def _openExpDataFile(self):

        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Load file", "")[0]

        if not filename:
            return 0

        self.expfilename = filename
        self.le_expDataFileName.setText(self.expfilename)

    def _setCalculationChanges(self):
        self.calctype = calc_options[self.comboBox_CalcType.currentText()]

        for i in range(self.n):
            for j in range(self.results_col_count - 2):
                self.tableWidget_Results.setItem(
                    i, 2 + j, QtWidgets.QTableWidgetItem("")
                )

        if self.calctype == "bubbleP":
            self.label_VarAnswer.setText("P")
            varunit = self.comboBox_Punit.currentText()
            col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            self.molarFractions_headers[2] = "Liquid molar fractions"

        elif self.calctype == "dewP":
            self.label_VarAnswer.setText("P")
            varunit = self.comboBox_Punit.currentText()
            col_headers = ["Name", "Formula", "x", "Phivap", "Philiq", "K"]
            self.molarFractions_headers[2] = "Vapor molar fractions"
        elif self.calctype == "bubbleT":
            self.label_VarAnswer.setText("T")
            varunit = self.comboBox_Tunit.currentText()
            col_headers = ["Name", "Formula", "y", "Phivap", "Philiq", "K"]
            self.molarFractions_headers[2] = "Liquid molar fractions"

        elif self.calctype == "dewT":
            self.label_VarAnswer.setText("T")
            varunit = self.comboBox_Tunit.currentText()
            col_headers = ["Name", "Formula", "x", "Phivap", "Philiq", "K"]
            self.molarFractions_headers[2] = "Vapor molar fractions"
        else:  # Flash calculation
            self.label_VarAnswer.setText("Ratio")
            varunit = "-"
            col_headers = ["Name", "Formula", "x", "y", "Phivap", "Philiq", "K"]
            self.molarFractions_headers[2] = "Feed molar fractions"

        self.label_VarAnswerUnits.setText("[{}]".format(varunit))

        self.tableWidget_MolarFractions.setHorizontalHeaderLabels(
            self.molarFractions_headers
        )

        self.results_col_count = len(col_headers)
        self.tableWidget_Results.setColumnCount(self.results_col_count)
        self.tableWidget_Results.setHorizontalHeaderLabels(col_headers)

    def _setEOSname(self):
        self.eosname = self.comboBox_EOS.currentText()

    def _PandTareValidNumbers(self):
        try:
            t = float(self.le_Tvalue.text()) * 1.0 + 1.0
            p = float(self.le_Pvalue.text()) * 1.0 + 1.0
            return True
        except:
            return False

    def _connectPlotCheckBox(self):
        self.checkBox_plotx.stateChanged.connect(self._uncheckY_and_XY)
        self.checkBox_ploty.stateChanged.connect(self._uncheckX_and_XY)
        self.checkBox_plotxy.stateChanged.connect(self._uncheckX_and_Y)

    def _disconnectPlotCheckBox(self):
        self.checkBox_plotx.stateChanged.disconnect(self._uncheckY_and_XY)
        self.checkBox_ploty.stateChanged.disconnect(self._uncheckX_and_XY)
        self.checkBox_plotxy.stateChanged.disconnect(self._uncheckX_and_Y)
