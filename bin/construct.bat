@echo off

set THIS=%~dp0
set OLD_PATH=%PATH%
set OLD_PYTHONPATH=%PYTHONPATH%
set PATH=%THIS%\current\bin;%THIS%\current\python\Scripts;%PATH%
set PYTHONPATH=%THIS%\current\lib;%PYTHONPATH%


call %THIS%\current\bin\construct.bat %*


set PATH=%OLD_PATH%
set PYTHONPATH=%OLD_PYTHONPATH%
set OLD_PATH=
set OLD_PYTHONPATH=
set THIS=
