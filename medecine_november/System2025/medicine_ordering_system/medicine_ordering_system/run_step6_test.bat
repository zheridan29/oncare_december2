@echo off
echo ============================================================
echo   Step 6.1: Create Test Payment Intent
echo ============================================================
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.
echo Running test payment intent creation...
echo.
python test_payment_intent_step6.py
echo.
echo ============================================================
pause

