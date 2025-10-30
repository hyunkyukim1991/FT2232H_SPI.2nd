# FT2232H Multi-Protocol Register Controller

## 🚀 개요

Excel 파일에서 레지스터 정보를 읽어와 트리 구조로 표시하고, FT2232H를 통한 **멀티 프로토콜 통신**(SPI/I2C/UART)으로 레지스터를 제어하는 전문적인 도구입니다.

## ✨ 주요 기능

### 🎯 레지스터 관리
- **Excel 기반 레지스터 정의**: Excel 파일에서 레지스터 구조 자동 파싱
- **트리 뷰어**: 계층적 레지스터 구조 표시
- **32비트 레지스터 제어**: 개별 비트 및 필드 단위 제어
- **시뮬레이션 모드**: 하드웨어 없이 소프트웨어 기능 테스트

### 📡 멀티 프로토콜 지원
- **SPI**: Mode 0-3 (CPOL/CPHA 조합) 지원
- **I2C**: Standard/Fast/Fast Plus/High Speed 모드
- **UART**: 다양한 데이터 포맷 (8N1, 8E1, 8O1, 7E1, 7O1)

### 🔧 고급 기능
- **Setup ComboBox**: 프로토콜별 세부 설정
- **HTML 포맷 의미 표시**: 레지스터 필드 설명 HTML 포맷팅
- **연결 가이드**: Help 메뉴의 종합적인 하드웨어/드라이버 설치 가이드

## 🔌 하드웨어 연결

### SPI 연결
```
FT2232H    <->    Target Device
────────────────────────────────
ADBUS0     <->    SCK  (Serial Clock)
ADBUS1     <->    MOSI (Master Out Slave In)
ADBUS2     <->    MISO (Master In Slave Out)
ADBUS3     <->    CS   (Chip Select)
GND        <->    GND
```

### I2C 연결
```
FT2232H    <->    Target Device
────────────────────────────────
ADBUS0     <->    SCL  (Serial Clock Line)
ADBUS1     <->    SDA  (Serial Data Line)
ADBUS2     <->    SDA  (Serial Data Line - bidirectional)
VCC        <->    VCC  (with 4.7kΩ pull-up resistors)
GND        <->    GND
```

### UART 연결
```
FT2232H    <->    Target Device
────────────────────────────────
ADBUS0     <->    TXD  (Transmit Data)
ADBUS1     <->    RXD  (Receive Data)
ADBUS2     <->    RTS  (Request to Send - 선택)
ADBUS3     <->    CTS  (Clear to Send - 선택)
GND        <->    GND
```

## 💻 소프트웨어 설치

### 필수 요구사항
```bash
pip install PySide6 pandas openpyxl pyftdi
```

### 드라이버 설치

#### Windows
1. **FTDI D2XX 드라이버**: https://ftdichip.com/drivers/d2xx-drivers/
2. **VCP 드라이버** (UART 사용 시): 동일 사이트에서 다운로드

#### Linux
```bash
sudo python -m pyftdi.udev
sudo usermod -a -G dialout $USER
```

#### macOS
```bash
brew install libusb
```

## 🎮 사용 방법

### 1. 애플리케이션 실행
```bash
python Register_Controller.py
```

### 2. Excel 파일 로드
- **File → Open Excel File** 또는 `Ctrl+O`
- 레지스터 정의가 포함된 Excel 파일 선택

### 3. 프로토콜 설정
1. **Protocol 선택**: SPI/I2C/UART 중 선택
2. **Setup 설정**: 프로토콜별 세부 옵션 설정
3. **FTDI URL 설정**: 기본값 `ftdi://ftdi:2232h/1`
4. **주파수/보드레이트 설정**: 통신 속도 설정

### 4. 장치 연결
- **Connect**: 실제 FT2232H 하드웨어 연결
- **Simulate Connection**: 시뮬레이션 모드 (하드웨어 없이 테스트)

### 5. 레지스터 제어
- **트리에서 레지스터 선택**: 좌측 트리뷰에서 레지스터 클릭
- **비트 조작**: 32개 비트 버튼으로 개별 비트 제어
- **16진수 값 입력**: SpinBox에서 직접 값 입력
- **Read/Write**: 실제 하드웨어 또는 시뮬레이션에서 데이터 읽기/쓰기

## ⚙️ 프로토콜별 설정

### SPI 모드
- **Mode 0**: CPOL=0, CPHA=0 (기본값)
- **Mode 1**: CPOL=0, CPHA=1
- **Mode 2**: CPOL=1, CPHA=0
- **Mode 3**: CPOL=1, CPHA=1
- **주파수 범위**: 1Hz ~ 30MHz

### I2C 모드
- **Standard Mode**: 100kHz
- **Fast Mode**: 400kHz
- **Fast Mode Plus**: 1MHz
- **High Speed Mode**: 3.4MHz

### UART 모드
- **8N1**: 8 data bits, No parity, 1 stop bit (기본값)
- **8E1**: 8 data bits, Even parity, 1 stop bit
- **8O1**: 8 data bits, Odd parity, 1 stop bit
- **7E1**: 7 data bits, Even parity, 1 stop bit
- **7O1**: 7 data bits, Odd parity, 1 stop bit
- **보드레이트**: 300 ~ 3,000,000 bps

## 📖 도움말

애플리케이션 내 **Help → Protocol Connection Guide** (F1)에서 상세한 연결 가이드를 확인할 수 있습니다:

- 하드웨어 연결 다이어그램
- 운영체제별 드라이버 설치 방법
- 프로토콜별 설정 옵션
- 문제 해결 가이드
- 핀 배치 및 신호 설명

## 🔧 문제 해결

### 연결 실패
1. FT2232H USB 연결 상태 확인
2. 장치 관리자에서 FTDI 장치 인식 확인
3. 다른 프로그램의 장치 사용 여부 확인
4. FTDI URL 형식 확인 (`ftdi://ftdi:2232h/1` 또는 `/2`)

### 통신 오류
1. 하드웨어 배선 재확인 (특히 GND 연결)
2. 프로토콜 설정이 대상 디바이스와 일치하는지 확인
3. 통신 속도를 낮춰서 테스트
4. 시뮬레이션 모드로 소프트웨어 기능 확인

### 드라이버 문제
- **Windows**: FTDI CDM 드라이버 재설치
- **Linux**: udev 규칙 및 사용자 권한 확인
- **macOS**: libusb 설치 상태 확인

## 🎯 Excel 파일 형식

레지스터 정의 Excel 파일은 다음 구조를 따라야 합니다:

```
| Addr | Bit  | Name    | Default | Description |
|------|------|---------|---------|-------------|
| 0x00 | 15:0 | RESET   | 0       | Reset Reg   |
| 0x01 | 15   | EN_VCM  | 0       | Enable VCM  |
| 0x01 | 14   | EN_TX   | 0       | Enable TX   |
```

- **Addr**: 레지스터 주소 (16진수)
- **Bit**: 비트 범위 (예: 15:0, 7, 3:0)
- **Name**: 필드 이름
- **Default**: 기본값
- **Description**: 설명

## 🚀 확장 가능성

- **다중 슬레이브 지원**: CS 핀 추가로 여러 장치 제어
- **스크립트 자동화**: Python 스크립트로 반복 작업 자동화
- **로그 분석**: 통신 내역 분석 및 디버깅
- **커스텀 프로토콜**: 특수 통신 프로토콜 추가
- **실시간 모니터링**: 센서 데이터 실시간 수집

## 📄 라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.