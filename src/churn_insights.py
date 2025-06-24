import pandas as pd
from pathlib import Path

DATA_PATH = Path('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv')


def load_dataset(path: Path) -> pd.DataFrame:
    """Load and preprocess the churn dataset."""
    df = pd.read_csv(path)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['ChurnFlag'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df


def churn_rate_by_category(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calculate churn rate by categorical column."""
    return (
        df.groupby(column)['ChurnFlag']
        .mean()
        .reset_index()
        .rename(columns={column: 'value', 'ChurnFlag': 'churn_rate'})
        .assign(feature=column)
        [["feature", "value", "churn_rate"]]
        .sort_values('churn_rate', ascending=False)
    )


def numeric_average_by_churn(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Average numeric column grouped by churn label."""
    return (
        df.groupby('Churn')[column]
        .mean()
        .reset_index()
        .rename(columns={'Churn': 'churn_label', column: 'average'})
        .assign(feature=column)
        [["feature", "churn_label", "average"]]
    )


def generate_insights(df: pd.DataFrame) -> pd.DataFrame:
    categorical_cols = [
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod'
    ]
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']

    cat_frames = [churn_rate_by_category(df, col) for col in categorical_cols]
    num_frames = [numeric_average_by_churn(df, col) for col in numeric_cols]

    cat_insights = pd.concat(cat_frames, ignore_index=True)
    num_insights = pd.concat(num_frames, ignore_index=True)

    return cat_insights, num_insights


def main():
    df = load_dataset(DATA_PATH)
    cat_insights, num_insights = generate_insights(df)

    output_dir = Path('data/processed')
    output_dir.mkdir(exist_ok=True)
    cat_insights.to_csv(output_dir / 'categorical_churn_rates.csv', index=False)
    num_insights.to_csv(output_dir / 'numeric_averages_by_churn.csv', index=False)
    print('Insights saved to', output_dir)


if __name__ == '__main__':
    main()
