@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo Arduino 데이터 길이 설정 및 업로드
echo ==========================================

:: Arduino CLI 경로 설정
set ARDUINO_CLI="C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
set SKETCH_PATH=Arduino_UNO_SPI_Clean
set BOARD_FQBN=arduino:avr:uno
set INO_FILE=%SKETCH_PATH%\Arduino_UNO_SPI_Clean.ino

echo.
echo 현재 지원되는 데이터 길이:
echo 1. 1바이트 (8비트)   - 최대값: 0xFF (255)
echo 2. 2바이트 (16비트)  - 최대값: 0xFFFF (65535)  [현재 설정]
echo 3. 4바이트 (32비트)  - 최대값: 0xFFFFFFFF
echo 4. 8바이트 (64비트)  - 최대값: 0xFFFFFFFFFFFFFFFF
echo.

set /p DATA_CHOICE="데이터 길이를 선택하세요 (1-4): "

if "%DATA_CHOICE%"=="1" (
    set DATA_LENGTH=1
    set DATA_DESC=1바이트 (8비트)
) else if "%DATA_CHOICE%"=="2" (
    set DATA_LENGTH=2  
    set DATA_DESC=2바이트 (16비트)
) else if "%DATA_CHOICE%"=="3" (
    set DATA_LENGTH=4
    set DATA_DESC=4바이트 (32비트)
) else if "%DATA_CHOICE%"=="4" (
    set DATA_LENGTH=8
    set DATA_DESC=8바이트 (64비트)
) else (
    echo 잘못된 선택입니다. 기본값 2바이트를 사용합니다.
    set DATA_LENGTH=2
    set DATA_DESC=2바이트 (16비트)
)

echo.
echo 선택된 데이터 길이: !DATA_DESC!

:: Arduino 코드에서 DATA_LENGTH_BYTES 값 변경
echo.
echo [단계 1] Arduino 코드 수정 중...

:: 백업 파일 생성
copy "%INO_FILE%" "%INO_FILE%.backup" >nul

:: PowerShell을 사용하여 파일 내용 변경
powershell -Command "(Get-Content '%INO_FILE%') -replace '#define DATA_LENGTH_BYTES \d+', '#define DATA_LENGTH_BYTES !DATA_LENGTH!' | Set-Content '%INO_FILE%'"

if %ERRORLEVEL% neq 0 (
    echo ❌ 파일 수정 실패!
    copy "%INO_FILE%.backup" "%INO_FILE%" >nul
    del "%INO_FILE%.backup" >nul
    pause
    exit /b 1
)

echo ✅ 데이터 길이가 !DATA_LENGTH!바이트로 설정되었습니다.

set /p PORT="포트를 입력하세요 (기본값: COM4): "
if "%PORT%"=="" set PORT=COM4

echo.
echo [단계 2] 컴파일 중...
%ARDUINO_CLI% compile --fqbn %BOARD_FQBN% %SKETCH_PATH%

if %ERRORLEVEL% neq 0 (
    echo ❌ 컴파일 실패!
    echo 백업 파일을 복원합니다...
    copy "%INO_FILE%.backup" "%INO_FILE%" >nul
    del "%INO_FILE%.backup" >nul
    pause
    exit /b 1
)

echo ✅ 컴파일 성공!

echo.
echo [단계 3] %PORT%로 업로드 중...
%ARDUINO_CLI% upload -p %PORT% --fqbn %BOARD_FQBN% %SKETCH_PATH%

if %ERRORLEVEL% neq 0 (
    echo ❌ 업로드 실패!
    echo 백업 파일을 복원하시겠습니까? (Y/N)
    set /p RESTORE=
    if /i "!RESTORE!"=="Y" (
        copy "%INO_FILE%.backup" "%INO_FILE%" >nul
        echo 백업 파일이 복원되었습니다.
    )
    del "%INO_FILE%.backup" >nul
    pause
    exit /b 1
)

:: 백업 파일 삭제
del "%INO_FILE%.backup" >nul

echo.
echo ==========================================
echo ✅ 업로드 완료!
echo ==========================================
echo.
echo 📋 설정된 구성:
echo   - 데이터 길이: !DATA_DESC!
echo   - 포트: %PORT%
echo   - 시리얼 속도: 115200 baud
echo.
echo 🔧 Python 코드 설정:
echo   Python에서 다음과 같이 설정하세요:
echo   set_data_length(!DATA_LENGTH!)
echo.
echo 💡 시리얼 모니터에서 다음 메시지를 확인하세요:
echo   "SPI Slave ready. Data length: !DATA_LENGTH! bytes"
echo.

pause