# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'register_controller.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QStatusBar, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_RegisterTreeViewer(object):
    def setupUi(self, RegisterTreeViewer):
        if not RegisterTreeViewer.objectName():
            RegisterTreeViewer.setObjectName(u"RegisterTreeViewer")
        RegisterTreeViewer.resize(1400, 800)
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
        self.action_protocol_guide = QAction(RegisterTreeViewer)
        self.action_protocol_guide.setObjectName(u"action_protocol_guide")
        self.action_about = QAction(RegisterTreeViewer)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(RegisterTreeViewer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setObjectName(u"main_layout")
        self.main_splitter = QSplitter(self.centralwidget)
        self.main_splitter.setObjectName(u"main_splitter")
        self.main_splitter.setOrientation(Qt.Horizontal)
        self.tree_widget = QTreeWidget(self.main_splitter)
        self.tree_widget.setObjectName(u"tree_widget")
        self.tree_widget.setMinimumSize(QSize(400, 0))
        self.tree_widget.setMaximumSize(QSize(500, 16777215))
        self.main_splitter.addWidget(self.tree_widget)
        self.control_widget = QWidget(self.main_splitter)
        self.control_widget.setObjectName(u"control_widget")
        self.control_widget.setMinimumSize(QSize(700, 0))
        self.control_layout = QVBoxLayout(self.control_widget)
        self.control_layout.setObjectName(u"control_layout")
        self.control_layout.setContentsMargins(0, 0, 0, 0)
        self.connection_group = QGroupBox(self.control_widget)
        self.connection_group.setObjectName(u"connection_group")
        self.connection_group.setMaximumSize(QSize(16777215, 160))
        self.connection_layout = QGridLayout(self.connection_group)
        self.connection_layout.setObjectName(u"connection_layout")
        self.protocol_label = QLabel(self.connection_group)
        self.protocol_label.setObjectName(u"protocol_label")

        self.connection_layout.addWidget(self.protocol_label, 0, 0, 1, 1)

        self.protocol_combo = QComboBox(self.connection_group)
        self.protocol_combo.addItem("")
        self.protocol_combo.addItem("")
        self.protocol_combo.addItem("")
        self.protocol_combo.setObjectName(u"protocol_combo")

        self.connection_layout.addWidget(self.protocol_combo, 0, 1, 1, 1)

        self.setup_label = QLabel(self.connection_group)
        self.setup_label.setObjectName(u"setup_label")

        self.connection_layout.addWidget(self.setup_label, 0, 2, 1, 1)

        self.setup_combo = QComboBox(self.connection_group)
        self.setup_combo.addItem("")
        self.setup_combo.addItem("")
        self.setup_combo.addItem("")
        self.setup_combo.addItem("")
        self.setup_combo.setObjectName(u"setup_combo")

        self.connection_layout.addWidget(self.setup_combo, 0, 3, 1, 1)

        self.url_label = QLabel(self.connection_group)
        self.url_label.setObjectName(u"url_label")

        self.connection_layout.addWidget(self.url_label, 1, 0, 1, 1)

        self.url_edit = QLineEdit(self.connection_group)
        self.url_edit.setObjectName(u"url_edit")

        self.connection_layout.addWidget(self.url_edit, 1, 1, 1, 3)

        self.freq_label = QLabel(self.connection_group)
        self.freq_label.setObjectName(u"freq_label")

        self.connection_layout.addWidget(self.freq_label, 2, 0, 1, 1)

        self.freq_edit = QLineEdit(self.connection_group)
        self.freq_edit.setObjectName(u"freq_edit")

        self.connection_layout.addWidget(self.freq_edit, 2, 1, 1, 1)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.connect_btn = QPushButton(self.connection_group)
        self.connect_btn.setObjectName(u"connect_btn")

        self.buttonLayout.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton(self.connection_group)
        self.disconnect_btn.setObjectName(u"disconnect_btn")
        self.disconnect_btn.setEnabled(False)

        self.buttonLayout.addWidget(self.disconnect_btn)


        self.connection_layout.addLayout(self.buttonLayout, 2, 2, 1, 2)

        self.simulate_btn = QPushButton(self.connection_group)
        self.simulate_btn.setObjectName(u"simulate_btn")

        self.connection_layout.addWidget(self.simulate_btn, 3, 0, 1, 2)


        self.control_layout.addWidget(self.connection_group)

        self.register_control_group = QGroupBox(self.control_widget)
        self.register_control_group.setObjectName(u"register_control_group")
        self.register_control_layout = QVBoxLayout(self.register_control_group)
        self.register_control_layout.setObjectName(u"register_control_layout")
        self.bit_control_frame = QFrame(self.register_control_group)
        self.bit_control_frame.setObjectName(u"bit_control_frame")
        self.bit_control_frame.setFrameShape(QFrame.StyledPanel)
        self.bit_control_layout = QVBoxLayout(self.bit_control_frame)
        self.bit_control_layout.setObjectName(u"bit_control_layout")
        self.bit_buttons_widget = QWidget(self.bit_control_frame)
        self.bit_buttons_widget.setObjectName(u"bit_buttons_widget")
        self.bit_buttons_widget.setMinimumSize(QSize(0, 80))

        self.bit_control_layout.addWidget(self.bit_buttons_widget)

        self.hex_value_layout = QHBoxLayout()
        self.hex_value_layout.setObjectName(u"hex_value_layout")
        self.hex_value_label = QLabel(self.bit_control_frame)
        self.hex_value_label.setObjectName(u"hex_value_label")

        self.hex_value_layout.addWidget(self.hex_value_label)

        self.hex_value_spinbox = QSpinBox(self.bit_control_frame)
        self.hex_value_spinbox.setObjectName(u"hex_value_spinbox")
        self.hex_value_spinbox.setDisplayIntegerBase(16)
        self.hex_value_spinbox.setMinimum(0)
        self.hex_value_spinbox.setMaximum(2147483647)
        self.hex_value_spinbox.setValue(0)
        self.hex_value_spinbox.setMaximumSize(QSize(120, 16777215))

        self.hex_value_layout.addWidget(self.hex_value_spinbox)

        self.dec_value_label = QLabel(self.bit_control_frame)
        self.dec_value_label.setObjectName(u"dec_value_label")

        self.hex_value_layout.addWidget(self.dec_value_label)

        self.dec_value_display = QLabel(self.bit_control_frame)
        self.dec_value_display.setObjectName(u"dec_value_display")

        self.hex_value_layout.addWidget(self.dec_value_display)

        self.hex_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hex_value_layout.addItem(self.hex_spacer)


        self.bit_control_layout.addLayout(self.hex_value_layout)


        self.register_control_layout.addWidget(self.bit_control_frame)

        self.spi_buttons_layout = QHBoxLayout()
        self.spi_buttons_layout.setObjectName(u"spi_buttons_layout")
        self.write_btn = QPushButton(self.register_control_group)
        self.write_btn.setObjectName(u"write_btn")
        self.write_btn.setEnabled(False)

        self.spi_buttons_layout.addWidget(self.write_btn)

        self.write_all_btn = QPushButton(self.register_control_group)
        self.write_all_btn.setObjectName(u"write_all_btn")
        self.write_all_btn.setEnabled(False)

        self.spi_buttons_layout.addWidget(self.write_all_btn)

        self.read_btn = QPushButton(self.register_control_group)
        self.read_btn.setObjectName(u"read_btn")
        self.read_btn.setEnabled(False)

        self.spi_buttons_layout.addWidget(self.read_btn)

        self.read_all_btn = QPushButton(self.register_control_group)
        self.read_all_btn.setObjectName(u"read_all_btn")
        self.read_all_btn.setEnabled(False)

        self.spi_buttons_layout.addWidget(self.read_all_btn)


        self.register_control_layout.addLayout(self.spi_buttons_layout)

        self.desc_label = QLabel(self.register_control_group)
        self.desc_label.setObjectName(u"desc_label")
        font = QFont()
        font.setBold(True)
        self.desc_label.setFont(font)

        self.register_control_layout.addWidget(self.desc_label)

        self.desc_text = QTextEdit(self.register_control_group)
        self.desc_text.setObjectName(u"desc_text")
        self.desc_text.setReadOnly(True)
        self.desc_text.setMaximumSize(QSize(16777215, 150))

        self.register_control_layout.addWidget(self.desc_text)


        self.control_layout.addWidget(self.register_control_group)

        self.log_group = QGroupBox(self.control_widget)
        self.log_group.setObjectName(u"log_group")
        self.log_group.setMaximumSize(QSize(16777215, 150))
        self.log_layout = QVBoxLayout(self.log_group)
        self.log_layout.setObjectName(u"log_layout")
        self.log_text = QTextEdit(self.log_group)
        self.log_text.setObjectName(u"log_text")
        self.log_text.setReadOnly(True)
        font1 = QFont()
        font1.setFamilies([u"Consolas"])
        font1.setPointSize(9)
        self.log_text.setFont(font1)

        self.log_layout.addWidget(self.log_text)

        self.clear_log_btn = QPushButton(self.log_group)
        self.clear_log_btn.setObjectName(u"clear_log_btn")
        self.clear_log_btn.setMaximumSize(QSize(100, 16777215))

        self.log_layout.addWidget(self.clear_log_btn)


        self.control_layout.addWidget(self.log_group)

        self.main_splitter.addWidget(self.control_widget)

        self.main_layout.addWidget(self.main_splitter)

        RegisterTreeViewer.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(RegisterTreeViewer)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1400, 22))
        self.menu_file = QMenu(self.menubar)
        self.menu_file.setObjectName(u"menu_file")
        self.menu_view = QMenu(self.menubar)
        self.menu_view.setObjectName(u"menu_view")
        self.menu_help = QMenu(self.menubar)
        self.menu_help.setObjectName(u"menu_help")
        RegisterTreeViewer.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(RegisterTreeViewer)
        self.statusbar.setObjectName(u"statusbar")
        RegisterTreeViewer.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_view.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menu_file.addAction(self.action_open_excel)
        self.menu_file.addAction(self.action_save_json)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menu_view.addAction(self.action_expand_all)
        self.menu_view.addAction(self.action_collapse_all)
        self.menu_help.addAction(self.action_protocol_guide)
        self.menu_help.addSeparator()
        self.menu_help.addAction(self.action_about)

        self.retranslateUi(RegisterTreeViewer)

        QMetaObject.connectSlotsByName(RegisterTreeViewer)
    # setupUi

    def retranslateUi(self, RegisterTreeViewer):
        RegisterTreeViewer.setWindowTitle(QCoreApplication.translate("RegisterTreeViewer", u"Register Tree Viewer with 32-bit Controller", None))
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
        self.action_protocol_guide.setText(QCoreApplication.translate("RegisterTreeViewer", u"Protocol Connection Guide", None))
