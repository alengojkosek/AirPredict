import pandas as pd
import numpy as np

from evidently import ColumnMapping

from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *

from evidently.test_suite import TestSuite
from evidently.tests.base_test import generate_column_tests
from evidently.test_preset import DataStabilityTestPreset, NoTargetPerformanceTestPreset
from evidently.tests import *

from evidently.dashboard import Dashboard
from evidently.tabs import DataDriftTab

from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection
from evidently.test_preset import DataDriftTestPreset

from evidently.analyzers.data_drift_analyzer import DataDriftAnalyzer

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
        DataDriftPreset(),
    ]
)

report.run(reference_data=reference, current_data=current)
report.save("evidently_report.html")