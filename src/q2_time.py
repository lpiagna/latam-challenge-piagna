from typing import List, Tuple, Dict
import json
import re


def _get_emoji_ocurrences(file_path: str) -> Dict:
    """
    Returns a dictionary with the number of occurrences of each emoji in a JSON file.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A dictionary where the keys are the Unicode representation of each emoji and the values
        are the number of times the emoji appears in the JSON file.
    """
    emoji_ocurrences = {}
    regex = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    try:
        with open(file_path, 'r') as f:
            for line in f:
                content = json.loads(line).get('content')
                emojis = regex.findall(content)
                
                for emoji in emojis:
                    emoji_ocurrences[emoji] = emoji_ocurrences.get(emoji, 0) + 1

        return emoji_ocurrences

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
        return {}

    except Exception as e:
        print(f"Error: {e}")
        return {}


def _get_top_emojis(emoji_ocurrences: Dict, top_n: int) -> List[Tuple[str, int]]:
    """
    Returns a list of the top n most used emojis.

    Args:
    - emoji_ocurrences (Dict): a dictionary where the keys are the Unicode representation of each
        emoji and the values are the number of times the emoji appears in the JSON file.
    - top_n (int): the number of top emojis to return.

    Returns:
    - A list of tuples, where each tuple contains:
        - emoji (str): the Unicode representation of the emoji.
        - count (int): the number of times the emoji appears in the JSON file.
    """
    
    return sorted(
        emoji_ocurrences.items(), key=lambda x: x[1], reverse=True
    )[:top_n]


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    """
    Returns the top 10 most used emojis in a JSON file.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A list of tuples, where each tuple contains:
        - emoji (str): the Unicode representation of the emoji.
        - count (int): the number of times the emoji appears in the JSON file.
    """

    emoji_ocurrences = _get_emoji_ocurrences(file_path)
    return _get_top_emojis(emoji_ocurrences, 10)






