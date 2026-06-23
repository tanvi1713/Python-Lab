"""
Core Logic Functions
====================
File scanning, categorization, hashing, and cleaning operations.
"""
import os
import shutil
import hashlib
import json
from pathlib import Path
from config import FILE_CATEGORIES


def get_file_category(filename):
    """Return category name for a given filename based on extension."""
    ext = os.path.splitext(filename)[1].lower()
    for category, exts in FILE_CATEGORIES.items():
        if ext in exts:
            return category
    return "Others"


def compute_hash(filepath):
    """SHA-256 hash a file in 8 KB chunks. Returns hex string or None on error."""
    try:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def format_size(size_bytes):
    """Convert bytes to a human-readable string like '3.2 MB'."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def scan_folder(folder_path):
    """
    Scan folder_path (top level only).
    Returns a dict with:
      files, duplicate_groups, category_summary, errors
    Does NOT modify anything on disk.
    """
    folder_path = os.path.realpath(folder_path)
    if not os.path.isdir(folder_path):
        return {"error": "Path is not a valid directory"}
    try:
        entries = os.listdir(folder_path)
    except PermissionError:
        return {"error": "Permission denied reading this folder"}

    files_info  = []
    hash_map    = {}   # md5 -> [file_entry, ...]
    errors      = []

    for filename in entries:
        filepath = os.path.join(folder_path, filename)
        if os.path.isdir(filepath) or filename.startswith("."):
            continue
        try:
            size      = os.path.getsize(filepath)
            category  = get_file_category(filename)
            file_hash = compute_hash(filepath)
            entry = {
                "name":     filename,
                "path":     filepath,
                "size":     size,
                "size_str": format_size(size),
                "category": category,
                "hash":     file_hash,
            }
            files_info.append(entry)
            if file_hash:
                hash_map.setdefault(file_hash, []).append(entry)
        except (OSError, PermissionError) as e:
            errors.append({"file": filename, "error": str(e)})

    duplicate_groups = [
        {"hash": h, "files": grp, "count": len(grp)}
        for h, grp in hash_map.items() if len(grp) > 1
    ]

    category_summary = {}
    for f in files_info:
        category_summary.setdefault(f["category"], []).append(f["name"])

    return {
        "folder":           folder_path,
        "total_files":      len(files_info),
        "files":            files_info,
        "duplicate_groups": duplicate_groups,
        "duplicate_count":  sum(len(g["files"]) - 1 for g in duplicate_groups),
        "category_summary": category_summary,
        "errors":           errors,
    }


def execute_cleaning(folder_path, delete_hashes):
    """
    Move files into category subfolders and delete selected duplicates.
    delete_hashes: set of SHA-256 hashes whose files the user chose to remove.
    Returns result summary dict.
    """
    folder_path = os.path.realpath(folder_path)
    if not os.path.isdir(folder_path):
        return {"error": "Folder no longer exists"}
    try:
        entries = os.listdir(folder_path)
    except PermissionError:
        return {"error": "Permission denied"}

    moved, deleted = 0, 0
    result_summary = {}
    errors = []

    # Pass 1: find which files to delete
    files_to_delete = set()
    if delete_hashes:
        for filename in entries:
            fp = os.path.join(folder_path, filename)
            if os.path.isfile(fp) and not filename.startswith("."):
                fhash = compute_hash(fp)
                if fhash in delete_hashes:
                    files_to_delete.add(fp)

    # Pass 2: delete then move
    for filename in entries:
        filepath = os.path.join(folder_path, filename)
        if not os.path.isfile(filepath) or filename.startswith("."):
            continue

        if filepath in files_to_delete:
            try:
                os.remove(filepath)
                deleted += 1
            except (OSError, PermissionError) as e:
                errors.append({"file": filename, "error": f"Delete failed: {e}"})
            continue

        category    = get_file_category(filename)
        dest_folder = os.path.join(folder_path, category)
        try:
            os.makedirs(dest_folder, exist_ok=True)
            dest_path = os.path.join(dest_folder, filename)
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                dest_path = os.path.join(dest_folder, f"{base}_copy{ext}")
            shutil.move(filepath, dest_path)
            moved += 1
            result_summary.setdefault(category, []).append(filename)
        except (OSError, PermissionError, shutil.Error) as e:
            errors.append({"file": filename, "error": str(e)})

    return {
        "moved":          moved,
        "deleted":        deleted,
        "result_summary": result_summary,
        "errors":         errors,
    }
