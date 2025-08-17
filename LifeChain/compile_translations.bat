@echo off
REM Translation Compilation Script
REM Run this after installing gettext

echo Compiling English translations...
python manage.py compilemessages --locale en

echo.
echo Compiling Urdu translations...
python manage.py compilemessages --locale ur

echo.
echo Compilation complete!
echo Check the locale/*/LC_MESSAGES/ directories for .mo files
pause
