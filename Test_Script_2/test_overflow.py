#!/usr/bin/env python3
"""
32비트 값 오버플로우 테스트 스크립트
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("32비트 오버플로우 테스트")
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # HEX 값 표시용 LineEdit
        self.hex_edit = QLineEdit("00000000")
        self.hex_edit.setMaxLength(8)
        layout.addWidget(QLabel("Hex Value:"))
        layout.addWidget(self.hex_edit)
        
        # DEC 값 표시용 Label
        self.dec_label = QLabel("0")
        layout.addWidget(QLabel("Dec Value:"))
        layout.addWidget(self.dec_label)
        
        # 테스트 버튼들
        test_button_1 = QPushButton("테스트 1: 0x7FFFFFFF (2147483647)")
        test_button_1.clicked.connect(lambda: self.set_value(0x7FFFFFFF))
        layout.addWidget(test_button_1)
        
        test_button_2 = QPushButton("테스트 2: 0x80000000 (2147483648)")
        test_button_2.clicked.connect(lambda: self.set_value(0x80000000))
        layout.addWidget(test_button_2)
        
        test_button_3 = QPushButton("테스트 3: 0xFFFFFFFF (4294967295)")
        test_button_3.clicked.connect(lambda: self.set_value(0xFFFFFFFF))
        layout.addWidget(test_button_3)
        
    def set_value(self, value):
        """값 설정 및 표시"""
        print(f"Setting value: {value} (0x{value:08X})")
        
        # HEX LineEdit에 값 설정
        self.hex_edit.setText(f"{value:08X}")
        
        # DEC Label에 값 설정
        self.dec_label.setText(str(value))
        
        print(f"✅ 성공: {value}")

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    
    print("32비트 오버플로우 테스트 시작")
    print("각 버튼을 클릭해서 오버플로우가 발생하는지 확인하세요.")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()