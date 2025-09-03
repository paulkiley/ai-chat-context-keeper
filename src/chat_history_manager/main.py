import uuid
from typing import Optional, List
from pathlib import Path

from .models import IndexEntry
from .config import settings
from .utils import (
    ensure_chat_history_dir_exists,
    get_next_chunk_number,
    write_chat_chunk,
    read_chat_index,
    update_chat_index,
    extract_latest_conversation,
    get_current_datetime,
    read_chat_chunk,
    apply_retention_policies,
    chat_history_lock,
)

def save_chat_history(
    full_conversation: str,
    project_name: str,
    topic: str,
    session_id: Optional[str] = None,
    summary: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    adrs: Optional[List[str]] = None,
    epics: Optional[List[str]] = None,
    capabilities: Optional[List[str]] = None,
    dry_run: bool = False,
) -> Path:
    """Saves a chunk of chat history and updates the index."""
    ensure_chat_history_dir_exists()

    session_id = session_id or str(uuid.uuid4())
    chunk_content = extract_latest_conversation(full_conversation)

    with chat_history_lock():
        chunk_number = get_next_chunk_number()
        prospective_path = (
            settings.CHAT_HISTORY_BASE_DIR / f"chat_history_{chunk_number:05d}.md"
        )
        current_datetime = get_current_datetime()

        if dry_run:
            return prospective_path

        file_path = write_chat_chunk(chunk_number, chunk_content)

        new_entry = IndexEntry(
            file=file_path.name,
            summary=summary or f"Chat chunk for {project_name} - {topic}",
        keywords=keywords or [project_name, topic],
        adrs=adrs or [],
        epics=epics or [],
        capabilities=capabilities or [],
        project_name=project_name,
        topic=topic,
        session_id=session_id,
            start_datetime=current_datetime,
            end_datetime=current_datetime,
        )
        update_chat_index(new_entry)
        # Apply retention if configured
        apply_retention_policies()
        return file_path

def retrieve_chat_history(
    project_name: Optional[str] = None,
    topic: Optional[str] = None,
    session_id: Optional[str] = None,
    limit_chunks: int = 1
) -> List[str]:
    """Retrieves relevant chat history chunks based on criteria."""
    index_entries = read_chat_index()
    
    relevant_chunks = []
    for entry in index_entries:
        match = True
        if project_name and entry.project_name != project_name:
            match = False
        if topic and entry.topic != topic:
            match = False
        if session_id and entry.session_id != session_id:
            match = False
        
        if match:
            chunk_number = int(entry.file.split("_")[-1].replace(".md", ""))
            if chunk_content := read_chat_chunk(chunk_number):
                relevant_chunks.append(chunk_content)
                if len(relevant_chunks) >= limit_chunks:
                    break
    
    return relevant_chunks
