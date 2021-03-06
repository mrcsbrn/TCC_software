from PySide2 import QtWidgets, QtGui

from ui.binary_interaction_parameters_ui import Ui_FormBinaryParameters


class EditBinaryInteractionParametersView(QtWidgets.QWidget, Ui_FormBinaryParameters):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/images/main_logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.setWindowIcon(icon)

        from Controllers.EditBinaryInteractionParametersController import (
            EditBinaryInteractionParametersController,
        )

        self.controller: EditBinaryInteractionParametersController = controller

        self.btn_ok.clicked.connect(self.clicked_ok)
        self.btn_cancel.clicked.connect(self.clicked_cancel)
        self.btn_setZero.clicked.connect(self.clicked_setZero)
        self.btn_setSymmetric.clicked.connect(self.clicked_setSymmetric)
        # self.btn_fitToExp.clicked.connect(self.clicked_fitToExp)

    def clicked_ok(self):
        self.controller.okClicked()

    def clicked_cancel(self):
        self.controller.cancelClicked()

    def clicked_setZero(self):
        self.controller.setZeroClicked()

    def clicked_setSymmetric(self):
        self.controller.setSymmetricClicked()

    # def clicked_fitToExp(self):
    #     self.controller.fitToExpClicked()
