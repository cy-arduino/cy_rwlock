@echo off
python -m pip install .
IF ERRORLEVEL 1 (
    echo Failed to install this package: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

pushd %~dp0

python -m coverage run test.py
IF ERRORLEVEL 1 (
    echo Failed to test this package: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

python -m coverage report -m

popd