#if QT_CONFIG(shortcut)
        self.action_protocol_guide.setShortcut(QCoreApplication.translate("RegisterTreeViewer", u"F1", None))
#endif // QT_CONFIG(shortcut)
        self.action_about.setText(QCoreApplication.translate("RegisterTreeViewer", u"About", None))
        ___qtreewidgetitem = self.tree_widget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("RegisterTreeViewer", u"Register/Field", None));
        self.connection_group.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"FT2232H Multi-Protocol Connection", None))
        self.protocol_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Protocol:", None))
        self.protocol_combo.setItemText(0, QCoreApplication.translate("RegisterTreeViewer", u"SPI", None))
        self.protocol_combo.setItemText(1, QCoreApplication.translate("RegisterTreeViewer", u"I2C", None))
        self.protocol_combo.setItemText(2, QCoreApplication.translate("RegisterTreeViewer", u"UART", None))

        self.setup_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Setup:", None))
        self.setup_combo.setItemText(0, QCoreApplication.translate("RegisterTreeViewer", u"Mode 0 (CPOL=0, CPHA=0)", None))
        self.setup_combo.setItemText(1, QCoreApplication.translate("RegisterTreeViewer", u"Mode 1 (CPOL=0, CPHA=1)", None))
        self.setup_combo.setItemText(2, QCoreApplication.translate("RegisterTreeViewer", u"Mode 2 (CPOL=1, CPHA=0)", None))
        self.setup_combo.setItemText(3, QCoreApplication.translate("RegisterTreeViewer", u"Mode 3 (CPOL=1, CPHA=1)", None))

