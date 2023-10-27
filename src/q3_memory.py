from typing import List, Tuple, Dict
import re
import json
from collections import Counter

def _get_user_mentions(file_path: str) -> Dict:
    """
    Returns a dictionary with the number of occurrences of each user mention in a JSON file.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A dictionary where the keys are the usernames mentioned in the JSON file and the values
      are the number of times the username appears in the JSON file.
    """
    user_mentions = {}
    regex = re.compile(r'@(\w+)')

    try:
        with open(file_path, 'r') as f:
            mentions = (regex.findall(json.loads(line).get('content')) for line in f)
            user_mentions = Counter(mention for sublist in mentions for mention in sublist)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
        return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}

    return user_mentions


def _get_top_mentions(user_mentions: Dict, top_n: int) -> List[Tuple[str, int]]:
    """
    Returns a list of the top n most mentioned users.

    Args:
    - user_mentions (Dict): a dictionary where the keys are the usernames mentioned in the JSON file
      and the values are the number of times the username appears in the JSON file.
    - top_n (int): the number of top mentions to return.

    Returns:
    - A list of tuples, where each tuple contains:
        - username (str): the username mentioned in the JSON file.
        - count (int): the number of times the username appears in the JSON file.
    """
    return sorted(
        user_mentions.items(), key=lambda x: x[1], reverse=True
    )[:top_n]


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    """
    Returns the top 10 most mentioned users in a JSON file.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A list of tuples, where each tuple contains:
        - username (str): the username mentioned in the JSON file.
        - count (int): the number of times the username appears in the JSON file.
    """
    user_mentions = _get_user_mentions(file_path)
    return _get_top_mentions(user_mentions, 10)
