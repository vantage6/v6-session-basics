from vantage6.common import info
from vantage6.algorithm.decorator.action import central
from vantage6.algorithm.decorator import algorithm_client
from vantage6.algorithm.client import AlgorithmClient


@central
@algorithm_client
def global_sum(client: AlgorithmClient, column: str) -> dict:
    info("Central function that sums the results of the federated sum function")

    # Collect all organization that participate in this collaboration.
    # These organizations will receive the task to compute the partial.
    info("Collecting participating organizations")
    organizations = client.organization.list()
    ids = [organization.get("id") for organization in organizations]

    info(f"Sending task to {len(ids)} organizations")
    task = client.task.create(
        name="central-sum",
        description="subtask",
        method="sum",
        organizations=ids,
        input_={"args": [column], "kwargs": {}},
    )

    info("Waiting for results...")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Partial results are in!")

    info("Computing global sum")
    global_sum = 0
    for output in results:
        global_sum += output["sum"]

    return {"global_sum": global_sum}


@central
@algorithm_client
def global_sum_dev(client: AlgorithmClient, column: str) -> dict:
    info("Central function that sums the results of the federated sum function")

    # Collect all organization that participate in this collaboration.
    # These organizations will receive the task to compute the partial.
    info("Collecting participating organizations")
    organizations = client.organization.list()
    ids = [organization.get("id") for organization in organizations]

    info(f"Sending task to {len(ids)} organizations")
    task = client.task.create(
        name="central-sum",
        description="subtask",
        method="sum_",
        organizations=ids,
        input_={"args": [column], "kwargs": {}},
    )

    info("Waiting for results...")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Partial results are in!")

    info("Computing global sum")
    global_sum = 0
    for output in results:
        global_sum += output["sum"]

    return {"global_sum": global_sum}
