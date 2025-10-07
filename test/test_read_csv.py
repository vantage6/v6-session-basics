from importlib.resources import files
import pandas as pd
import pytest

from vantage6.mock.mock_network import MockNetwork, MockUserClient


@pytest.fixture
def mock_client() -> MockUserClient:
    test_data = files("v6-session-basics").joinpath("data/test_data.csv")
    mock_network = MockNetwork(
        module_name="v6-session-basics",
        datasets=[
            {
                "test_data_1": {
                    "database": test_data,
                    "db_type": "csv",
                },
            },
            {
                "test_data_1": {
                    "database": test_data,
                    "db_type": "csv",
                },
            }
        ]
    )
    return MockUserClient(mock_network)


def test_read_csv_function(mock_client: MockUserClient):
    """Test the read_csv function"""
    # Get organizations
    orgs = mock_client.organization.list()
    org_ids = [org["id"] for org in orgs]

    # Create task
    mock_client.dataframe.create(
        method="read_csv",
        organizations=org_ids,
        arguments={},
        action="data_extraction",
        label="test_data_1",
        name="my_dataframe_by_frank"
    )

    # A data extraction job should create a dataframe on each node, lets check if this
    # is the case. Note that in the mock network we store the dataframes in the Python
    # session as pandas dataframes while in the real network we store them at disk as
    # parquet files.
    for node in mock_client.network.nodes:
        assert len(node.dataframes) == 1
        assert "my_dataframe_by_frank" in node.dataframes
        assert isinstance(node.dataframes["my_dataframe_by_frank"], pd.DataFrame)