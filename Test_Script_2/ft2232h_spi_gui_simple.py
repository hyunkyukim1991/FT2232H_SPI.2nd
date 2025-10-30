#!/usr/bin/env python3
"""
FT2232H SPI Master GUI - Arduino Slave 통신 (간단한 .ui 로드)
.ui 파일을 더 간단하게 로드하는 방식입니다.
"""

import sys
import time
import struct
from typing import Optional, Tuple
from PySide6.QtCore import Qt, QThread, Signal, QTimer, QFile, QIODevice
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout
from PySide6.QtUiTools import QUiLoader
import os

try:
    from pyftdi.spi import SpiController
    from pyftdi.ftdi import Ftdi
except ImportError:
    SpiController = None
    Ftdi = None

# 전역 변수 - SPI 데이터 설정
DATA_LENGTH_BYTES = 2  # 데이터 길이 (바이트 단위, 기본값: 4바이트 = 32비트)
MAX_DATA_VALUE = (1 << (DATA_LENGTH_BYTES * 8)) - 1  # 최대 데이터 값

def set_data_length(length_bytes: int):
    """데이터 길이 설정 (1, 2, 4, 8 바이트 지원)"""
    global DATA_LENGTH_BYTES, MAX_DATA_VALUE
    if length_bytes in [1, 2, 4, 8] or length_bytes > 0:
        DATA_LENGTH_BYTES = length_bytes
        MAX_DATA_VALUE = (1 << (DATA_LENGTH_BYTES * 8)) - 1
        print(f"데이터 길이가 {DATA_LENGTH_BYTES}바이트로 설정되었습니다. 최대값: 0x{MAX_DATA_VALUE:X}")
    else:
        raise ValueError("데이터 길이는 1, 2, 4, 8 바이트 또는 양의 정수여야 합니다.")

def get_data_length():
    """현재 데이터 길이 반환"""
    return DATA_LENGTH_BYTES

def get_max_data_value():
    """현재 최대 데이터 값 반환"""
    return MAX_DATA_VALUE

