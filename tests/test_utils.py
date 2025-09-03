from chat_history_manager.utils import (
    ensure_chat_history_dir_exists,
    extract_latest_conversation,
    read_chat_chunk,
    write_chat_chunk,
)


def test_chunk_roundtrip(temp_history_dir):
    ensure_chat_history_dir_exists()
    path = write_chat_chunk(1, "hello")
    assert path.exists()
    assert path.parent == temp_history_dir
    assert read_chat_chunk(1) == "hello"


def test_extract_latest_conversation_truncates():
    long = "A" * 5000
    out = extract_latest_conversation(long)
    # default chunk size is 4000 per settings
    assert len(out) == 4000
    assert out == "A" * 4000
