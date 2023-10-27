from typing import List, Tuple
from datetime import datetime
import json


def _get_top_10_dates(file_path: str) -> List[str]:
    """
    Returns the top 10 dates with the most tweets.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A list of strings, where each string is a date in the format "YYYY-MM-DD".
    """
    tweets_by_date = {}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                day = tweet['date'].split("T")[0]
                tweets_by_date[day] = tweets_by_date.get(day, 0) + 1

        # Get top 10 days
        return [
            day for day, _ in sorted(
                tweets_by_date.items(), key=lambda x: x[1], reverse=True
            )[:10]
        ]

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
        return []

    except Exception as e:
        print(f"Error: {e}")
        return []

def _get_most_common_username(file_path: str, day: str) -> Tuple[datetime.date, str]:
    """
    Returns the most frequent username for a given date.

    Args:
    - file_path (str): the path to the JSON file.
    - day (str): the date in the format "YYYY-MM-DD".

    Returns:
    - A tuple containing:
        - date (datetime.date): the date with the most tweets.
        - username (str): the most frequent username for that date.
    """
    usernames = {}
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                tweet = json.loads(line)
                if tweet['date'].split("T")[0] == day:
                    usernames[tweet['user']['username']] = usernames.get(
                        tweet['user']['username'], 0
                    ) + 1
        
        day = datetime.strptime(day, "%Y-%m-%d").date()

        return (day, max(usernames, key=usernames.get))

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return (None, None)

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
        return (None, None)

    except Exception as e:
        print(f"Error: {e}")
        return (None, None)


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    """
    Returns the top 10 days with the most tweets and the most frequent username for each day.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A list of tuples, where each tuple contains:
        - date (datetime.date): the date with the most tweets.
        - username (str): the most frequent username for that date.
    """

    days = _get_top_10_dates(file_path)

    return [
        _get_most_common_username(file_path, day)
        for day in days
    ]
