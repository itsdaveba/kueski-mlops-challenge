from pathlib import Path

# Directories
BASE_PATH = Path(__file__).parent.parent.resolve()
CONFIG_DIR = Path(BASE_PATH, 'config')
TEST_DIR = Path(BASE_PATH, 'tests')
STORES_DIR = Path(BASE_PATH, 'stores')

MODEL_DIR = Path(STORES_DIR, 'models')
BLOB_DIR = Path(STORES_DIR, 'blob')

# Create directories
CONFIG_DIR.mkdir(exist_ok=True)
TEST_DIR.mkdir(exist_ok=True)
STORES_DIR.mkdir(exist_ok=True)

MODEL_DIR.mkdir(exist_ok=True)
BLOB_DIR.mkdir(exist_ok=True)

# Files
DATASET_FILENAME = 'dataset_credit_risk.csv'
CLEAN_DATASET_FILENAME = 'api_dataset.csv'