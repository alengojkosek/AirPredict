import evidently
import pandas as pd
import numpy as np

from sklearn.datasets import fetch_california_housing

from evidently import ColumnMapping

from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset, DataQualityPreset, RegressionPreset
from evidently.metrics import *

from evidently.test_suite import TestSuite
from evidently.tests.base_test import generate_column_tests
from evidently.test_preset import DataStabilityTestPreset, NoTargetPerformanceTestPreset, RegressionTestPreset
from evidently.tests import *

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

data = pd.read_csv('current_data.csv', as_frame=True)

airpredict_data = data.frame

airpredict_data.rename(columns={'pm10': 'target'}, inplace=True)
airpredict_data['prediction'] = airpredict_data['target'].values + np.random.normal(0, 5, airpredict_data.shape[0])

reference = airpredict_data.sample(n=5000, replace=False)
current = airpredict_data.sample(n=5000, replace=False)

report = Report(metrics=[
    DataDriftPreset(),
])

report.run(reference_data=reference, current_data=current)
report.save_html("evidently_report.html")
