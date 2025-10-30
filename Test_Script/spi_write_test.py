#!/usr/bin/env python3
"""
FT2232H SPI Write 전용 테스트 스크립트
특정 주소에 데이터를 쓰기만 하는 단순한 테스트
"""

import time
import logging
from typing import Optional

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from pyftdi.spi import SpiController
    from pyftdi.ftdi import Ftdi
    import struct
except ImportError as e:
    logger.error(f"Required libraries not available: {e}")
    logger.error("Install with: pip install pyftdi")
    exit(1)

class SPI_Writer:
    """SPI Write 전용 클래스"""
    
    def __init__(self, url: str = "ftdi://ftdi:2232h/1", cs: int = 0, 
                 freq: int = 1_000_000, mode: int = 0):
        """
        초기화
        
        Args:
            url: FTDI 장치 URL
            cs: Chip Select 핀 번호 (0-3, AD3=0, AD4=1, AD5=2, AD6=3)
            freq: SPI 클럭 주파수 (Hz)
            mode: SPI 모드 (0-3)
        """
        self.url = url
        self.cs = cs
        self.freq = freq
        self.mode = mode
        
        self.spi_ctrl: Optional[SpiController] = None
        self.slave = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """FT2232H에 연결"""
        try:
            logger.info(f"Connecting to {self.url}")
            logger.info(f"CS Pin: AD{3+self.cs} (CS{self.cs})")
            
            # SPI 컨트롤러 생성 및 설정
            self.spi_ctrl = SpiController()
            self.spi_ctrl.configure(self.url)
            
            # SPI Slave 포트 설정
            self.slave = self.spi_ctrl.get_port(
                cs=self.cs, 
                freq=self.freq, 
                mode=self.mode
            )
            
            self.is_connected = True
            logger.info(f"Connected successfully - CS={self.cs}, Freq={self.freq}Hz, Mode={self.mode}")
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.disconnect()
            return False
    
    def disconnect(self):
        """연결 해제"""
        try:
            if self.spi_ctrl:
                self.spi_ctrl.terminate()
            self.spi_ctrl = None
            self.slave = None
            self.is_connected = False
            logger.info("Disconnected")
        except Exception as e:
            logger.error(f"Disconnect error: {e}")
    
    def write_data(self, address: int, data: int) -> bool:
        """
        지정된 주소에 데이터 쓰기 전용
        
        Args:
            address: 7비트 주소 (0x00-0x7F)
            data: 4바이트 데이터 (0x00000000-0xFFFFFFFF)
            
        Returns:
            성공 여부
        """
        if not self.is_connected or not self.slave:
            logger.error("Not connected to FT2232H")
            return False
            
        try:
            # RW_BIT = A[7], Address = A[6:0] 형식으로 주소 바이트 구성
            # RW_BIT: 0 = Write, 1 = Read
            rw_bit = 0  # Write 고정
            addr_byte = (rw_bit << 7) | (address & 0x7F)
            
            # 5바이트 전송 프레임 구성 (RW+Address 1바이트 + Data 4바이트, Big-endian)
            tx_frame = struct.pack('>BI', addr_byte, data & 0xFFFFFFFF)
            
            logger.info(f"WRITE -> Addr=0x{address:02X}, RW_Byte=0x{addr_byte:02X}, Data=0x{data:08X}")
            logger.debug(f"TX bytes: {tx_frame.hex().upper()}")
            
            # SPI 트랜잭션 실행 (Write 전용이므로 응답 확인 안함)
            rx_frame = self.slave.exchange(tx_frame, duplex=True)
            
            logger.debug(f"RX bytes: {rx_frame.hex().upper()}")
            logger.info("✅ Write completed")
            return True
                
        except Exception as e:
            logger.error(f"SPI write failed: {e}")
            return False

def main():
    """메인 함수 - Write 테스트"""
    print("=" * 50)
    print("FT2232H SPI Write 전용 테스트")
    print("=" * 50)
    
    # 테스트 설정
    TEST_ADDRESS = 0x01  # 테스트할 주소
    TEST_DATA = 0x12345678  # 쓸 데이터
    
    print(f"테스트 주소: 0x{TEST_ADDRESS:02X}")
    print(f"쓸 데이터: 0x{TEST_DATA:08X}")
    
    # SPI Writer 초기화
    writer = SPI_Writer(
        url="ftdi://ftdi:2232h/1",
        cs=0,  # AD3 핀 사용
        freq=1_000_000,  # 1MHz
        mode=0
    )
    
    try:
        # 연결
        print("\n1. FT2232H 연결 중...")
        if not writer.connect():
            print("❌ 연결 실패!")
            return
        
        print("✅ 연결 성공!")
        
        # Write 테스트
        print("\n2. SPI Write 테스트...")
        success = writer.write_data(TEST_ADDRESS, TEST_DATA)
        
        if success:
            print("✅ Write 성공!")
        else:
            print("❌ Write 실패!")
            
        # # 추가 테스트 (다른 데이터로)
        # print("\n3. 추가 Write 테스트...")
        # test_data_list = [
        #     0xAABBCCDD,
        #     0x11223344,
        #     0xFFFFFFFF,
        #     0x00000000
        # ]
        
        # for i, data in enumerate(test_data_list, 1):
        #     print(f"\n테스트 #{i}: 0x{data:08X}")
        #     success = writer.write_data(TEST_ADDRESS, data)
        #     if success:
        #         print(f"✅ 테스트 #{i} 성공")
        #     else:
        #         print(f"❌ 테스트 #{i} 실패")
        #     time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
    
    finally:
        print("\n4. 연결 해제...")
        writer.disconnect()
        print("✅ 완료")

if __name__ == "__main__":
    main()