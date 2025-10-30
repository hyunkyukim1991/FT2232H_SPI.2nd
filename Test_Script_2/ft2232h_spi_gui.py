#!/usr/bin/env python3
"""
FT2232H SPI Master GUI - Arduino Slave 통신
간단한 GUI로 SPI 통신을 테스트할 수 있습니다.
"""

import sys
import time
import struct
from typing import Optional, Tuple
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QSpinBox,
    QComboBox, QGroupBox, QCheckBox, QMessageBox, QGridLayout
)

try:
    from pyftdi.spi import SpiController
    from pyftdi.ftdi import Ftdi
except ImportError:
    SpiController = None
    Ftdi = None


class SPI_Worker(QThread):
    """SPI 통신 워커 스레드"""
    log_signal = Signal(str)
    response_signal = Signal(int, int)  # address, data
    error_signal = Signal(str)
    connected_signal = Signal(bool)
    
    def __init__(self):
        super().__init__()
        self.spi_ctrl = None
        self.slave = None
        self.is_connected = False
        
    def connect_device(self, url: str, cs: int, freq: int, mode: int):
        """FT2232H 연결"""
        try:
            if SpiController is None:
                self.error_signal.emit("pyftdi가 설치되지 않았습니다. pip install pyftdi")
                return
                
            self.spi_ctrl = SpiController()
            self.spi_ctrl.configure(url)
            self.slave = self.spi_ctrl.get_port(cs=cs, freq=freq, mode=mode)
            
            self.is_connected = True
            self.connected_signal.emit(True)
            self.log_signal.emit(f"연결 성공: {url}, CS={cs}, {freq}Hz, Mode={mode}")
            
        except Exception as e:
            self.error_signal.emit(f"연결 실패: {str(e)}")
            self.connected_signal.emit(False)
            
    def disconnect_device(self):
        """연결 해제"""
        try:
            if self.spi_ctrl:
                self.spi_ctrl.terminate()
            self.spi_ctrl = None
            self.slave = None
            self.is_connected = False
            self.connected_signal.emit(False)
            self.log_signal.emit("연결 해제됨")
        except Exception as e:
            self.error_signal.emit(f"연결 해제 오류: {str(e)}")
            
    def send_spi_frame(self, address: int, data: int, is_write: bool = True):
        """SPI 프레임 전송 (RW_BIT + Address + Data)"""
        if not self.is_connected or not self.slave:
            self.error_signal.emit("FT2232H가 연결되지 않았습니다")
            return
            
        try:
            # RW_BIT = A[7], Address = A[6:0] 형식으로 주소 구성
            # RW_BIT: 0 = Write, 1 = Read
            rw_bit = 0 if is_write else 1
            addr_byte = (rw_bit << 7) | (address & 0x7F)
            
            # 5바이트 프레임 구성 (RW+Address 1바이트 + Data 4바이트)
            tx_frame = struct.pack('>BI', addr_byte, data & 0xFFFFFFFF)
            
            operation = "Write" if is_write else "Read"
            self.log_signal.emit(f"송신 ({operation}): Addr=0x{address:02X}, RW_Byte=0x{addr_byte:02X}, Data=0x{data:08X}")
            
            # SPI 트랜잭션
            rx_frame = self.slave.exchange(tx_frame, duplex=True)
            
            # 응답 파싱
            if len(rx_frame) >= 5:
                resp_rw_addr, resp_data = struct.unpack('>BI', rx_frame[:5])
                resp_rw_bit = (resp_rw_addr >> 7) & 0x01
                resp_addr = resp_rw_addr & 0x7F
                resp_operation = "Write" if resp_rw_bit == 0 else "Read"
                
                self.log_signal.emit(f"수신 ({resp_operation}): Addr=0x{resp_addr:02X}, RW_Byte=0x{resp_rw_addr:02X}, Data=0x{resp_data:08X}")
                self.response_signal.emit(resp_addr, resp_data)
            else:
                self.error_signal.emit(f"잘못된 응답 길이: {len(rx_frame)} bytes")
                
        except Exception as e:
            self.error_signal.emit(f"SPI 전송 오류: {str(e)}")
    
    def read_register(self, address: int):
        """레지스터 읽기 (RW_BIT = 1)"""
        self.send_spi_frame(address, 0x00000000, is_write=False)
    
    def write_register(self, address: int, data: int):
        """레지스터 쓰기 (RW_BIT = 0)"""
        self.send_spi_frame(address, data, is_write=True)


