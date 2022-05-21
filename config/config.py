from pathlib import Path

# Directories
BASE_PATH = Path(__file__).parent.parent.resolve()
DATA_DIR = Path(BASE_PATH, 'data')
CONFIG_DIR = Path(BASE_PATH, 'config')
MODEL_REGISTRY = Path(BASE_PATH, 'models')

# Create directories
DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
MODEL_REGISTRY.mkdir(parents=True, exist_ok=True)

# Files
DATASET_FILENAME = 'dataset_credit_risk.csv'
CLEAN_DATASET_FILENAME = 'clean_dataset.csv'