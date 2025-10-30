#!/usr/bin/env python3
"""
FT2232H SPI 연결 테스트 스크립트
빠른 연결 및 기본 기능 테스트
"""

import time
import sys

try:
    from pyftdi.ftdi import Ftdi
    from pyftdi.spi import SpiController
except ImportError:
    print("❌ pyftdi 라이브러리가 설치되지 않았습니다.")
    print("설치 명령: pip install pyftdi")
    sys.exit(1)

def test_backend():
    """USB 백엔드 테스트"""
    print("=== USB 백엔드 테스트 ===")
    try:
        import usb.backend.libusb1
        backend = usb.backend.libusb1.get_backend()
        if backend:
            print("✅ libusb1 백엔드 사용 가능")
            return True
        else:
            print("❌ libusb1 백엔드 없음")
            return False
    except ImportError:
        print("❌ pyusb 설치되지 않음")
        return False

def scan_devices():
    """FTDI 장치 스캔"""
    print("\n=== FTDI 장치 스캔 ===")
    try:
        devices = Ftdi.list_devices()
        if devices:
            print(f"✅ {len(devices)}개의 FTDI 장치 발견:")
            for i, (vid, pid, serial) in enumerate(devices):
                print(f"  {i+1}. VID=0x{vid:04X}, PID=0x{pid:04X}, Serial={serial}")
            return devices
        else:
            print("❌ FTDI 장치를 찾을 수 없습니다.")
            return []
    except Exception as e:
        print(f"❌ 장치 스캔 실패: {e}")
        return []

def test_connection(url="ftdi://ftdi:2232h/1"):
    """FT2232H 연결 테스트"""
    print(f"\n=== 연결 테스트: {url} ===")
    try:
        controller = SpiController()
        controller.configure(url)
        
        slave = controller.get_port(cs=0, freq=1000000, mode=0)
        print("✅ SPI 연결 성공")
        
        # 간단한 데이터 전송 테스트 (RW_BIT 형식)
        test_data = b'\x83\x00\x00\x00\x00'  # RW_BIT=1 + Address 0x03 (read millis) + dummy data
        print("📤 테스트 데이터 전송 (Read millis)...")
        
        response = slave.exchange(test_data, duplex=True)
        print(f"📥 응답 수신: {response.hex().upper()}")
        
        if len(response) == 5:
            rw_addr_byte = response[0]
            rw_bit = (rw_addr_byte >> 7) & 0x01
            addr = rw_addr_byte & 0x7F
            data = int.from_bytes(response[1:5], byteorder='big')
            operation = "Write" if rw_bit == 0 else "Read"
            
            print(f"   RW_Byte: 0x{rw_addr_byte:02X}")
            print(f"   Operation: {operation} (RW_BIT={rw_bit})")
            print(f"   주소: 0x{addr:02X}")
            print(f"   데이터: 0x{data:08X} ({data})")
            print("✅ 통신 테스트 성공")
        else:
            print(f"⚠️ 예상과 다른 응답 길이: {len(response)} bytes")
        
        controller.terminate()
        return True
        
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
        
        # 상세한 오류 분석
        error_str = str(e).lower()
        if "no backend available" in error_str:
            print("\n💡 해결 방법:")
            print("1. FTDI D2XX 드라이버 설치: https://ftdichip.com/drivers/d2xx-drivers/")
            print("2. libusb DLL 설치 (Windows)")
            print("3. 시스템 재부팅 후 재시도")
        elif "not found" in error_str:
            print("\n💡 해결 방법:")
            print("1. FT2232H USB 연결 확인")
            print("2. 장치 관리자에서 FTDI 장치 확인")
            print("3. URL 변경 시도 (예: ftdi://ftdi:2232h/2)")
        elif "access" in error_str or "permission" in error_str:
            print("\n💡 해결 방법:")
            print("1. 관리자 권한으로 실행")
            print("2. 다른 프로그램에서 장치 사용 여부 확인")
            
        return False

def main():
    """메인 테스트 함수"""
    print("🔧 FT2232H SPI 연결 진단 도구")
    print("=" * 50)
    
    # 1. 백엔드 테스트
    backend_ok = test_backend()
    
    # 2. 장치 스캔
    devices = scan_devices()
    
    # 3. 연결 테스트
    if devices or not backend_ok:
        # 일반적인 URL들로 테스트
        test_urls = [
            "ftdi://ftdi:2232h/1",
            "ftdi://ftdi:2232h/2", 
            "ftdi:///1",
            "ftdi:///2"
        ]
        
        success = False
        for url in test_urls:
            if test_connection(url):
                success = True
                break
            time.sleep(0.5)
        
        if success:
            print("\n🎉 모든 테스트 통과!")
            print("이제 ft2232h_spi_master.py 또는 ft2232h_spi_gui.py를 실행할 수 있습니다.")
        else:
            print("\n❌ 연결 테스트 실패")
            print("하드웨어 연결과 드라이버 설치를 확인해주세요.")
    else:
        print("\n⚠️ 장치가 발견되지 않았습니다.")
        print("FT2232H가 연결되어 있고 드라이버가 설치되어 있는지 확인해주세요.")
    
    print("\n" + "=" * 50)
    input("아무 키나 누르면 종료됩니다...")

if __name__ == "__main__":
    main()