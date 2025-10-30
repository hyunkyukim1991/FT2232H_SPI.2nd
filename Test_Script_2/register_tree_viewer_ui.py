# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_tree_viewer.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QSpacerItem,
    QSplitter, QStatusBar, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_RegisterTreeViewer(object):
    def setupUi(self, RegisterTreeViewer):
        if not RegisterTreeViewer.objectName():
            RegisterTreeViewer.setObjectName(u"RegisterTreeViewer")
        RegisterTreeViewer.resize(1046, 569)
        self.action_open_excel = QAction(RegisterTreeViewer)
        self.action_open_excel.setObjectName(u"action_open_excel")
        self.action_save_json = QAction(RegisterTreeViewer)
        self.action_save_json.setObjectName(u"action_save_json")
        self.action_exit = QAction(RegisterTreeViewer)
        self.action_exit.setObjectName(u"action_exit")
        self.action_expand_all = QAction(RegisterTreeViewer)
        self.action_expand_all.setObjectName(u"action_expand_all")
        self.action_collapse_all = QAction(RegisterTreeViewer)
        self.action_collapse_all.setObjectName(u"action_collapse_all")
        self.action_about = QAction(RegisterTreeViewer)
        self.action_about.setObjectName(u"action_about")
        self.actionSPI = QAction(RegisterTreeViewer)
        self.actionSPI.setObjectName(u"actionSPI")
        self.actionI2C = QAction(RegisterTreeViewer)
        self.actionI2C.setObjectName(u"actionI2C")
        self.actionSerial = QAction(RegisterTreeViewer)
        self.actionSerial.setObjectName(u"actionSerial")
        self.centralwidget = QWidget(RegisterTreeViewer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setObjectName(u"main_layout")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tree_widget = QTreeWidget(self.splitter)
        self.tree_widget.setObjectName(u"tree_widget")
        self.tree_widget.setMinimumSize(QSize(600, 0))
        self.splitter.addWidget(self.tree_widget)
        self.desc_widget = QWidget(self.splitter)
        self.desc_widget.setObjectName(u"desc_widget")
        self.desc_widget.setMinimumSize(QSize(300, 0))
        self.desc_widget.setMaximumSize(QSize(400, 16777215))
        self.desc_layout = QVBoxLayout(self.desc_widget)
        self.desc_layout.setObjectName(u"desc_layout")
        self.desc_layout.setContentsMargins(0, 0, 0, 0)
        self.desc_label = QLabel(self.desc_widget)
        self.desc_label.setObjectName(u"desc_label")
        font = QFont()
        font.setBold(True)
        self.desc_label.setFont(font)

        self.desc_layout.addWidget(self.desc_label)

        self.desc_text = QTextEdit(self.desc_widget)
        self.desc_text.setObjectName(u"desc_text")
        self.desc_text.setMaximumSize(QSize(16777215, 200))
        self.desc_text.setReadOnly(True)

        self.desc_layout.addWidget(self.desc_text)

        self.vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.desc_layout.addItem(self.vertical_spacer)

        self.splitter.addWidget(self.desc_widget)

        self.main_layout.addWidget(self.splitter)

        RegisterTreeViewer.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(RegisterTreeViewer)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1046, 33))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        self.menuSetup = QMenu(self.menubar)
        self.menuSetup.setObjectName(u"menuSetup")
        RegisterTreeViewer.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(RegisterTreeViewer)
        self.statusbar.setObjectName(u"statusbar")
        RegisterTreeViewer.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menuSetup.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_open_excel)
        self.menu_file.addAction(self.action_save_json)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_view.addAction(self.action_expand_all)
        self.menu_view.addAction(self.action_collapse_all)
        self.menu_help.addAction(self.action_about)
        self.menuSetup.addSeparator()
        self.menuSetup.addAction(self.actionSPI)
        self.menuSetup.addAction(self.actionI2C)
        self.menuSetup.addAction(self.actionSerial)

        self.retranslateUi(RegisterTreeViewer)

        QMetaObject.connectSlotsByName(RegisterTreeViewer)
    # setupUi

    def retranslateUi(self, RegisterTreeViewer):
        RegisterTreeViewer.setWindowTitle(QCoreApplication.translate("RegisterTreeViewer", u"Register Tree Viewer", None))
        self.action_open_excel.setText(QCoreApplication.translate("RegisterTreeViewer", u"Open Excel File", None))
#if QT_CONFIG(shortcut)
        self.action_open_excel.setShortcut(QCoreApplication.translate("RegisterTreeViewer", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.action_save_json.setText(QCoreApplication.translate("RegisterTreeViewer", u"Save as JSON", None))
#if QT_CONFIG(shortcut)
        self.action_save_json.setShortcut(QCoreApplication.translate("RegisterTreeViewer", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_exit.setText(QCoreApplication.translate("RegisterTreeViewer", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.action_exit.setShortcut(QCoreApplication.translate("RegisterTreeViewer", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_expand_all.setText(QCoreApplication.translate("RegisterTreeViewer", u"Expand All", None))
#if QT_CONFIG(shortcut)
        self.action_expand_all.setShortcut(QCoreApplication.translate("RegisterTreeViewer", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.action_collapse_all.setText(QCoreApplication.translate("RegisterTreeViewer", u"Collapse All", None))
#if QT_CONFIG(shortcut)
        self.action_collapse_all.setShortcut(QCoreApplication.translate("RegisterTreeViewer", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("RegisterTreeViewer", u"About", None))
        self.actionSPI.setText(QCoreApplication.translate("RegisterTreeViewer", u"SPI", None))
        self.actionI2C.setText(QCoreApplication.translate("RegisterTreeViewer", u"I2C", None))
        self.actionSerial.setText(QCoreApplication.translate("RegisterTreeViewer", u"Serial", None))
        ___qtreewidgetitem = self.tree_widget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("RegisterTreeViewer", u"Register/Field", None));
        self.desc_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Description:", None))
        self.desc_text.setPlaceholderText(QCoreApplication.translate("RegisterTreeViewer", u"Select a register or field to view description", None))
        self.menu_file.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"File", None))
        self.menu_view.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"View", None))
        self.menu_help.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"Help", None))
        self.menuSetup.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"Setup", None))
    # retranslateUi

