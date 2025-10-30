#!/usr/bin/env python3
"""
FT2232H SPI Master GUI - Arduino Slave 통신 (.ui 파일 사용)
.ui 파일을 로드하여 GUI를 구성합니다.
"""

import sys
import time
import struct
from typing import Optional, Tuple
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6 import QtCore
import os

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


class SPI_Master_GUI_From_UI(QWidget):
    """FT2232H SPI Master GUI (.ui 파일에서 로드)"""
    
    def __init__(self):
        super().__init__()
        self.worker = SPI_Worker()
        self.ui = None
        
        # .ui 파일 로드
        self.load_ui()
        
        # UI 요소들에 대한 참조 설정
        self.setup_ui_references()
        
        # 시그널 연결
        self.connect_signals()
        
        # 자동 millis() 읽기용 타이머
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.auto_read_millis)
        
    def load_ui(self):
        """UI 파일 로드"""
        try:
            loader = QUiLoader()
            ui_file_path = os.path.join(os.path.dirname(__file__), "ft2232h_spi_gui.ui")
            
            # UI 파일 존재 확인
            if not os.path.exists(ui_file_path):
                raise FileNotFoundError(f"UI 파일을 찾을 수 없습니다: {ui_file_path}")
            
            # UI 파일 로드
            ui_file = QtCore.QFile(ui_file_path)
            if not ui_file.open(QtCore.QFile.ReadOnly):
                raise Exception(f"UI 파일을 열 수 없습니다: {ui_file_path}")
            
            self.ui = loader.load(ui_file, self)
            ui_file.close()
                
            # 로드된 UI를 현재 위젯에 설정
            if self.ui:
                # UI의 레이아웃을 현재 위젯에 적용
                from PySide6.QtWidgets import QVBoxLayout
                layout = QVBoxLayout(self)
                layout.addWidget(self.ui)
                layout.setContentsMargins(0, 0, 0, 0)
                
                # 창 설정
                self.setWindowTitle(self.ui.windowTitle())
                self.setMinimumSize(self.ui.minimumSize())
            else:
                raise Exception("UI 로드 실패: loader.load() 반환값이 None입니다")
                
        except Exception as e:
            QMessageBox.critical(self, "UI 로드 오류", f"UI 파일을 로드할 수 없습니다:\n{str(e)}\n\n파일 경로: {ui_file_path}")
            sys.exit(1)
            
    def setup_ui_references(self):
        """UI 요소들에 대한 참조 설정"""
        if not self.ui:
            return
            
        # UI 요소들 찾기 (올바른 Qt 클래스 타입 사용)
        from PySide6.QtWidgets import QLineEdit, QSpinBox, QComboBox, QPushButton, QCheckBox, QLabel, QTextEdit
        
        self.url_edit = self.ui.findChild(QLineEdit, "url_edit")
        self.cs_spin = self.ui.findChild(QSpinBox, "cs_spin")
        self.freq_edit = self.ui.findChild(QLineEdit, "freq_edit")
        self.mode_combo = self.ui.findChild(QComboBox, "mode_combo")
        self.connect_btn = self.ui.findChild(QPushButton, "connect_btn")
        self.disconnect_btn = self.ui.findChild(QPushButton, "disconnect_btn")
        
        self.addr_edit = self.ui.findChild(QLineEdit, "addr_edit")
        self.data_edit = self.ui.findChild(QLineEdit, "data_edit")
        self.read_btn = self.ui.findChild(QPushButton, "read_btn")
        self.write_btn = self.ui.findChild(QPushButton, "write_btn")
        
        self.test_read1_btn = self.ui.findChild(QPushButton, "test_read1_btn")
        self.test_read2_btn = self.ui.findChild(QPushButton, "test_read2_btn")
        self.test_read3_btn = self.ui.findChild(QPushButton, "test_read3_btn")
        self.test_write1_btn = self.ui.findChild(QPushButton, "test_write1_btn")
        
        self.auto_checkbox = self.ui.findChild(QCheckBox, "auto_checkbox")
        
        self.resp_addr_label = self.ui.findChild(QLabel, "resp_addr_label")
        self.resp_data_label = self.ui.findChild(QLabel, "resp_data_label")
        self.resp_dec_label = self.ui.findChild(QLabel, "resp_dec_label")
        
        self.log_text = self.ui.findChild(QTextEdit, "log_text")
        self.clear_log_btn = self.ui.findChild(QPushButton, "clear_log_btn")
        
        # 찾지 못한 위젯들 로그
        missing_widgets = []
        for name, widget in [
            ("url_edit", self.url_edit), ("cs_spin", self.cs_spin), ("freq_edit", self.freq_edit),
            ("mode_combo", self.mode_combo), ("connect_btn", self.connect_btn), ("disconnect_btn", self.disconnect_btn),
            ("addr_edit", self.addr_edit), ("data_edit", self.data_edit), ("read_btn", self.read_btn),
            ("write_btn", self.write_btn), ("test_read1_btn", self.test_read1_btn), ("test_read2_btn", self.test_read2_btn),
            ("test_read3_btn", self.test_read3_btn), ("test_write1_btn", self.test_write1_btn), ("auto_checkbox", self.auto_checkbox),
            ("resp_addr_label", self.resp_addr_label), ("resp_data_label", self.resp_data_label), ("resp_dec_label", self.resp_dec_label),
            ("log_text", self.log_text), ("clear_log_btn", self.clear_log_btn)
        ]:
            if widget is None:
                missing_widgets.append(name)
        
        if missing_widgets:
            print(f"경고: 다음 위젯들을 찾을 수 없습니다: {', '.join(missing_widgets)}")
        
    def connect_signals(self):
        """시그널 연결"""
        if not self.ui:
            return
            
        # 버튼 이벤트
        if self.connect_btn:
            self.connect_btn.clicked.connect(self.on_connect)
        if self.disconnect_btn:
            self.disconnect_btn.clicked.connect(self.on_disconnect)
        if self.read_btn:
            self.read_btn.clicked.connect(self.on_read)
        if self.write_btn:
            self.write_btn.clicked.connect(self.on_write)
        
        # 테스트 버튼들
        if self.test_read1_btn:
            self.test_read1_btn.clicked.connect(lambda: self.worker.read_register(0x01))
        if self.test_read2_btn:
            self.test_read2_btn.clicked.connect(lambda: self.worker.read_register(0x02))
        if self.test_read3_btn:
            self.test_read3_btn.clicked.connect(lambda: self.worker.read_register(0x03))
        if self.test_write1_btn:
            self.test_write1_btn.clicked.connect(lambda: self.worker.write_register(0x01, 0x12345678))
        
        # 자동 읽기 체크박스
        if self.auto_checkbox:
            self.auto_checkbox.toggled.connect(self.on_auto_toggle)
        
        # 로그 지우기 버튼
        if self.clear_log_btn and self.log_text:
            self.clear_log_btn.clicked.connect(self.log_text.clear)
        
        # 워커 시그널
        self.worker.log_signal.connect(self.append_log)
        self.worker.response_signal.connect(self.on_response)
        self.worker.error_signal.connect(self.on_error)
        self.worker.connected_signal.connect(self.on_connection_changed)
        
    def on_connect(self):
        """연결 버튼 클릭"""
        try:
            url = self.url_edit.text().strip() if self.url_edit else ""
            cs = self.cs_spin.value() if self.cs_spin else 0
            freq = int(self.freq_edit.text().strip()) if self.freq_edit else 1000000
            mode = int(self.mode_combo.currentText()) if self.mode_combo else 0
            
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
            addr_text = self.addr_edit.text().strip() if self.addr_edit else ""
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
            addr_text = self.addr_edit.text().strip() if self.addr_edit else ""
            data_text = self.data_edit.text().strip() if self.data_edit else ""
            
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
        if self.connect_btn:
            self.connect_btn.setEnabled(not connected)
        if self.disconnect_btn:
            self.disconnect_btn.setEnabled(connected)
        if self.read_btn:
            self.read_btn.setEnabled(connected)
        if self.write_btn:
            self.write_btn.setEnabled(connected)
        
        for btn in [self.test_read1_btn, self.test_read2_btn, self.test_read3_btn, self.test_write1_btn]:
            if btn:
                btn.setEnabled(connected)
        
        if self.auto_checkbox:
            self.auto_checkbox.setEnabled(connected)
            if not connected:
                self.auto_checkbox.setChecked(False)
            
    def on_response(self, address: int, data: int):
        """응답 수신"""
        if self.resp_addr_label:
            self.resp_addr_label.setText(f"0x{address:02X}")
        if self.resp_data_label:
            self.resp_data_label.setText(f"0x{data:08X}")
        if self.resp_dec_label:
            self.resp_dec_label.setText(f"{data}")
        
    def on_error(self, message: str):
        """오류 처리"""
        self.append_log(f"❌ 오류: {message}")
        QMessageBox.critical(self, "오류", message)
        
    def append_log(self, message: str):
        """로그 추가"""
        if self.log_text:
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
    
    window = SPI_Master_GUI_From_UI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()