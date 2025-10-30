@echo off
echo ======================================
echo Arduino UNO SPI Clean 업로드 스크립트
echo ======================================

:: Arduino CLI 경로 설정
set ARDUINO_CLI="C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"

:: 프로젝트 설정
set SKETCH_PATH=Arduino_UNO_SPI_Clean
set BOARD_FQBN=arduino:avr:uno
set PORT=COM4

echo.
echo [1단계] 연결된 보드 확인 중...
%ARDUINO_CLI% board list

echo.
echo [2단계] 스케치 컴파일 중...
%ARDUINO_CLI% compile --fqbn %BOARD_FQBN% %SKETCH_PATH%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ 컴파일 실패!
    pause
    exit /b 1
)

echo.
echo ✅ 컴파일 성공!

echo.
echo [3단계] Arduino UNO에 업로드 중 (포트: %PORT%)...
%ARDUINO_CLI% upload -p %PORT% --fqbn %BOARD_FQBN% %SKETCH_PATH%

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ 업로드 실패!
    echo.
    echo 가능한 해결책:
    echo - 다른 프로그램이 %PORT% 포트를 사용 중인지 확인
    echo - Arduino IDE 시리얼 모니터가 열려있다면 닫기
    echo - USB 케이블 연결 상태 확인
    echo - 포트 번호가 올바른지 확인 (COM4, COM6 등)
    pause
    exit /b 1
)

echo.
echo ✅ 업로드 완료!
echo.
echo 📋 업로드된 설정:
echo   - 보드: Arduino UNO
echo   - 포트: %PORT%
echo   - 데이터 길이: 2바이트
echo   - 시리얼 속도: 115200 baud
echo.
echo 🔧 다음 단계:
echo   1. 시리얼 모니터를 115200 baud로 열어서 "SPI Slave ready" 메시지 확인
echo   2. Python 코드에서 set_data_length(2) 설정
echo   3. SPI 통신 테스트 시작
echo.

pause