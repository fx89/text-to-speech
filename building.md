## Building

If not already installed, install the tools

```
pip install build
```
```
pip install twine
```


To work locally, install the package in editable mode

```
python -m pip install -e .
```

To build the package, use the following command (generates sdist and wheel in the dist directory)

```
python -m build
```

To check for warnings in the dist directory, run
```
twine check dist/*
```

To upload the package, run
```
twine upload dist/*
```
