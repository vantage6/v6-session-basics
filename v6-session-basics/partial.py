"""
This file contains all partial algorithm functions, that are normally executed
on all nodes for which the algorithm is executed.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled). From there, they are sent to the partial task
or directly to the user (if they requested partial results).
"""

import time
import pandas as pd
from vantage6.common import info, error
from vantage6.algorithm.decorator import data, source_database
from .tmp import dataframe, dataframes
from vantage6.algorithm.decorator.action import (
    data_extraction,
    pre_processing,
    federated,
)


@data_extraction
@source_database
def read_csv(connection_details: dict) -> dict:
    info(f"Reading CSV file from {connection_details['uri']}")
    return pd.read_csv(connection_details["uri"])


@pre_processing
@data(1)
def pre_process(df1: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    info(f"Pre-processing data for column {column} with dtype {dtype}")
    df1[column] = df1[column].astype(dtype)
    return df1


@federated
@data(1)
def sum(df1: pd.DataFrame, column: str) -> dict:
    info(f"Summing column {column}")
    return {"sum": int(df1[column].sum())}


@federated
def sleep(seconds: int) -> dict:
    info(f"Sleeping for {seconds} seconds")
    time.sleep(seconds)
    return {"sleep": "done"}


@federated
@dataframe(1)
def sum_dev(df1: pd.DataFrame, column: str) -> dict:
    info(f"Summing column {column}")
    return {"sum": int(df1[column].sum())}


@federated
@dataframes
def sum_many(dfs: dict[str, pd.DataFrame], column: str) -> dict:
    sums = {}
    for df_name, df in dfs.items():
        sums[df_name] = int(df[column].sum())
    return {"sums": sums}
