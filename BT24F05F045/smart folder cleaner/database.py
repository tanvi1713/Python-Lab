"""
Database Operations
===================
SQLite logging, history, and report generation.
"""
import sqlite3
import json
import logging
from datetime import datetime
from config import DB_PATH, CAT_ICONS

logger = logging.getLogger(__name__)


def init_db():
    """Initialize the SQLite database with the cleanup_logs table."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cleanup_logs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_path   TEXT    NOT NULL,
            files_moved   INTEGER DEFAULT 0,
            dupes_removed INTEGER DEFAULT 0,
            summary       TEXT,
            created_at    TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()


def log_to_db(folder_path, moved, deleted, summary):
    """Log a cleanup operation to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO cleanup_logs (folder_path,files_moved,dupes_removed,summary) VALUES(?,?,?,?)",
            (folder_path, moved, deleted, summary)
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.warning("Failed to log cleanup to database: %s", e)


def fetch_logs(limit=30):
    """Fetch the most recent cleanup logs from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"SELECT * FROM cleanup_logs ORDER BY created_at DESC LIMIT {limit}"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        logger.warning("Failed to fetch logs from database: %s", e)
        return []


def build_report(folder_path, result):
    """
    Generate a human-readable text report from a cleaning result.
    
    Args:
        folder_path: The folder that was cleaned
        result: The result dict from execute_cleaning()
    
    Returns:
        Multi-line string report
    """
    # Build result_table from result_summary if needed
    result_table = [
        {"folder": cat, "file_count": len(fnames), "files": fnames}
        for cat, fnames in result.get("result_summary", {}).items()
    ]

    lines = [
        "=" * 54,
        "   SMART FOLDER CLEANER  —  Cleaning Report",
        "=" * 54,
        f"Folder    : {folder_path}",
        f"Date      : {datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}",
        f"Moved     : {result.get('moved', 0)} files",
        f"Deleted   : {result.get('deleted', 0)} duplicates",
        "",
        "-" * 54,
        "Category Breakdown",
        "-" * 54,
    ]
    for row in result_table:
        lines.append(f"\n  {CAT_ICONS.get(row['folder'],'📁')}  {row['folder']}  ({row['file_count']} files)")
        for f in row.get("files", []):
            lines.append(f"       •  {f}")
    
    if result.get("errors"):
        lines += ["", "-" * 54, "Errors / Warnings", "-" * 54]
        for e in result["errors"]:
            lines.append(f"  ✗  {e['file']} : {e['error']}")
    
    lines += ["", "=" * 54, "  End of Report", "=" * 54]
    return "\n".join(lines)
