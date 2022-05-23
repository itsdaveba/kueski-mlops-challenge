# Configuration

Configure the directory names in `config/config.py`

```python
# Directories
BASE_PATH = Path(__file__).parent.parent.resolve()
CONFIG_DIR = Path(BASE_PATH, 'config')
DATA_DIR = Path(BASE_PATH, 'data')
TEST_DIR = Path(BASE_PATH, 'tests')
BLOB_DIR = Path(BASE_PATH, 'blob')
MODEL_DIR = Path(BASE_PATH, 'models')
```

Configure the model parameters in `params.json`

```json
{
    "test_size": 0.3,
    "n_estimators": 5,
    "random_state": 123
}
```

::: config.config