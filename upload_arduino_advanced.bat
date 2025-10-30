@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Arduino 업로드 스크립트 (고급 버전)
echo ==========================================

:: Arduino CLI 경로 설정
set ARDUINO_CLI="C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"

:: 프로젝트 설정
set SKETCH_PATH=Arduino_UNO_SPI_Clean

echo.
echo [단계 1] 연결된 보드 확인 중...
%ARDUINO_CLI% board list

echo.
echo 사용 가능한 보드 타입:
echo 1. Arduino UNO (arduino:avr:uno)
echo 2. Arduino Nano (arduino:avr:nano)  
echo 3. Arduino Mega (arduino:avr:mega)
echo 4. 수동 입력

set /p BOARD_CHOICE="보드 타입을 선택하세요 (1-4): "

if "%BOARD_CHOICE%"=="1" (
    set BOARD_FQBN=arduino:avr:uno
    set BOARD_NAME=Arduino UNO
) else if "%BOARD_CHOICE%"=="2" (
    set BOARD_FQBN=arduino:avr:nano
    set BOARD_NAME=Arduino Nano
) else if "%BOARD_CHOICE%"=="3" (
    set BOARD_FQBN=arduino:avr:mega
    set BOARD_NAME=Arduino Mega
) else if "%BOARD_CHOICE%"=="4" (
    set /p BOARD_FQBN="보드 FQBN을 입력하세요 (예: arduino:avr:uno): "
    set BOARD_NAME=사용자 정의
) else (
    echo 잘못된 선택입니다. 기본값 Arduino UNO를 사용합니다.
    set BOARD_FQBN=arduino:avr:uno
    set BOARD_NAME=Arduino UNO
)

echo.
set /p PORT="포트를 입력하세요 (예: COM4): "

if "%PORT%"=="" (
    echo 포트가 입력되지 않았습니다. 기본값 COM4를 사용합니다.
    set PORT=COM4
)

echo.
echo [단계 2] 설정 확인
echo   - 스케치: %SKETCH_PATH%
echo   - 보드: !BOARD_NAME! (!BOARD_FQBN!)
echo   - 포트: %PORT%
echo.

set /p CONFIRM="계속 진행하시겠습니까? (Y/N): "
if /i not "%CONFIRM%"=="Y" if /i not "%CONFIRM%"=="y" (
    echo 작업이 취소되었습니다.
    pause
    exit /b 0
)

echo.
echo [단계 3] 스케치 컴파일 중...
%ARDUINO_CLI% compile --fqbn !BOARD_FQBN! %SKETCH_PATH% --verbose

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ 컴파일 실패!
    echo 오류를 확인하고 다시 시도해주세요.
    pause
    exit /b 1
)

echo.
echo ✅ 컴파일 성공!

echo.
echo [단계 4] !BOARD_NAME!에 업로드 중 (포트: %PORT%)...
%ARDUINO_CLI% upload -p %PORT% --fqbn !BOARD_FQBN! %SKETCH_PATH% --verbose

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ 업로드 실패!
    echo.
    echo 문제 해결 가이드:
    echo 1. 포트 확인: 다른 포트 번호를 시도해보세요 (COM3, COM5, COM6 등)
    echo 2. 프로그램 종료: Arduino IDE, 시리얼 모니터, Python 스크립트 등을 종료
    echo 3. 하드웨어 확인: USB 케이블 연결 상태와 Arduino 전원 확인
    echo 4. 드라이버 확인: Arduino 드라이버가 올바르게 설치되었는지 확인
    echo 5. 보드 타입: 올바른 보드 타입을 선택했는지 확인
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✅ 업로드 완료!
echo ==========================================
echo.
echo 📋 업로드된 설정:
echo   - 보드: !BOARD_NAME!
echo   - 포트: %PORT%
echo   - 데이터 길이: 2바이트 (수정 가능)
echo   - 시리얼 속도: 115200 baud
echo.
echo 🔧 다음 단계:
echo   1. 시리얼 모니터 열기 (115200 baud)
echo   2. "SPI Slave ready. Data length: 2 bytes" 메시지 확인
echo   3. Python에서 set_data_length(2) 설정
echo   4. SPI 통신 테스트
echo.
echo 💡 팁: 데이터 길이를 변경하려면 Arduino 코드의
echo     DATA_LENGTH_BYTES 값을 수정하고 다시 업로드하세요.
echo.

pause