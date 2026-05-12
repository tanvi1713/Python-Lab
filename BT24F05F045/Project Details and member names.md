
PROJECT NAME-
# Smart Folder Cleaner

Member Names- Tanvi Pardeshi(BT24F05F045)
Sheetal Nimbarte(BT24F05F043)

A professional GUI application built entirely with Python's built-in tkinter library. No Flask, no web browser, no external packages needed.

## Project Structure

The application is organized into separate modules for maintainability:

```
smart_cleaner_app/
├── main.py              # Entry point (run this to start the app)
├── config.py            # Constants, themes, fonts, and file categories
├── core.py              # Core logic: scanning, hashing, categorization
├── database.py          # SQLite operations: logging and reporting
├── gui.py               # Tkinter GUI application (SmartCleanerApp class)
└── README.md            # This file
```

### Module Descriptions

#### `main.py` – Entry Point
- Main script to run the application
- Initializes the Tkinter root window
- Sets up high-DPI support for Windows
- Creates and runs the `SmartCleanerApp`

#### `config.py` – Configuration & Constants
- **Themes**: `DARK` and `LIGHT` color palettes
- **Fonts**: Typography definitions (headings, labels, buttons, etc.)
- **File Categories**: Icon mappings and file extension groups
- **Database**: Path to the SQLite log file
- **Window Settings**: Default geometry and minimum window size

#### `core.py` – Core Business Logic
- `get_file_category(filename)` – Categorize files by extension
- `compute_hash(filepath)` – Generate MD5 hash for files
- `format_size(size_bytes)` – Human-readable file sizes
- `scan_folder(folder_path)` – Scan and analyze folder contents
- `execute_cleaning(folder_path, delete_hashes)` – Organize and delete files

#### `database.py` – Database Operations
- `init_db()` – Create the SQLite cleanup_logs table
- `log_to_db(...)` – Record a cleanup operation
- `fetch_logs(limit)` – Retrieve recent cleanup history
- `build_report(folder_path, result)` – Generate text report

#### `gui.py` – GUI Application
- `SmartCleanerApp` class – Main application window
- **Three Tabs**:
  - **Scan & Organize**: Browse folders, preview changes
  - **Duplicates**: Select duplicate files to delete
  - **Results & History**: View cleanup summaries and past operations
- **Features**:
  - Dark/light theme toggle
  - Category-based file organization
  - Duplicate detection via MD5 hashing
  - History tracking and reports
  - Multi-threaded scanning and cleaning

## Running the Application

### Requirements
- Python 3.8+
- tkinter (included with Python)

### Quick Start

```bash
# Navigate to the project directory
cd smart_cleaner_app

# Run the application
python main.py
```

## Features

✅ **Scan & Organize**
- Browse and select a folder
- Preview files to be organized
- See category breakdown before committing

✅ **Duplicate Detection**
- MD5 hashing for accurate duplicate detection
- Checkbox selection for which duplicates to remove
- File size and path information displayed

✅ **Safe Cleaning**
- Confirmation dialog before any changes
- Files moved into category subfolders (Images/, Videos/, etc.)
- Error handling and logging

✅ **Dark/Light Mode**
- Toggle between professional dark and light themes
- Consistent design across all views

✅ **History & Reports**
- SQLite database tracks all cleanup operations
- Generate downloadable text reports
- View 30 most recent operations

✅ **Multi-threaded**
- Scanning and cleaning run in background threads
- GUI remains responsive during operations

## File Categories

- **Images**: jpg, jpeg, png, gif, bmp, svg, webp, ico, tiff, raw
- **Videos**: mp4, avi, mkv, mov, wmv, flv, webm, m4v, mpeg, 3gp
- **Documents**: pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv, json, xml, html, and more
- **Audio**: mp3, wav, aac, flac, ogg, wma, m4a, opus, aiff
- **Archives**: zip, rar, 7z, tar, gz, bz2, xz
- **Code**: py, js, ts, java, c, cpp, h, cs, php, rb, go, rs, swift, kt, sh, bat, sql
- **Others**: All remaining files

## Architecture Notes

### Separation of Concerns
- **config.py**: All theme/UX constants in one place
- **core.py**: Pure business logic, no GUI dependencies
- **database.py**: All persistence operations
- **gui.py**: Only tkinter UI code
- **main.py**: Bootstrap and entry point

### Threading
- Scan and clean operations run on daemon threads
- GUI callbacks scheduled on main thread via `root.after()`
- Prevents UI freezing during long operations

### Theming
- Global `config.COLORS` dictionary updated on theme toggle
- Recursive widget traversal to re-theme entire tree
- Special handling for specific widgets and component types

## Future Enhancements

- Configuration file for user preferences
- Undo/restore functionality
- Scheduled cleaning
- Folder monitoring
- Custom category rules
- File preview (thumbnails, metadata)

## License

This project is provided as-is for educational and personal use.
