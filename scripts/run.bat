python -m pip install .
pushd %~dp0
python -m coverage run test.py
python -m coverage report -m
popd
