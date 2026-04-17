"""
Utility functions.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def split_message(text: str, max_length: int = 4096) -> List[str]:
    """
    Split a long message into chunks that fit Telegram's message limit.
    Attempts to split at paragraph boundaries, avoiding splitting inside code blocks.
    """
    if len(text) <= max_length:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break

        # Find a safe split point
        split_at = max_length
        # Prefer splitting at double newline (paragraph)
        double_newline = text.rfind('\n\n', 0, max_length)
        if double_newline != -1:
            split_at = double_newline + 2
        else:
            # Otherwise split at single newline
            single_newline = text.rfind('\n', 0, max_length)
            if single_newline != -1:
                split_at = single_newline + 1
            else:
                # No newline, check if we are inside a code block
                # Simple heuristic: if there's an odd number of ``` before split_at, move split point earlier
                backticks_count = text[:max_length].count('```')
                if backticks_count % 2 == 1:
                    # Inside a code block, try to split before the opening ```
                    last_backtick = text.rfind('```', 0, max_length)
                    if last_backtick != -1:
                        split_at = last_backtick
                    else:
                        # fallback to max_length
                        split_at = max_length
                else:
                    split_at = max_length

        chunk = text[:split_at].rstrip()
        chunks.append(chunk)
        text = text[split_at:].lstrip()
    return chunks

def extract_photo_info(photo_array: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract the largest photo file_id and dimensions.
    """
    if not photo_array:
        return {}
    # Telegram sends multiple sizes; the last is the largest
    largest = photo_array[-1]
    return {
        "file_id": largest.get("file_id"),
        "width": largest.get("width"),
        "height": largest.get("height"),
        "file_size": largest.get("file_size"),
    }