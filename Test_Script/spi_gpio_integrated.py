#!/usr/bin/env python3
"""
FT2232H SPI + GPIO 통합 제어 스크립트
SPI: Channel A, GPIO: Channel A의 여분 핀 사용
"""

import time
from pyftdi.spi import SpiController
from pyftdi.gpio import GpioMpsseController

class FT2232H_SPI_GPIO_Controller:
    def __init__(self):
        self.spi = None
        self.gpio = None
        self.spi_slave = None
        
    def connect_spi(self):
        """SPI 연결 (Channel A)"""
        try:
            self.spi = SpiController()
            self.spi.configure('ftdi://0x0403:0x6010/1')  # Channel A
            self.spi_slave = self.spi.get_port(cs=0, freq=1000000, mode=0)
            print("✅ SPI 연결 성공 (Channel A)")
            return True
        except Exception as e:
            print(f"❌ SPI 연결 실패: {e}")
            return False
    
    def connect_gpio(self):
        """GPIO 연결 (Channel A의 여분 핀)"""
        try:
            # 주의: SPI와 함께 사용시에는 SPI 핀(CS, CLK, MOSI, MISO) 제외
            self.gpio = GpioMpsseController()
            self.gpio.configure('ftdi://0x0403:0x6010/1')  # Channel A
            
            # GPIO 핀 매핑 (SPI 핀 제외)
            # SPI 사용 핀: CS(0), CLK(1), MOSI(2), MISO(3)
            # GPIO 사용 가능 핀: 4, 5, 6, 7
            gpio_mask = 0xF0  # 상위 4비트 (핀 4-7)
            self.gpio.set_direction(gpio_mask, gpio_mask)  # 출력 모드
            
            print("✅ GPIO 연결 성공 (핀 4-7 사용)")
            return True
        except Exception as e:
            print(f"❌ GPIO 연결 실패: {e}")
            return False
    
    def spi_write_read(self, address, write_data=None):
        """SPI 쓰기/읽기"""
        if not self.spi_slave:
            print("❌ SPI가 연결되지 않음")
            return None
        
        try:
            if write_data is not None:
                # Write 명령 (RW_BIT = 0)
                rw_bit = 0
                addr_with_rw = (address & 0x7F) | (rw_bit << 7)
                
                # 5바이트 전송: Address+RW + 4바이트 데이터
                tx_data = [addr_with_rw] + list(write_data.to_bytes(4, 'big'))
                response = self.spi_slave.exchange(tx_data)
                
                print(f"SPI Write - Addr: 0x{address:02X}, Data: 0x{write_data:08X}")
                return response
            else:
                # Read 명령 (RW_BIT = 1)
                rw_bit = 1
                addr_with_rw = (address & 0x7F) | (rw_bit << 7)
                
                # 5바이트 전송: Address+RW + 4바이트 더미
                tx_data = [addr_with_rw, 0x00, 0x00, 0x00, 0x00]
                response = self.spi_slave.exchange(tx_data)
                
                # 응답에서 데이터 추출 (2-5바이트)
                read_data = int.from_bytes(response[1:5], 'big')
                print(f"SPI Read  - Addr: 0x{address:02X}, Data: 0x{read_data:08X}")
                return read_data
                
        except Exception as e:
            print(f"❌ SPI 통신 실패: {e}")
            return None
    
    def gpio_control(self, pin, state):
        """GPIO 핀 제어 (핀 4-7만 사용)"""
        if not self.gpio:
            print("❌ GPIO가 연결되지 않음")
            return
        
        if pin < 4 or pin > 7:
            print(f"❌ 잘못된 핀 번호: {pin} (4-7만 사용 가능)")
            return
        
        try:
            current_state = self.gpio.read()
            
            if state:
                new_state = current_state | (1 << pin)
            else:
                new_state = current_state & ~(1 << pin)
            
            self.gpio.write(new_state)
            print(f"GPIO 핀 {pin}: {'ON' if state else 'OFF'}")
            
        except Exception as e:
            print(f"❌ GPIO 제어 실패: {e}")
    
    def gpio_pattern(self):
        """GPIO LED 패턴 테스트"""
        if not self.gpio:
            print("❌ GPIO가 연결되지 않음")
            return
        
        print("GPIO LED 패턴 테스트 시작...")
        
        try:
            # 순차 점등 (핀 4-7)
            for pin in range(4, 8):
                self.gpio_control(pin, True)
                time.sleep(0.2)
                self.gpio_control(pin, False)
                time.sleep(0.1)
            
            # 모든 핀 동시 점등
            self.gpio.write(0xF0)  # 핀 4-7 ON
            time.sleep(0.5)
            self.gpio.write(0x00)  # 모든 핀 OFF
            
            print("✅ GPIO 패턴 테스트 완료")
            
        except Exception as e:
            print(f"❌ GPIO 패턴 테스트 실패: {e}")
    
    def combined_test(self):
        """SPI + GPIO 통합 테스트"""
        print("=" * 60)
        print("FT2232H SPI + GPIO 통합 테스트")
        print("=" * 60)
        
        # SPI 연결
        if not self.connect_spi():
            return
        
        # GPIO 연결 (같은 Channel A 사용)
        if not self.connect_gpio():
            self.disconnect()
            return
        
        try:
            print("\n1. SPI 통신 테스트...")
            
            # SPI Write 테스트
            self.spi_write_read(0x10, 0x12345678)
            time.sleep(0.1)
            
            # SPI Read 테스트
            self.spi_write_read(0x10)
            time.sleep(0.1)
            
            print("\n2. GPIO 제어 테스트...")
            
            # GPIO 패턴 테스트
            self.gpio_pattern()
            
            print("\n3. SPI + GPIO 동시 테스트...")
            
            # SPI 통신과 GPIO 제어 동시 수행
            for i in range(3):
                # SPI 쓰기
                self.spi_write_read(0x20 + i, 0xAABBCCDD + i)
                
                # GPIO 점등
                self.gpio_control(4 + (i % 4), True)
                time.sleep(0.3)
                
                # SPI 읽기
                self.spi_write_read(0x20 + i)
                
                # GPIO 소등
                self.gpio_control(4 + (i % 4), False)
                time.sleep(0.2)
            
            print("\n✅ 통합 테스트 완료!")
            
        except Exception as e:
            print(f"❌ 통합 테스트 실패: {e}")
        
        finally:
            self.disconnect()
    
    def disconnect(self):
        """연결 해제"""
        try:
            if self.gpio:
                self.gpio.write(0x00)  # 모든 GPIO OFF
                self.gpio.terminate()
                print("✅ GPIO 연결 해제")
        except:
            pass
        
        try:
            if self.spi:
                self.spi.terminate()
                print("✅ SPI 연결 해제")
        except:
            pass

def main():
    controller = FT2232H_SPI_GPIO_Controller()
    
    print("FT2232H SPI + GPIO 통합 제어")
    print("1. 통합 테스트 실행")
    print("2. SPI만 테스트")
    print("3. GPIO만 테스트")
    
    choice = input("선택하세요 (1-3): ").strip()
    
    if choice == '1':
        controller.combined_test()
    elif choice == '2':
        if controller.connect_spi():
            controller.spi_write_read(0x15, 0x12345678)
            controller.spi_write_read(0x15)
            controller.disconnect()
    elif choice == '3':
        if controller.connect_gpio():
            controller.gpio_pattern()
            controller.disconnect()
    else:
        print("통합 테스트를 실행합니다...")
        controller.combined_test()

if __name__ == "__main__":
    main()