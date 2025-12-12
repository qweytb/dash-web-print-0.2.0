@echo off
chcp 65001 >nul
:: ==========================================================
::  一键把 Granian 注册成 Windows 服务（nssm 版）
::  成功启动后访问 http://127.0.0.1:8050
::  必须以管理员身份运行
:: ==========================================================

:: ==========  用户只需改这几行  ==========
set SVC_NAME=GranianDash
set WORK_DIR=D:\python\web-dash\web-拖拽-打印票据0.2.0
set PY_EXE=D:\miniforge3\envs\drag_and_drop_2.0_env\Scripts\granian.exe
set MODULE=app:app.server
set PORT=8050
set WORKERS=4
:: ========================================

:: 取得脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "NSSM=%SCRIPT_DIR%nssm.exe"
if not exist "%NSSM%" (
    echo [ERROR] 请将 nssm.exe 放到本脚本同级目录！
    echo 当前检测路径：%NSSM%
    pause & exit /b 1
)

:: 如果存在旧服务，先停掉删掉
sc query %SVC_NAME% >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] 停止并删除已存在的服务...
    net stop %SVC_NAME% 2>nul
    "%NSSM%" remove %SVC_NAME% confirm
)

:: 创建日志目录
if not exist "%WORK_DIR%\logs" mkdir "%WORK_DIR%\logs"

echo [INFO] 注册服务：%SVC_NAME%
"%NSSM%" install %SVC_NAME% "%PY_EXE%" >nul
"%NSSM%" set %SVC_NAME% AppParameters "--interface wsgi --host 0.0.0.0 --port %PORT% --workers %WORKERS% %MODULE%" >nul
"%NSSM%" set %SVC_NAME% AppDirectory  "%WORK_DIR%" >nul
"%NSSM%" set %SVC_NAME% AppEnvironmentExtra "PYTHONPATH=%WORK_DIR%" >nul
"%NSSM%" set %SVC_NAME% DisplayName   "Granian Dash App" >nul
"%NSSM%" set %SVC_NAME% Description   "Granian WSGI Server for Dash on Windows" >nul
"%NSSM%" set %SVC_NAME% Start         SERVICE_AUTO_START >nul
"%NSSM%" set %SVC_NAME% AppStdout     "%WORK_DIR%\logs\service_out.log" >nul
"%NSSM%" set %SVC_NAME% AppStderr      "%WORK_DIR%\logs\service_err.log" >nul
"%NSSM%" set %SVC_NAME% AppRotateFiles 1 >nul
"%NSSM%" set %SVC_NAME% AppRotateBytes 10485760 >nul

echo [INFO] 启动服务...
net start %SVC_NAME%
if %errorlevel% equ 0 (
    echo [OK] 服务启动成功！浏览器访问 http://127.0.0.1:%PORT% 验证
) else (
    echo [ERROR] 服务启动失败，请查看 %WORK_DIR%\logs\service_err.log
)
pause