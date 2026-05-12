"""
Configuration & Constants
==========================
Theme, fonts, file categories, and color palettes.
"""
import os

# ═══════════════════════════════════════════════
# COLOUR PALETTE & FONTS
# ═══════════════════════════════════════════════
DARK = {
    "bg":          "#0D1117",   # main window background
    "bg2":         "#161B22",   # card / panel background
    "bg3":         "#21262D",   # input / treeview row background
    "border":      "#30363D",   # dividers and borders
    "accent":      "#58A6FF",   # blue highlight (buttons, active)
    "accent2":     "#1F6FEB",   # darker blue for pressed states
    "success":     "#3FB950",   # green
    "warning":     "#D29922",   # amber
    "error":       "#F85149",   # red
    "purple":      "#BC8CFF",   # duplicate badge
    "fg":          "#E6EDF3",   # primary text
    "fg2":         "#8B949E",   # secondary / muted text
    "fg3":         "#484F58",   # very dim text
    "select":      "#1F6FEB33", # treeview selection
    "hover":       "#1C2128",   # button / row hover
}

LIGHT = {
    "bg":          "#F6F8FA",
    "bg2":         "#FFFFFF",
    "bg3":         "#F0F3F7",
    "border":      "#D0D7DE",
    "accent":      "#0969DA",
    "accent2":     "#0550AE",
    "success":     "#1A7F37",
    "warning":     "#9A6700",
    "error":       "#CF222E",
    "purple":      "#8250DF",
    "fg":          "#1F2328",
    "fg2":         "#636C76",
    "fg3":         "#ADBAC7",
    "select":      "#0969DA22",
    "hover":       "#EAF0F8",
}

# Active theme (start with dark)
COLORS = dict(DARK)

# ═══════════════════════════════════════════════
# FONTS
# ═══════════════════════════════════════════════
FONT_HEAD  = ("Segoe UI", 22, "bold")
FONT_TITLE = ("Segoe UI", 13, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO  = ("Consolas", 9)
FONT_BTN   = ("Segoe UI Semibold", 10, "bold")
FONT_STAT  = ("Segoe UI", 28, "bold")

# ═══════════════════════════════════════════════
# FILE CATEGORIES
# ═══════════════════════════════════════════════
CAT_ICONS = {
    "Images":    "🖼",
    "Videos":    "🎬",
    "Documents": "📄",
    "Audio":     "🎵",
    "Archives":  "📦",
    "Code":      "💻",
    "Others":    "📎",
}

FILE_CATEGORIES = {
    "Images":    [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                  ".webp", ".ico", ".tiff", ".raw"],
    "Videos":    [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv",
                  ".webm", ".m4v", ".mpeg", ".3gp"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                  ".pptx", ".txt", ".csv", ".odt", ".ods", ".odp",
                  ".rtf", ".md", ".json", ".xml", ".html", ".htm"],
    "Audio":     [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma",
                  ".m4a", ".opus", ".aiff"],
    "Archives":  [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code":      [".py", ".js", ".ts", ".java", ".c", ".cpp", ".h",
                  ".cs", ".php", ".rb", ".go", ".rs", ".swift", ".kt",
                  ".sh", ".bat", ".sql"],
}

# ═══════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cleaner_log.db")

# ═══════════════════════════════════════════════
# APP WINDOW
# ═══════════════════════════════════════════════
WINDOW_TITLE = "🧹 Smart Folder Cleaner"
DEFAULT_GEOMETRY = "1000x720"
MIN_GEOMETRY = (820, 600)
