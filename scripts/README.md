# Reproducibility scripts

These scripts are provided to enable reproducibility of the ontology
extraction. Python scripts are provided for accessibility of Windows users and
are to be called using:

```bash
python scripts/<path to script>
```

Linux, MacOS and other Unix-like systems users are encouraged to use make. 

```bash
make clean
make all
```

To rebuild the imports call:

```bash
make clean-imports
make imports
```