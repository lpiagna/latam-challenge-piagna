from typing import List, Tuple
from datetime import datetime
import statistics
import json

import pandas as pd

def _read_data_to_df(file_path: str) -> pd.DataFrame:
    """
    Reads data from a JSON file and returns a pandas DataFrame.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - df (pd.DataFrame): a pandas DataFrame containing the data from the JSON file.
    """
    days = []
    usernames = []

    with open(file_path, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            days.append(tweet['date'])
            usernames.append(tweet['user']['username'])

    df = pd.DataFrame()
    df["day"] = days
    df["username"] = usernames

    return df

def _format_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the date column of a pandas DataFrame.

    Args:
    - df (pd.DataFrame): the pandas DataFrame to format.

    Returns:
    - df (pd.DataFrame): the pandas DataFrame with the date column formatted.
    """
    df["day"] = df.day.apply(
        lambda x: datetime.strptime(x.split("T")[0], "%Y-%m-%d").date()
    )
    return df

def _get_metrics(df: pd.DataFrame) -> Tuple[List[datetime.date], List[str]]:
    """
    Calculates the top 10 days with the most occurrences and the most frequent username.

    Args:
    - df (pd.DataFrame): the pandas DataFrame to analyze.

    Returns:
    - A tuple containing two lists:
        - days (List[datetime.date]): the top 10 days with the most occurrences.
        - users (List[str]): the most frequent username for each of the top 10 days.
    """
    # Get ocurrences by date & most frequent username
    df = df.groupby("day").agg([
        ('count', 'count'), 
        ('username', lambda x: statistics.mode(x))
    ])

    # Get top 10 days
    df = df.sort_values(
        by=[('username', 'count')], ascending=False
    ).head(10)

    days, users = df.index.tolist(), df.username.username.tolist()
    
    return list(zip(days, users))

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Returns the top 10 days with the most occurrences and the most frequent username.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A list of tuples, where each tuple contains:
        - date (datetime.date): the date with the most occurrences.
        - username (str): the most frequent username for that date.
    """
    try:
        tweets = _read_data_to_df(file_path)
        tweets = _format_date(tweets)
        return _get_metrics(tweets)
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
        return []
    
    except Exception as e:
        print(f"Error: {e}")
        return []


