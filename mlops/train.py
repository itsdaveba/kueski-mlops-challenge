from typing import Any
from collections import namedtuple

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score

def split(
    df: pd.DataFrame,
    params: namedtuple
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the dataset into train and test sets.

    Set ``status`` column as the target value and set the
    ``age``, ``years_on_the_job``, ``nb_previous_loans``,
    ``avg_amount_loans_previous`` and ``flag_own_car``
    columns as the features. Use the ``SMOTE`` method
    to over-sample the train set.

    Parameters:
        df (DataFrame):
            Dataset.
        params (namedtuple):
            Parameters for ``test_size`` and ``random_state``.

    Returns:
        ``X_train``, ``X_test``, ``y_train`` and ``y_test`` sets.
    """
    df = df.copy()
    Y = df['status'].astype('int')
    df.drop(['status'], axis=1, inplace=True)
    df.drop(['id'], axis=1, inplace=True)
    X = df
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y,
        stratify=Y,
        test_size=params.test_size,
        random_state=params.random_state
    )
    sm = SMOTE(random_state=params.random_state)
    X_train, y_train = sm.fit_resample(X_train, y_train)
    return X_train, X_test, y_train, y_test

def train(df: pd.DataFrame, params: namedtuple) -> dict[str, Any]:
    """
    Train a ``RandomForestClassifier`` on the dataset.

    Fill all ``NaN`` values with zero, split the data into
    train and test sets, fit the model and test to compute the metrics.

    Parameters:
        df (DataFrame):
            Dataset.
        params (namedtuple):
            Parameters for ``n_estimators`` and ``random_state``.

    Returns:
        Artifacts of the trained model (parameters, model and metrics).
    """
    df = df.copy()
    df.fillna(0, inplace=True)
    X_train, X_test, y_train, y_test = split(df, params)

    model = RandomForestClassifier(
        n_estimators=params.n_estimators,
        random_state=params.random_state
    )
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    artifacts = {
        'params': params,
        'model': model,
        'metrics': {
            'accuracy': accuracy_score(y_test, y_predict),
            'precision': precision_score(y_test, y_predict),
            'recall': recall_score(y_test, y_predict),
            'conf_matrix': confusion_matrix(y_test,y_predict).tolist()
        }
    }
    return artifacts