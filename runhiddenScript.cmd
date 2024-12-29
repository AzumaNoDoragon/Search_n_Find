@echo off
:start
python searchScript.py
if %errorlevel% gtr 0 goto start
