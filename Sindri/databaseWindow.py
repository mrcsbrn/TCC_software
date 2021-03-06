import os.path

from PySide2 import QtWidgets, QtGui, QtCore

import db
from DatabaseInterface.databaseSearchFunctions import getQueryBySearchNameFormulaOrCas
from db_addSubstanceProperties import Form_AddSubstanceProperties
from db_editSubstanceProperties import Form_EditSubstanceProperties
from ui.db_ui import Ui_databaseWindow


class databaseWindow(QtWidgets.QWidget, Ui_databaseWindow):
    def __init__(self, parent=None):
        super(databaseWindow, self).__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        self.dbfile = db.database_file
        # 26 colunas
        self.col_headers = [
            "Formula",
            "Name",
            "CAS #",
            "Mol. Wt.",
            "Tfp [K]",
            "Tb [K]",
            "Tc [K]",
            "Pc [bar]",
            "Vc [cm3/mol]",
            "Zc",
            "Omega",
            "T range (Cp) [K]",
            "a0",
            "a1",
            "a2",
            "a3",
            "a4",
            "Cp IG",
            "Cp liq.",
            "Antoine A",
            "Antoine B",
            "Antoine C",
            "Pvp min [bar]",
            "Tmin [K]",
            "Pvp max [bar]",
            "Tmax [K]",
        ]

        self.tableWidget_db.setHorizontalHeaderLabels(self.col_headers)
        header = self.tableWidget_db.horizontalHeader()
        # for i in range(len(self.col_headers)):
        #     header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget_db.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        self.load_db()
        self.database_changed = False

        # button icons
        self.btn_search.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/search_button.png"))
        )
        self.btn_save_db.setIcon(QtGui.QIcon(QtGui.QPixmap(":/images/save_button.png")))
        self.btn_addSubstance.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/add_button.png"))
        )
        self.btn_deleteSubstance.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/delete_button.png"))
        )
        self.btn_clearSearch.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/clear_button.png"))
        )
        self.btn_editSubstance.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/edit_button.png"))
        )
        self.btn_RestoreOriginalDB.setIcon(
            QtGui.QIcon(QtGui.QPixmap(":/images/restore_button.png"))
        )

        # row highlight
        from css.genStyleSheet import (
            genTableWidgetHighlightedRowSS,
            genlistWidgetHighlightedRowSS,
        )

        genTableWidgetHighlightedRowSS(self.tableWidget_db)

        self.le_db_search.setFocus()

    def load_db(self):
        # Abrir banco de dados
        if os.path.isfile(self.dbfile):
            self.show_full_db()
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Database not found")
            error_dialog.exec_()
            raise Exception("Database not found")

    def show_full_db(self):
        try:
            query = "SELECT * from v_all_properties_including_correlations"
            db.cursor.execute(query)
            results = db.cursor.fetchall()
            self.update_table_db(results)
        except:
            pass

    def update_table_db(self, results):
        self.tableWidget_db.setRowCount(0)

        for row_number, row_data in enumerate(results):
            self.tableWidget_db.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.tableWidget_db.setItem(
                    row_number, col_number, QtWidgets.QTableWidgetItem(str(data))
                )

    def search_substance(self):
        substance_string_name = str(self.le_db_search.text())
        if substance_string_name == "":
            self.show_full_db()
        else:
            try:
                query = getQueryBySearchNameFormulaOrCas(substance_string_name)
                db.cursor.execute(query)
                results = db.cursor.fetchall()
                self.update_table_db(results)
            except:
                self.tableWidget_db.setRowCount(0)

    def add_substance(self):
        self.addSubstanceWindow = Form_AddSubstanceProperties()
        self.addSubstanceWindow.signal.connect(self.is_database_edited)
        self.addSubstanceWindow.signal.connect(self.search_substance)
        self.addSubstanceWindow.show()

    def restore_original_database(self):

        restore_msg = "Are you sure you want to restore the database?"
        choice = QtWidgets.QMessageBox.question(
            self,
            "Restoring database",
            restore_msg,
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )

        if choice == QtWidgets.QMessageBox.Yes:
            try:
                from shutil import copyfile

                db.db.close()
                copyfile(db.database_file + ".orig", db.database_file)
                db.init()
                self.search_substance()
                self.database_changed = False
            except:
                msg = QtWidgets.QMessageBox.about(
                    self, "Error", "Could not restore original database"
                )

    def edit_substance(self):

        current_row = self.tableWidget_db.currentRow()
        if current_row >= 0:
            hr = self.get_row_values(26)
            self.editSubstanceWindow = Form_EditSubstanceProperties(hl_row=hr)
            self.editSubstanceWindow.signal_changes_made.connect(self.search_substance)
            self.editSubstanceWindow.signal_changes_made.connect(
                self.is_database_edited
            )
            self.editSubstanceWindow.show()

    def is_database_edited(self, s):
        if s == True:
            self.database_changed = True

    def get_row_values(self, n):

        row_values = []
        current_row = self.tableWidget_db.currentRow()

        for i in range(n):
            item = self.tableWidget_db.item(current_row, i).text()
            row_values.append(item)

        return row_values

    def del_substance(self):

        current_row = self.tableWidget_db.currentRow()
        if current_row >= 0:

            row_values = self.get_row_values(3)
            choice = QtWidgets.QMessageBox.question(
                self,
                "Deleting item",
                "Are you sure you want to delete '" + row_values[1] + "'?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )

            if choice == QtWidgets.QMessageBox.Yes:
                try:
                    self.database_changed = True
                    query = (
                        "SELECT substance_id FROM substance WHERE name='"
                        + str(row_values[1])
                        + "' AND formula='"
                        + row_values[0]
                        + "' AND cas='"
                        + row_values[2]
                        + "'"
                    )
                    db.cursor.execute(query)
                    substance_id = "'{:d}'".format(db.cursor.fetchone()[0])
                    query = "DELETE from cp_correlations where substance_id={0}".format(
                        substance_id
                    )
                    db.cursor.execute(query)
                    query = "DELETE FROM antoine_correlations where substance_id={0}".format(
                        substance_id
                    )
                    db.cursor.execute(query)
                    query = "DELETE FROM substance where substance_id={0}".format(
                        substance_id
                    )
                    db.cursor.execute(query)
                    self.search_substance()
                except Exception as e:
                    print(str(e))
                    pass

    def save_db(self):
        self.database_changed = False
        choice = QtWidgets.QMessageBox.question(
            self,
            "Saving database",
            "Are you sure you want to save the database?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if choice == QtWidgets.QMessageBox.Yes:
            try:
                db.db.commit()
                msg = QtWidgets.QMessageBox.about(
                    self, "Confirmation", "Database has been saved"
                )
                msg.exec_()
            except:
                pass
        else:
            db.db.rollback()
            self.show_full_db()

    def clear_search(self):
        self.le_db_search.clear()
        self.le_db_search.setFocus()

    def closeEvent(self, QCloseEvent):
        if self.database_changed:
            quit_msg = "Do you want to save the database?"
            choice = QtWidgets.QMessageBox.question(
                self,
                "Database has been changed",
                quit_msg,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if choice == QtWidgets.QMessageBox.Yes:
                db.db.commit()
            elif choice == QtWidgets.QMessageBox.No:
                db.db.rollback()
        self.database_changed = False
        self.le_db_search.clear()
        self.show_full_db()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = databaseWindow()
    ui.show()
    sys.exit(app.exec_())
