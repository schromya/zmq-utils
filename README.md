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


## Usage

| Command      | Description |
|--------------|-------------|
| `zmq-broker` | Start a ZeroMQ broker that forwards messages and publishes logs. |
| `zmq-logger` | Subscribe to broker logs and print/store them in JSONL format. |

---

### zmq-broker


```bash
zmq-broker push_pull [options]
```

| Options        | Type   | Required | Description |
|----------------|--------|----------|-------------|
| `--push_host`  | string | Yes      | Host/IP where the broker listens for producer PUSH connections. |
| `--push_port`  | int    | Yes      | Port where the broker listens for producer PUSH connections. |
| `--pull_host`  | string | Yes      | Host/IP where the broker forwards tasks to workers (they PULL). |
| `--pull_port`  | int    | Yes      | Port where the broker forwards tasks to workers. |
| `--log_host`   | string | Yes      | Host/IP where the PUB socket binds for log subscribers. |
| `--log_port`   | int    | Yes      | Port where the PUB socket binds. |

#### Example
```bash
zmq-broker push_pull \
  --push_host 127.0.0.1 --push_port 5555 \
  --pull_host 127.0.0.1 --pull_port 5556 \
  --log_host 127.0.0.1 --log_port 5557
```



### zmq-logger

```bash
zmq-logger [options]
```

| Options           | Type   | Required | Description |
|-------------------|--------|----------|-------------|
| `--log_host`      | string | Yes       | Host/IP of the PUB socket to connect to. |
| `--log_port`      | int    | Yes       | Port of the PUB socket to connect to. |
| `--socket_pattern`| string | Yes       | Socket pattern to interpret messages (choices: `push_pull`, `pub_sub`). |
| `--storage_path`  | string | No        | Path to write JSONL logs. If omitted, logs are printed to stdout. |


#### Example
```bash
zmq-logger \
  --log_host 127.0.0.1 --log_port 5557 \
  --socket_pattern push_pull \
  --storage_path ./data/pull_push_log.json
```

## Running tests
```bash
pytest -s tests/test_logger.py
```


