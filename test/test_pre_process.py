from importlib.resources import files

import pandas as pd
import pytest
from vantage6.mock.network import MockNetwork, MockUserClient


@pytest.fixture
def mock_client() -> MockUserClient:
    test_data = files("v6-session-basics").joinpath("data/test_data.csv")
    mock_network = MockNetwork(
        module_name="v6-session-basics",
        datasets=[
            {
                "test_data_1": {
                    "database": pd.read_csv(test_data),
                    "db_type": "csv",
                },
            },
            {
                "test_data_1": {
                    "database": pd.read_csv(test_data),
                    "db_type": "csv",
                },
            },
        ],
    )
    return mock_network.user_client


def test_pre_process_function(mock_client: MockUserClient):
    """Test the pre_process function"""
    # Get organizations
    # orgs = mock_client.organization.list()
    # org_ids = [org["id"] for org in orgs]
    DATAFRAME_ID = 1

    # Check what dtype the dataframe has
    old_response = mock_client.network.server.get_dataframe(DATAFRAME_ID)
    old_dtypes = [
        column["dtype"] for column in old_response["columns"] if column["name"] == "Age"
    ]
    assert [str(dtype) for dtype in old_dtypes] == [
        "int64" for _ in range(len(old_dtypes))
    ]

    # Note that the tasks here are run in sequence, thus sleeping for 1 seconds will
    # be multiplied by the number of organizations.
    mock_client.dataframe.preprocess(
        id_=DATAFRAME_ID,
        image="mock-image",
        method="pre_process",
        arguments={"column": "Age", "dtype": "int32"},
    )

    df_response = mock_client.network.server.get_dataframe(DATAFRAME_ID)
    new_dtypes = [
        column["dtype"] for column in df_response["columns"] if column["name"] == "Age"
    ]
    assert old_dtypes != new_dtypes
    assert [str(dtype) for dtype in new_dtypes] == [
        "int32" for _ in range(len(new_dtypes))
    ]