#if QT_CONFIG(tooltip)
        self.setup_combo.setToolTip(QCoreApplication.translate("RegisterTreeViewer", u"Protocol-specific configuration options", None))
#endif // QT_CONFIG(tooltip)
        self.url_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"FTDI URL:", None))
        self.url_edit.setText(QCoreApplication.translate("RegisterTreeViewer", u"ftdi://ftdi:2232h/1", None))
        self.freq_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Frequency:", None))
        self.freq_edit.setText(QCoreApplication.translate("RegisterTreeViewer", u"1000000", None))
        self.connect_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Connect", None))
        self.disconnect_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Disconnect", None))
        self.simulate_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Simulate Connection", None))
        self.simulate_btn.setStyleSheet(QCoreApplication.translate("RegisterTreeViewer", u"background-color: #FFC107; color: black; font-weight: bold;", None))
#if QT_CONFIG(tooltip)
        self.simulate_btn.setToolTip(QCoreApplication.translate("RegisterTreeViewer", u"\uac00\uc0c1\uc73c\ub85c FT2232H\uac00 \uc5f0\uacb0\ub41c \uac83\ucc98\ub7fc \ub3d9\uc791\ud569\ub2c8\ub2e4 (\ud558\ub4dc\uc6e8\uc5b4 \uc5c6\uc774 \ud14c\uc2a4\ud2b8 \uac00\ub2a5)", None))
