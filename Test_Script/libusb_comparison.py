#!/usr/bin/env python3
"""
libusb0 vs libusb1 차이점 및 성능 비교 스크립트
"""

import time
import sys

def compare_usb_backends():
    """USB 백엔드 비교 분석"""
    print("=" * 60)
    print("libusb0 vs libusb1 비교 분석")
    print("=" * 60)
    
    # 백엔드 가용성 확인
    backends_info = {}
    
    print("\n1. 백엔드 가용성 확인:")
    
    # libusb1 확인
    try:
        import usb.backend.libusb1
        backend1 = usb.backend.libusb1.get_backend()
        if backend1:
            backends_info['libusb1'] = {
                'available': True,
                'backend': backend1,
                'version': getattr(backend1, 'lib', {}).get('libusb_get_version', 'Unknown')
            }
            print("✅ libusb1: 사용 가능")
        else:
            backends_info['libusb1'] = {'available': False}
            print("❌ libusb1: 백엔드 없음")
    except Exception as e:
        backends_info['libusb1'] = {'available': False, 'error': str(e)}
        print(f"❌ libusb1: 오류 - {e}")
    
    # libusb0 확인
    try:
        import usb.backend.libusb0
        backend0 = usb.backend.libusb0.get_backend()
        if backend0:
            backends_info['libusb0'] = {
                'available': True,
                'backend': backend0
            }
            print("✅ libusb0: 사용 가능")
        else:
            backends_info['libusb0'] = {'available': False}
            print("❌ libusb0: 백엔드 없음")
    except Exception as e:
        backends_info['libusb0'] = {'available': False, 'error': str(e)}
        print(f"❌ libusb0: 오류 - {e}")
    
    print("\n2. 기능 비교:")
    
    features = {
        'libusb0': {
            'API 스타일': '동기식 중심',
            '멀티스레딩': '제한적',
            '핫플러그': '미지원',
            '성능': '기본적',
            '메모리 관리': '단순',
            'Windows 드라이버': 'libusb0.sys',
            'FTDI 지원': '기본적',
            'pyftdi 호환성': '부분적'
        },
        'libusb1': {
            'API 스타일': '비동기 + 동기',
            '멀티스레딩': '완전 지원',
            '핫플러그': '지원',
            '성능': '향상됨',
            '메모리 관리': '고급',
            'Windows 드라이버': 'libusbK.sys/WinUSB',
            'FTDI 지원': '완전 지원',
            'pyftdi 호환성': '완전'
        }
    }
    
    for backend_name, feature_dict in features.items():
        available = backends_info.get(backend_name, {}).get('available', False)
        status = "✅ 사용 가능" if available else "❌ 사용 불가"
        
        print(f"\n📚 {backend_name.upper()} ({status}):")
        for feature, value in feature_dict.items():
            print(f"   • {feature}: {value}")
    
    print("\n3. 권장사항:")
    
    libusb1_available = backends_info.get('libusb1', {}).get('available', False)
    libusb0_available = backends_info.get('libusb0', {}).get('available', False)
    
    if libusb1_available:
        print("🎯 권장: libusb1 사용")
        print("   • 최신 기능과 향상된 성능")
        print("   • pyftdi와 완전 호환")
        print("   • FT2232H GPIO 완전 지원")
    elif libusb0_available:
        print("⚠️ 현재 상황: libusb0만 사용 가능")
        print("   • 기본적인 기능은 동작")
        print("   • 일부 고급 기능 제한")
        print("   • 업그레이드 권장")
    else:
        print("❌ 심각: USB 백엔드 없음")
        print("   • Zadig로 드라이버 설치 필요")
    
    print("\n4. 드라이버 업그레이드 가이드:")
    print("   1. Zadig 다운로드: https://zadig.akeo.ie/")
    print("   2. 관리자 권한으로 실행")
    print("   3. Options → List All Devices")
    print("   4. FT2232H 선택")
    print("   5. libusbK (v3.x.x.x) 선택")
    print("   6. Replace Driver 클릭")
    print("   7. 재부팅")
    
    return backends_info

def performance_test():
    """간단한 성능 테스트"""
    print("\n" + "=" * 60)
    print("USB 백엔드 성능 테스트")
    print("=" * 60)
    
    try:
        from pyftdi.ftdi import Ftdi
        
        # 장치 검색 성능 테스트
        test_count = 5
        
        print(f"\n장치 검색 성능 테스트 ({test_count}회):")
        
        times = []
        for i in range(test_count):
            start_time = time.time()
            try:
                devices = Ftdi.list_devices()
                end_time = time.time()
                elapsed = end_time - start_time
                times.append(elapsed)
                print(f"  테스트 {i+1}: {elapsed:.3f}초 ({len(devices)}개 장치)")
            except Exception as e:
                print(f"  테스트 {i+1}: 실패 - {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            print(f"\n평균 검색 시간: {avg_time:.3f}초")
            
            if avg_time < 0.1:
                print("✅ 성능: 우수")
            elif avg_time < 0.5:
                print("✅ 성능: 양호")
            else:
                print("⚠️ 성능: 개선 필요 (드라이버 업그레이드 권장)")
        
    except ImportError:
        print("❌ pyftdi 없음")

def main():
    print("libusb0 vs libusb1 비교 분석 도구")
    print("1. 백엔드 비교 분석")
    print("2. 성능 테스트")
    print("3. 전체 실행")
    
    choice = input("선택하세요 (1-3): ").strip()
    
    if choice == '1':
        compare_usb_backends()
    elif choice == '2':
        performance_test()
    else:
        compare_usb_backends()
        performance_test()

if __name__ == "__main__":
    main()