def parse_hex_input(input_text: str) -> int:
    """16진수 입력을 파싱 (0x01, 01, 1 형태 모두 지원)"""
    if not input_text:
        return 0
    
    text = input_text.strip()
    
    try:
        # 0x 또는 0X로 시작하는 경우
        if text.lower().startswith('0x'):
            return int(text, 16)
        # 16진수 문자만 포함된 경우
        elif all(c in '0123456789ABCDEFabcdef' for c in text):
            return int(text, 16)
        # 10진수인 경우
        else:
            return int(text, 10)
    except ValueError:
        raise ValueError(f"잘못된 입력: '{input_text}'. 16진수(01, 0x01) 또는 10진수를 입력해주세요.")


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
            global DATA_LENGTH_BYTES, MAX_DATA_VALUE
            
            # RW_BIT = A[7], Address = A[6:0] 형식으로 주소 구성
            # RW_BIT: 0 = Write, 1 = Read
            rw_bit = 0 if is_write else 1
            addr_byte = (rw_bit << 7) | (address & 0x7F)
            
            # 가변 길이 프레임 구성 (RW+Address 1바이트 + Data N바이트)
            data_masked = data & MAX_DATA_VALUE
            
            # 동적 struct format 생성
            if DATA_LENGTH_BYTES == 1:
                format_str = '>BB'
                tx_frame = struct.pack(format_str, addr_byte, data_masked)
            elif DATA_LENGTH_BYTES == 2:
                format_str = '>BH'
                tx_frame = struct.pack(format_str, addr_byte, data_masked)
            elif DATA_LENGTH_BYTES == 4:
                format_str = '>BI'
                tx_frame = struct.pack(format_str, addr_byte, data_masked)
            elif DATA_LENGTH_BYTES == 8:
                format_str = '>BQ'
                tx_frame = struct.pack(format_str, addr_byte, data_masked)
            else:
                # 임의 길이 지원
                tx_frame = struct.pack('>B', addr_byte) + data_masked.to_bytes(DATA_LENGTH_BYTES, byteorder='big')
            
            operation = "Write" if is_write else "Read"
            data_format = f"0{DATA_LENGTH_BYTES*2}X"  # 데이터 길이에 따른 16진수 포맷
            self.log_signal.emit(f"송신 ({operation}): Addr=0x{address:02X}, RW_Byte=0x{addr_byte:02X}, Data=0x{data_masked:{data_format}} ({DATA_LENGTH_BYTES}바이트)")
            
            # 디버그 모드일 때만 바이트 레벨 로그 출력
            if hasattr(self.parent, 'debug_mode') and self.parent.debug_mode:
                tx_bytes = " ".join([f"0x{b:02X}" for b in tx_frame])
                self.log_signal.emit(f"TX 바이트: {tx_bytes}")
            
            # SPI 트랜잭션 (1단계 방식)
            rx_frame = self.slave.exchange(tx_frame, duplex=True)
            
            # 디버그 모드일 때만 바이트 레벨 로그 출력
            if hasattr(self.parent, 'debug_mode') and self.parent.debug_mode:
                rx_bytes = " ".join([f"0x{b:02X}" for b in rx_frame])
                self.log_signal.emit(f"RX 바이트: {rx_bytes}")
            
            # 응답 파싱
            expected_frame_size = 1 + DATA_LENGTH_BYTES  # RW+Address(1바이트) + Data(N바이트)
            if len(rx_frame) >= expected_frame_size:
                # 동적 응답 파싱
                resp_rw_addr = struct.unpack('>B', rx_frame[:1])[0]
                
                if DATA_LENGTH_BYTES == 1:
                    resp_data = struct.unpack('>B', rx_frame[1:2])[0]
                elif DATA_LENGTH_BYTES == 2:
                    resp_data = struct.unpack('>H', rx_frame[1:3])[0]
                elif DATA_LENGTH_BYTES == 4:
                    resp_data = struct.unpack('>I', rx_frame[1:5])[0]
                elif DATA_LENGTH_BYTES == 8:
                    resp_data = struct.unpack('>Q', rx_frame[1:9])[0]
                else:
                    resp_data = int.from_bytes(rx_frame[1:1+DATA_LENGTH_BYTES], byteorder='big')
                
                resp_rw_bit = (resp_rw_addr >> 7) & 0x01
                resp_addr = resp_rw_addr & 0x7F
                resp_operation = "Write" if resp_rw_bit == 0 else "Read"
                
                data_format = f"0{DATA_LENGTH_BYTES*2}X"  # 데이터 길이에 따른 16진수 포맷
                self.log_signal.emit(f"수신 ({resp_operation}): Addr=0x{resp_addr:02X}, RW_Byte=0x{resp_rw_addr:02X}, Data=0x{resp_data:{data_format}} ({DATA_LENGTH_BYTES}바이트)")
                self.response_signal.emit(resp_addr, resp_data)
            else:
                self.error_signal.emit(f"잘못된 응답 길이: {len(rx_frame)} bytes (예상: {expected_frame_size} bytes)")
                
        except Exception as e:
            self.error_signal.emit(f"SPI 전송 오류: {str(e)}")
    
    def read_register(self, address: int):
        """레지스터 읽기 (RW_BIT = 1)"""
        self.send_spi_frame(address, 0, is_write=False)
    
    def write_register(self, address: int, data: int):
        """레지스터 쓰기 (RW_BIT = 0)"""
        self.send_spi_frame(address, data, is_write=True)


