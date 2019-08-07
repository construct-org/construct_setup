@echo off

set THIS=%~dp0
set OLD_PATH=%PATH%
set OLD_PYTHONPATH=%PYTHONPATH%
set PATH=%THIS%\latest\bin;%THIS%\latest\python\Scripts;%PATH%
set PYTHONPATH=%THIS%\latest\lib;%PYTHONPATH%


call %THIS%\latest\bin\construct.bat %*


set PATH=%OLD_PATH%
set PYTHONPATH=%OLD_PYTHONPATH%
set OLD_PATH=
set OLD_PYTHONPATH=
set THIS=
