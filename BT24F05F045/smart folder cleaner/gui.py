"""
GUI Application
===============
Main tkinter-based graphical interface for Smart Folder Cleaner.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import logging
from datetime import datetime

import config
from core import scan_folder, execute_cleaning, format_size
from database import init_db, log_to_db, fetch_logs, build_report

logger = logging.getLogger(__name__)


class SmartCleanerApp:
    """
    Main application window built with tkinter.
    Uses a notebook (tab widget) to separate the three main views:
      Tab 0 — Scan & Organize
      Tab 1 — Duplicates
      Tab 2 — Results & History
    """

    def __init__(self, root):
        self.root   = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.DEFAULT_GEOMETRY)
        self.root.minsize(*config.MIN_GEOMETRY)

        # ── State variables ──
        self.folder_path  = tk.StringVar()
        self.dark_mode    = True
        self.scan_data    = None      # last scan result dict
        self.clean_result = None      # last clean result dict
        # checkbox vars for duplicates  {hash: {filepath: BooleanVar}}
        self.dupe_vars    = {}

        init_db()
        self._build_ui()
        self._apply_theme()
        self._center_window()

    # ───────────────────────────────────────────
    # Window helpers
    # ───────────────────────────────────────────

    def _center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - w) // 2
        y  = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    # ───────────────────────────────────────────
    # Build UI
    # ───────────────────────────────────────────

    def _build_ui(self):
        # ── Root grid ──
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # ── Top nav bar ──
        self._build_navbar()

        # ── Main content (notebook tabs) ──
        self.nb = ttk.Notebook(self.root)
        self.nb.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

        self.tab_scan   = tk.Frame(self.nb)
        self.tab_dupes  = tk.Frame(self.nb)
        self.tab_result = tk.Frame(self.nb)

        self.nb.add(self.tab_scan,   text="  📂  Scan & Organize  ")
        self.nb.add(self.tab_dupes,  text="  🔁  Duplicates  ")
        self.nb.add(self.tab_result, text="  ✅  Results & History  ")

        self._build_scan_tab()
        self._build_dupes_tab()
        self._build_result_tab()

        # ── Status bar ──
        self._build_statusbar()

    # ──── Navbar ────

    def _build_navbar(self):
        nav = tk.Frame(self.root, height=56)
        nav.grid(row=0, column=0, sticky="ew")
        nav.columnconfigure(1, weight=1)
        nav.grid_propagate(False)
        self._nav = nav

        # Brand
        brand = tk.Label(nav, text="🧹  SmartCleaner",
                         font=("Segoe UI", 14, "bold"))
        brand.grid(row=0, column=0, padx=20, pady=12, sticky="w")
        self._brand_lbl = brand

        # Right-side buttons
        btn_frame = tk.Frame(nav)
        btn_frame.grid(row=0, column=2, padx=16, sticky="e")
        self._navbtn_frame = btn_frame

        self._theme_btn = self._nav_button(btn_frame, "☀  Light Mode",
                                            self._toggle_theme)
        self._history_btn = self._nav_button(btn_frame, "🕒  History",
                                              self._show_history)
        self._theme_btn.pack(side="left", padx=(0, 6))
        self._history_btn.pack(side="left")

    def _nav_button(self, parent, text, cmd):
        """Small outlined button for the navbar."""
        btn = tk.Button(parent, text=text, command=cmd,
                        font=config.FONT_SMALL, cursor="hand2",
                        relief="flat", bd=0, padx=12, pady=5)
        return btn

    # ──── Scan Tab ────

    def _build_scan_tab(self):
        tab = self.tab_scan
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

        # ── Hero heading ──
        hero = tk.Frame(tab)
        hero.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 0))
        self._hero_frame = hero

        h1 = tk.Label(hero, text="Declutter your folders, instantly.",
                       font=("Segoe UI", 18, "bold"), anchor="w")
        h1.pack(fill="x")
        self._h1 = h1

        sub = tk.Label(hero,
                       text="Enter a folder path, scan to preview changes, then confirm to clean.",
                       font=config.FONT_LABEL, anchor="w")
        sub.pack(fill="x", pady=(4, 0))
        self._sub = sub

        # ── Separator ──
        ttk.Separator(tab).grid(row=1, column=0, sticky="ew",
                                padx=24, pady=16)

        # ── Folder input row ──
        inp_frame = tk.Frame(tab)
        inp_frame.grid(row=2, column=0, sticky="ew", padx=24)
        inp_frame.columnconfigure(1, weight=1)
        self._inp_frame = inp_frame

        lbl = tk.Label(inp_frame, text="Folder Path:", font=config.FONT_LABEL)
        lbl.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self._path_lbl = lbl

        entry = tk.Entry(inp_frame, textvariable=self.folder_path,
                         font=config.FONT_MONO, relief="flat", bd=0)
        entry.grid(row=0, column=1, sticky="ew", ipady=8, padx=(0, 8))
        entry.bind("<Return>", lambda e: self._start_scan())
        self._path_entry = entry

        # Thin border frame around entry
        self._entry_border = tk.Frame(inp_frame, height=1)
        self._entry_border.grid(row=1, column=1, sticky="ew", padx=(0, 8))

        browse_btn = tk.Button(inp_frame, text="📁  Browse",
                               command=self._browse_folder,
                               font=config.FONT_BTN, cursor="hand2",
                               relief="flat", bd=0, padx=14, pady=7)
        browse_btn.grid(row=0, column=2, padx=(0, 8))
        self._browse_btn = browse_btn

        scan_btn = tk.Button(inp_frame, text="🔍  Scan Folder",
                             command=self._start_scan,
                             font=config.FONT_BTN, cursor="hand2",
                             relief="flat", bd=0, padx=18, pady=7)
        scan_btn.grid(row=0, column=3)
        self._scan_btn = scan_btn

        # ── Progress bar (hidden until scanning) ──
        self._progress_var = tk.DoubleVar()
        self._progress_bar = ttk.Progressbar(tab, variable=self._progress_var,
                                             maximum=100, mode="indeterminate")

        # ── Category preview cards ──
        cards_outer = tk.Frame(tab)
        cards_outer.grid(row=3, column=0, sticky="nsew", padx=24, pady=16)
        cards_outer.columnconfigure(0, weight=1)
        cards_outer.rowconfigure(1, weight=1)
        self._cards_outer = cards_outer

        cat_title = tk.Label(cards_outer,
                             text="Files will be organized into:",
                             font=config.FONT_TITLE, anchor="w")
        cat_title.grid(row=0, column=0, sticky="w", pady=(0, 10))
        self._cat_title = cat_title

        # Canvas + scrollbar for the card grid
        canvas = tk.Canvas(cards_outer, highlightthickness=0)
        vbar   = ttk.Scrollbar(cards_outer, orient="vertical",
                               command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        canvas.grid(row=1, column=0, sticky="nsew")
        vbar.grid(row=1, column=1, sticky="ns")
        self._cards_canvas  = canvas
        self._cards_vbar    = vbar

        self._cards_inner   = tk.Frame(canvas)
        self._cards_window  = canvas.create_window(
            (0, 0), window=self._cards_inner, anchor="nw"
        )
        self._cards_inner.bind("<Configure>", self._on_cards_configure)
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(
                        self._cards_window, width=e.width))

        # Default prompt cards
        self._render_default_cards()

        # ── Bottom action row ──
        action_row = tk.Frame(tab)
        action_row.grid(row=4, column=0, sticky="ew",
                        padx=24, pady=(0, 16))
        action_row.columnconfigure(0, weight=1)
        self._action_row = action_row

        self._scan_status = tk.Label(action_row, text="",
                                     font=config.FONT_SMALL, anchor="w")
        self._scan_status.grid(row=0, column=0, sticky="w")

        self._confirm_btn = tk.Button(
            action_row, text="✓  Confirm & Clean",
            command=self._confirm_clean,
            font=config.FONT_BTN, cursor="hand2",
            relief="flat", bd=0, padx=22, pady=9,
            state="disabled"
        )
        self._confirm_btn.grid(row=0, column=1, sticky="e")

    def _render_default_cards(self):
        """Show placeholder category cards before any scan."""
        for w in self._cards_inner.winfo_children():
            w.destroy()
        for i, (cat, icon) in enumerate(config.CAT_ICONS.items()):
            self._make_cat_card(self._cards_inner, cat, icon, "—", i)

    def _render_scan_cards(self, category_summary):
        """Populate cards with real file counts from a scan."""
        for w in self._cards_inner.winfo_children():
            w.destroy()
        if not category_summary:
            lbl = tk.Label(self._cards_inner,
                           text="No files found to organize.",
                           font=config.FONT_LABEL)
            lbl.grid(padx=8, pady=8)
            return
        for i, (cat, files) in enumerate(category_summary.items()):
            icon = config.CAT_ICONS.get(cat, "📎")
            count_str = f"{len(files)} file{'s' if len(files) != 1 else ''}"
            self._make_cat_card(self._cards_inner, cat, icon, count_str, i)

    def _make_cat_card(self, parent, name, icon, count, idx):
        """Create one category card widget."""
        col = idx % 4
        row = idx // 4
        card = tk.Frame(parent, relief="flat", bd=0, padx=14, pady=14)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        parent.columnconfigure(col, weight=1)

        icon_lbl = tk.Label(card, text=icon, font=("Segoe UI", 26))
        icon_lbl.pack()
        name_lbl = tk.Label(card, text=name, font=("Segoe UI", 10, "bold"))
        name_lbl.pack(pady=(4, 2))
        cnt_lbl  = tk.Label(card, text=count, font=config.FONT_SMALL)
        cnt_lbl.pack()

        # Store widgets for re-theming
        card._children_labels = [icon_lbl, name_lbl, cnt_lbl]
        card._is_cat_card = True
        return card

    def _on_cards_configure(self, event):
        self._cards_canvas.configure(
            scrollregion=self._cards_canvas.bbox("all")
        )

    # ──── Duplicates Tab ────

    def _build_dupes_tab(self):
        tab = self.tab_dupes
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # Header
        hdr = tk.Frame(tab)
        hdr.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 12))
        hdr.columnconfigure(1, weight=1)
        self._dupe_hdr = hdr

        title = tk.Label(hdr, text="🔁  Duplicate Files",
                         font=config.FONT_TITLE, anchor="w")
        title.grid(row=0, column=0, sticky="w")
        self._dupe_title = title

        self._dupe_info = tk.Label(
            hdr,
            text="Run a scan first to detect duplicates.",
            font=config.FONT_SMALL, anchor="e"
        )
        self._dupe_info.grid(row=0, column=2, sticky="e")

        del_btn = tk.Button(hdr, text="🗑  Delete Selected",
                            command=self._delete_selected_dupes,
                            font=config.FONT_SMALL, cursor="hand2",
                            relief="flat", bd=0, padx=10, pady=4)
        del_btn.grid(row=0, column=3, padx=(8, 0))
        self._del_btn = del_btn

        # Scrollable frame for duplicate groups
        outer = tk.Frame(tab)
        outer.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 16))
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        self._dupe_outer = outer

        dupe_canvas = tk.Canvas(outer, highlightthickness=0)
        dupe_vbar   = ttk.Scrollbar(outer, orient="vertical",
                                    command=dupe_canvas.yview)
        dupe_canvas.configure(yscrollcommand=dupe_vbar.set)
        dupe_canvas.grid(row=0, column=0, sticky="nsew")
        dupe_vbar.grid(row=0, column=1, sticky="ns")
        self._dupe_canvas = dupe_canvas
        self._dupe_vbar   = dupe_vbar

        self._dupe_inner = tk.Frame(dupe_canvas)
        self._dupe_win   = dupe_canvas.create_window(
            (0, 0), window=self._dupe_inner, anchor="nw"
        )
        self._dupe_inner.bind("<Configure>", lambda e: dupe_canvas.configure(
            scrollregion=dupe_canvas.bbox("all")))
        dupe_canvas.bind("<Configure>",
                         lambda e: dupe_canvas.itemconfig(
                             self._dupe_win, width=e.width))

        placeholder = tk.Label(self._dupe_inner,
                               text="No scan data yet. Go to 'Scan & Organize' first.",
                               font=config.FONT_LABEL)
        placeholder.pack(padx=20, pady=40)
        self._dupe_placeholder = placeholder

    def _render_dupes(self, duplicate_groups):
        """Populate the duplicates tab with checkboxes."""
        for w in self._dupe_inner.winfo_children():
            w.destroy()
        self.dupe_vars = {}

        if not duplicate_groups:
            lbl = tk.Label(self._dupe_inner,
                           text="🎉  No duplicates found! Your folder is already clean.",
                           font=("Segoe UI", 11), pady=40)
            lbl.pack()
            self._dupe_info.config(text="0 duplicate groups")
            return

        total_dupes = sum(len(g["files"]) - 1 for g in duplicate_groups)
        self._dupe_info.config(
            text=f"{len(duplicate_groups)} groups · {total_dupes} extra copies"
        )

        for gi, group in enumerate(duplicate_groups):
            self.dupe_vars[group["hash"]] = {}

            # Group header
            ghdr = tk.Frame(self._dupe_inner, pady=6)
            ghdr.pack(fill="x", padx=8, pady=(12 if gi > 0 else 4, 0))
            self._theme_widget(ghdr, "bg2")

            short_hash = group["hash"][:20] + "…"
            gh_lbl = tk.Label(
                ghdr,
                text=f"  🔁  Group {gi + 1}  —  {group['count']} identical files   "
                     f"[{short_hash}]",
                font=("Segoe UI", 9, "bold"), anchor="w", padx=8, pady=4
            )
            gh_lbl.pack(fill="x")
            self._theme_widget(gh_lbl, "bg2", fg="warning")

            # File rows
            for fi, finfo in enumerate(group["files"]):
                var = tk.BooleanVar(value=False)
                self.dupe_vars[group["hash"]][finfo["path"]] = var

                row_frame = tk.Frame(self._dupe_inner)
                row_frame.pack(fill="x", padx=8, pady=1)

                cb = tk.Checkbutton(
                    row_frame, variable=var, text="",
                    cursor="hand2", relief="flat"
                )
                cb.pack(side="left", padx=(8, 0))

                file_lbl = tk.Label(
                    row_frame,
                    text=f"  {finfo['name']}",
                    font=("Segoe UI", 10, "bold"), anchor="w"
                )
                file_lbl.pack(side="left")

                size_lbl = tk.Label(
                    row_frame,
                    text=f"  {finfo['size_str']}",
                    font=config.FONT_SMALL, anchor="w"
                )
                size_lbl.pack(side="left")

                path_lbl = tk.Label(
                    row_frame,
                    text=f"   {finfo['path']}",
                    font=config.FONT_MONO, anchor="w"
                )
                path_lbl.pack(side="left", fill="x", expand=True)

                del_btn = tk.Button(row_frame, text=" ✗ DELETE ",
                                    font=("Segoe UI", 8, "bold"),
                                    padx=6, pady=2, cursor="hand2",
                                    relief="flat", bd=0,
                                    command=lambda p=finfo["path"]: self._delete_single_dupe(p))
                del_btn.pack(side="right", padx=8)
                self._theme_widget(del_btn, "error", fg="bg")

                # Show/hide DELETE button based on checkbox
                def _on_check(v=var, btn=del_btn):
                    if v.get():
                        btn.pack(side="right", padx=8)
                    else:
                        btn.pack_forget()

                _on_check()  # init state
                var.trace_add("write", lambda *a, fn=_on_check: fn())

                self._theme_row(row_frame, file_lbl, size_lbl, path_lbl, cb)

    def _theme_row(self, frame, *labels):
        """Apply theme colours to a duplicate row."""
        frame.config(bg=config.COLORS["bg"])
        for w in labels:
            try:
                w.config(bg=config.COLORS["bg"], fg=config.COLORS["fg2"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme widget %s: %s", w.winfo_class(), e)

    def _select_all_dupes(self):
        """DEPRECATED: Kept for backward compatibility. Use _delete_selected_dupes instead."""
        for hsh in self.dupe_vars:
            for var in self.dupe_vars[hsh].values():
                var.set(True)

    def _deselect_all_dupes(self):
        """DEPRECATED: Use _delete_selected_dupes instead."""
        for hsh in self.dupe_vars:
            for var in self.dupe_vars[hsh].values():
                var.set(False)

    def _delete_selected_dupes(self):
        """Delete all selected duplicate files immediately."""
        if not self.scan_data:
            messagebox.showwarning("No Scan Data",
                                   "Please run a scan first.")
            return
        
        # Collect checked duplicate files
        files_to_delete = []
        for hsh, file_vars in self.dupe_vars.items():
            for filepath, var in file_vars.items():
                if var.get():
                    files_to_delete.append(filepath)
        
        if not files_to_delete:
            messagebox.showinfo("No Selection",
                               "Please select files to delete.")
            return
        
        # Confirmation dialog
        msg = (
            f"Delete {len(files_to_delete)} selected duplicate file(s)?\n\n"
            f"Files:\n"
        )
        for f in files_to_delete[:5]:  # Show first 5 files
            msg += f"  • {f}\n"
        if len(files_to_delete) > 5:
            msg += f"  ... and {len(files_to_delete) - 5} more\n"
        
        msg += "\nThis action CANNOT be undone."
        
        if not messagebox.askyesno("Confirm Delete", msg, icon="warning"):
            return
        
        # Delete files
        deleted_count = 0
        errors = []
        
        for filepath in files_to_delete:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    deleted_count += 1
                    # Uncheck the file
                    for hsh, file_vars in self.dupe_vars.items():
                        if filepath in file_vars:
                            file_vars[filepath].set(False)
            except Exception as e:
                errors.append(f"{os.path.basename(filepath)}: {str(e)}")
        
        # Show result
        if errors:
            messagebox.showwarning(
                "Deletion Completed with Errors",
                f"Deleted: {deleted_count} files\n\nErrors:\n" + "\n".join(errors[:5])
            )
        else:
            messagebox.showinfo(
                "Deletion Complete",
                f"Successfully deleted {deleted_count} duplicate file(s)."
            )
        
        self._set_status(f"Deleted {deleted_count} duplicate files.", "success")

    def _delete_single_dupe(self, filepath):
        """Delete a single duplicate file immediately."""
        if not os.path.exists(filepath):
            messagebox.showwarning("File Not Found",
                                   f"File no longer exists:\n{filepath}")
            return
        
        # Confirmation dialog
        filename = os.path.basename(filepath)
        msg = (
            f"Delete this duplicate file?\n\n"
            f"  {filename}\n\n"
            f"Location:\n  {filepath}\n\n"
            f"This action CANNOT be undone."
        )
        
        if not messagebox.askyesno("Confirm Delete", msg, icon="warning"):
            return
        
        # Delete file
        try:
            os.remove(filepath)
            # Uncheck the file
            for hsh, file_vars in self.dupe_vars.items():
                if filepath in file_vars:
                    file_vars[filepath].set(False)
            messagebox.showinfo("Deleted", f"File deleted successfully.\n\n{filename}")
            self._set_status(f"Deleted: {filename}", "success")
        except Exception as e:
            messagebox.showerror("Deletion Error",
                                f"Could not delete file:\n{str(e)}")
            self._set_status(f"Error deleting file: {str(e)}", "error")

    # ──── Results Tab ────

    def _build_result_tab(self):
        tab = self.tab_result
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(2, weight=1)

        # Stat cards row
        self._stats_frame = tk.Frame(tab)
        self._stats_frame.grid(row=0, column=0, sticky="ew",
                               padx=24, pady=(20, 0))

        # Treeview for result table
        tree_frame = tk.Frame(tab)
        tree_frame.grid(row=1, column=0, sticky="nsew", padx=24, pady=16)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(1, weight=1)
        self._tree_frame = tree_frame

        tree_title = tk.Label(tree_frame, text="Organization Summary",
                              font=config.FONT_TITLE, anchor="w")
        tree_title.grid(row=0, column=0, sticky="w", pady=(0, 8))
        self._tree_title = tree_title

        cols = ("folder", "count", "files")
        tree = ttk.Treeview(tree_frame, columns=cols,
                            show="headings", height=10)
        tree.heading("folder", text="📁  Folder")
        tree.heading("count",  text="#  Files")
        tree.heading("files",  text="File Names")
        tree.column("folder", width=150, minwidth=100)
        tree.column("count",  width=80,  minwidth=60, anchor="center")
        tree.column("files",  width=500, minwidth=300)
        tree.grid(row=1, column=0, sticky="nsew")
        self._result_tree = tree

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical",
                                    command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.grid(row=1, column=1, sticky="ns")

        # History section
        hist_frame = tk.Frame(tab)
        hist_frame.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 16))
        hist_frame.columnconfigure(0, weight=1)
        hist_frame.rowconfigure(1, weight=1)
        self._hist_frame = hist_frame

        hist_hdr = tk.Frame(hist_frame)
        hist_hdr.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        hist_hdr.columnconfigure(0, weight=1)
        self._hist_hdr = hist_hdr

        hist_title = tk.Label(hist_hdr, text="🕒  Cleanup History",
                              font=config.FONT_TITLE, anchor="w")
        hist_title.grid(row=0, column=0, sticky="w")
        self._hist_title = hist_title

        refresh_btn = tk.Button(hist_hdr, text="↻  Refresh",
                                command=self._load_history,
                                font=config.FONT_SMALL, cursor="hand2",
                                relief="flat", bd=0, padx=10, pady=4)
        refresh_btn.grid(row=0, column=1, sticky="e")
        self._refresh_btn = refresh_btn

        # History treeview
        h_cols = ("date", "folder", "moved", "deleted")
        h_tree = ttk.Treeview(hist_frame, columns=h_cols,
                              show="headings", height=6)
        h_tree.heading("date",    text="Date & Time")
        h_tree.heading("folder",  text="Folder")
        h_tree.heading("moved",   text="Moved")
        h_tree.heading("deleted", text="Deleted")
        h_tree.column("date",    width=150, minwidth=130)
        h_tree.column("folder",  width=400, minwidth=200)
        h_tree.column("moved",   width=80,  anchor="center")
        h_tree.column("deleted", width=80,  anchor="center")
        h_tree.grid(row=1, column=0, sticky="nsew")
        self._hist_tree = h_tree

        h_scroll = ttk.Scrollbar(hist_frame, orient="vertical",
                                 command=h_tree.yview)
        h_tree.configure(yscrollcommand=h_scroll.set)
        h_scroll.grid(row=1, column=1, sticky="ns")

        # Bottom action row
        act = tk.Frame(tab)
        act.grid(row=3, column=0, sticky="ew", padx=24, pady=(0, 16))
        act.columnconfigure(0, weight=1)
        self._result_act = act

        self._dl_report_btn = tk.Button(
            act, text="⬇  Download Report",
            command=self._download_report,
            font=config.FONT_BTN, cursor="hand2",
            relief="flat", bd=0, padx=18, pady=8
        )
        self._dl_report_btn.grid(row=0, column=1, sticky="e", padx=(8, 0))

        self._new_clean_btn = tk.Button(
            act, text="🧹  Clean Another Folder",
            command=self._reset,
            font=config.FONT_BTN, cursor="hand2",
            relief="flat", bd=0, padx=18, pady=8
        )
        self._new_clean_btn.grid(row=0, column=2, sticky="e")

        self._load_history()

    def _render_stats(self, result):
        for w in self._stats_frame.winfo_children():
            w.destroy()

        stats = [
            ("Total Processed", result.get("moved", 0) + result.get("deleted", 0), "accent"),
            ("Files Moved",     result.get("moved", 0),     "success"),
            ("Dupes Removed",   result.get("deleted", 0),   "error"),
            ("Categories",      len(result.get("result_summary",{})), "purple"),
        ]
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(self._stats_frame, padx=20, pady=16)
            card.grid(row=0, column=i, padx=(0, 12), sticky="nsew")
            self._stats_frame.columnconfigure(i, weight=1)

            num_lbl = tk.Label(card, text=str(value), font=config.FONT_STAT)
            num_lbl.pack()
            txt_lbl = tk.Label(card, text=label, font=config.FONT_SMALL)
            txt_lbl.pack()

            self._theme_widget(card, "bg2")
            self._theme_widget(num_lbl, "bg2", fg=color)
            self._theme_widget(txt_lbl, "bg2", fg="fg2")

    def _render_result_tree(self, result_summary):
        for row in self._result_tree.get_children():
            self._result_tree.delete(row)
        for cat, files in result_summary.items():
            icon  = config.CAT_ICONS.get(cat, "📎")
            files_str = ",  ".join(files)
            self._result_tree.insert("", "end",
                values=(f"{icon}  {cat}",
                        len(files), files_str))

    def _load_history(self):
        for row in self._hist_tree.get_children():
            self._hist_tree.delete(row)
        logs = fetch_logs()
        if not logs:
            self._hist_tree.insert("", "end",
                values=("—", "No history yet", "—", "—"))
            return
        for log in logs:
            self._hist_tree.insert("", "end", values=(
                log.get("created_at", ""),
                log.get("folder_path", ""),
                log.get("files_moved", 0),
                log.get("dupes_removed", 0),
            ))

    # ──── Status Bar ────

    def _build_statusbar(self):
        bar = tk.Frame(self.root, height=28)
        bar.grid(row=2, column=0, sticky="ew")
        bar.grid_propagate(False)
        self._statusbar = bar

        self._status_lbl = tk.Label(bar, text="Ready  ·  Enter a folder path to begin.",
                                    font=config.FONT_SMALL, anchor="w")
        self._status_lbl.pack(side="left", padx=16, pady=4)

        self._status_dot = tk.Label(bar, text="●", font=config.FONT_SMALL)
        self._status_dot.pack(side="right", padx=16)

    def _set_status(self, text, dot_color="success"):
        self._status_lbl.config(text=text)
        self._status_dot.config(fg=config.COLORS[dot_color])

    # ═══════════════════════════════════════════
    # ACTIONS
    # ═══════════════════════════════════════════

    def _browse_folder(self):
        path = filedialog.askdirectory(title="Select a folder to clean")
        if path:
            self.folder_path.set(path)

    def _start_scan(self):
        path = self.folder_path.get().strip()
        if not path:
            messagebox.showwarning("No Path", "Please enter or browse to a folder path.")
            return
        if not os.path.isdir(path):
            messagebox.showerror("Invalid Path",
                                 f"This path does not exist or is not a folder:\n{path}")
            return
        if not os.access(path, os.R_OK):
            messagebox.showerror("Permission Denied",
                                 "Python cannot read this folder. Check permissions.")
            return

        # Disable UI, show progress
        self._scan_btn.config(state="disabled", text="⏳  Scanning…")
        self._confirm_btn.config(state="disabled")
        self._set_status("Scanning…  Computing MD5 hashes for all files…", "warning")
        self._progress_bar.grid(row=2, column=0, columnspan=4,
                                sticky="ew", padx=0, pady=(8, 0),
                                in_=self._inp_frame)
        self._progress_bar.start(12)

        # Run in background thread so the GUI stays responsive
        threading.Thread(target=self._scan_worker, args=(path,),
                         daemon=True).start()

    def _scan_worker(self, path):
        """Background thread: runs scan and posts results to GUI."""
        result = scan_folder(path)
        # Schedule GUI update on main thread
        self.root.after(0, self._on_scan_done, result)

    def _on_scan_done(self, result):
        """Called on main thread when scan finishes."""
        self._progress_bar.stop()
        self._progress_bar.grid_forget()
        self._scan_btn.config(state="normal", text="🔍  Scan Folder")

        if "error" in result:
            messagebox.showerror("Scan Error", result["error"])
            self._set_status(f"Error: {result['error']}", "error")
            return

        self.scan_data = result
        n = result["total_files"]
        d = result["duplicate_count"]

        # Update category cards
        self._render_scan_cards(result["category_summary"])

        # Update duplicates tab
        self._render_dupes(result["duplicate_groups"])

        # Enable confirm button
        self._confirm_btn.config(state="normal")

        self._scan_status.config(
            text=f"Found  {n} file{'s' if n!=1 else ''}  ·  "
                 f"{d} duplicate{'s' if d!=1 else ''}  ·  Ready to clean"
        )
        self._set_status(
            f"Scan complete  ·  {n} files found  ·  {d} duplicates  ·  "
            f"Check 'Duplicates' tab, then click Confirm.",
            "success"
        )

        # Switch to scan tab to show results
        self.nb.select(0)

    def _confirm_clean(self):
        if not self.scan_data:
            messagebox.showwarning("Not Scanned",
                                   "Please scan a folder first.")
            return

        path = self.scan_data["folder"]

        # Collect checked duplicate hashes
        delete_hashes = set()
        for hsh, file_vars in self.dupe_vars.items():
            if any(v.get() for v in file_vars.values()):
                delete_hashes.add(hsh)

        # Safety confirmation
        n       = self.scan_data["total_files"]
        n_del   = sum(1 for h, fv in self.dupe_vars.items()
                      for v in fv.values() if v.get())
        msg = (
            f"You are about to:\n\n"
            f"  • Organize {n} files into category subfolders\n"
            f"  • Permanently delete {n_del} selected duplicate file(s)\n\n"
            f"Folder:  {path}\n\n"
            f"This CANNOT be undone. Continue?"
        )
        if not messagebox.askyesno("Confirm Cleaning", msg, icon="warning"):
            return

        self._confirm_btn.config(state="disabled", text="⏳  Cleaning…")
        self._scan_btn.config(state="disabled")
        self._set_status("Cleaning in progress…  Moving files…", "warning")

        threading.Thread(
            target=self._clean_worker,
            args=(path, delete_hashes),
            daemon=True
        ).start()

    def _clean_worker(self, path, delete_hashes):
        result = execute_cleaning(path, delete_hashes)
        # Log to database
        summary_json = str({
            "moved": result.get("moved", 0),
            "deleted": result.get("deleted", 0),
            "categories": {k: len(v) for k, v in result.get("result_summary", {}).items()}
        })
        log_to_db(path, result.get("moved", 0), result.get("deleted", 0), summary_json)
        self.root.after(0, self._on_clean_done, result)

    def _on_clean_done(self, result):
        self._confirm_btn.config(state="normal", text="✓  Confirm & Clean")
        self._scan_btn.config(state="normal")

        if "error" in result:
            messagebox.showerror("Cleaning Error", result["error"])
            self._set_status(f"Error: {result['error']}", "error")
            return

        self.clean_result = result
        self._render_stats(result)
        self._render_result_tree(result["result_summary"])
        self._load_history()

        m = result.get("moved", 0)
        d = result.get("deleted", 0)
        self._set_status(
            f"✅  Done!  {m} files moved  ·  {d} duplicates deleted.",
            "success"
        )

        if result.get("errors"):
            errs = "\n".join(f"• {e['file']}: {e['error']}"
                             for e in result["errors"])
            messagebox.showwarning("Some Errors Occurred",
                                   f"The following files had issues:\n\n{errs}")

        # Switch to Results tab
        self.nb.select(2)
        messagebox.showinfo(
            "Cleaning Complete",
            f"✅  Done!\n\n"
            f"Files moved   : {m}\n"
            f"Dupes deleted : {d}\n\n"
            f"See the Results tab for details."
        )

    def _download_report(self):
        if not self.clean_result:
            messagebox.showinfo("No Results",
                                "Clean a folder first to generate a report.")
            return
        report_text = build_report(
            self.scan_data["folder"] if self.scan_data else "Unknown",
            self.clean_result
        )
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"cleaning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            title="Save Cleaning Report"
        )
        if not save_path:
            return
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            messagebox.showinfo("Report Saved", f"Report saved to:\n{save_path}")
            self._set_status(f"Report saved: {save_path}", "success")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def _reset(self):
        self.folder_path.set("")
        self.scan_data    = None
        self.clean_result = None
        self.dupe_vars    = {}
        self._render_default_cards()
        self._scan_status.config(text="")
        self._confirm_btn.config(state="disabled")
        for w in self._dupe_inner.winfo_children():
            w.destroy()
        tk.Label(self._dupe_inner,
                 text="No scan data yet. Go to 'Scan & Organize' first.",
                 font=config.FONT_LABEL).pack(padx=20, pady=40)
        for row in self._result_tree.get_children():
            self._result_tree.delete(row)
        for w in self._stats_frame.winfo_children():
            w.destroy()
        self.nb.select(0)
        self._set_status("Ready  ·  Enter a folder path to begin.")

    def _show_history(self):
        """Open a popup with cleanup history."""
        win = tk.Toplevel(self.root)
        win.title("Cleanup History")
        win.geometry("700x400")
        win.configure(bg=config.COLORS["bg"])
        win.grab_set()

        tk.Label(win, text="🕒  Cleanup History",
                 font=config.FONT_TITLE, bg=config.COLORS["bg"], fg=config.COLORS["fg"]
                 ).pack(padx=20, pady=(16, 8), anchor="w")

        cols = ("date", "folder", "moved", "deleted")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=14)
        tree.heading("date",    text="Date & Time")
        tree.heading("folder",  text="Folder")
        tree.heading("moved",   text="Moved")
        tree.heading("deleted", text="Deleted")
        tree.column("date",    width=140)
        tree.column("folder",  width=360)
        tree.column("moved",   width=70, anchor="center")
        tree.column("deleted", width=70, anchor="center")
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        logs = fetch_logs()
        if not logs:
            tree.insert("", "end", values=("—", "No history yet", "—", "—"))
        for log in logs:
            tree.insert("", "end", values=(
                log.get("created_at", ""),
                log.get("folder_path", ""),
                log.get("files_moved", 0),
                log.get("dupes_removed", 0),
            ))

    # ═══════════════════════════════════════════
    # THEMING
    # ═══════════════════════════════════════════

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        config.COLORS.clear()
        config.COLORS.update(config.DARK if self.dark_mode else config.LIGHT)
        self._theme_btn.config(
            text="☀  Light Mode" if self.dark_mode else "🌙  Dark Mode"
        )
        self._apply_theme()

    def _apply_theme(self):
        """Re-colour every widget in the window."""
        self.root.configure(bg=config.COLORS["bg"])

        # ttk style overrides
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook",
                        background=config.COLORS["bg"], borderwidth=0,
                        tabmargins=[0, 6, 0, 0])
        style.configure("TNotebook.Tab",
                        background=config.COLORS["bg2"], foreground=config.COLORS["fg2"],
                        padding=[14, 8], font=config.FONT_LABEL,
                        borderwidth=0)
        style.map("TNotebook.Tab",
                  background=[("selected", config.COLORS["bg"]),
                               ("active", config.COLORS["hover"])],
                  foreground=[("selected", config.COLORS["accent"]),
                               ("active",   config.COLORS["fg"])])

        style.configure("Treeview",
                        background=config.COLORS["bg2"], foreground=config.COLORS["fg"],
                        fieldbackground=config.COLORS["bg2"], rowheight=26,
                        font=config.FONT_SMALL, borderwidth=0)
        style.configure("Treeview.Heading",
                        background=config.COLORS["bg3"], foreground=config.COLORS["fg2"],
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Treeview",
                  background=[("selected", config.COLORS["accent2"])],
                  foreground=[("selected", "#ffffff")])

        style.configure("Vertical.TScrollbar",
                        background=config.COLORS["bg3"], troughcolor=config.COLORS["bg"],
                        arrowcolor=config.COLORS["fg3"], borderwidth=0)
        style.configure("TProgressbar",
                        troughcolor=config.COLORS["bg3"], background=config.COLORS["accent"],
                        borderwidth=0)
        style.configure("TSeparator", background=config.COLORS["border"])

        # Colour all our custom frames/labels
        self._colour_tree(self.root)

    def _colour_tree(self, widget):
        """Recursively apply theme colours to all tk widgets."""
        wtype = widget.winfo_class()

        # Frames
        if wtype in ("Frame", "Labelframe"):
            try:
                widget.config(bg=config.COLORS["bg"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme Frame %s: %s", widget, e)

        # Labels
        elif wtype == "Label":
            try:
                widget.config(bg=config.COLORS["bg"], fg=config.COLORS["fg"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme Label %s: %s", widget, e)

        # Buttons
        elif wtype == "Button":
            try:
                widget.config(bg=config.COLORS["bg3"], fg=config.COLORS["fg"],
                              activebackground=config.COLORS["hover"],
                              activeforeground=config.COLORS["accent"],
                              highlightbackground=config.COLORS["border"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme Button %s: %s", widget, e)

        # Entry
        elif wtype == "Entry":
            try:
                widget.config(bg=config.COLORS["bg3"], fg=config.COLORS["fg"],
                              insertbackground=config.COLORS["accent"],
                              selectbackground=config.COLORS["accent2"],
                              disabledbackground=config.COLORS["bg2"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme Entry %s: %s", widget, e)

        # Checkbutton
        elif wtype == "Checkbutton":
            try:
                widget.config(bg=config.COLORS["bg"], fg=config.COLORS["fg"],
                              activebackground=config.COLORS["bg"],
                              activeforeground=config.COLORS["accent"],
                              selectcolor=config.COLORS["bg3"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme Checkbutton %s: %s", widget, e)

        # Canvas
        elif wtype == "Canvas":
            try:
                widget.config(bg=config.COLORS["bg"])
            except (tk.TclError, KeyError) as e:
                logger.debug("Could not theme Canvas %s: %s", widget, e)

        # Special overrides for named widgets
        try:
            if widget is self._nav:
                widget.config(bg=config.COLORS["bg2"])
            elif widget is self._navbtn_frame:
                widget.config(bg=config.COLORS["bg2"])
            elif widget is self._brand_lbl:
                widget.config(bg=config.COLORS["bg2"], fg=config.COLORS["accent"])
            elif widget is self._statusbar:
                widget.config(bg=config.COLORS["bg2"])
            elif widget is self._status_lbl:
                widget.config(bg=config.COLORS["bg2"], fg=config.COLORS["fg2"])
            elif widget is self._status_dot:
                widget.config(bg=config.COLORS["bg2"])
            elif widget is self._scan_btn:
                widget.config(bg=config.COLORS["accent"], fg="#000000",
                              activebackground=config.COLORS["accent2"],
                              activeforeground="#ffffff")
            elif widget is self._confirm_btn:
                widget.config(bg=config.COLORS["success"], fg="#000000",
                              activebackground=config.COLORS["success"])
            elif widget is self._browse_btn:
                widget.config(bg=config.COLORS["bg3"], fg=config.COLORS["fg"])
            elif widget is self._dl_report_btn:
                widget.config(bg=config.COLORS["bg3"], fg=config.COLORS["fg"])
            elif widget is self._new_clean_btn:
                widget.config(bg=config.COLORS["accent"], fg="#000000",
                              activebackground=config.COLORS["accent2"])
            elif widget is self._theme_btn:
                widget.config(bg=config.COLORS["bg2"], fg=config.COLORS["fg2"],
                              activebackground=config.COLORS["hover"])
            elif widget is self._history_btn:
                widget.config(bg=config.COLORS["bg2"], fg=config.COLORS["fg2"],
                              activebackground=config.COLORS["hover"])
            elif widget is self._h1:
                widget.config(fg=config.COLORS["fg"])
            elif widget is self._sub:
                widget.config(fg=config.COLORS["fg2"])
            elif widget is self._entry_border:
                widget.config(bg=config.COLORS["border"])
            elif widget is self._scan_status:
                widget.config(fg=config.COLORS["fg2"])
            elif widget is self._dupe_info:
                widget.config(fg=config.COLORS["fg2"])
            elif widget is self._cat_title:
                widget.config(fg=config.COLORS["fg"])
            elif widget is self._tree_title:
                widget.config(fg=config.COLORS["fg"])
            elif widget is self._hist_title:
                widget.config(fg=config.COLORS["fg"])
        except (tk.TclError, KeyError, AttributeError) as e:
            logger.debug("Could not apply special theme override: %s", e)

        # Cat cards
        if hasattr(widget, "_is_cat_card"):
            widget.config(bg=config.COLORS["bg2"])
            for lbl in getattr(widget, "_children_labels", []):
                lbl.config(bg=config.COLORS["bg2"], fg=config.COLORS["fg"])

        # Recurse
        for child in widget.winfo_children():
            self._colour_tree(child)

    def _theme_widget(self, widget, bg_key, fg=None):
        """Quick helper to set bg/fg from colour key strings."""
        try:
            widget.config(bg=config.COLORS[bg_key])
            if fg:
                widget.config(fg=config.COLORS[fg])
        except (tk.TclError, KeyError) as e:
            logger.debug("Could not theme widget %s: %s", widget.winfo_class(), e)