class SPI_Master_GUI_Simple(QWidget):
    """FT2232H SPI Master GUI (간단한 .ui 로드)"""
    
    def __init__(self):
        super().__init__()
        self.worker = SPI_Worker()
        
        # UI 로드 시도, 실패시 폴백
        if not self.load_ui_file():
            self.create_fallback_ui()
        
        # 시그널 연결
        self.connect_signals()
        
        # 자동 millis() 읽기용 타이머
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.auto_read_millis)
        
    def load_ui_file(self) -> bool:
        """UI 파일 로드 시도"""
        try:
            ui_file_path = os.path.join(os.path.dirname(__file__), "ft2232h_spi_gui.ui")
            
            # UI 파일 존재 확인
            if not os.path.exists(ui_file_path):
                print(f"UI 파일을 찾을 수 없습니다: {ui_file_path}")
                return False
            
            # UI 파일 로드
            loader = QUiLoader()
            ui_file = QFile(ui_file_path)
            
            if not ui_file.open(QIODevice.ReadOnly):
                print(f"UI 파일을 열 수 없습니다: {ui_file_path}")
                return False
            
            ui_widget = loader.load(ui_file, self)
            ui_file.close()
            
            if ui_widget is None:
                print("UI 위젯 로드 실패")
                return False
            
            # UI를 메인 위젯에 추가
            layout = QVBoxLayout(self)
            layout.addWidget(ui_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # 창 설정
            self.setWindowTitle("FT2232H SPI Master - Arduino Slave 통신")
            self.setMinimumSize(800, 600)
            
            # UI 요소 찾기
            self.find_ui_elements(ui_widget)
            
            print("UI 파일 로드 성공!")
            return True
            
        except Exception as e:
            print(f"UI 로드 오류: {str(e)}")
            return False
    
    def find_ui_elements(self, ui_widget):
        """UI 요소들 찾기"""
        from PySide6.QtWidgets import QLineEdit, QSpinBox, QComboBox, QPushButton, QCheckBox, QLabel, QTextEdit
        
        # 연결 관련
        self.url_edit = ui_widget.findChild(QLineEdit, "url_edit")
        self.cs_spin = ui_widget.findChild(QSpinBox, "cs_spin")
        self.freq_edit = ui_widget.findChild(QLineEdit, "freq_edit")
        self.mode_combo = ui_widget.findChild(QComboBox, "mode_combo")
        self.connect_btn = ui_widget.findChild(QPushButton, "connect_btn")
        self.disconnect_btn = ui_widget.findChild(QPushButton, "disconnect_btn")
        
        # SPI 통신 관련
        self.addr_edit = ui_widget.findChild(QLineEdit, "addr_edit")
        self.data_edit = ui_widget.findChild(QLineEdit, "data_edit")
        self.read_btn = ui_widget.findChild(QPushButton, "read_btn")
        self.write_btn = ui_widget.findChild(QPushButton, "write_btn")
        
        # 테스트 버튼들
        self.test_read1_btn = ui_widget.findChild(QPushButton, "test_read1_btn")
        self.test_read2_btn = ui_widget.findChild(QPushButton, "test_read2_btn")  
        self.test_read3_btn = ui_widget.findChild(QPushButton, "test_read3_btn")
        self.test_write1_btn = ui_widget.findChild(QPushButton, "test_write1_btn")
        self.test_write2_btn = ui_widget.findChild(QPushButton, "test_write2_btn")  # 추가
        
        # 기타
        self.auto_checkbox = ui_widget.findChild(QCheckBox, "auto_checkbox")
        self.resp_addr_label = ui_widget.findChild(QLabel, "resp_addr_label")
        self.resp_data_label = ui_widget.findChild(QLabel, "resp_data_label")
        self.resp_dec_label = ui_widget.findChild(QLabel, "resp_dec_label")
        self.log_text = ui_widget.findChild(QTextEdit, "log_text")
        self.clear_log_btn = ui_widget.findChild(QPushButton, "clear_log_btn")
        
        # 새로 추가된 위젯들 (없을 수 있음)
        self.data_length_combo = ui_widget.findChild(QComboBox, "data_length_combo")
        self.debug_checkbox = ui_widget.findChild(QCheckBox, "debug_checkbox")
        self.auto_read_checkbox = ui_widget.findChild(QCheckBox, "auto_read_checkbox")
        self.status_label = ui_widget.findChild(QLabel, "status_label")
        self.save_log_btn = ui_widget.findChild(QPushButton, "save_log_btn")
        self.data_input = ui_widget.findChild(QLineEdit, "data_input")
        self.addr_input = ui_widget.findChild(QLineEdit, "addr_input")
    
    def create_fallback_ui(self):
        """UI 파일 로드 실패시 기본 UI 생성"""
        print("기본 UI를 생성합니다...")
        
        # 기본 UI를 프로그래밍 방식으로 생성
        from PySide6.QtWidgets import (
            QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
            QTextEdit, QSpinBox, QComboBox, QGroupBox, QCheckBox, QGridLayout
        )
        from PySide6.QtGui import QFont
        
        self.setWindowTitle("FT2232H SPI Master - Arduino Slave 통신 (기본 UI)")
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
        conn_layout.addWidget(self.cs_spin, 1, 1)
        
        conn_layout.addWidget(QLabel("주파수(Hz):"), 1, 2)
        self.freq_edit = QLineEdit("100000")
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
        spi_group = QGroupBox("SPI 통신")
        spi_layout = QGridLayout(spi_group)
        
        spi_layout.addWidget(QLabel("주소 (HEX):"), 0, 0)
        self.addr_edit = QLineEdit("01")
        self.addr_edit.setPlaceholderText("예: 01, 0x01, 1A (0~7F)")
        self.addr_edit.setMaxLength(4)  # 최대 4자리 (0x7F = 127까지)
        self.addr_edit.textChanged.connect(self.validate_addr_input)
        spi_layout.addWidget(self.addr_edit, 0, 1)
        
        spi_layout.addWidget(QLabel("데이터 (HEX):"), 0, 2)
        self.data_edit = QLineEdit("1234")
        data_max_chars = DATA_LENGTH_BYTES * 2  # 2바이트 = 4자리
        max_val_hex = f"{MAX_DATA_VALUE:X}"
        self.data_edit.setPlaceholderText(f"예: 1234, 0x1234 (0~{max_val_hex})")
        self.data_edit.setMaxLength(data_max_chars + 2)  # 0x 포함
        self.data_edit.textChanged.connect(self.validate_data_input)
        spi_layout.addWidget(self.data_edit, 0, 3)
        
        self.read_btn = QPushButton("읽기")
        self.write_btn = QPushButton("쓰기")
        self.read_btn.setEnabled(False)
        self.write_btn.setEnabled(False)
        
        spi_layout.addWidget(self.read_btn, 1, 1)
        spi_layout.addWidget(self.write_btn, 1, 2)
        
        layout.addWidget(spi_group)
        
        # 설정 그룹
        settings_group = QGroupBox("설정 및 제어")
        settings_layout = QHBoxLayout(settings_group)
        
        # 데이터 길이 설정
        settings_layout.addWidget(QLabel("데이터 길이:"))
        self.data_length_combo = QComboBox()
        self.data_length_combo.addItems(["1바이트", "2바이트", "4바이트", "8바이트"])
        self.data_length_combo.setCurrentIndex(1)  # 기본값: 2바이트
        self.data_length_combo.currentIndexChanged.connect(self.on_data_length_changed)
        settings_layout.addWidget(self.data_length_combo)
        
        # 디버그 모드 토글
        self.debug_checkbox = QCheckBox("디버그 모드 (상세 로그)")
        self.debug_mode = False
        self.debug_checkbox.toggled.connect(self.on_debug_mode_toggled)
        settings_layout.addWidget(self.debug_checkbox)
        
        # 자동 읽기 모드
        self.auto_read_checkbox = QCheckBox("쓰기 후 자동 읽기")
        self.auto_read_checkbox.setChecked(True)
        settings_layout.addWidget(self.auto_read_checkbox)
        
        # 연결 상태 표시
        settings_layout.addStretch()
        self.status_label = QLabel("연결 해제됨")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        settings_layout.addWidget(self.status_label)
        
        layout.addWidget(settings_group)
        
        # 간단한 테스트 버튼들
        test_group = QGroupBox("빠른 테스트")
        test_layout = QHBoxLayout(test_group)
        self.test_read1_btn = QPushButton("읽기: 0x01")
        self.test_write1_btn = QPushButton("쓰기: 0x01 = 0x5678")
        self.test_read1_btn.setEnabled(False)
        self.test_write1_btn.setEnabled(False)
        
        test_layout.addWidget(self.test_write1_btn)
        test_layout.addWidget(self.test_read1_btn)
        
        # 추가 테스트 버튼
        self.test_write2_btn = QPushButton("쓰기: 0x02 = 0xABCD")
        self.test_read2_btn = QPushButton("읽기: 0x02")
        self.test_write2_btn.setEnabled(False)
        self.test_read2_btn.setEnabled(False)
        
        test_layout.addWidget(self.test_write2_btn)
        test_layout.addWidget(self.test_read2_btn)
        test_layout.addStretch()
        
        layout.addWidget(test_group)
        
        # 응답 표시 - 더 명확하게
        resp_group = QGroupBox("마지막 응답")
        resp_layout = QGridLayout(resp_group)
        
        resp_layout.addWidget(QLabel("주소:"), 0, 0)
        self.resp_addr_label = QLabel("--")
        self.resp_addr_label.setStyleSheet("font-family: monospace; background-color: #f0f0f0; padding: 2px;")
        resp_layout.addWidget(self.resp_addr_label, 0, 1)
        
        resp_layout.addWidget(QLabel("데이터 (HEX):"), 0, 2)
        self.resp_data_label = QLabel("--")
        self.resp_data_label.setStyleSheet("font-family: monospace; background-color: #f0f0f0; padding: 2px;")
        resp_layout.addWidget(self.resp_data_label, 0, 3)
        
        resp_layout.addWidget(QLabel("데이터 (DEC):"), 0, 4)
        self.resp_dec_label = QLabel("--")
        self.resp_dec_label.setStyleSheet("font-family: monospace; background-color: #f0f0f0; padding: 2px;")
        resp_layout.addWidget(self.resp_dec_label, 0, 5)
        
        layout.addWidget(resp_group)
        
        # 로그 그룹
        log_group = QGroupBox("통신 로그")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(180)
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        log_control_layout = QHBoxLayout()
        self.clear_log_btn = QPushButton("로그 지우기")
        self.save_log_btn = QPushButton("로그 저장")
        log_control_layout.addWidget(self.clear_log_btn)
        log_control_layout.addWidget(self.save_log_btn)
        log_control_layout.addStretch()
        log_layout.addLayout(log_control_layout)
        
        layout.addWidget(log_group)
        
        # 기본값 설정 (addr_edit, data_edit는 이미 생성됨)
        self.test_read2_btn = None
        self.test_read3_btn = None
        self.auto_checkbox = None
        
    def connect_signals(self):
        """시그널 연결"""
        # 기본 버튼 이벤트
        if self.connect_btn:
            self.connect_btn.clicked.connect(self.on_connect)
        if self.disconnect_btn:
            self.disconnect_btn.clicked.connect(self.on_disconnect)
        if self.read_btn:
            self.read_btn.clicked.connect(self.on_read_btn_click)
        if self.write_btn:
            self.write_btn.clicked.connect(self.on_write_btn_click)
        
        # 테스트 버튼들 (있는 경우만)
        if self.test_read1_btn:
            self.test_read1_btn.clicked.connect(lambda: self.worker.read_register(0x01))
        if self.test_read2_btn:
            self.test_read2_btn.clicked.connect(lambda: self.worker.read_register(0x02))
        if self.test_write1_btn:
            self.test_write1_btn.clicked.connect(lambda: self.worker.write_register(0x01, 0x5678))
        if self.test_write2_btn:
            self.test_write2_btn.clicked.connect(lambda: self.worker.write_register(0x02, 0xABCD))
        
        # 자동 읽기 체크박스
        if self.auto_checkbox:
            self.auto_checkbox.toggled.connect(self.on_auto_toggle)
        
        # 로그 제어 버튼들
        if self.clear_log_btn:
            self.clear_log_btn.clicked.connect(self.log_text.clear)
        if hasattr(self, 'save_log_btn') and self.save_log_btn:
            self.save_log_btn.clicked.connect(self.save_log_to_file)
        
        # 워커 시그널
        self.worker.log_signal.connect(self.append_log)
        self.worker.response_signal.connect(self.on_response)
        self.worker.error_signal.connect(self.on_error)
        self.worker.connected_signal.connect(self.on_connection_changed)
        
    def on_connect(self):
        """연결 버튼 클릭"""
        try:
            url = self.url_edit.text().strip() if self.url_edit else "ftdi://ftdi:2232h/1"
            cs = self.cs_spin.value() if self.cs_spin else 0
            freq = int(self.freq_edit.text().strip()) if self.freq_edit else 100000
            mode = int(self.mode_combo.currentText()) if self.mode_combo else 0
            
            self.worker.connect_device(url, cs, freq, mode)
            
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "주파수는 숫자로 입력해주세요.")
        except Exception as e:
            QMessageBox.critical(self, "연결 오류", str(e))
            
    def on_disconnect(self):
        """연결 해제 버튼 클릭"""
        self.worker.disconnect_device()
    
    def on_read_btn_click(self):
        """읽기 버튼 클릭"""
        try:
            if self.addr_edit:
                addr_text = self.addr_edit.text().strip()
                address = parse_hex_input(addr_text)
                
                if address > 0x7F:  # 주소는 7비트 (0-127)
                    QMessageBox.warning(self, "입력 오류", f"주소는 0x00~0x7F (0~127) 범위여야 합니다.\n입력값: 0x{address:02X}")
                    return
                
                self.worker.read_register(address)
                self.append_log(f"읽기 요청: 주소 0x{address:02X}")
            else:
                # 기본값 사용
                self.worker.read_register(0x01)
                
        except ValueError as e:
            QMessageBox.warning(self, "입력 오류", str(e))
        except Exception as e:
            QMessageBox.critical(self, "오류", f"읽기 오류: {str(e)}")
    
    def on_write_btn_click(self):
        """쓰기 버튼 클릭"""
        try:
            address = 0x01  # 기본값
            data = 0x1234   # 기본값
            
            if self.addr_edit:
                addr_text = self.addr_edit.text().strip()
                address = parse_hex_input(addr_text)
                
                if address > 0x7F:  # 주소는 7비트 (0-127)
                    QMessageBox.warning(self, "입력 오류", f"주소는 0x00~0x7F (0~127) 범위여야 합니다.\n입력값: 0x{address:02X}")
                    return
            
            if self.data_edit:
                data_text = self.data_edit.text().strip()
                data = parse_hex_input(data_text)
                
                if data > MAX_DATA_VALUE:  # 데이터 길이 확인
                    QMessageBox.warning(self, "입력 오류", f"데이터는 0x00~0x{MAX_DATA_VALUE:X} 범위여야 합니다.\n입력값: 0x{data:X}\n현재 데이터 길이: {DATA_LENGTH_BYTES}바이트")
                    return
            
            self.worker.write_register(address, data)
            data_format = f"0{DATA_LENGTH_BYTES*2}X"
            self.append_log(f"쓰기 요청: 주소 0x{address:02X}, 데이터 0x{data:{data_format}}")
            
        except ValueError as e:
            QMessageBox.warning(self, "입력 오류", str(e))
        except Exception as e:
            QMessageBox.critical(self, "오류", f"쓰기 오류: {str(e)}")
    
    def validate_addr_input(self, text):
        """주소 입력 실시간 유효성 검사"""
        if not text:
            return
        
        try:
            value = parse_hex_input(text)
            if value > 0x7F:
                self.addr_edit.setStyleSheet("QLineEdit { background-color: #ffcccc; }")
                self.addr_edit.setToolTip(f"주소 범위 초과: 0x{value:02X} > 0x7F")
            else:
                self.addr_edit.setStyleSheet("")
                self.addr_edit.setToolTip(f"주소: 0x{value:02X}")
        except ValueError:
            self.addr_edit.setStyleSheet("QLineEdit { background-color: #ffcccc; }")
            self.addr_edit.setToolTip("잘못된 16진수 형식")
    
    def validate_data_input(self, text):
        """데이터 입력 실시간 유효성 검사"""
        if not text:
            return
        
        try:
            value = parse_hex_input(text)
            if value > MAX_DATA_VALUE:
                self.data_edit.setStyleSheet("QLineEdit { background-color: #ffcccc; }")
                data_format = f"0{DATA_LENGTH_BYTES*2}X"
                self.data_edit.setToolTip(f"데이터 범위 초과: 0x{value:{data_format}} > 0x{MAX_DATA_VALUE:{data_format}}")
            else:
                self.data_edit.setStyleSheet("")
                data_format = f"0{DATA_LENGTH_BYTES*2}X"
                self.data_edit.setToolTip(f"데이터: 0x{value:{data_format}}")
        except ValueError:
            self.data_edit.setStyleSheet("QLineEdit { background-color: #ffcccc; }")
            self.data_edit.setToolTip("잘못된 16진수 형식")
        
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
        
        # 주소/데이터 입력 필드도 활성화/비활성화
        if self.addr_edit:
            self.addr_edit.setEnabled(connected)
        if self.data_edit:
            self.data_edit.setEnabled(connected)
        
        if self.auto_checkbox:
            self.auto_checkbox.setEnabled(connected)
            if not connected:
                self.auto_checkbox.setChecked(False)
            
    def on_response(self, address: int, data: int):
        """응답 수신"""
        if self.resp_addr_label:
            self.resp_addr_label.setText(f"주소: 0x{address:02X}")
        if self.resp_data_label:
            data_format = f"0{DATA_LENGTH_BYTES*2}X"  # 데이터 길이에 따른 16진수 포맷
            self.resp_data_label.setText(f"데이터: 0x{data:{data_format}} ({DATA_LENGTH_BYTES}바이트)")
        if self.resp_dec_label:
            self.resp_dec_label.setText(f"십진수: {data}")
        
    def on_error(self, message: str):
        """오류 처리"""
        self.append_log(f"❌ 오류: {message}")
        QMessageBox.critical(self, "오류", message)
        
    def append_log(self, message: str):
        """로그 추가"""
        if self.log_text:
            timestamp = time.strftime("%H:%M:%S")
            self.log_text.append(f"[{timestamp}] {message}")
    
    def on_debug_mode_toggled(self, enabled: bool):
        """디버그 모드 토글 핸들러"""
        global DEBUG_MODE
        DEBUG_MODE = enabled
        status = "활성화" if enabled else "비활성화"
        self.append_log(f"디버그 모드 {status}")
        
        # 디버그 모드에 따라 로깅 수준 조정
        if self.debug_mode_cb and hasattr(self, 'log_level_cb'):
            self.log_level_cb.setEnabled(enabled)
    
    def on_data_length_changed(self, index: int):
        """데이터 길이 변경 핸들러"""
        global DATA_LENGTH_BYTES
        old_length = DATA_LENGTH_BYTES
        
        # 콤보박스 인덱스에 따라 데이터 길이 설정
        if index == 0:  # "1 byte"
            DATA_LENGTH_BYTES = 1
        elif index == 1:  # "2 bytes"
            DATA_LENGTH_BYTES = 2
        elif index == 2:  # "4 bytes"
            DATA_LENGTH_BYTES = 4
        else:
            DATA_LENGTH_BYTES = 2  # 기본값
            
        self.append_log(f"데이터 길이 변경: {old_length} → {DATA_LENGTH_BYTES} bytes")
        
        # 데이터 필드 리셋 (길이가 변경되었으므로)
        if hasattr(self, 'data_input') and self.data_input:
            self.data_input.clear()
            self.data_input.setPlaceholderText(f"예: {'FF' * DATA_LENGTH_BYTES}")
    
    def save_log_to_file(self):
        """로그를 파일로 저장"""
        try:
            if not self.log_text:
                self.append_log("저장할 로그가 없습니다.")
                return
                
            # 파일 이름에 타임스탬프 포함
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"spi_log_{timestamp}.txt"
            
            # 로그 내용 가져오기
            log_content = self.log_text.toPlainText()
            
            # 파일로 저장
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"SPI Communication Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(log_content)
                
            self.append_log(f"로그가 저장되었습니다: {filename}")
            
        except Exception as e:
            self.append_log(f"로그 저장 실패: {str(e)}")
        
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
    
    window = SPI_Master_GUI_Simple()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()