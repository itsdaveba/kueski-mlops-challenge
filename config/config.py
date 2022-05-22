from pathlib import Path

# Directories
BASE_PATH = Path(__file__).parent.parent.resolve()
DATA_DIR = Path(BASE_PATH, 'data')
CONFIG_DIR = Path(BASE_PATH, 'config')
MODEL_DIR = Path(BASE_PATH, 'models')
TEST_DIR = Path(BASE_PATH, 'tests')

# Create directories
DATA_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)
TEST_DIR.mkdir(exist_ok=True)

# Files
DATASET_FILENAME = 'dataset_credit_risk.csv'
CLEAN_DATASET_FILENAME = 'api_dataset.csv'