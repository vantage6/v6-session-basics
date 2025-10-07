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
    return MockUserClient(mock_network)

def test_metadata_function(mock_client: MockUserClient):
    """Test the metadata function"""
    # Get organizations
    orgs = mock_client.organization.list()
    org_ids = [org["id"] for org in orgs]

    # Create task
    task = mock_client.task.create(
        method="metadata", organizations=org_ids, arguments={}
    )

    # Wait for results
    results = mock_client.wait_for_results(task.get("id"))

    # Assertions
    assert results is not None
    assert len(results) == 2  # Two organizations
    for result in results:
        assert "task_id" in result
        assert "node_id" in result
        assert "collaboration_id" in result
        assert "organization_id" in result
        assert "temporary_directory" in result
        assert "output_file" in result
        assert "input_file" in result
        assert "token" in result
        assert "action" in result

    print(results)
