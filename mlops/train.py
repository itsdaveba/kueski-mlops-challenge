from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score

def split(df, params):
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

def train(df, params):
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