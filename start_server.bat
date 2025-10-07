@echo off
echo Ativando ambiente virtual...
call .\venv\Scripts\activate.bat

echo.
echo Ambiente virtual ativado!
echo Iniciando servidor Django...
echo.

python manage.py runserver

pause

