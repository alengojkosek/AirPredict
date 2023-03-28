import pandas as pd
import numpy as np
from evidently.report import Report
from evidently.metrics import base_metrics, regression_metrics
from evidently.metric import DataDrift, TargetDrift, DataQuality
from evidently.presets import DataDriftPreset, TargetDriftPreset, DataQualityPreset, RegressionPreset
from evidently.test_suite import TestSuite
from evidently.tests.base import generate_tests
from evidently.test import DataStabilityTest, NoTargetPerformanceTest, RegressionTest
import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

data = pd.read_csv('./data/processed/current_data.csv')

airpredict_data = data.copy()
airpredict_data.rename(columns={'pm10': 'target'}, inplace=True)
airpredict_data['prediction'] = airpredict_data['target'].values + np.random.normal(0, 5, airpredict_data.shape[0])

reference = airpredict_data.sample(n=5000, replace=False)
current = airpredict_data.sample(n=5000, replace=False)

report = Report(
    [
        DataDrift(),
    ]
)

report.run(reference_data=reference, current_data=current)
report.save("evidently_report.html")