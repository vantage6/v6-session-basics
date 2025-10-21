from importlib.resources import files

import pandas as pd
import pytest
from vantage6.mock.network import MockNetwork, MockUserClient

TEST_DATAFRAME = pd.read_csv(files("v6-session-basics").joinpath("data/test_data.csv"))
DATAFRAME_LABEL = "test_data_1"


@pytest.fixture
def mock_client() -> MockUserClient:
    mock_network = MockNetwork(
        module_name="v6-session-basics",
        datasets=[
            {
                DATAFRAME_LABEL: {
                    "database": TEST_DATAFRAME,
                    "db_type": "csv",
                },
            },
            {
                DATAFRAME_LABEL: {
                    "database": TEST_DATAFRAME,
                    "db_type": "csv",
                },
            },
        ],
    )
    return mock_network.user_client


def test_sum_function(mock_client: MockUserClient):
    """Test the sum function"""
    # Get organizations
    orgs = mock_client.organization.list()
    org_ids = [org["id"] for org in orgs]

    # Note that the tasks here are run in sequence, thus sleeping for 1 seconds will
    # be multiplied by the number of organizations.
    column_to_sum = "Age"
    task = mock_client.task.create(
        method="sum",
        organizations=org_ids,
        arguments={"column": column_to_sum},
        databases=[{"label": DATAFRAME_LABEL}],
    )

    print(task)
    # Wait for results
    results = mock_client.wait_for_results(task.get("id"))

    print(results)
    assert results[0]["sum"] == TEST_DATAFRAME[column_to_sum].sum()
