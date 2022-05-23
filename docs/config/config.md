# Configuration

Configure the directory names in `config/config.py`

```python
# Directories
BASE_PATH = Path(__file__).parent.parent.resolve()
CONFIG_DIR = Path(BASE_PATH, 'config')
TEST_DIR = Path(BASE_PATH, 'tests')
STORES_DIR = Path(BASE_PATH, 'stores')

MODEL_DIR = Path(STORES_DIR, 'models')
BLOB_DIR = Path(STORES_DIR, 'blob')
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