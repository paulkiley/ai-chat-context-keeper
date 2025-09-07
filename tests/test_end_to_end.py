from pathlib import Path

from chat_history_manager.main import retrieve_chat_history, save_chat_history
from chat_history_manager.utils import read_chat_index


def test_save_updates_index_and_retrieve(temp_history_dir):
    # Save two chunks for same project with different topics
    p = save_chat_history("conv-1-P1-T1", project_name="P1", topic="T1", summary="S1")
    assert p.exists()

    p2 = save_chat_history("conv-2-P1-T2", project_name="P1", topic="T2", summary="S2")
    assert p2.exists()

    # Index should have newest first
    index = read_chat_index()
    assert len(index) >= 2
    assert index[0].summary == "S2"
    assert index[1].summary == "S1"

    # Retrieve by filters
    chunks_all = retrieve_chat_history(project_name="P1", limit_chunks=5)
    assert len(chunks_all) >= 2
    assert "conv-2-P1-T2" in chunks_all[0]
    assert "conv-1-P1-T1" in chunks_all[1]

    # Filter by topic
    chunks_t1 = retrieve_chat_history(project_name="P1", topic="T1", limit_chunks=5)
    assert len(chunks_t1) == 1
    assert "conv-1-P1-T1" in chunks_t1[0]


def test_lockfile_cleanup(temp_history_dir):
    # Ensure lock file is removed after save
    save_chat_history("conv", project_name="L", topic="T")
    lock_path = Path(temp_history_dir) / ".chm.lock"
    assert not lock_path.exists()
