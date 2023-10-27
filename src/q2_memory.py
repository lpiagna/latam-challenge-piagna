from typing import List, Tuple, Dict
import json
import re
from collections import Counter

def _get_emoji_ocurrences(file_path: str) -> Counter:
    """
    Returns a Counter object with the number of occurrences of each emoji in a JSON file.

    Args:
    - file_path (str): the path to the JSON file.

    Returns:
    - A Counter object where the keys are the Unicode representation of each emoji and the values
        are the number of times the emoji appears in the JSON file.
    """
    emoji_ocurrences = Counter()
    regex = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

    try:
        with open(file_path, 'r') as f:
            for line in f:
                content = json.loads(line).get('content')
                emojis = (emoji for emoji in regex.findall(content))
                emoji_ocurrences.update(emojis)

        return emoji_ocurrences

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return Counter()

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{file_path}'.")
        return Counter()

    except Exception as e:
        print(f"Error: {e}")
        return Counter()


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
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
    return emoji_ocurrences.most_common(10)



