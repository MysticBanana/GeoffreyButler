from typing import Any, Tuple, Union, Optional
import re


def url_by_str(content: str) -> str:
    return is_url(content) or ""


def is_url(content: str) -> Optional[str]:
    regex = re.compile(
        "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.search(regex, content):
        result = regex.search(content)
        url = result.group(0)
        return url
    else:
        return None


def is_playlist(url: str) -> bool:
    pass