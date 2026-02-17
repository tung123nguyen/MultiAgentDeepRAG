# file_tools.py

import os
import hashlib
from langchain_core.messages import ToolMessage

from typing import Annotated
from langchain.agents import AgentState
from typing_extensions import NotRequired

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

BASE_FILE_DIR = os.getenv("AGENT_FILE_BASE_DIR", "agent_files")

# -------------------------
# Shared Agent State
# -------------------------

class DeepAgentState(AgentState):
    """
    Shared state for all agents (orchestrator, researcher, editor).

    Inherits from LangChain's AgentState and adds:
    - user_id:    separate users
    - thread_id:  separate conversations per user

    Files are stored on REAL disk, not in state.
    """
    user_id: NotRequired[str]
    thread_id: NotRequired[str]

## Utility Methods
def _thread_folder(state: DeepAgentState) -> str:
    """Return the folder for this user/thread, create if missing."""
    user = state.get("user_id") or "default_user"
    thread = state.get("thread_id") or "default_thread"
    folder = os.path.join(BASE_FILE_DIR, user, thread)
    os.makedirs(folder, exist_ok=True)
    return folder

def generate_hash(text: str, length: int = 6) -> str:
    """Generate a short hash from text for unique file naming."""
    return hashlib.md5(text.encode()).hexdigest()[:length]


def _disk_path(state: DeepAgentState, file_path: str) -> str:
    """
    Build real filesystem path as:
        agent_files/<user_id>/<thread_id>/<file_path>
    """
    folder = _thread_folder(state)
    safe_path = file_path.lstrip("/\\")
    full = os.path.join(folder, safe_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    return full