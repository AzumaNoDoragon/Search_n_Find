@echo off
:: Verifica se o Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python não está instalado. Por favor, instale Python primeiro.
    exit /b 1
)

:: Instala as bibliotecas listadas em requirements.txt
pip install -r requirements.txt

playwright install

echo Bibliotecas instaladas com sucesso.
echo.
echo Depois da instalacao das bibliotecas podesse rodar diretamente o 'run_script.vbs'
echo.

:: Pergunta ao usuário se deseja rodar outro script .cmd
set /p user_input="Deseja rodar o outro script? (y/n): "

if /i "%user_input%"=="y" (
    call runhidden.cmd
) else (
    echo O outro script nao sera executado.
)

pause
exit