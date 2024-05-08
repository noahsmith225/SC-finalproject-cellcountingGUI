"""
Final Project - Development of a Python-based GUI for Interactive Cell Analysis and Quantification

Authors: Valentina Matos Romero, Noah Daniel Smith
Last Modified May 7, 2024

Note:This code defines the user interface (UI) for a Python-based GUI used for interactive cell analysis and
quantification. It sets up various widgets and layouts using PySide2's QtWidgets module to create a functional
interface for users to input parameters and view results. The architecture of the code was created with QT designer.
"""


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Check if MainWindow has an object name; if not, set it to "MainWindow"
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # Set the initial size of MainWindow to 590x272
        MainWindow.resize(590, 272)

        self.action = QAction(MainWindow)  # Create QAction
        self.action.setObjectName(u"action")  # Set object name for QAction

        self.centralwidget = QWidget(MainWindow)  # Create central QWidget
        self.centralwidget.setObjectName(u"centralwidget")  # Set object name for central QWidget

        self.gridLayout_2 = QGridLayout(self.centralwidget)  # Create QGridLayout for central QWidget
        self.gridLayout_2.setObjectName(u"gridLayout_2")  # Set object name for QGridLayout of central QWidget

        self.frame = QFrame(self.centralwidget)  # Create QFrame for central QWidget
        self.frame.setObjectName(u"frame")  # Set object name for QFrame
        self.frame.setFrameShape(QFrame.StyledPanel)  # Set frame's shape to StyledPanel
        self.frame.setFrameShadow(QFrame.Raised)  # Set frame's shadow to Raised

        self.gridLayout_3 = QGridLayout(self.frame)  # Create QGridLayout for QFrame
        self.gridLayout_3.setObjectName(u"gridLayout_3")  # Set object name for QGridLayout of QFrame
        self.gridLayout = QGridLayout()  # Create QGridLayout for organizing widgets
        self.gridLayout.setObjectName(u"gridLayout")  # Set object name for QGridLayout

        self.label_4 = QLabel(self.frame)  # Create QLabel and add to QFrame
        self.label_4.setObjectName(u"label_4")  # Set object name for QLabel

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.sizeobject_SB = QDoubleSpinBox(self.frame)  # Create a QDoubleSpinBox widget within the frame
        self.sizeobject_SB.setObjectName(u"sizeobject_SB")  # Set the object name of the QDoubleSpinBox
        self.sizeobject_SB.setDecimals(2)  # Set the number of decimal places displayed to 1
        self.sizeobject_SB.setSingleStep(0.05)  # Set the step value when incrementing/decrementing to 0.1
        self.sizeobject_SB.setValue(0.1)  # Set the initial value of the QDoubleSpinBox to 0.2

        self.gridLayout.addWidget(self.sizeobject_SB, 0, 1, 1, 1)  # Add the sizeobject_SB widget to gridLayout

        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)  # Add gridLayout to gridLayout_3

        self.horizontalLayout_5 = QHBoxLayout()  # Create a QHBoxLayout
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")  # Set object name for layout

        self.label_6 = QLabel(self.frame)  # Create a QLabel within the frame
        self.label_6.setObjectName(u"label_6")  # Set object name for the label

        self.horizontalLayout_5.addWidget(self.label_6)  # Add the label to the QHBoxLayout

        self.image_LE = QLineEdit(self.frame)  # Create a QLineEdit within the frame
        self.image_LE.setObjectName(u"image_LE")  # Set object name for the line edit

        self.horizontalLayout_5.addWidget(self.image_LE)  # Add the line edit to the QHBoxLayout

        self.browseimagepath_TB = QToolButton(self.frame)  # Create a QToolButton within the frame
        self.browseimagepath_TB.setObjectName(u"browseimagepath_TB")  # Set object name for the tool button

        self.horizontalLayout_5.addWidget(self.browseimagepath_TB)  # Add the tool button to the QHBoxLayout

        self.gridLayout_3.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)  # Add QHBoxLayout to gridLayout_3

        self.horizontalLayout_3 = QHBoxLayout()  # Create another QHBoxLayout
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")  # Set object name for the layout

        self.label_5 = QLabel(self.frame)  # Create another QLabel within the frame
        self.label_5.setObjectName(u"label_5")  # Set object name for the label

        self.horizontalLayout_3.addWidget(self.label_5)  # Add the label to the QHBoxLayout

        self.watershed_CB = QComboBox(self.frame)  # Create a QComboBox within the frame
        self.watershed_CB.addItem("")  # Add an item to the combo box
        self.watershed_CB.addItem("")  # Add another item to the combo box
        self.watershed_CB.setObjectName(u"watershed_CB")  # Set object name for the combo box

        self.horizontalLayout_3.addWidget(self.watershed_CB)  # Add the combo box to the QHBoxLayout

        self.gridLayout_3.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)  # Add QHBoxLayout to gridLayout_3

        self.horizontalLayout_4 = QHBoxLayout()  # Create another QHBoxLayout
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")  # Set object name for the layout

        self.horizontalSpacer = QSpacerItem(478, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)  # Create a spacer item
        self.horizontalLayout_4.addItem(self.horizontalSpacer)  # Add the spacer item to the QHBoxLayout

        self.submit_PB = QPushButton(self.frame)  # Create a QPushButton within the frame
        self.submit_PB.setObjectName(u"submit_PB")  # Set object name for the button
        self.submit_PB.setMaximumSize(QSize(60, 16777215))  # Set the maximum size for the button

        self.horizontalLayout_4.addWidget(self.submit_PB)  # Add the button to the QHBoxLayout

        self.gridLayout_3.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)  # Add QHBoxLayout to gridLayout_3

        self.horizontalLayout = QHBoxLayout()  # Create another QHBoxLayout
        self.horizontalLayout.setObjectName(u"horizontalLayout")  # Set object name for the layout

        self.label = QLabel(self.frame)  # Create another QLabel within the frame
        self.label.setObjectName(u"label")  # Set object name for the label

        self.horizontalLayout.addWidget(self.label)  # Add the label to the QHBoxLayout

        self.horizontalSpacer_2 = QSpacerItem(490, 20, QSizePolicy.Expanding,
                                              QSizePolicy.Minimum)  # Create another spacer item
        self.horizontalLayout.addItem(self.horizontalSpacer_2)  # Add the spacer item to the QHBoxLayout

        self.gridLayout_3.addLayout(self.horizontalLayout, 4, 0, 1, 1)  # Add QHBoxLayout to gridLayout_3

        self.qtable = QTableView(self.frame)  # Create a QTableView within the frame
        self.qtable.setObjectName(u"qtable")  # Set object name for the table view

        self.gridLayout_3.addWidget(self.qtable, 5, 0, 1, 1)  # Add the table view to gridLayout_3

        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)  # Add the frame to gridLayout_2

        MainWindow.setCentralWidget(self.centralwidget)  # Set the central widget of the main window
        self.statusbar = QStatusBar(MainWindow)  # Create a status bar for the main window
        self.statusbar.setObjectName(u"statusbar")  # Set object name for the status bar
        MainWindow.setStatusBar(self.statusbar)  # Set the status bar for the main window

        self.retranslateUi(MainWindow)  # Call the retranslateUi function to set up translations

        # Connect signals to slots
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    # Translate UI components
    def retranslateUi(self, MainWindow):
        # Set the window title
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cell Detection Hub", None))
        # Set text for action
        self.action.setText(QCoreApplication.translate("MainWindow", u"Get threshold", None))
        # Set text for label_4
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Minimum size object:", None))
        # Set text for label_6
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Image directory:", None))
        # Set text for browseimagepath_TB
        self.browseimagepath_TB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        # Set text for label_5
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"UseWatershed:", None))
        # Set item text for watershed_CB at index 0
        self.watershed_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"True", None))
        # Set item text for watershed_CB at index 1
        self.watershed_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"False", None))
        # Set text for submit_PB
        self.submit_PB.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        # Set text for label
        self.label.setText(QCoreApplication.translate("MainWindow", u"RESULTS:", None))
    # retranslateUi

