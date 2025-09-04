# zmq_utils
Utils for logging and monitoring ZeroMQ


## Local Installation

Create your virtual environment:
```bash
python3 -m venv venv_zmqu
```

Activate your venv:
```bash
source venv_zmqu/bin/activate   # Linux / macOS
# OR
venv_zmqu\Scripts\activate      # Windows (cmd)
```

Install package:

```bash
pip install -e .
# OR
pip install -e .[test]  # For Running tests
```


## Running

```bash
zmq-echo
```


## Running test
```bash
pytest -s tests/test_broker_logger.py
```