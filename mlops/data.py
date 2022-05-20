import pandas as pd

def _to_datetime(df, columns, inplace=False):
    if not inplace:
        df = df.copy()
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    if not inplace:
        return df

def preprocess(df, inplace=False):
    if not inplace:
        df = df.copy()
    df.sort_values(by=["id", "loan_date"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = _to_datetime(df, columns=["loan_date", "birthday", "job_start_date"], inplace=inplace)
    if not inplace:
        return df

def feature_engineering(df):
    df = df.copy()
    df_grouped = df.groupby("id")
    df["nb_previous_loans"] = df_grouped["loan_date"].rank(method="first") - 1
    df['avg_amount_loans_previous'] = df.groupby('id')['loan_amount'].apply(lambda x: x.shift().expanding().mean())
    df['age'] = (pd.to_datetime('today').normalize() - df['birthday']).dt.days // 365
    df['years_on_the_job'] = (pd.to_datetime('today').normalize() - df['job_start_date']).dt.days // 365
    df['flag_own_car'] = df['flag_own_car'].apply(lambda x : 0 if x == 'N' else 1)
    return df[['id', 'age', 'years_on_the_job', 'nb_previous_loans', 'avg_amount_loans_previous', 'flag_own_car', 'status']]