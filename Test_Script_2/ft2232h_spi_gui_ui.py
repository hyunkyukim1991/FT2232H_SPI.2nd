# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ft2232h_spi_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_SPI_Master_GUI(object):
    def setupUi(self, SPI_Master_GUI):
        if not SPI_Master_GUI.objectName():
            SPI_Master_GUI.setObjectName(u"SPI_Master_GUI")
        SPI_Master_GUI.resize(800, 600)
        SPI_Master_GUI.setMinimumSize(QSize(800, 600))
        self.verticalLayout = QVBoxLayout(SPI_Master_GUI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.conn_group = QGroupBox(SPI_Master_GUI)
        self.conn_group.setObjectName(u"conn_group")
        self.conn_layout = QGridLayout(self.conn_group)
        self.conn_layout.setObjectName(u"conn_layout")
        self.url_label = QLabel(self.conn_group)
        self.url_label.setObjectName(u"url_label")

        self.conn_layout.addWidget(self.url_label, 0, 0, 1, 1)

        self.url_edit = QLineEdit(self.conn_group)
        self.url_edit.setObjectName(u"url_edit")

        self.conn_layout.addWidget(self.url_edit, 0, 1, 1, 2)

        self.cs_label = QLabel(self.conn_group)
        self.cs_label.setObjectName(u"cs_label")

        self.conn_layout.addWidget(self.cs_label, 1, 0, 1, 1)

        self.cs_spin = QSpinBox(self.conn_group)
        self.cs_spin.setObjectName(u"cs_spin")
        self.cs_spin.setMaximum(3)

        self.conn_layout.addWidget(self.cs_spin, 1, 1, 1, 1)

        self.freq_label = QLabel(self.conn_group)
        self.freq_label.setObjectName(u"freq_label")

        self.conn_layout.addWidget(self.freq_label, 1, 2, 1, 1)

        self.freq_edit = QLineEdit(self.conn_group)
        self.freq_edit.setObjectName(u"freq_edit")

        self.conn_layout.addWidget(self.freq_edit, 1, 3, 1, 1)

        self.mode_label = QLabel(self.conn_group)
        self.mode_label.setObjectName(u"mode_label")

        self.conn_layout.addWidget(self.mode_label, 2, 0, 1, 1)

        self.mode_combo = QComboBox(self.conn_group)
        self.mode_combo.addItem("")
        self.mode_combo.addItem("")
        self.mode_combo.addItem("")
        self.mode_combo.addItem("")
        self.mode_combo.setObjectName(u"mode_combo")

        self.conn_layout.addWidget(self.mode_combo, 2, 1, 1, 1)

        self.connect_btn = QPushButton(self.conn_group)
        self.connect_btn.setObjectName(u"connect_btn")

        self.conn_layout.addWidget(self.connect_btn, 2, 2, 1, 1)

        self.disconnect_btn = QPushButton(self.conn_group)
        self.disconnect_btn.setObjectName(u"disconnect_btn")
        self.disconnect_btn.setEnabled(False)

        self.conn_layout.addWidget(self.disconnect_btn, 2, 3, 1, 1)


        self.verticalLayout.addWidget(self.conn_group)

        self.spi_group = QGroupBox(SPI_Master_GUI)
        self.spi_group.setObjectName(u"spi_group")
        self.spi_layout = QGridLayout(self.spi_group)
        self.spi_layout.setObjectName(u"spi_layout")
        self.addr_label = QLabel(self.spi_group)
        self.addr_label.setObjectName(u"addr_label")

        self.spi_layout.addWidget(self.addr_label, 0, 0, 1, 1)

        self.addr_edit = QLineEdit(self.spi_group)
        self.addr_edit.setObjectName(u"addr_edit")
        self.addr_edit.setMaximumSize(QSize(100, 16777215))

        self.spi_layout.addWidget(self.addr_edit, 0, 1, 1, 1)

        self.data_label = QLabel(self.spi_group)
        self.data_label.setObjectName(u"data_label")

        self.spi_layout.addWidget(self.data_label, 0, 2, 1, 1)

        self.data_edit = QLineEdit(self.spi_group)
        self.data_edit.setObjectName(u"data_edit")
        self.data_edit.setMaximumSize(QSize(150, 16777215))

        self.spi_layout.addWidget(self.data_edit, 0, 3, 1, 1)

        self.read_btn = QPushButton(self.spi_group)
        self.read_btn.setObjectName(u"read_btn")
        self.read_btn.setEnabled(False)
        self.read_btn.setStyleSheet(u"background-color: #4CAF50; color: white;")

        self.spi_layout.addWidget(self.read_btn, 0, 4, 1, 1)

        self.write_btn = QPushButton(self.spi_group)
        self.write_btn.setObjectName(u"write_btn")
        self.write_btn.setEnabled(False)
        self.write_btn.setStyleSheet(u"background-color: #2196F3; color: white;")

        self.spi_layout.addWidget(self.write_btn, 0, 5, 1, 1)

        self.test_label = QLabel(self.spi_group)
        self.test_label.setObjectName(u"test_label")

        self.spi_layout.addWidget(self.test_label, 1, 0, 1, 1)

        self.test_read1_btn = QPushButton(self.spi_group)
        self.test_read1_btn.setObjectName(u"test_read1_btn")
        self.test_read1_btn.setEnabled(False)

        self.spi_layout.addWidget(self.test_read1_btn, 1, 1, 1, 1)

        self.test_read2_btn = QPushButton(self.spi_group)
        self.test_read2_btn.setObjectName(u"test_read2_btn")
        self.test_read2_btn.setEnabled(False)

        self.spi_layout.addWidget(self.test_read2_btn, 1, 2, 1, 1)

        self.test_read3_btn = QPushButton(self.spi_group)
        self.test_read3_btn.setObjectName(u"test_read3_btn")
        self.test_read3_btn.setEnabled(False)

        self.spi_layout.addWidget(self.test_read3_btn, 1, 3, 1, 1)

        self.test_write1_btn = QPushButton(self.spi_group)
        self.test_write1_btn.setObjectName(u"test_write1_btn")
        self.test_write1_btn.setEnabled(False)

        self.spi_layout.addWidget(self.test_write1_btn, 1, 4, 1, 1)

        self.auto_checkbox = QCheckBox(self.spi_group)
        self.auto_checkbox.setObjectName(u"auto_checkbox")
        self.auto_checkbox.setEnabled(False)

        self.spi_layout.addWidget(self.auto_checkbox, 2, 0, 1, 3)


        self.verticalLayout.addWidget(self.spi_group)

        self.resp_group = QGroupBox(SPI_Master_GUI)
        self.resp_group.setObjectName(u"resp_group")
        self.resp_layout = QHBoxLayout(self.resp_group)
        self.resp_layout.setObjectName(u"resp_layout")
        self.resp_addr_title = QLabel(self.resp_group)
        self.resp_addr_title.setObjectName(u"resp_addr_title")

        self.resp_layout.addWidget(self.resp_addr_title)

        self.resp_addr_label = QLabel(self.resp_group)
        self.resp_addr_label.setObjectName(u"resp_addr_label")

        self.resp_layout.addWidget(self.resp_addr_label)

        self.resp_data_title = QLabel(self.resp_group)
        self.resp_data_title.setObjectName(u"resp_data_title")

        self.resp_layout.addWidget(self.resp_data_title)

        self.resp_data_label = QLabel(self.resp_group)
        self.resp_data_label.setObjectName(u"resp_data_label")

        self.resp_layout.addWidget(self.resp_data_label)

        self.resp_dec_title = QLabel(self.resp_group)
        self.resp_dec_title.setObjectName(u"resp_dec_title")

        self.resp_layout.addWidget(self.resp_dec_title)

        self.resp_dec_label = QLabel(self.resp_group)
        self.resp_dec_label.setObjectName(u"resp_dec_label")

        self.resp_layout.addWidget(self.resp_dec_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.resp_layout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.resp_group)

        self.log_group = QGroupBox(SPI_Master_GUI)
        self.log_group.setObjectName(u"log_group")
        self.log_layout = QVBoxLayout(self.log_group)
        self.log_layout.setObjectName(u"log_layout")
        self.log_text = QTextEdit(self.log_group)
        self.log_text.setObjectName(u"log_text")
        self.log_text.setMaximumSize(QSize(16777215, 200))
        self.log_text.setReadOnly(True)

        self.log_layout.addWidget(self.log_text)

        self.clear_log_btn = QPushButton(self.log_group)
        self.clear_log_btn.setObjectName(u"clear_log_btn")

        self.log_layout.addWidget(self.clear_log_btn)


        self.verticalLayout.addWidget(self.log_group)


        self.retranslateUi(SPI_Master_GUI)

        QMetaObject.connectSlotsByName(SPI_Master_GUI)
    # setupUi

    def retranslateUi(self, SPI_Master_GUI):
        SPI_Master_GUI.setWindowTitle(QCoreApplication.translate("SPI_Master_GUI", u"FT2232H SPI Master - Arduino Slave \ud1b5\uc2e0", None))
        self.conn_group.setTitle(QCoreApplication.translate("SPI_Master_GUI", u"FT2232H \uc5f0\uacb0 \uc124\uc815", None))
        self.url_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"FTDI URL:", None))
        self.url_edit.setText(QCoreApplication.translate("SPI_Master_GUI", u"ftdi://ftdi:2232h/1", None))
        self.cs_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"CS:", None))
        self.freq_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc8fc\ud30c\uc218(Hz):", None))
        self.freq_edit.setText(QCoreApplication.translate("SPI_Master_GUI", u"100000", None))
        self.mode_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"SPI \ubaa8\ub4dc:", None))
        self.mode_combo.setItemText(0, QCoreApplication.translate("SPI_Master_GUI", u"0", None))
        self.mode_combo.setItemText(1, QCoreApplication.translate("SPI_Master_GUI", u"1", None))
        self.mode_combo.setItemText(2, QCoreApplication.translate("SPI_Master_GUI", u"2", None))
        self.mode_combo.setItemText(3, QCoreApplication.translate("SPI_Master_GUI", u"3", None))

        self.connect_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc5f0\uacb0", None))
        self.disconnect_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc5f0\uacb0 \ud574\uc81c", None))
        self.spi_group.setTitle(QCoreApplication.translate("SPI_Master_GUI", u"SPI \ud1b5\uc2e0 (RW_BIT + Address)", None))
        self.addr_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc8fc\uc18c (0-127):", None))
        self.addr_edit.setText(QCoreApplication.translate("SPI_Master_GUI", u"01", None))
        self.data_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"\ub370\uc774\ud130 (Hex):", None))
        self.data_edit.setText(QCoreApplication.translate("SPI_Master_GUI", u"5678", None))
        self.read_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc77d\uae30 (RW=1)", None))
        self.write_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc4f0\uae30 (RW=0)", None))
        self.test_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"\ube60\ub978 \ud14c\uc2a4\ud2b8:", None))
        self.test_read1_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc77d\uae30 Addr 0x01", None))
        self.test_read2_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc77d\uae30 Addr 0x02", None))
        self.test_read3_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc77d\uae30 Addr 0x03", None))
        self.test_write1_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc4f0\uae30 Addr 0x01", None))
        self.auto_checkbox.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc790\ub3d9 millis() \uc77d\uae30 (Addr 0x03)", None))
        self.resp_group.setTitle(QCoreApplication.translate("SPI_Master_GUI", u"\ub9c8\uc9c0\ub9c9 \uc751\ub2f5", None))
        self.resp_addr_title.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc8fc\uc18c:", None))
        self.resp_addr_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"--", None))
        self.resp_data_title.setText(QCoreApplication.translate("SPI_Master_GUI", u"\ub370\uc774\ud130:", None))
        self.resp_data_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"--", None))
        self.resp_dec_title.setText(QCoreApplication.translate("SPI_Master_GUI", u"\uc2ed\uc9c4\uc218:", None))
        self.resp_dec_label.setText(QCoreApplication.translate("SPI_Master_GUI", u"--", None))
        self.log_group.setTitle(QCoreApplication.translate("SPI_Master_GUI", u"\ub85c\uadf8", None))
        self.clear_log_btn.setText(QCoreApplication.translate("SPI_Master_GUI", u"\ub85c\uadf8 \uc9c0\uc6b0\uae30", None))
    # retranslateUi

