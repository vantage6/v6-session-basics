from importlib.resources import files

import pytest
from vantage6.algorithm.client.mock_client import MockAlgorithmClient


@pytest.fixture
def mock_client() -> MockAlgorithmClient:
    test_data = files("v6-session-basics").joinpath("data/test_data.csv")
    return MockAlgorithmClient(
        datasets=[
            [
                {
                    "database": test_data,
                    "db_type": "csv",
                },
            ],
            [
                {
                    "database": test_data,
                    "db_type": "csv",
                }
            ],
        ],
        module="v6-session-basics",
    )


def test_metadata_function(mock_client: MockAlgorithmClient):
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
