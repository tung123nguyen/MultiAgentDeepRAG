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