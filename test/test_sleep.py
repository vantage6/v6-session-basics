from importlib.resources import files

from vantage6.mock.mock_network import MockNetwork, MockUserClient
import pytest


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
    return mock_network.user_client

def test_sleep_function(mock_client: MockUserClient):
    """Test the metadata function"""
    # Get organizations
    orgs = mock_client.organization.list()
    org_ids = [org["id"] for org in orgs]

    # Note that the tasks here are run in sequence, thus sleeping for 1 seconds will
    # be multiplied by the number of organizations.
    task = mock_client.task.create(
        method="sleep", organizations=org_ids, arguments={"seconds": 1}
    )

    # Wait for results
    results = mock_client.wait_for_results(task.get("id"))

    # Assertions
    assert results is not None
    assert len(results) == 2  # Two organizations
    for result in results:
        assert "sleep" in result
        assert result["sleep"] == "done"