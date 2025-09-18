"""
This file contains all partial algorithm functions, that are normally executed
on all nodes for which the algorithm is executed.

The results in a return statement are sent to the vantage6 server (after
encryption if that is enabled). From there, they are sent to the partial task
or directly to the user (if they requested partial results).
"""

import time
import pandas as pd
from vantage6.common import info
from vantage6.algorithm.decorator.data import dataframe, dataframes
from vantage6.algorithm.decorator.action import (
    data_extraction,
    preprocessing,
    federated,
)


@data_extraction
def read_csv(connection_details: dict) -> dict:
    info(f"Reading CSV file from {connection_details['uri']}")
    return pd.read_csv(connection_details["uri"])


@preprocessing
@dataframe(1)
def pre_process(df1: pd.DataFrame, column: str, dtype: str) -> pd.DataFrame:
    info(f"Pre-processing data for column {column} with dtype {dtype}")
    df1[column] = df1[column].astype(dtype)
    return df1


@federated
@dataframe(1)
def sum(df1: pd.DataFrame, column: str) -> dict:
    info(f"Summing column {column}")
    return {"sum": int(df1[column].sum())}


@federated
def sleep(seconds: int) -> dict:
    info(f"Starting sleep task for {seconds} seconds")
    for i in range(seconds):
        info(f"Sleeping: {i + 1} second(s) elapsed")
        time.sleep(1)
    info("Sleep task completed")
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


@federated
@dataframe(2)
def two_df_sum(df1: pd.DataFrame, df2: pd.DataFrame, column: str) -> dict:
    info(f"Summing column {column} of two dataframes")
    return {"sum": int(df1[column].sum() + df2[column].sum())}
