del /f /q dist
python3 setup.py sdist && twine upload dist/*
