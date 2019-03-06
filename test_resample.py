import pytest
import os
import pandas as pd

@pytest.fixture()
def sample_summary(request):
    summary_filename = os.path.join(".", "cache", "summary_WAS.csv")
    summary = pd.DataFrame.from_csv(summary_filename)
    return summary

def test_resample(sample_summary):
    print(sample_summary)
    new_summary = sample_summary.resample(2, how="mean")
    print(sample_summary)