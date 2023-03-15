# easy-dlc-analyzer

## Install

```
edm env create easy-dlc-analyzer --version 3.8
edm install -e easy-dlc-analyzer chaco opencv_python pandas tables traits traitsui  
edm run -e easy-dlc-analyzer -- pip install build
edm run -e easy-dlc-analyzer -- python -m build
edm run -e easy-dlc-analyzer -- pip install dist\easy_dlc_analyzer-0.0.0-py3-none-any.whl
```
