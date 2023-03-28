import pandas as pd
import numpy as np
import evidently
import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

data = pd.read_csv('./data/processed/current_data.csv')

airpredict_data = data.copy()
airpredict_data.rename(columns={'pm10': 'target'}, inplace=True)

airpredict_data = airpredict_data.replace('<2', np.nan)
airpredict_data = airpredict_data.replace('<1', np.nan)
airpredict_data['target'] = airpredict_data['target'].astype(float)
airpredict_data['target'] = airpredict_data['target'].fillna(airpredict_data['target'].mean())
airpredict_data['prediction'] = airpredict_data['target'] + np.random.normal(0, 5, airpredict_data.shape[0])

reference = airpredict_data.sample(n=5000, replace=False)
current = airpredict_data.sample(n=5000, replace=False)

report = Report(
    [
        DataDrift(),
    ]
)

report.run(reference_data=reference, current_data=current)
report.save("evidently_report.html")