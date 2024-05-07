# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(590, 314)
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(9, 9, 566, 384))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.image_LE = QLineEdit(self.frame)
        self.image_LE.setObjectName(u"image_LE")

        self.horizontalLayout_5.addWidget(self.image_LE)

        self.browseimagepath_TB = QToolButton(self.frame)
        self.browseimagepath_TB.setObjectName(u"browseimagepath_TB")

        self.horizontalLayout_5.addWidget(self.browseimagepath_TB)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.sizeobject_SB = QDoubleSpinBox(self.frame)
        self.sizeobject_SB.setObjectName(u"sizeobject_SB")
        self.sizeobject_SB.setDecimals(1)
        self.sizeobject_SB.setSingleStep(0.100000000000000)
        self.sizeobject_SB.setValue(0.200000000000000)

        self.gridLayout.addWidget(self.sizeobject_SB, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_3.addWidget(self.label_5)

        self.watershed_CB = QComboBox(self.frame)
        self.watershed_CB.addItem("")
        self.watershed_CB.addItem("")
        self.watershed_CB.setObjectName(u"watershed_CB")

        self.horizontalLayout_3.addWidget(self.watershed_CB)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(478, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.submit_PB = QPushButton(self.frame)
        self.submit_PB.setObjectName(u"submit_PB")
        self.submit_PB.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_4.addWidget(self.submit_PB)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"QProgressBar{\n"
"	background-color: rgb(200, 200, 200);\n"
"	color: rgb(170, 85, 127);\n"
"	border-style: solid;\n"
"	border-radius: 10px;\n"
"	text-align: center;\n"
"	\n"
"}\n"
"\n"
"QProgressBar::Chunk{\n"
"border-radius:10px;\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(195, 112, 254, 255), stop:1 rgba(164, 203, 255, 255));\n"
"}\n"
"")
        self.progressBar.setValue(24)

        self.horizontalLayout_2.addWidget(self.progressBar)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(490, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 0, 1, 1)

        self.qtable = QTableView(self.frame)
        self.qtable.setObjectName(u"qtable")

        self.gridLayout_2.addWidget(self.qtable, 6, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Cell Detection Hub", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"Get threshold", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Image directory:", None))
        self.browseimagepath_TB.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Minimum size object:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"UseWatershed:", None))
        self.watershed_CB.setItemText(0, QCoreApplication.translate("MainWindow", u"True", None))
        self.watershed_CB.setItemText(1, QCoreApplication.translate("MainWindow", u"False", None))

        self.submit_PB.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Cell count progress:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"RESULTS:", None))
    # retranslateUi

