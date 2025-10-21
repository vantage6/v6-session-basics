from importlib.resources import files

import pandas as pd
import pytest
from vantage6.mock.network import MockNetwork, MockUserClient

# Read full dataframe and split into 4 random subsets
full_df = pd.read_csv(files("v6-session-basics").joinpath("data/test_data.csv"))
TEST_DATAFRAME_1 = full_df.sample(n=10, random_state=42)
TEST_DATAFRAME_2 = full_df.sample(n=15, random_state=43)
TEST_DATAFRAME_3 = full_df.sample(n=11, random_state=44)
TEST_DATAFRAME_4 = full_df.sample(n=15, random_state=45)
DATAFRAME_LABEL_1 = "test_data_1"
DATAFRAME_LABEL_2 = "test_data_2"


@pytest.fixture
def mock_client() -> MockUserClient:
    mock_network = MockNetwork(
        module_name="v6-session-basics",
        datasets=[
            {
                DATAFRAME_LABEL_1: {
                    "database": TEST_DATAFRAME_1,
                    "db_type": "csv",
                },
                DATAFRAME_LABEL_2: {
                    "database": TEST_DATAFRAME_2,
                    "db_type": "csv",
                },
            },
            {
                DATAFRAME_LABEL_1: {
                    "database": TEST_DATAFRAME_3,
                    "db_type": "csv",
                },
                DATAFRAME_LABEL_2: {
                    "database": TEST_DATAFRAME_4,
                    "db_type": "csv",
                },
            },
        ],
    )
    return mock_network.user_client


def test_sum_many_function(mock_client: MockUserClient):
    """Test the sum_many function"""
    # Get organizations
    orgs = mock_client.organization.list()
    org_ids = [org["id"] for org in orgs]

    column_to_sum = "Age"
    task = mock_client.task.create(
        method="sum_many",
        organizations=org_ids,
        arguments={"column": column_to_sum},
        databases=[[{"label": DATAFRAME_LABEL_1}, {"label": DATAFRAME_LABEL_2}]],
    )

    # Wait for results
    results = mock_client.wait_for_results(task.get("id"))
    print(results)

    # # Verify results
    assert results is not None
    assert len(results) == len(org_ids)  # Two organizations

    assert "sums" in results[0]
    assert DATAFRAME_LABEL_1 in results[0]["sums"]
    assert (
        results[0]["sums"][DATAFRAME_LABEL_1] == TEST_DATAFRAME_1[column_to_sum].sum()
    )
    assert (
        results[0]["sums"][DATAFRAME_LABEL_2] == TEST_DATAFRAME_2[column_to_sum].sum()
    )
    assert (
        results[1]["sums"][DATAFRAME_LABEL_1] == TEST_DATAFRAME_3[column_to_sum].sum()
    )
    assert (
        results[1]["sums"][DATAFRAME_LABEL_2] == TEST_DATAFRAME_4[column_to_sum].sum()
    )
