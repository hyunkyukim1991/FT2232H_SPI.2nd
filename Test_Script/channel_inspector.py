#!/usr/bin/env python3
"""
FT2232H Channel A & B 종합 점검 스크립트
두 채널의 상태, 드라이버, 기능을 모두 점검합니다.
"""

import time
import sys
from typing import Dict, List, Optional

def check_usb_backends():
    """USB 백엔드 확인"""
    print("🔍 USB 백엔드 확인:")
    backends = {}
    
    # libusb1 확인
    try:
        import usb.backend.libusb1
        backend = usb.backend.libusb1.get_backend()
        backends['libusb1'] = backend is not None
        print(f"   libusb1: {'✅ 사용 가능' if backend else '❌ 없음'}")
    except:
        backends['libusb1'] = False
        print("   libusb1: ❌ 없음")
    
    # libusb0 확인
    try:
        import usb.backend.libusb0
        backend = usb.backend.libusb0.get_backend()
        backends['libusb0'] = backend is not None
        print(f"   libusb0: {'✅ 사용 가능' if backend else '❌ 없음'}")
    except:
        backends['libusb0'] = False
        print("   libusb0: ❌ 없음")
    
    return backends

def scan_ftdi_devices():
    """FTDI 장치 스캔"""
    print("\n🔍 FTDI 장치 스캔:")
    
    try:
        from pyftdi.ftdi import Ftdi
        devices = Ftdi.list_devices()
        
        if not devices:
            print("   ❌ FTDI 장치 없음")
            return []
        
        print(f"   ✅ {len(devices)}개 장치 발견:")
        for i, device in enumerate(devices):
            try:
                if len(device) >= 3:
                    vid, pid, serial = device[:3]
                    print(f"      Device {i}: VID=0x{vid:04X}, PID=0x{pid:04X}, Serial={serial}")
                else:
                    print(f"      Device {i}: {str(device)}")
            except Exception as e:
                print(f"      Device {i}: {str(device)[:100]} (파싱 오류: {e})")
        
        return devices
        
    except Exception as e:
        print(f"   ❌ 스캔 실패: {e}")
        return []

def test_channel_connection(channel: str, url: str):
    """특정 채널 연결 테스트"""
    print(f"\n🔧 Channel {channel} 연결 테스트 ({url}):")
    
    results = {
        'spi': False,
        'gpio': False,
        'uart': False,
        'errors': []
    }
    
    # SPI 테스트
    try:
        from pyftdi.spi import SpiController
        spi = SpiController()
        spi.configure(url)
        slave = spi.get_port(cs=0, freq=1000000, mode=0)
        
        # 간단한 SPI 테스트
        test_data = [0x01, 0x02, 0x03, 0x04, 0x05]
        response = slave.exchange(test_data)
        
        results['spi'] = True
        print(f"   SPI: ✅ 연결 성공 (응답: {len(response)}바이트)")
        
        spi.terminate()
        
    except Exception as e:
        results['errors'].append(f"SPI: {str(e)[:50]}...")
        print(f"   SPI: ❌ 실패 - {str(e)[:50]}...")
    
    # GPIO 테스트
    try:
        from pyftdi.gpio import GpioMpsseController
        gpio = GpioMpsseController()
        gpio.configure(url)
        
        # GPIO 설정 테스트
        gpio.set_direction(0x0F, 0x0F)  # 하위 4비트 출력
        gpio.write(0x0F)  # 모든 핀 HIGH
        time.sleep(0.1)
        gpio.write(0x00)  # 모든 핀 LOW
        
        results['gpio'] = True
        print(f"   GPIO: ✅ 연결 성공")
        
        gpio.terminate()
        
    except Exception as e:
        results['errors'].append(f"GPIO: {str(e)[:50]}...")
        print(f"   GPIO: ❌ 실패 - {str(e)[:50]}...")
    
    # UART 테스트 (시리얼 포트 확인)
    try:
        import serial.tools.list_ports
        
        # COM 포트 확인
        ports = serial.tools.list_ports.comports()
        ftdi_ports = [p for p in ports if 'FTDI' in p.description or 'FT232' in p.description or 'USB Serial' in p.description]
        
        if ftdi_ports:
            results['uart'] = True
            print(f"   UART: ✅ COM 포트 발견 ({len(ftdi_ports)}개)")
            for port in ftdi_ports:
                print(f"      {port.device}: {port.description}")
        else:
            print("   UART: ❌ COM 포트 없음")
            
    except Exception as e:
        results['errors'].append(f"UART: {str(e)[:50]}...")
        print(f"   UART: ❌ 확인 실패 - {str(e)[:50]}...")
    
    return results

