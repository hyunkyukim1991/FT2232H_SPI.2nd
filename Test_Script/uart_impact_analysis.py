#!/usr/bin/env python3
"""
FT2232H 드라이버 변경 시 UART 영향 분석 및 해결 방안
"""

def analyze_driver_impact():
    """드라이버 변경이 UART에 미치는 영향 분석"""
    print("=" * 70)
    print("FT2232H 드라이버 변경 시 UART 영향 분석")
    print("=" * 70)
    
    print("\n🔍 현재 상황:")
    print("• FT2232H는 2개의 채널(A, B)을 가짐")
    print("• 각 채널은 독립적으로 드라이버 할당 가능")
    print("• UART는 FTDI VCP 드라이버 필요")
    print("• GPIO/SPI는 libusbK 드라이버 필요")
    
    print("\n📊 드라이버별 기능 비교:")
    
    drivers = {
        "FTDI VCP (Virtual COM Port)": {
            "UART/시리얼": "✅ 완전 지원",
            "COM 포트": "✅ 생성됨",
            "Arduino IDE": "✅ 사용 가능",
            "SPI/GPIO": "❌ 제한적",
            "pyftdi": "❌ 호환성 문제"
        },
        "libusbK": {
            "UART/시리얼": "❌ 지원 안함",
            "COM 포트": "❌ 생성 안됨",
            "Arduino IDE": "❌ 사용 불가",
            "SPI/GPIO": "✅ 완전 지원",
            "pyftdi": "✅ 완전 호환"
        },
        "libusb-win32 (libusb0)": {
            "UART/시리얼": "❌ 지원 안함",
            "COM 포트": "❌ 생성 안됨",
            "Arduino IDE": "❌ 사용 불가",
            "SPI/GPIO": "✅ 기본 지원",
            "pyftdi": "✅ 부분 호환"
        }
    }
    
    for driver_name, features in drivers.items():
        print(f"\n🔧 {driver_name}:")
        for feature, support in features.items():
            print(f"   • {feature}: {support}")
    
    print("\n⚠️ 중요한 점:")
    print("• FT2232H에서 libusbK로 변경하면 COM 포트가 사라집니다")
    print("• Arduino IDE에서 해당 포트를 사용할 수 없게 됩니다")
    print("• 시리얼 모니터 기능을 사용할 수 없게 됩니다")

def show_solutions():
    """해결 방안 제시"""
    print("\n" + "=" * 70)
    print("해결 방안 및 대안")
    print("=" * 70)
    
    print("\n🎯 방안 1: 선택적 드라이버 변경 (권장)")
    print("   • Channel A: libusbK (SPI/GPIO용)")
    print("   • Channel B: FTDI VCP (UART용)")
    print("   • 장점: 두 기능 모두 사용 가능")
    print("   • 단점: 설정이 복잡할 수 있음")
    
    print("\n🎯 방안 2: 필요에 따라 드라이버 교체")
    print("   • SPI/GPIO 작업시: libusbK로 변경")
    print("   • Arduino 작업시: FTDI VCP로 복원")
    print("   • 장점: 각 작업에 최적화")
    print("   • 단점: 매번 드라이버 변경 필요")
    
    print("\n🎯 방안 3: 별도 UART 장치 사용")
    print("   • FT2232H: libusbK (SPI/GPIO 전용)")
    print("   • 별도 USB-UART: Arduino 연결용")
    print("   • 장점: 드라이버 충돌 없음")
    print("   • 단점: 추가 하드웨어 필요")
    
    print("\n🎯 방안 4: 현재 상태 유지 (실용적)")
    print("   • libusb0로 SPI/GPIO 사용 (현재 작동 중)")
    print("   • UART는 필요시 VCP 드라이버로 복원")
    print("   • 장점: 현재 상태에서 문제없이 작동")
    print("   • 단점: 최적 성능은 아님")

def show_step_by_step_guide():
    """단계별 가이드"""
    print("\n" + "=" * 70)
    print("단계별 실행 가이드")
    print("=" * 70)
    
    print("\n📋 방안 1 실행 단계 (선택적 드라이버 변경):")
    print("1. 장치 관리자에서 현재 상태 확인")
    print("   • Win+X → 장치 관리자")
    print("   • 'USB Serial Converter A' 및 'B' 확인")
    
    print("\n2. Zadig 다운로드 및 실행")
    print("   • https://zadig.akeo.ie/ 에서 다운로드")
    print("   • 관리자 권한으로 실행")
    
    print("\n3. 고급 옵션 설정")
    print("   • Options → List All Devices 체크")
    print("   • Options → Ignore Hubs or Composite Parents 체크")
    
    print("\n4. Channel A만 변경 (SPI/GPIO용)")
    print("   • 'USB Serial Converter A' 선택")
    print("   • 드라이버를 'libusbK (v3.x.x.x)'로 변경")
    print("   • 'Replace Driver' 클릭")
    
    print("\n5. Channel B는 유지 (UART용)")
    print("   • 'USB Serial Converter B'는 변경하지 않음")
    print("   • FTDI VCP 드라이버 유지")
    
    print("\n6. 결과 확인")
    print("   • Channel A: SPI/GPIO 사용 가능")
    print("   • Channel B: COM 포트로 UART 사용 가능")
    
    print("\n📋 복원 방법 (필요시):")
    print("1. Zadig에서 해당 장치 선택")
    print("2. 드라이버를 'FTDI VCP'로 변경")
    print("3. 또는 장치 제거 후 재연결하여 자동 복원")

def check_current_status():
    """현재 드라이버 상태 확인"""
    print("\n" + "=" * 70)
    print("현재 시스템 상태 확인")
    print("=" * 70)
    
    try:
        from pyftdi.ftdi import Ftdi
        
        print("\n🔍 FTDI 장치 확인:")
        devices = Ftdi.list_devices()
        if devices:
            for i, device in enumerate(devices):
                print(f"   Device {i}: {str(device)[:100]}")
        else:
            print("   FTDI 장치 없음")
        
        print("\n💡 권장사항:")
        print("   • 현재 libusb0로 SPI/GPIO가 작동 중")
        print("   • UART가 필요하지 않다면 현재 상태 유지")
        print("   • UART가 필요하면 Channel B만 VCP로 유지")
        
    except Exception as e:
        print(f"   오류: {e}")
    
    print("\n🔧 Windows COM 포트 확인 방법:")
    print("   1. 장치 관리자 열기 (Win+X → 장치 관리자)")
    print("   2. '포트(COM 및 LPT)' 확장")
    print("   3. 'USB Serial Port (COMx)' 확인")
    print("   4. 있으면 UART 사용 가능, 없으면 libusbK로 변경됨")

def main():
    print("FT2232H 드라이버 변경과 UART 영향 분석")
    print("1. 드라이버별 기능 비교")
    print("2. 해결 방안")
    print("3. 단계별 가이드")
    print("4. 현재 상태 확인")
    print("5. 전체 분석")
    
    choice = input("선택하세요 (1-5): ").strip()
    
    if choice == '1':
        analyze_driver_impact()
    elif choice == '2':
        show_solutions()
    elif choice == '3':
        show_step_by_step_guide()
    elif choice == '4':
        check_current_status()
    else:
        analyze_driver_impact()
        show_solutions()
        show_step_by_step_guide()
        check_current_status()

if __name__ == "__main__":
    main()