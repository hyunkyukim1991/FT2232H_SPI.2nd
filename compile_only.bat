@echo off
echo ======================================
echo Arduino SPI Clean 컴파일 전용 스크립트
echo ======================================

:: Arduino CLI 경로 설정
set ARDUINO_CLI="C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"

:: 프로젝트 설정
set SKETCH_PATH=Arduino_UNO_SPI_Clean
set BOARD_FQBN=arduino:avr:uno

echo.
echo 스케치 경로: %SKETCH_PATH%
echo 보드 타입: Arduino UNO (%BOARD_FQBN%)
echo.

echo [컴파일 시작]
%ARDUINO_CLI% compile --fqbn %BOARD_FQBN% %SKETCH_PATH% --verbose

if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ 컴파일 실패!
    echo 코드를 확인하고 다시 시도해주세요.
) else (
    echo.
    echo ✅ 컴파일 성공!
    echo 이제 upload_arduino.bat를 실행하여 업로드할 수 있습니다.
)

echo.
pause