def comprehensive_channel_test():
    """종합 채널 테스트"""
    print("=" * 80)
    print("FT2232H Channel A & B 종합 점검")
    print("=" * 80)
    
    # 백엔드 확인
    backends = check_usb_backends()
    
    # FTDI 장치 스캔
    devices = scan_ftdi_devices()
    if not devices:
        print("\n❌ FTDI 장치가 없어서 테스트를 계속할 수 없습니다.")
        return
    
    # 채널별 테스트
    channels = {
        'A': [
            'ftdi://0x0403:0x6010/1',
            'ftdi://ftdi:2232h/1',
            'ftdi:///1'
        ],
        'B': [
            'ftdi://0x0403:0x6010/2',
            'ftdi://ftdi:2232h/2',
            'ftdi:///2'
        ]
    }
    
    results = {}
    
    for channel, urls in channels.items():
        print(f"\n{'='*50}")
        print(f"Channel {channel} 테스트")
        print(f"{'='*50}")
        
        channel_results = {
            'connected': False,
            'working_url': None,
            'functions': {'spi': False, 'gpio': False, 'uart': False},
            'errors': []
        }
        
        # 여러 URL로 연결 시도
        for url in urls:
            print(f"\n🔗 URL 시도: {url}")
            
            try:
                # 기본 연결 테스트
                from pyftdi.ftdi import Ftdi
                # URL 유효성 확인
                test_result = test_channel_connection(channel, url)
                
                if test_result['spi'] or test_result['gpio']:
                    channel_results['connected'] = True
                    channel_results['working_url'] = url
                    channel_results['functions'].update({
                        'spi': test_result['spi'],
                        'gpio': test_result['gpio'],
                        'uart': test_result['uart']
                    })
                    print(f"   ✅ Channel {channel} 연결 성공!")
                    break
                else:
                    channel_results['errors'].extend(test_result['errors'])
                    
            except Exception as e:
                error_msg = str(e)[:50]
                channel_results['errors'].append(f"URL {url}: {error_msg}...")
                print(f"   ❌ 연결 실패: {error_msg}...")
        
        results[channel] = channel_results
    
    return results

def generate_report(results: Dict):
    """결과 리포트 생성"""
    print(f"\n{'='*80}")
    print("📊 종합 점검 결과 리포트")
    print(f"{'='*80}")
    
    for channel, data in results.items():
        print(f"\n🔷 Channel {channel}:")
        
        if data['connected']:
            print(f"   상태: ✅ 연결됨")
            print(f"   작동 URL: {data['working_url']}")
            print(f"   기능:")
            print(f"      SPI:  {'✅' if data['functions']['spi'] else '❌'}")
            print(f"      GPIO: {'✅' if data['functions']['gpio'] else '❌'}")
            print(f"      UART: {'✅' if data['functions']['uart'] else '❌'}")
        else:
            print(f"   상태: ❌ 연결 실패")
            if data['errors']:
                print(f"   오류:")
                for error in data['errors'][:3]:  # 최대 3개만 표시
                    print(f"      • {error}")
    
    print(f"\n💡 권장사항:")
    
    # Channel A 분석
    if results['A']['connected']:
        functions_a = results['A']['functions']
        if functions_a['spi'] and functions_a['gpio']:
            print("   • Channel A: SPI + GPIO 통합 사용 권장")
        elif functions_a['spi']:
            print("   • Channel A: SPI 전용 사용")
        elif functions_a['gpio']:
            print("   • Channel A: GPIO 전용 사용")
    else:
        print("   • Channel A: 연결 문제 해결 필요")
    
    # Channel B 분석
    if results['B']['connected']:
        functions_b = results['B']['functions']
        if functions_b['uart']:
            print("   • Channel B: UART 사용 가능 (Arduino IDE 호환)")
        if functions_b['spi'] or functions_b['gpio']:
            print("   • Channel B: SPI/GPIO 사용 가능 (백업 채널)")
    else:
        print("   • Channel B: UART 전용으로 설정 권장 (FTDI VCP 드라이버)")
    
    # 전체 권장사항
    a_connected = results['A']['connected']
    b_connected = results['B']['connected']
    
    if a_connected and b_connected:
        print("\n🎯 최적 구성:")
        print("   • Channel A: SPI/GPIO (현재 작업)")
        print("   • Channel B: UART (Arduino IDE)")
        print("   • 두 채널 독립적 사용 가능")
    elif a_connected:
        print("\n🎯 현재 구성:")
        print("   • Channel A만 사용 가능")
        print("   • SPI/GPIO 작업 가능")
        print("   • UART 필요시 드라이버 변경 고려")
    else:
        print("\n⚠️ 문제 상황:")
        print("   • 두 채널 모두 연결 문제")
        print("   • 드라이버 재설치 필요")

def show_troubleshooting():
    """문제 해결 가이드"""
    print(f"\n{'='*80}")
    print("🔧 문제 해결 가이드")
    print(f"{'='*80}")
    
    print("\n1. Channel A 문제:")
    print("   • SPI/GPIO 연결 실패시 → libusb0/libusbK 드라이버 확인")
    print("   • 'No such FTDI port' 오류 → URL 형식 변경")
    print("   • 'NoneType' 오류 → 드라이버 호환성 문제")
    
    print("\n2. Channel B 문제:")
    print("   • UART 연결 실패시 → FTDI VCP 드라이버 설치")
    print("   • COM 포트 없음 → 장치 관리자에서 확인")
    print("   • SPI/GPIO 연결 실패시 → Channel A 사용 권장")
    
    print("\n3. 전체 해결 방법:")
    print("   • Zadig로 드라이버 선택적 변경")
    print("   • 장치 제거 후 재연결")
    print("   • USB 케이블 및 포트 확인")
    print("   • 다른 프로그램에서 장치 사용 중인지 확인")

def main():
    print("FT2232H Channel A & B 종합 점검")
    
    # 바로 전체 점검 실행
    print("전체 점검을 실행합니다...")
    results = comprehensive_channel_test()
    if results:
        generate_report(results)
        show_troubleshooting()

if __name__ == "__main__":
    main()