from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class IndexEntry(BaseModel):
    """
    Pydantic model representing a single entry in the chat history index.
    Provides data validation and a clear schema.
    """

    file: str = Field(..., description="The filename of the chat chunk, e.g., 'chat_history_00001.md'")
    summary: str = Field(..., description="A brief summary of the chunk's content.")
    project_name: str = Field(..., description="The name of the project or repository.")
    topic: str = Field(..., description="The specific topic or task being discussed.")
    session_id: str = Field(..., description="Unique ID for the conversation session.")
    start_datetime: datetime = Field(..., description="The start timestamp of the chunk.")
    end_datetime: datetime = Field(..., description="The end timestamp of the chunk.")
    keywords: Optional[List[str]] = Field(default_factory=list, description="A list of keywords for searchability.")
    adrs: Optional[List[str]] = Field(default_factory=list, description="Related ADR IDs (e.g., ['0003']).")
    epics: Optional[List[str]] = Field(default_factory=list, description="Related Epic links/IDs.")
    capabilities: Optional[List[str]] = Field(default_factory=list, description="Capability tags.")
