import re


def clean_string(s: str) -> str:
    """
    Clean a string by removing extra whitespace characters.

    Args:
        s (str): The string to clean.

    Returns:
        str: The cleaned string.
    """
    # Replace all whitespace characters (newlines, tabs, multiple spaces) with a single space
    cleaned_string = re.sub(r"\s+", " ", s)
    # Remove leading and trailing spaces
    cleaned_string = cleaned_string.strip()
    return cleaned_string