class SPI_Master_GUI(QWidget):
    """FT2232H SPI Master GUI"""
    
    def __init__(self):
        super().__init__()
        self.worker = SPI_Worker()
        self.setup_ui()
        self.connect_signals()
        
        # 자동 millis() 읽기용 타이머
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.auto_read_millis)
        
    def setup_ui(self):
        """UI 구성"""
        self.setWindowTitle("FT2232H SPI Master - Arduino Slave 통신")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # 연결 그룹
        conn_group = QGroupBox("FT2232H 연결 설정")
        conn_layout = QGridLayout(conn_group)
        
        conn_layout.addWidget(QLabel("FTDI URL:"), 0, 0)
        self.url_edit = QLineEdit("ftdi://ftdi:2232h/1")
        conn_layout.addWidget(self.url_edit, 0, 1, 1, 2)
        
        conn_layout.addWidget(QLabel("CS:"), 1, 0)
        self.cs_spin = QSpinBox()
        self.cs_spin.setRange(0, 3)
        self.cs_spin.setValue(0)
        conn_layout.addWidget(self.cs_spin, 1, 1)
        
        conn_layout.addWidget(QLabel("주파수(Hz):"), 1, 2)
        self.freq_edit = QLineEdit("1000000")
        conn_layout.addWidget(self.freq_edit, 1, 3)
        
        conn_layout.addWidget(QLabel("SPI 모드:"), 2, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["0", "1", "2", "3"])
        conn_layout.addWidget(self.mode_combo, 2, 1)
        
        self.connect_btn = QPushButton("연결")
        self.disconnect_btn = QPushButton("연결 해제")
        self.disconnect_btn.setEnabled(False)
        conn_layout.addWidget(self.connect_btn, 2, 2)
        conn_layout.addWidget(self.disconnect_btn, 2, 3)
        
        layout.addWidget(conn_group)
        
        # SPI 통신 그룹
        spi_group = QGroupBox("SPI 통신 (RW_BIT + Address)")
        spi_layout = QGridLayout(spi_group)
        
        spi_layout.addWidget(QLabel("주소 (0-127):"), 0, 0)
        self.addr_edit = QLineEdit("01")
        self.addr_edit.setMaximumWidth(100)
        spi_layout.addWidget(self.addr_edit, 0, 1)
        
        spi_layout.addWidget(QLabel("데이터 (Hex):"), 0, 2)
        self.data_edit = QLineEdit("12345678")
        self.data_edit.setMaximumWidth(150)
        spi_layout.addWidget(self.data_edit, 0, 3)
        
        # Read/Write 버튼들
        self.read_btn = QPushButton("읽기 (RW=1)")
        self.read_btn.setEnabled(False)
        self.read_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        spi_layout.addWidget(self.read_btn, 0, 4)
        
        self.write_btn = QPushButton("쓰기 (RW=0)")
        self.write_btn.setEnabled(False)
        self.write_btn.setStyleSheet("background-color: #2196F3; color: white;")
        spi_layout.addWidget(self.write_btn, 0, 5)
        
        # 빠른 테스트 버튼들
        spi_layout.addWidget(QLabel("빠른 테스트:"), 1, 0)
        
        self.test_read1_btn = QPushButton("읽기 Addr 0x01")
        self.test_read2_btn = QPushButton("읽기 Addr 0x02")
        self.test_read3_btn = QPushButton("읽기 Addr 0x03")
        self.test_write1_btn = QPushButton("쓰기 Addr 0x01")
        
        for btn in [self.test_read1_btn, self.test_read2_btn, self.test_read3_btn, self.test_write1_btn]:
            btn.setEnabled(False)
            
        spi_layout.addWidget(self.test_read1_btn, 1, 1)
        spi_layout.addWidget(self.test_read2_btn, 1, 2)
        spi_layout.addWidget(self.test_read3_btn, 1, 3)
        spi_layout.addWidget(self.test_write1_btn, 1, 4)
        
        # 자동 millis() 읽기
        self.auto_checkbox = QCheckBox("자동 millis() 읽기 (Addr 0x03)")
        self.auto_checkbox.setEnabled(False)
        spi_layout.addWidget(self.auto_checkbox, 2, 0, 1, 3)
        
        layout.addWidget(spi_group)
        
        # 응답 표시 그룹
        resp_group = QGroupBox("마지막 응답")
        resp_layout = QHBoxLayout(resp_group)
        
        resp_layout.addWidget(QLabel("주소:"))
        self.resp_addr_label = QLabel("--")
        resp_layout.addWidget(self.resp_addr_label)
        
        resp_layout.addWidget(QLabel("데이터:"))
        self.resp_data_label = QLabel("--")
        resp_layout.addWidget(self.resp_data_label)
        
        resp_layout.addWidget(QLabel("십진수:"))
        self.resp_dec_label = QLabel("--")
        resp_layout.addWidget(self.resp_dec_label)
        
        resp_layout.addStretch()
        layout.addWidget(resp_group)
        
        # 로그 표시
        log_group = QGroupBox("로그")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        clear_log_btn = QPushButton("로그 지우기")
        clear_log_btn.clicked.connect(self.log_text.clear)
        log_layout.addWidget(clear_log_btn)
        
        layout.addWidget(log_group)
        
    def connect_signals(self):
        """시그널 연결"""
        # 버튼 이벤트
        self.connect_btn.clicked.connect(self.on_connect)
        self.disconnect_btn.clicked.connect(self.on_disconnect)
        self.read_btn.clicked.connect(self.on_read)
        self.write_btn.clicked.connect(self.on_write)
        
        # 테스트 버튼들
        self.test_read1_btn.clicked.connect(lambda: self.worker.read_register(0x01))
        self.test_read2_btn.clicked.connect(lambda: self.worker.read_register(0x02))
        self.test_read3_btn.clicked.connect(lambda: self.worker.read_register(0x03))
        self.test_write1_btn.clicked.connect(lambda: self.worker.write_register(0x01, 0x12345678))
        
        # 자동 읽기 체크박스
        self.auto_checkbox.toggled.connect(self.on_auto_toggle)
        
        # 워커 시그널
        self.worker.log_signal.connect(self.append_log)
        self.worker.response_signal.connect(self.on_response)
        self.worker.error_signal.connect(self.on_error)
        self.worker.connected_signal.connect(self.on_connection_changed)
        
    def on_connect(self):
        """연결 버튼 클릭"""
        try:
            url = self.url_edit.text().strip()
            cs = self.cs_spin.value()
            freq = int(self.freq_edit.text().strip())
            mode = int(self.mode_combo.currentText())
            
            self.worker.connect_device(url, cs, freq, mode)
            
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "주파수는 숫자로 입력해주세요.")
        except Exception as e:
            QMessageBox.critical(self, "연결 오류", str(e))
            
    def on_disconnect(self):
        """연결 해제 버튼 클릭"""
        self.worker.disconnect_device()
        
    def on_read(self):
        """읽기 버튼 클릭"""
        try:
            addr_text = self.addr_edit.text().strip()
            address = int(addr_text, 16) if addr_text else 0
            
            if address > 127:
                QMessageBox.warning(self, "주소 오류", "주소는 0-127 범위여야 합니다.")
                return
                
            self.worker.read_register(address)
            
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "주소는 16진수로 입력해주세요.")
        except Exception as e:
            QMessageBox.critical(self, "읽기 오류", str(e))
            
    def on_write(self):
        """쓰기 버튼 클릭"""
        try:
            addr_text = self.addr_edit.text().strip()
            data_text = self.data_edit.text().strip()
            
            address = int(addr_text, 16) if addr_text else 0
            data = int(data_text, 16) if data_text else 0
            
            if address > 127:
                QMessageBox.warning(self, "주소 오류", "주소는 0-127 범위여야 합니다.")
                return
                
            self.worker.write_register(address, data)
            
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "주소와 데이터는 16진수로 입력해주세요.")
        except Exception as e:
            QMessageBox.critical(self, "쓰기 오류", str(e))
            
    def quick_test(self, address: int, data: int, is_write: bool = True):
        """빠른 테스트 함수"""
        if is_write:
            self.worker.write_register(address, data)
        else:
            self.worker.read_register(address)
        
    def on_auto_toggle(self, checked: bool):
        """자동 읽기 토글"""
        if checked:
            self.auto_timer.start(1000)  # 1초마다
            self.append_log("자동 millis() 읽기 시작 (Addr 0x03)")
        else:
            self.auto_timer.stop()
            self.append_log("자동 millis() 읽기 중지")
            
    def auto_read_millis(self):
        """자동으로 millis() 읽기"""
        self.worker.read_register(0x03)
        
    def on_connection_changed(self, connected: bool):
        """연결 상태 변경"""
        self.connect_btn.setEnabled(not connected)
        self.disconnect_btn.setEnabled(connected)
        self.read_btn.setEnabled(connected)
        self.write_btn.setEnabled(connected)
        
        for btn in [self.test_read1_btn, self.test_read2_btn, self.test_read3_btn, self.test_write1_btn]:
            btn.setEnabled(connected)
            
        self.auto_checkbox.setEnabled(connected)
        
        if not connected:
            self.auto_checkbox.setChecked(False)
            
    def on_response(self, address: int, data: int):
        """응답 수신"""
        self.resp_addr_label.setText(f"0x{address:02X}")
        self.resp_data_label.setText(f"0x{data:08X}")
        self.resp_dec_label.setText(f"{data}")
        
    def on_error(self, message: str):
        """오류 처리"""
        self.append_log(f"❌ 오류: {message}")
        QMessageBox.critical(self, "오류", message)
        
    def append_log(self, message: str):
        """로그 추가"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        
    def closeEvent(self, event):
        """종료시 정리"""
        self.auto_timer.stop()
        self.worker.disconnect_device()
        event.accept()


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # pyftdi 확인
    if SpiController is None:
        QMessageBox.critical(None, "라이브러리 오류", 
                           "pyftdi가 설치되지 않았습니다.\n\n"
                           "설치 명령: pip install pyftdi")
        return
    
    window = SPI_Master_GUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()