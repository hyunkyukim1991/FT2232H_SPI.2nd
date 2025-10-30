"""
32비트 unsigned integer를 지원하는 Custom QSpinBox
"""

from PySide6.QtWidgets import QSpinBox
from PySide6.QtCore import Signal, QObject

class UInt32SpinBox(QSpinBox):
    """32비트 unsigned integer를 지원하는 커스텀 SpinBox"""
    
    # 32비트 unsigned 값 변경 시그널
    uint32ValueChanged = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._uint32_value = 0
        self._max_uint32 = 0xFFFFFFFF
        
        # 내부 QSpinBox는 signed 범위만 사용
        super().setRange(-2147483648, 2147483647)
        super().valueChanged.connect(self._on_internal_value_changed)
        
    def setUInt32Range(self, minimum=0, maximum=0xFFFFFFFF):
        """32비트 unsigned 범위 설정"""
        self._min_uint32 = max(0, minimum)
        self._max_uint32 = min(0xFFFFFFFF, maximum)
        
    def setUInt32Value(self, value):
        """32비트 unsigned 값 설정"""
        if not isinstance(value, int):
            return
            
        # 32비트 범위로 제한
        value = max(0, min(self._max_uint32, value))
        
        if value != self._uint32_value:
            self._uint32_value = value
            self._update_display()
            self.uint32ValueChanged.emit(int(value))
    
    def uint32Value(self):
        """현재 32비트 unsigned 값 반환"""
        return self._uint32_value
    
    def _update_display(self):
        """표시 업데이트"""
        # 32비트 값을 signed 범위로 변환하여 표시
        if self._uint32_value <= 2147483647:
            display_value = self._uint32_value
        else:
            # 큰 값은 음수로 변환하여 내부적으로 처리
            display_value = self._uint32_value - 4294967296
            
        super().blockSignals(True)
        super().setValue(display_value)
        super().blockSignals(False)
    
    def _on_internal_value_changed(self, value):
        """내부 SpinBox 값 변경 처리"""
        # signed 값을 unsigned로 변환
        if value < 0:
            uint32_value = value + 4294967296
        else:
            uint32_value = value
            
        if uint32_value != self._uint32_value:
            self._uint32_value = uint32_value
            self.uint32ValueChanged.emit(int(uint32_value))
    
    def textFromValue(self, value):
        """값을 텍스트로 변환 (16진수 표시)"""
        if value < 0:
            uint32_value = value + 4294967296
        else:
            uint32_value = value
        return f"0x{uint32_value:08X}"
    
    def valueFromText(self, text):
        """텍스트를 값으로 변환"""
        try:
            # 16진수 또는 10진수 파싱
            text = text.strip().replace("0x", "").replace("0X", "")
            uint32_value = int(text, 16) if text else 0
            
            # 32비트 범위로 제한
            uint32_value = max(0, min(self._max_uint32, uint32_value))
            
            # signed 범위로 변환
            if uint32_value <= 2147483647:
                return uint32_value
            else:
                return uint32_value - 4294967296
        except ValueError:
            return 0