#!/usr/bin/env python3
import time

from chat_history_manager.main import save_chat_history


def main():
    payload = "X" * 8000
    t0 = time.perf_counter()
    p = save_chat_history(payload, project_name="Bench", topic="Latency", summary="bench")
    t1 = time.perf_counter()
    print(f"save_path={p} elapsed_ms={(t1-t0)*1000:.2f}")


if __name__ == "__main__":
    main()
