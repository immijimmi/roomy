:: Requires pytest~=7.4.0 and coverage~=7.2.7 to be installed
:: This script will run any test files it discovers in the directory and provide a breakdown of code coverage

cd ..
coverage run -m --source=. --omit="test\*,setup.py" pytest -v
coverage report

pause
