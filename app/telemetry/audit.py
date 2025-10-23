import os 
import csv 
import json
import sqlite3
from datetime import datetime
from typing  import Optional, Dict, Any
import threading

class AuditLogger:
    """
    Simple multi-sink audit logger:
      - JSONL file (ndjson)
      - CSV file
      - SQLite (synchronous, protected by a lock for simplicity)
    Use in low-volume local env; upgrade to async queue if needed.
    """

    def __init__(
            self ,
            jsonl_path : str = "logs/audit.jsonl",
            csv_path : str = "logs/audit.csv",
            sqlite_path : str = "logs/audit.db",
    ):
        # store the paths provided by the caller
        self.jsonl_path = jsonl_path
        self.csv_path = csv_path
        self.sqlite_path = sqlite_path

        # Ensure directories exist. Use '.' when dirname is empty (path in cwd).
        jsonl_dir = os.path.dirname(self.jsonl_path) or "."
        os.makedirs(jsonl_dir, exist_ok=True)

        # thread lock to serialize writes
        self._lock = threading.Lock()

        # CSV header (fixed schema)
        self._csv_header = [
            "ts",
            "request_id",
            "endpoint",
            "model",
            "prompt_len",
            "response_len",
            "status",
            "duration_ms",
            "stream",
        ]

        # Create CSV file with header if needed
        if self.csv_path:
            csv_dir = os.path.dirname(self.csv_path) or "."
            os.makedirs(csv_dir, exist_ok=True)
            if not os.path.exists(self.csv_path):
                with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=self._csv_header)
                    writer.writeheader()

        # SQLite setup
        if self.sqlite_path:
            sqlite_dir = os.path.dirname(self.sqlite_path) or "."
            os.makedirs(sqlite_dir, exist_ok=True)
            with sqlite3.connect(self.sqlite_path) as conn:
                conn.execute("""
                CREATE TABLE IF NOT EXISTS audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT,
                    request_id TEXT,
                    endpoint TEXT,
                    model TEXT,
                    prompt_len INTEGER,
                    response_len INTEGER,
                    status TEXT,
                    duration_ms INTEGER,
                    stream BOOLEAN
                )
                """)
                conn.commit()


    def log(self , entry  : Dict[str , Any]) -> None:
        """
        entry expected keys:
          ts (ISO str), request_id, endpoint, model,
          prompt_len (int), response_len (int), status (str), duration_ms (int), stream (bool)
        """
        e = {
            "ts": entry.get("ts") or datetime.now().isoformat(timespec="milliseconds") + "Z",
            "request_id": entry.get("request_id", "-"),
            "endpoint": entry.get("endpoint", "-"),
            "model": entry.get("model", "-"),
            "prompt_len": int(entry.get("prompt_len", 0)),
            "response_len": int(entry.get("response_len", 0)),
            "status": entry.get("status", "ok"),
            "duration_ms": int(entry.get("duration_ms", 0)),
            "stream": bool(entry.get("stream", False)),
        }

        with self._lock:
            #JSONL
            with open(self.jsonl_path, "a", encoding="utf-8") as jf:
                jf.write(json.dumps(e,ensure_ascii=False) + "\n")

                #CSV
                if self.csv_path:
                    with open(self.csv_path, "a", newline="", encoding="utf-8") as cf:
                        writer = csv.DictWriter(cf , fieldnames = self._csv_header)
                        writer.writerow({
                        "ts": e["ts"],
                        "request_id": e["request_id"],
                        "endpoint": e["endpoint"],
                        "model": e["model"],
                        "prompt_len": e["prompt_len"],
                        "response_len": e["response_len"],
                        "status": e["status"],
                        "duration_ms": e["duration_ms"],
                        "stream": int(e["stream"]),
                        })
                

                #SQLITE
                if self.sqlite_path:
                    with sqlite3.connect(self.sqlite_path) as conn:
                        conn.execute(
                            """
                            INSERT INTO audit(ts,request_id,endpoint,model,prompt_len,response_len,status,duration_ms,stream)
                            VALUES(?,?,?,?,?,?,?,?,?)
                            """,
                            (
                                e["ts"],
                                e["request_id"],
                                e["endpoint"],
                                e["model"],
                                e["prompt_len"],
                                e["response_len"],
                                e["status"],
                                e["duration_ms"],
                                int(e["stream"]),
                            )
                        )
                        conn.commit()