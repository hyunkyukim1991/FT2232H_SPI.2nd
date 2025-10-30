#!/usr/bin/env python3
"""
FT2232H SPI Read 전용 테스트 스크립트
특정 주소에서 데이터를 읽기만 하는 단순한 테스트
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

class SPI_Reader:
    """SPI Read 전용 클래스"""
    
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
    
    def read_data(self, address: int) -> Optional[int]:
        """
        지정된 주소에서 데이터 읽기 전용
        
        Args:
            address: 7비트 주소 (0x00-0x7F)
            
        Returns:
            읽은 데이터 또는 None
        """
        if not self.is_connected or not self.slave:
            logger.error("Not connected to FT2232H")
            return None
            
        try:
            # RW_BIT = A[7], Address = A[6:0] 형식으로 주소 바이트 구성
            # RW_BIT: 0 = Write, 1 = Read
            rw_bit = 1  # Read 고정
            addr_byte = (rw_bit << 7) | (address & 0x7F)
            
            # 5바이트 전송 프레임 구성 (RW+Address 1바이트 + Dummy Data 4바이트, Big-endian)
            tx_frame = struct.pack('>BI', addr_byte, 0x00000000)
            
            logger.info(f"READ -> Addr=0x{address:02X}, RW_Byte=0x{addr_byte:02X}")
            logger.debug(f"TX bytes: {tx_frame.hex().upper()}")
            
            # SPI 트랜잭션 실행 (Duplex 모드)
            rx_frame = self.slave.exchange(tx_frame, duplex=True)
            
            logger.debug(f"RX bytes: {rx_frame.hex().upper()}")
            
            # 응답 프레임 파싱 (RW+Address 1바이트 + Data 4바이트, Big-endian)
            if len(rx_frame) >= 5:
                resp_rw_addr, resp_data = struct.unpack('>BI', rx_frame[:5])
                resp_rw_bit = (resp_rw_addr >> 7) & 0x01
                resp_addr = resp_rw_addr & 0x7F
                
                logger.info(f"RX <- READ: Addr=0x{resp_addr:02X}, RW_Byte=0x{resp_rw_addr:02X}, Data=0x{resp_data:08X}")
                
                # 주소 확인
                if resp_addr == address:
                    logger.info("✅ Address match")
                    return resp_data
                else:
                    logger.warning(f"Address mismatch: sent 0x{address:02X}, got 0x{resp_addr:02X}")
                    return resp_data  # 데이터는 반환하되 경고만 출력
            else:
                logger.warning(f"Invalid response length: {len(rx_frame)} bytes")
                return None
                
        except Exception as e:
            logger.error(f"SPI read failed: {e}")
            return None

def main():
    """메인 함수 - Read 테스트"""
    print("=" * 50)
    print("FT2232H SPI Read 전용 테스트")
    print("=" * 50)
    
    # 테스트 설정
    test_addresses = [0x01, 0x02, 0x03]  # 테스트할 주소들
    
    print(f"테스트 주소들: {[f'0x{addr:02X}' for addr in test_addresses]}")
    
    # SPI Reader 초기화
    reader = SPI_Reader(
        url="ftdi://ftdi:2232h/1",
        cs=0,  # AD3 핀 사용
        freq=1_000_000,  # 1MHz
        mode=0
    )
    
    try:
        # 연결
        print("\n1. FT2232H 연결 중...")
        if not reader.connect():
            print("❌ 연결 실패!")
            return
        
        print("✅ 연결 성공!")
        
        # Read 테스트
        print("\n2. SPI Read 테스트...")
        
        for i, address in enumerate(test_addresses, 1):
            print(f"\n--- 테스트 #{i}: 주소 0x{address:02X} 읽기 ---")
            
            data = reader.read_data(address)
            
            if data is not None:
                print(f"✅ Read 성공!")
                print(f"📖 읽은 데이터: 0x{data:08X} ({data})")
                
                # 특별한 주소의 경우 추가 정보 표시
                if address == 0x03:
                    print(f"   (millis 값으로 추정)")
            else:
                print(f"❌ Read 실패!")
            
            time.sleep(0.5)
        
        # 연속 읽기 테스트 (주소 0x03 - millis)
        print(f"\n3. 연속 읽기 테스트 (주소 0x03 - millis)")
        print("5초간 1초마다 읽기...")
        
        for i in range(5):
            print(f"\n읽기 #{i+1}:")
            data = reader.read_data(0x03)
            if data is not None:
                print(f"  millis() = {data} (0x{data:08X})")
            else:
                print(f"  읽기 실패")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ 사용자 중단")
    
    finally:
        print("\n4. 연결 해제...")
        reader.disconnect()
        print("✅ 완료")

if __name__ == "__main__":
    main()