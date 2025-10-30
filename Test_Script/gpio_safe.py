#!/usr/bin/env python3
"""
FT2232H GPIO 안전한 명령어 스크립트 (libusb0 호환)
"""

import time
import sys

def safe_gpio_connect(channel='A'):
    """안전한 GPIO 연결"""
    try:
        from pyftdi.gpio import GpioMpsseController
        
        # 여러 연결 방법 시도
        urls = [
            f'ftdi://0x0403:0x6010/{1 if channel.upper() == "A" else 2}',
            f'ftdi:///{1 if channel.upper() == "A" else 2}',
        ]
        
        for url in urls:
            try:
                gpio = GpioMpsseController()
                gpio.configure(url, frequency=1000000)
                print(f"✅ Channel {channel.upper()} 연결 성공 ({url})")
                return gpio
            except Exception as e:
                print(f"   시도 실패: {url} - {str(e)[:30]}...")
                continue
        
        print(f"❌ Channel {channel.upper()} 모든 연결 시도 실패")
        return None
        
    except ImportError:
        print("❌ pyftdi 라이브러리 없음")
        return None

def gpio_command(channel, action, value=None):
    """GPIO 명령 실행"""
    print(f"🔧 Channel {channel.upper()} {action} 명령 실행...")
    
    # GPIO 연결
    gpio = safe_gpio_connect(channel)
    if not gpio:
        return False
    
    try:
        # 출력 모드 설정 (읽기 제외)
        if action != 'read':
            gpio.set_direction(0xFF, 0xFF)  # 모든 핀 출력
            print(f"✅ Channel {channel.upper()} 출력 모드 설정")
        
        # 명령 실행
        if action == 'on':
            if value is not None:
                # 특정 핀 ON
                pin = int(value)
                current = gpio.read()
                new_value = current | (1 << pin)
                gpio.write(new_value)
                print(f"✅ 핀 {pin} ON")
            else:
                # 모든 핀 ON
                gpio.write(0xFF)
                print(f"✅ 모든 핀 ON")
        
        elif action == 'off':
            if value is not None:
                # 특정 핀 OFF
                pin = int(value)
                current = gpio.read()
                new_value = current & ~(1 << pin)
                gpio.write(new_value)
                print(f"✅ 핀 {pin} OFF")
            else:
                # 모든 핀 OFF
                gpio.write(0x00)
                print(f"✅ 모든 핀 OFF")
        
        elif action == 'write':
            if value is not None:
                val = int(value, 0)  # 0x, 0b 지원
                gpio.write(val)
                print(f"✅ 출력: 0x{val:02X} (0b{val:08b})")
            else:
                print("❌ write 명령어는 값이 필요합니다")
        
        elif action == 'read':
            val = gpio.read()
            print(f"📥 입력: 0x{val:02X} (0b{val:08b})")
        
        elif action == 'blink':
            # 깜빡임 테스트
            print("깜빡임 테스트 시작...")
            for i in range(5):
                gpio.write(0xFF)
                time.sleep(0.3)
                gpio.write(0x00)
                time.sleep(0.3)
            print("✅ 깜빡임 완료")
        
        elif action == 'pattern':
            # 패턴 테스트
            print("패턴 테스트 시작...")
            # 순차 점등
            for i in range(8):
                gpio.write(1 << i)
                time.sleep(0.2)
            # 모든 핀 OFF
            gpio.write(0x00)
            print("✅ 패턴 완료")
        
        else:
            print(f"❌ 알 수 없는 명령: {action}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 명령 실행 실패: {e}")
        return False
    
    # finally:
    #     try:
    #         gpio.write(0x00)  # 안전을 위해 모든 핀 OFF
    #         gpio.terminate()
    #     except:
    #         pass

def main():
    """메인 함수"""
    if len(sys.argv) < 3:
        print("FT2232H GPIO 간단 명령어")
        print("=" * 40)
        print("사용법:")
        print("  python gpio_safe.py A on         # Channel A 모든 핀 ON")
        print("  python gpio_safe.py A off        # Channel A 모든 핀 OFF")
        print("  python gpio_safe.py A on 0       # Channel A 핀 0 ON")
        print("  python gpio_safe.py A off 1      # Channel A 핀 1 OFF")
        print("  python gpio_safe.py A write 0xFF # Channel A에 0xFF 출력")
        print("  python gpio_safe.py A read       # Channel A 입력 읽기")
        print("  python gpio_safe.py A blink      # Channel A 깜빡임")
        print("  python gpio_safe.py A pattern    # Channel A 패턴 테스트")
        print("  python gpio_safe.py B on 2       # Channel B 핀 2 ON")
        return
    
    channel = sys.argv[1]
    action = sys.argv[2]
    value = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        success = gpio_command(channel, action, value)
        if success:
            print("✅ 명령 완료")
        else:
            print("❌ 명령 실패")
    
    except KeyboardInterrupt:
        print("\n⚠️ 사용자 중단")
    except Exception as e:
        print(f"❌ 오류: {e}")

if __name__ == "__main__":
    main()