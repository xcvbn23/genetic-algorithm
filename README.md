# Genetic Algorithm

### Examples

- [six_hump_camelback](./examples/six_hump_camelback.py)
- [sum](./examples/sum.py)
- [wifi_optimisation](./examples/wifi_optimisation.py)

#### Running examples

    python -m examples.<EXAMPLE_NAME>

For example;

    python -m example.sum

## Development

### Create venv in venv directory

```shell
python -m venv venv
```

### Activate venv

#### Windows

##### In cmd.exe

```
venv\Scripts\activate.bat
```

##### In PowerShell

```
venv\Scripts\Activate.ps1
```

#### In GNU/Linux, MacOS and BSD variants

```
source venv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Testing

```
pytest -vvv -rP
```