from pathlib import Path

BASE_PATH = Path(__file__).parent.parent.resolve()
DATA_DIR = Path(BASE_PATH, 'data')
CONFIG_DIR = Path(BASE_PATH, 'config')
MODEL_REGISTRY = Path(BASE_PATH, 'models')

DATASET_FILENAME = 'dataset_credit_risk.csv'
CLEAN_DATASET_FILENAME = 'clean_dataset.csv'