#endif // QT_CONFIG(tooltip)
        self.register_control_group.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"32-bit Register Control (16x2 Array)", None))
        self.hex_value_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Hex Value (0x):", None))
        self.dec_value_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Dec:", None))
        self.dec_value_display.setText(QCoreApplication.translate("RegisterTreeViewer", u"0", None))
        self.dec_value_display.setStyleSheet(QCoreApplication.translate("RegisterTreeViewer", u"font-weight: bold;", None))
        self.write_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Write", None))
        self.write_btn.setStyleSheet(QCoreApplication.translate("RegisterTreeViewer", u"background-color: #2196F3; color: white; font-weight: bold;", None))
        self.write_all_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Write All", None))
        self.write_all_btn.setStyleSheet(QCoreApplication.translate("RegisterTreeViewer", u"background-color: #FF9800; color: white; font-weight: bold;", None))
        self.read_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Read", None))
        self.read_btn.setStyleSheet(QCoreApplication.translate("RegisterTreeViewer", u"background-color: #4CAF50; color: white; font-weight: bold;", None))
        self.read_all_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Read All", None))
        self.read_all_btn.setStyleSheet(QCoreApplication.translate("RegisterTreeViewer", u"background-color: #9C27B0; color: white; font-weight: bold;", None))
        self.desc_label.setText(QCoreApplication.translate("RegisterTreeViewer", u"Description:", None))
        self.desc_text.setPlaceholderText(QCoreApplication.translate("RegisterTreeViewer", u"Select a register or field to view description", None))
        self.log_group.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"Communication Log", None))
        self.clear_log_btn.setText(QCoreApplication.translate("RegisterTreeViewer", u"Clear Log", None))
        self.menu_file.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"File", None))
        self.menu_view.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"View", None))
        self.menu_help.setTitle(QCoreApplication.translate("RegisterTreeViewer", u"Help", None))
    # retranslateUi

