"""
In-memory conversation storage per user.
Designed to be easily replaced with Redis or a database.
"""
from typing import List, Dict, Any
from collections import deque
from bot.config import MAX_HISTORY_PER_USER

# Global in-memory store
_user_memory: Dict[int, deque] = {}

def get_user_memory(user_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve the conversation history for a user.
    Returns a list of messages in OpenAI format.
    """
    if user_id not in _user_memory:
        return []
    return list(_user_memory[user_id])

def add_user_message(user_id: int, role: str, content: str) -> None:
    """
    Add a message to the user's conversation history.
    Role: 'system', 'user', 'assistant'
    """
    if user_id not in _user_memory:
        _user_memory[user_id] = deque(maxlen=MAX_HISTORY_PER_USER)
    _user_memory[user_id].append({"role": role, "content": content})

def clear_user_memory(user_id: int) -> None:
    """
    Clear the conversation history for a user.
    """
    if user_id in _user_memory:
        del _user_memory[user_id]

def get_all_users() -> List[int]:
    """
    Return list of user IDs with active memory (for debugging).
    """
    return list(_user_memory.keys())