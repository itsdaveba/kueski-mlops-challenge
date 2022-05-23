from pathlib import Path

# Directories
BASE_PATH = Path(__file__).parent.parent.resolve()
CONFIG_DIR = Path(BASE_PATH, 'config')
DATA_DIR = Path(BASE_PATH, 'data')
TEST_DIR = Path(BASE_PATH, 'tests')
BLOB_DIR = Path(BASE_PATH, 'blob')
MODEL_DIR = Path(BASE_PATH, 'models')

# Create directories
CONFIG_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
TEST_DIR.mkdir(exist_ok=True)
BLOB_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)

# Files
DATASET_FILENAME = 'dataset_credit_risk.csv'
CLEAN_DATASET_FILENAME = 'api_dataset.csv'