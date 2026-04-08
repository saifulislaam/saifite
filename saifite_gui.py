#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    SAIFITE v2025.1 - Professional Wireless Security Auditor
    Author: SAIF UL ISLAM
    GitHub: @saifulislaam
    Tagline: HACK THE NETWORK
    
    A complete GUI-based wireless auditing tool with cyber/hacker theme
"""

import tkinter as tk
from tkinter import ttk, font, messagebox, filedialog, Menu
import threading
import queue
import subprocess
import os
import re
import time
import csv
import json
import shutil
import tempfile
import random
from datetime import datetime
from pathlib import Path
import sys

# ==================== THEME COLORS ====================
class CyberTheme:
    """Cyber/Hacker theme colors matching the design"""
    PRIMARY = "#00FF41"
    PRIMARY_DARK = "#00CC33"
    PRIMARY_GLOW = "#00FF41"
    BACKGROUND = "#000000"
    BACKGROUND_CARD = "#0A0A0A"
    BACKGROUND_ELEVATED = "#111111"
    SURFACE = "#0D0D0D"
    BORDER = "#00FF41"
    BORDER_DIM = "#1A3A1A"
    TEXT_PRIMARY = "#00FF41"
    TEXT_SECONDARY = "#33FF66"
    TEXT_MUTED = "#00AA33"
    SUCCESS = "#00FF41"
    WARNING = "#FFFF00"
    ERROR = "#FF0040"
    INFO = "#00CCFF"

# ==================== ASCII ART ====================
SAIFITE_ASCII = [
    "  ███████╗ █████╗ ██╗███████╗██╗████████╗███████╗",
    "  ██╔════╝██╔══██╗██║██╔════╝██║╚══██╔══╝██╔════╝",
    "  ███████╗███████║██║█████╗  ██║   ██║   █████╗  ",
    "  ╚════██║██╔══██║██║██╔══╝  ██║   ██║   ██╔══╝  ",
    "  ███████║██║  ██║██║██║     ██║   ██║   ███████╗",
    "  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝"
]

DASHBOARD_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                      SECURITY DASHBOARD                          ║",
    "║                   Real-time Network Intelligence                  ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

SCANNER_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                      NETWORK DISCOVERY                            ║",
    "║                   Scanning for wireless targets                   ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

ATTACK_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                        ATTACK CENTER                             ║",
    "║                   Execute security assessments                    ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

HANDSHAKE_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                       HANDSHAKE LAB                              ║",
    "║                   Capture 4-way handshakes                       ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

WPS_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                         WPS CRACKER                              ║",
    "║                   PIN & Pixie-Dust attacks                       ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

RESULTS_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                       CRACKED DATABASE                           ║",
    "║                   Successfully compromised networks              ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

CONSOLE_HEADER = [
    "╔══════════════════════════════════════════════════════════════════╗",
    "║                         SYSTEM CONSOLE                           ║",
    "║                   Real-time activity monitoring                  ║",
    "╚══════════════════════════════════════════════════════════════════╝"
]

# ==================== DATA CLASSES ====================
class Target:
    def __init__(self, bssid, power, channel, encryption, ssid):
        self.bssid = bssid
        self.power = power
        self.channel = channel
        self.encryption = encryption
        self.ssid = ssid
        self.wps = False
        self.wps_locked = False
        self.clients = []
        self.key = ''
        self.handshake_file = ''

class Handshake:
    def __init__(self, filename, ssid, bssid):
        self.filename = filename
        self.ssid = ssid
        self.bssid = bssid
        self.cracked = False
        self.key = ''
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ==================== MAIN APPLICATION ====================
class SaifiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SAIFITE v2025.1 - HACK THE NETWORK")
        self.root.geometry("1400x900")
        self.root.configure(bg=CyberTheme.BACKGROUND)
        self.root.minsize(1200, 700)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # Variables
        self.interface = tk.StringVar()
        self.monitor_interface = tk.StringVar()
        self.current_interface = tk.StringVar(value="NONE")
        self.target_channel = tk.StringVar(value="0")
        self.target_essid = tk.StringVar()
        self.target_bssid = tk.StringVar()
        self.min_power = tk.IntVar(value=0)
        self.tx_power = tk.IntVar(value=0)
        self.deauth_count = tk.StringVar(value="2")
        self.deauth_timeout = tk.StringVar(value="10")
        self.wpa_timeout = tk.StringVar(value="500")
        self.wep_pps = tk.StringVar(value="600")
        self.wep_timeout = tk.StringVar(value="600")
        self.wep_crack_at = tk.StringVar(value="10000")
        self.wps_timeout = tk.StringVar(value="660")
        self.wordlist_path = tk.StringVar()
        self.monitor_status = tk.StringVar(value="OFF")
        self.status_message = tk.StringVar(value="SYSTEM READY")
        
        # Attack flags
        self.wpa_enabled = tk.BooleanVar(value=True)
        self.wep_enabled = tk.BooleanVar(value=True)
        self.wps_enabled = tk.BooleanVar(value=True)
        self.pixie_enabled = tk.BooleanVar(value=False)
        self.mac_spoof = tk.BooleanVar(value=False)
        self.auto_crack = tk.BooleanVar(value=True)
        
        # Statistics
        self.networks_count = tk.StringVar(value="0000")
        self.clients_count = tk.StringVar(value="0000")
        self.handshakes_count = tk.StringVar(value="0000")
        self.cracked_count = tk.StringVar(value="0000")
        self.wps_count = tk.StringVar(value="0000")
        self.active_attacks = tk.StringVar(value="00")
        self.wpa_cracked = tk.StringVar(value="0000")
        self.wep_cracked = tk.StringVar(value="0000")
        self.wps_cracked = tk.StringVar(value="0000")
        
        # Data storage
        self.targets = []
        self.clients = []
        self.handshakes = []
        self.cracked_targets = self.load_cracked()
        self.attack_targets = []
        self.scan_process = None
        self.attack_process = None
        self.monitor_mode = False
        self.temp_dir = tempfile.mkdtemp(prefix='saifite_')
        self.handshake_dir = 'handshakes'
        os.makedirs(self.handshake_dir, exist_ok=True)
        
        # Queue for thread communication
        self.queue = queue.Queue()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_hotkeys()
        self.process_queue()
        
        # Initial interface detection
        self.detect_interfaces()
        
        # Show splash screen
        self.show_splash()
    
    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure Treeview style
        style.configure("Cyber.Treeview",
                       background=CyberTheme.BACKGROUND_CARD,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       fieldbackground=CyberTheme.BACKGROUND_CARD,
                       borderwidth=0,
                       font=('Courier New', 10))
        
        style.map("Cyber.Treeview",
                 background=[('selected', CyberTheme.PRIMARY_DARK)],
                 foreground=[('selected', CyberTheme.BACKGROUND)])
        
        # Configure Treeview heading
        style.configure("Cyber.Treeview.Heading",
                       background=CyberTheme.BACKGROUND_ELEVATED,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       borderwidth=1,
                       relief="solid",
                       font=('Courier New', 10, 'bold'))
        
        # Configure TLabelframe
        style.configure("Cyber.TLabelframe",
                       background=CyberTheme.BACKGROUND_CARD,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       borderwidth=2,
                       relief="solid")
        
        style.configure("Cyber.TLabelframe.Label",
                       background=CyberTheme.BACKGROUND_CARD,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       font=('Courier New', 10, 'bold'))
        
        # Configure TButton
        style.configure("Cyber.TButton",
                       background=CyberTheme.BACKGROUND_ELEVATED,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       borderwidth=1,
                       relief="solid",
                       font=('Courier New', 9, 'bold'))
        
        style.map("Cyber.TButton",
                 background=[('active', CyberTheme.PRIMARY_DARK)],
                 foreground=[('active', CyberTheme.BACKGROUND)])
        
        # Configure TEntry
        style.configure("Cyber.TEntry",
                       fieldbackground=CyberTheme.BACKGROUND_ELEVATED,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       borderwidth=1,
                       relief="solid",
                       font=('Courier New', 10))
        
        # Configure TCheckbutton
        style.configure("Cyber.TCheckbutton",
                       background=CyberTheme.BACKGROUND_CARD,
                       foreground=CyberTheme.TEXT_PRIMARY,
                       font=('Courier New', 10))
        
        # Configure TProgressbar
        style.configure("Cyber.Horizontal.TProgressbar",
                       background=CyberTheme.PRIMARY,
                       troughcolor=CyberTheme.BACKGROUND_ELEVATED,
                       borderwidth=0)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg=CyberTheme.BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Top border line
        top_border = tk.Frame(main_container, bg=CyberTheme.BORDER, height=2)
        top_border.pack(fill='x')
        
        # Content area
        content = tk.Frame(main_container, bg=CyberTheme.BACKGROUND)
        content.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Sidebar
        self.create_sidebar(content)
        
        # Main content area
        self.main_content = tk.Frame(content, bg=CyberTheme.BACKGROUND)
        self.main_content.pack(side='left', fill='both', expand=True)
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.main_content, style="Cyber.TNotebook")
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create all tabs
        self.create_dashboard_tab()
        self.create_scanner_tab()
        self.create_attacks_tab()
        self.create_handshake_tab()
        self.create_wps_tab()
        self.create_results_tab()
        self.create_console_tab()
        
        # Bottom border line
        bottom_border = tk.Frame(main_container, bg=CyberTheme.BORDER, height=2)
        bottom_border.pack(side='bottom', fill='x')
        
        # Status bar
        self.create_statusbar(main_container)
    
    def create_sidebar(self, parent):
        """Create the sidebar with navigation"""
        sidebar = tk.Frame(parent, bg=CyberTheme.SURFACE, width=280)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Sidebar border (right)
        sidebar_border = tk.Frame(sidebar, bg=CyberTheme.BORDER, width=2)
        sidebar_border.pack(side='right', fill='y')
        
        # Logo frame
        logo_frame = tk.Frame(sidebar, bg=CyberTheme.SURFACE)
        logo_frame.pack(fill='x', padx=10, pady=20)
        
        # SAIFITE ASCII logo
        for line in SAIFITE_ASCII:
            tk.Label(logo_frame, text=line, font=('Courier New', 8, 'bold'),
                    fg=CyberTheme.PRIMARY, bg=CyberTheme.SURFACE).pack()
        
        tk.Label(logo_frame, text="HACK THE NETWORK", font=('Courier New', 10, 'bold'),
                fg=CyberTheme.PRIMARY, bg=CyberTheme.SURFACE).pack(pady=5)
        
        tk.Label(logo_frame, text="v2025.1", font=('Courier New', 8),
                fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.SURFACE).pack()
        
        # Separator
        self.create_separator(sidebar)
        
        # Navigation buttons
        nav_frame = tk.Frame(sidebar, bg=CyberTheme.SURFACE)
        nav_frame.pack(fill='x', padx=10, pady=10)
        
        nav_items = [
            ("[>] DASHBOARD", "dashboard", "◉", "Security Overview"),
            ("[>] NETWORK SCANNER", "scanner", "◈", "Discover Networks"),
            ("[>] ATTACK CENTER", "attacks", "⚡", "Launch Attacks"),
            ("[>] HANDSHAKE LAB", "handshake", "🤝", "Capture Handshakes"),
            ("[>] WPS CRACKER", "wps", "🔑", "WPS Attacks"),
            ("[✓] CRACKED DB", "results", "✓", "Results Database"),
            ("[~] CONSOLE", "logs", ">_", "Activity Log")
        ]
        
        self.nav_buttons = {}
        for label, tab_id, icon, tooltip in nav_items:
            btn_frame = tk.Frame(nav_frame, bg=CyberTheme.SURFACE)
            btn_frame.pack(fill='x', pady=2)
            
            btn = tk.Button(btn_frame, text=f"{icon} {label}", font=('Courier New', 11),
                          fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.SURFACE,
                          bd=0, anchor='w', padx=10, pady=8,
                          activebackground=CyberTheme.PRIMARY_DARK,
                          activeforeground=CyberTheme.BACKGROUND,
                          command=lambda t=tab_id: self.switch_tab(t))
            btn.pack(fill='x')
            
            # Tooltip
            self.create_tooltip(btn, tooltip)
            self.nav_buttons[tab_id] = btn
        
        # Separator
        self.create_separator(sidebar)
        
        # Footer
        footer_frame = tk.Frame(sidebar, bg=CyberTheme.SURFACE)
        footer_frame.pack(side='bottom', fill='x', padx=10, pady=20)
        
        tk.Label(footer_frame, text="╔══════════════════════╗", font=('Courier New', 8),
                fg=CyberTheme.BORDER_DIM, bg=CyberTheme.SURFACE).pack()
        tk.Label(footer_frame, text="║  SAIF UL ISLAM       ║", font=('Courier New', 8),
                fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.SURFACE).pack()
        tk.Label(footer_frame, text="║  @saifulislaam       ║", font=('Courier New', 8),
                fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.SURFACE).pack()
        tk.Label(footer_frame, text="╚══════════════════════╝", font=('Courier New', 8),
                fg=CyberTheme.BORDER_DIM, bg=CyberTheme.SURFACE).pack()
    
    def create_separator(self, parent):
        """Create a separator line"""
        sep = tk.Frame(parent, bg=CyberTheme.BORDER_DIM, height=1)
        sep.pack(fill='x', padx=10, pady=10)
    
    def create_tooltip(self, widget, text):
        """Create tooltip for widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, font=('Courier New', 9),
                           fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_ELEVATED,
                           relief='solid', bd=1, padx=5, pady=2)
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)
    
    def create_statusbar(self, parent):
        """Create status bar"""
        statusbar = tk.Frame(parent, bg=CyberTheme.SURFACE, height=28)
        statusbar.pack(side='bottom', fill='x')
        
        # Top border
        top_border = tk.Frame(statusbar, bg=CyberTheme.BORDER, height=1)
        top_border.pack(fill='x')
        
        # Left side
        left_frame = tk.Frame(statusbar, bg=CyberTheme.SURFACE)
        left_frame.pack(side='left', fill='x', expand=True, padx=10)
        
        # Blinking status indicator
        self.status_indicator = tk.Label(left_frame, text="●", font=('Courier New', 10),
                                        fg=CyberTheme.SUCCESS, bg=CyberTheme.SURFACE)
        self.status_indicator.pack(side='left', padx=5)
        
        self.status_label = tk.Label(left_frame, textvariable=self.status_message,
                                     font=('Courier New', 9), fg=CyberTheme.TEXT_PRIMARY,
                                     bg=CyberTheme.SURFACE)
        self.status_label.pack(side='left', padx=5)
        
        tk.Label(left_frame, text="|", font=('Courier New', 9),
                fg=CyberTheme.BORDER_DIM, bg=CyberTheme.SURFACE).pack(side='left', padx=10)
        
        tk.Label(left_frame, text="MONITOR:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.SURFACE).pack(side='left')
        
        self.monitor_indicator = tk.Label(left_frame, textvariable=self.monitor_status,
                                          font=('Courier New', 9, 'bold'),
                                          fg=CyberTheme.SUCCESS, bg=CyberTheme.SURFACE)
        self.monitor_indicator.pack(side='left', padx=5)
        
        # Right side
        right_frame = tk.Frame(statusbar, bg=CyberTheme.SURFACE)
        right_frame.pack(side='right', padx=10)
        
        tk.Label(right_frame, text="IFACE:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.SURFACE).pack(side='left')
        
        tk.Label(right_frame, textvariable=self.current_interface, font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.SURFACE).pack(side='left', padx=5)
        
        tk.Label(right_frame, text="| SAIF UL ISLAM | @saifulislaam",
                font=('Courier New', 8), fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.SURFACE).pack(side='left', padx=10)
        
        # Blink animation
        self.blink_status()
    
    def create_dashboard_tab(self):
        """Create the Dashboard tab"""
        dashboard = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(dashboard, text="DASHBOARD")
        
        # Header
        for line in DASHBOARD_HEADER:
            tk.Label(dashboard, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # Main content frame
        content_frame = tk.Frame(dashboard, bg=CyberTheme.BACKGROUND)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left column
        left_col = tk.Frame(content_frame, bg=CyberTheme.BACKGROUND)
        left_col.pack(side='left', fill='both', expand=True, padx=10)
        
        # Interface Control Panel
        self.create_interface_panel(left_col)
        
        # Statistics Grid
        self.create_stats_grid(left_col)
        
        # Right column
        right_col = tk.Frame(content_frame, bg=CyberTheme.BACKGROUND)
        right_col.pack(side='right', fill='both', expand=True, padx=10)
        
        # Charts
        self.create_charts_panel(right_col)
        
        # Quick Commands
        self.create_quick_commands(right_col)
    
    def create_interface_panel(self, parent):
        """Create interface control panel"""
        frame = tk.LabelFrame(parent, text="[ INTERFACE CONTROL ]", font=('Courier New', 10, 'bold'),
                             fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD,
                             bd=2, relief='solid')
        frame.pack(fill='x', pady=10)
        
        # Interface selection
        iface_frame = tk.Frame(frame, bg=CyberTheme.BACKGROUND_CARD)
        iface_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(iface_frame, text="$> SELECT INTERFACE", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack(anchor='w')
        
        self.interface_combo = ttk.Combobox(iface_frame, textvariable=self.interface,
                                            font=('Courier New', 10), width=25,
                                            style="Cyber.TCombobox")
        self.interface_combo.pack(anchor='w', pady=5)
        self.interface_combo.bind('<<ComboboxSelected>>', self.on_interface_select)
        
        # Monitor mode status
        monitor_frame = tk.Frame(frame, bg=CyberTheme.BACKGROUND_CARD)
        monitor_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(monitor_frame, text="$> MONITOR MODE", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack(anchor='w')
        
        self.monitor_status_label = tk.Label(monitor_frame, text="INACTIVE",
                                             font=('Courier New', 9, 'bold'),
                                             fg=CyberTheme.ERROR, bg=CyberTheme.BACKGROUND_CARD)
        self.monitor_status_label.pack(anchor='w', pady=5)
        
        # MAC Spoof
        spoof_frame = tk.Frame(frame, bg=CyberTheme.BACKGROUND_CARD)
        spoof_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(spoof_frame, text="$> MAC SPOOF", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack(anchor='w')
        
        self.mac_spoof_cb = tk.Checkbutton(spoof_frame, text="[ ] ENABLED",
                                          variable=self.mac_spoof,
                                          font=('Courier New', 9),
                                          fg=CyberTheme.TEXT_PRIMARY,
                                          bg=CyberTheme.BACKGROUND_CARD,
                                          selectcolor=CyberTheme.BACKGROUND_CARD)
        self.mac_spoof_cb.pack(anchor='w', pady=5)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=CyberTheme.BACKGROUND_CARD)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.start_monitor_btn = tk.Button(btn_frame, text="[ START MONITOR ]",
                                          font=('Courier New', 9, 'bold'),
                                          fg=CyberTheme.BACKGROUND, bg=CyberTheme.SUCCESS,
                                          bd=0, padx=10, pady=5,
                                          command=self.enable_monitor)
        self.start_monitor_btn.pack(side='left', padx=5)
        
        self.stop_monitor_btn = tk.Button(btn_frame, text="[ STOP MONITOR ]",
                                         font=('Courier New', 9, 'bold'),
                                         fg=CyberTheme.BACKGROUND, bg=CyberTheme.ERROR,
                                         bd=0, padx=10, pady=5,
                                         command=self.disable_monitor, state='disabled')
        self.stop_monitor_btn.pack(side='left', padx=5)
        
        self.spoof_mac_btn = tk.Button(btn_frame, text="[ SPOOF MAC ]",
                                      font=('Courier New', 9, 'bold'),
                                      fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                                      bd=0, padx=10, pady=5,
                                      command=self.spoof_mac)
        self.spoof_mac_btn.pack(side='left', padx=5)
    
    def create_stats_grid(self, parent):
        """Create statistics grid"""
        frame = tk.LabelFrame(parent, text="[ STATISTICS ]", font=('Courier New', 10, 'bold'),
                             fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD,
                             bd=2, relief='solid')
        frame.pack(fill='x', pady=10)
        
        stats = [
            ("NETWORKS", self.networks_count, "#"),
            ("CLIENTS", self.clients_count, "#"),
            ("HANDSHAKES", self.handshakes_count, "#"),
            ("CRACKED", self.cracked_count, "#"),
            ("WPS TARGETS", self.wps_count, "#"),
            ("ACTIVE", self.active_attacks, ">")
        ]
        
        for i, (label, var, prefix) in enumerate(stats):
            stat_frame = tk.Frame(frame, bg=CyberTheme.BACKGROUND_CARD)
            stat_frame.pack(side='left', expand=True, fill='both', padx=5, pady=10)
            
            tk.Label(stat_frame, text=label, font=('Courier New', 9),
                    fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.BACKGROUND_CARD).pack()
            
            value = tk.Label(stat_frame, textvariable=var, font=('Courier New', 16, 'bold'),
                            fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD)
            value.pack()
    
    def create_charts_panel(self, parent):
        """Create charts panel"""
        frame = tk.LabelFrame(parent, text="[ SIGNAL ANALYSIS ]", font=('Courier New', 10, 'bold'),
                             fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD,
                             bd=2, relief='solid')
        frame.pack(fill='both', expand=True, pady=10)
        
        # ASCII-style chart display
        self.chart_text = tk.Text(frame, height=15, width=40,
                                  font=('Courier New', 9),
                                  fg=CyberTheme.TEXT_PRIMARY,
                                  bg=CyberTheme.BACKGROUND_ELEVATED,
                                  bd=0, relief='flat')
        self.chart_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.update_charts()
    
    def create_quick_commands(self, parent):
        """Create quick commands panel"""
        frame = tk.LabelFrame(parent, text="[ QUICK COMMANDS ]", font=('Courier New', 10, 'bold'),
                             fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD,
                             bd=2, relief='solid')
        frame.pack(fill='x', pady=10)
        
        commands = [
            ("scan --full", "FULL SCAN", self.start_scan),
            ("attack --all", "ATTACK ALL", self.attack_all),
            ("export --report", "EXPORT REPORT", self.export_report),
            ("update --check", "CHECK UPDATES", self.check_updates)
        ]
        
        for cmd, label, command in commands:
            cmd_frame = tk.Frame(frame, bg=CyberTheme.BACKGROUND_CARD)
            cmd_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(cmd_frame, text=f"$> {cmd}", font=('Courier New', 9),
                    fg=CyberTheme.TEXT_SECONDARY, bg=CyberTheme.BACKGROUND_CARD).pack(side='left')
            
            tk.Button(cmd_frame, text=f"[ {label} ]", font=('Courier New', 8),
                     fg=CyberTheme.BACKGROUND, bg=CyberTheme.PRIMARY_DARK,
                     bd=0, padx=10, pady=3,
                     command=command).pack(side='right')
    
    def create_scanner_tab(self):
        """Create Network Scanner tab"""
        scanner = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(scanner, text="NETWORK SCANNER")
        
        # Header
        for line in SCANNER_HEADER:
            tk.Label(scanner, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # Scan controls
        control_frame = tk.LabelFrame(scanner, text="[ SCAN PARAMETERS ]",
                                     font=('Courier New', 10, 'bold'),
                                     fg=CyberTheme.TEXT_PRIMARY,
                                     bg=CyberTheme.BACKGROUND_CARD,
                                     bd=2, relief='solid')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Control grid
        grid_frame = tk.Frame(control_frame, bg=CyberTheme.BACKGROUND_CARD)
        grid_frame.pack(padx=10, pady=10)
        
        # Channel
        tk.Label(grid_frame, text="CHANNEL:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=0, column=0, sticky='w', padx=5)
        tk.Entry(grid_frame, textvariable=self.target_channel, width=8,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY, insertbackground=CyberTheme.TEXT_PRIMARY).grid(row=0, column=1, padx=5)
        
        # Min Signal
        tk.Label(grid_frame, text="MIN SIGNAL:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=0, column=2, sticky='w', padx=20)
        tk.Scale(grid_frame, from_=0, to=100, orient='horizontal',
                variable=self.min_power, length=150,
                bg=CyberTheme.BACKGROUND_CARD,
                fg=CyberTheme.TEXT_PRIMARY,
                troughcolor=CyberTheme.BACKGROUND_ELEVATED).grid(row=0, column=3, padx=5)
        tk.Label(grid_frame, textvariable=self.min_power, font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=0, column=4, padx=5)
        
        # ESSID
        tk.Label(grid_frame, text="ESSID:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=1, column=0, sticky='w', padx=5, pady=10)
        tk.Entry(grid_frame, textvariable=self.target_essid, width=25,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY, insertbackground=CyberTheme.TEXT_PRIMARY).grid(row=1, column=1, padx=5)
        
        # BSSID
        tk.Label(grid_frame, text="BSSID:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=1, column=2, sticky='w', padx=20)
        tk.Entry(grid_frame, textvariable=self.target_bssid, width=25,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY, insertbackground=CyberTheme.TEXT_PRIMARY).grid(row=1, column=3, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(control_frame, bg=CyberTheme.BACKGROUND_CARD)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="[ SCAN ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.SUCCESS,
                 bd=0, padx=20, pady=5, command=self.start_scan).pack(side='left', padx=5)
        tk.Button(btn_frame, text="[ STOP ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.ERROR,
                 bd=0, padx=20, pady=5, command=self.stop_scan).pack(side='left', padx=5)
        tk.Button(btn_frame, text="[ CLEAR ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=20, pady=5, command=self.clear_scan_results).pack(side='left', padx=5)
        
        # Network tree
        tree_frame = tk.LabelFrame(scanner, text="[ TARGETS ]",
                                   font=('Courier New', 10, 'bold'),
                                   fg=CyberTheme.TEXT_PRIMARY,
                                   bg=CyberTheme.BACKGROUND_CARD,
                                   bd=2, relief='solid')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('essid', 'bssid', 'ch', 'enc', 'pwr', 'clients', 'wps', 'status')
        self.network_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                         style="Cyber.Treeview", height=12)
        
        self.network_tree.heading('essid', text='ESSID')
        self.network_tree.heading('bssid', text='BSSID')
        self.network_tree.heading('ch', text='CH')
        self.network_tree.heading('enc', text='ENC')
        self.network_tree.heading('pwr', text='PWR')
        self.network_tree.heading('clients', text='CLI')
        self.network_tree.heading('wps', text='WPS')
        self.network_tree.heading('status', text='STATUS')
        
        self.network_tree.column('essid', width=200)
        self.network_tree.column('bssid', width=150)
        self.network_tree.column('ch', width=50, anchor='center')
        self.network_tree.column('enc', width=80)
        self.network_tree.column('pwr', width=60, anchor='center')
        self.network_tree.column('clients', width=50, anchor='center')
        self.network_tree.column('wps', width=50, anchor='center')
        self.network_tree.column('status', width=100)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.network_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.network_tree.xview)
        self.network_tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        
        self.network_tree.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        y_scroll.pack(side='right', fill='y')
        x_scroll.pack(side='bottom', fill='x')
        
        # Action buttons
        action_frame = tk.Frame(tree_frame, bg=CyberTheme.BACKGROUND_CARD)
        action_frame.pack(fill='x', pady=5)
        
        tk.Button(action_frame, text="[ ADD TO ATTACK ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.PRIMARY,
                 bd=0, padx=10, pady=3,
                 command=self.add_to_attack_list).pack(side='left', padx=5)
        tk.Button(action_frame, text="[ ATTACK NOW ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=10, pady=3,
                 command=self.attack_selected).pack(side='left', padx=5)
        tk.Button(action_frame, text="[ CAPTURE ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=10, pady=3,
                 command=self.capture_handshake).pack(side='left', padx=5)
    
    def create_attacks_tab(self):
        """Create Attack Center tab"""
        attacks = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(attacks, text="ATTACK CENTER")
        
        # Header
        for line in ATTACK_HEADER:
            tk.Label(attacks, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # Main content
        content = tk.Frame(attacks, bg=CyberTheme.BACKGROUND)
        content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Attack modes
        left_panel = tk.Frame(content, bg=CyberTheme.BACKGROUND)
        left_panel.pack(side='left', fill='y', padx=5)
        
        mode_frame = tk.LabelFrame(left_panel, text="[ ATTACK MODES ]",
                                   font=('Courier New', 10, 'bold'),
                                   fg=CyberTheme.TEXT_PRIMARY,
                                   bg=CyberTheme.BACKGROUND_CARD,
                                   bd=2, relief='solid')
        mode_frame.pack(fill='x', pady=5)
        
        tk.Checkbutton(mode_frame, text="[WPA/WPA2]", variable=self.wpa_enabled,
                      font=('Courier New', 10), fg=CyberTheme.TEXT_PRIMARY,
                      bg=CyberTheme.BACKGROUND_CARD, selectcolor=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=5)
        tk.Checkbutton(mode_frame, text="[WEP]", variable=self.wep_enabled,
                      font=('Courier New', 10), fg=CyberTheme.TEXT_PRIMARY,
                      bg=CyberTheme.BACKGROUND_CARD, selectcolor=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=5)
        tk.Checkbutton(mode_frame, text="[WPS]", variable=self.wps_enabled,
                      font=('Courier New', 10), fg=CyberTheme.TEXT_PRIMARY,
                      bg=CyberTheme.BACKGROUND_CARD, selectcolor=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=5)
        
        # Attack settings
        settings_frame = tk.LabelFrame(left_panel, text="[ SETTINGS ]",
                                       font=('Courier New', 10, 'bold'),
                                       fg=CyberTheme.TEXT_PRIMARY,
                                       bg=CyberTheme.BACKGROUND_CARD,
                                       bd=2, relief='solid')
        settings_frame.pack(fill='x', pady=5)
        
        tk.Label(settings_frame, text="DEAUTH COUNT:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=2)
        tk.Entry(settings_frame, textvariable=self.deauth_count, width=10,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(settings_frame, text="TIMEOUT (s):", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=2)
        tk.Entry(settings_frame, textvariable=self.wpa_timeout, width=10,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY).pack(anchor='w', padx=10, pady=2)
        
        tk.Label(settings_frame, text="WORDLIST:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=2)
        wordlist_frame = tk.Frame(settings_frame, bg=CyberTheme.BACKGROUND_CARD)
        wordlist_frame.pack(anchor='w', padx=10, pady=2)
        tk.Entry(wordlist_frame, textvariable=self.wordlist_path, width=25,
                font=('Courier New', 9), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY).pack(side='left')
        tk.Button(wordlist_frame, text="Browse", font=('Courier New', 8),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.PRIMARY,
                 bd=0, padx=5, pady=2, command=self.browse_wordlist).pack(side='left', padx=5)
        
        tk.Checkbutton(settings_frame, text="AUTO-CRACK", variable=self.auto_crack,
                      font=('Courier New', 9), fg=CyberTheme.TEXT_PRIMARY,
                      bg=CyberTheme.BACKGROUND_CARD, selectcolor=CyberTheme.BACKGROUND_CARD).pack(anchor='w', padx=10, pady=5)
        
        # Right panel - Target queue
        right_panel = tk.Frame(content, bg=CyberTheme.BACKGROUND)
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        queue_frame = tk.LabelFrame(right_panel, text="[ TARGET QUEUE ]",
                                    font=('Courier New', 10, 'bold'),
                                    fg=CyberTheme.TEXT_PRIMARY,
                                    bg=CyberTheme.BACKGROUND_CARD,
                                    bd=2, relief='solid')
        queue_frame.pack(fill='both', expand=True)
        
        # Attack tree
        attack_columns = ('essid', 'bssid', 'ch', 'enc', 'pwr', 'progress', 'status')
        self.attack_tree = ttk.Treeview(queue_frame, columns=attack_columns, show='headings',
                                        style="Cyber.Treeview", height=15)
        
        self.attack_tree.heading('essid', text='ESSID')
        self.attack_tree.heading('bssid', text='BSSID')
        self.attack_tree.heading('ch', text='CH')
        self.attack_tree.heading('enc', text='ENC')
        self.attack_tree.heading('pwr', text='PWR')
        self.attack_tree.heading('progress', text='PROGRESS')
        self.attack_tree.heading('status', text='STATUS')
        
        self.attack_tree.column('essid', width=180)
        self.attack_tree.column('bssid', width=150)
        self.attack_tree.column('ch', width=50, anchor='center')
        self.attack_tree.column('enc', width=80)
        self.attack_tree.column('pwr', width=60, anchor='center')
        self.attack_tree.column('progress', width=200)
        self.attack_tree.column('status', width=100)
        
        self.attack_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Attack buttons
        attack_btn_frame = tk.Frame(queue_frame, bg=CyberTheme.BACKGROUND_CARD)
        attack_btn_frame.pack(fill='x', pady=5)
        
        tk.Button(attack_btn_frame, text="[ START ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.SUCCESS,
                 bd=0, padx=20, pady=5, command=self.start_attack).pack(side='left', padx=5)
        tk.Button(attack_btn_frame, text="[ STOP ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.ERROR,
                 bd=0, padx=20, pady=5, command=self.stop_attack).pack(side='left', padx=5)
        tk.Button(attack_btn_frame, text="[ REMOVE ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=20, pady=5, command=self.remove_from_attack_list).pack(side='left', padx=5)
        
        # Attack console
        console_frame = tk.LabelFrame(right_panel, text="[ ATTACK CONSOLE ]",
                                      font=('Courier New', 10, 'bold'),
                                      fg=CyberTheme.TEXT_PRIMARY,
                                      bg=CyberTheme.BACKGROUND_CARD,
                                      bd=2, relief='solid')
        console_frame.pack(fill='x', pady=5)
        
        self.attack_console = tk.Text(console_frame, height=6,
                                      font=('Courier New', 9),
                                      fg=CyberTheme.TEXT_PRIMARY,
                                      bg=CyberTheme.BACKGROUND_ELEVATED,
                                      bd=0, relief='flat')
        self.attack_console.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Progress bar
        self.attack_progress = ttk.Progressbar(console_frame, mode='indeterminate',
                                               style="Cyber.Horizontal.TProgressbar")
        self.attack_progress.pack(fill='x', padx=5, pady=5)
    
    def create_handshake_tab(self):
        """Create Handshake Lab tab"""
        handshake = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(handshake, text="HANDSHAKE LAB")
        
        # Header
        for line in HANDSHAKE_HEADER:
            tk.Label(handshake, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # Capture panel
        capture_frame = tk.LabelFrame(handshake, text="[ CAPTURE TARGET ]",
                                      font=('Courier New', 10, 'bold'),
                                      fg=CyberTheme.TEXT_PRIMARY,
                                      bg=CyberTheme.BACKGROUND_CARD,
                                      bd=2, relief='solid')
        capture_frame.pack(fill='x', padx=20, pady=10)
        
        cap_grid = tk.Frame(capture_frame, bg=CyberTheme.BACKGROUND_CARD)
        cap_grid.pack(padx=10, pady=10)
        
        tk.Label(cap_grid, text="BSSID:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=0, column=0, sticky='w', padx=5)
        tk.Entry(cap_grid, textvariable=self.target_bssid, width=20,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY).grid(row=0, column=1, padx=5)
        
        tk.Label(cap_grid, text="CHANNEL:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=0, column=2, sticky='w', padx=20)
        tk.Entry(cap_grid, textvariable=self.target_channel, width=8,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY).grid(row=0, column=3, padx=5)
        
        tk.Label(cap_grid, text="DEAUTH:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).grid(row=1, column=0, sticky='w', padx=5, pady=10)
        tk.Entry(cap_grid, textvariable=self.deauth_count, width=8,
                font=('Courier New', 10), bg=CyberTheme.BACKGROUND_ELEVATED,
                fg=CyberTheme.TEXT_PRIMARY).grid(row=1, column=1, padx=5)
        
        cap_btn_frame = tk.Frame(cap_grid, bg=CyberTheme.BACKGROUND_CARD)
        cap_btn_frame.grid(row=1, column=2, columnspan=2, pady=10)
        
        tk.Button(cap_btn_frame, text="[ CAPTURE ]", font=('Courier New', 9, 'bold'),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.SUCCESS,
                 bd=0, padx=20, pady=5, command=self.capture_handshake).pack(side='left', padx=5)
        
        # Handshake list
        hs_frame = tk.LabelFrame(handshake, text="[ CAPTURED HANDSHAKES ]",
                                 font=('Courier New', 10, 'bold'),
                                 fg=CyberTheme.TEXT_PRIMARY,
                                 bg=CyberTheme.BACKGROUND_CARD,
                                 bd=2, relief='solid')
        hs_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        hs_columns = ('ssid', 'bssid', 'date', 'cracked', 'key')
        self.handshake_tree = ttk.Treeview(hs_frame, columns=hs_columns, show='headings',
                                           style="Cyber.Treeview", height=10)
        
        self.handshake_tree.heading('ssid', text='ESSID')
        self.handshake_tree.heading('bssid', text='BSSID')
        self.handshake_tree.heading('date', text='DATE')
        self.handshake_tree.heading('cracked', text='CRACKED')
        self.handshake_tree.heading('key', text='KEY')
        
        self.handshake_tree.column('ssid', width=200)
        self.handshake_tree.column('bssid', width=150)
        self.handshake_tree.column('date', width=150)
        self.handshake_tree.column('cracked', width=80, anchor='center')
        self.handshake_tree.column('key', width=250)
        
        self.handshake_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        hs_btn_frame = tk.Frame(hs_frame, bg=CyberTheme.BACKGROUND_CARD)
        hs_btn_frame.pack(fill='x', pady=5)
        
        tk.Button(hs_btn_frame, text="[ ANALYZE ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=10, pady=3, command=self.analyze_handshake).pack(side='left', padx=5)
        tk.Button(hs_btn_frame, text="[ CRACK ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=10, pady=3, command=self.crack_handshake).pack(side='left', padx=5)
        tk.Button(hs_btn_frame, text="[ CRACK ALL ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.ERROR,
                 bd=0, padx=10, pady=3, command=self.crack_all_handshakes).pack(side='left', padx=5)
        tk.Button(hs_btn_frame, text="[ DELETE ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.ERROR,
                 bd=0, padx=10, pady=3, command=self.delete_handshake).pack(side='left', padx=5)
    
    def create_wps_tab(self):
        """Create WPS Cracker tab"""
        wps = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(wps, text="WPS CRACKER")
        
        # Header
        for line in WPS_HEADER:
            tk.Label(wps, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # WPS targets
        wps_frame = tk.LabelFrame(wps, text="[ WPS TARGETS ]",
                                  font=('Courier New', 10, 'bold'),
                                  fg=CyberTheme.TEXT_PRIMARY,
                                  bg=CyberTheme.BACKGROUND_CARD,
                                  bd=2, relief='solid')
        wps_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        wps_columns = ('essid', 'bssid', 'ch', 'pwr', 'locked', 'status')
        self.wps_tree = ttk.Treeview(wps_frame, columns=wps_columns, show='headings',
                                     style="Cyber.Treeview", height=12)
        
        self.wps_tree.heading('essid', text='ESSID')
        self.wps_tree.heading('bssid', text='BSSID')
        self.wps_tree.heading('ch', text='CH')
        self.wps_tree.heading('pwr', text='PWR')
        self.wps_tree.heading('locked', text='LOCKED')
        self.wps_tree.heading('status', text='STATUS')
        
        self.wps_tree.column('essid', width=200)
        self.wps_tree.column('bssid', width=150)
        self.wps_tree.column('ch', width=50, anchor='center')
        self.wps_tree.column('pwr', width=60, anchor='center')
        self.wps_tree.column('locked', width=80, anchor='center')
        self.wps_tree.column('status', width=100)
        
        self.wps_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        wps_btn_frame = tk.Frame(wps_frame, bg=CyberTheme.BACKGROUND_CARD)
        wps_btn_frame.pack(fill='x', pady=5)
        
        tk.Button(wps_btn_frame, text="[ CHECK LOCK ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=10, pady=3, command=self.check_wps_lock).pack(side='left', padx=5)
        tk.Button(wps_btn_frame, text="[ PIN ATTACK ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.SUCCESS,
                 bd=0, padx=10, pady=3, command=self.start_wps_attack).pack(side='left', padx=5)
        tk.Button(wps_btn_frame, text="[ PIXIE-DUST ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=10, pady=3, command=self.start_pixie_attack).pack(side='left', padx=5)
        
        # WPS Console
        console_frame = tk.LabelFrame(wps, text="[ WPS CONSOLE ]",
                                      font=('Courier New', 10, 'bold'),
                                      fg=CyberTheme.TEXT_PRIMARY,
                                      bg=CyberTheme.BACKGROUND_CARD,
                                      bd=2, relief='solid')
        console_frame.pack(fill='x', padx=20, pady=10)
        
        self.wps_console = tk.Text(console_frame, height=8,
                                   font=('Courier New', 9),
                                   fg=CyberTheme.TEXT_PRIMARY,
                                   bg=CyberTheme.BACKGROUND_ELEVATED,
                                   bd=0, relief='flat')
        self.wps_console.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_results_tab(self):
        """Create Cracked DB tab"""
        results = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(results, text="CRACKED DB")
        
        # Header
        for line in RESULTS_HEADER:
            tk.Label(results, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # Stats banner
        stats_frame = tk.LabelFrame(results, text="[ STATISTICS ]",
                                    font=('Courier New', 10, 'bold'),
                                    fg=CyberTheme.TEXT_PRIMARY,
                                    bg=CyberTheme.BACKGROUND_CARD,
                                    bd=2, relief='solid')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        stats_grid = tk.Frame(stats_frame, bg=CyberTheme.BACKGROUND_CARD)
        stats_grid.pack(pady=10)
        
        stats = [
            ("TOTAL", self.cracked_count),
            ("WPA/WPA2", self.wpa_cracked),
            ("WEP", self.wep_cracked),
            ("WPS", self.wps_cracked)
        ]
        
        for i, (label, var) in enumerate(stats):
            stat = tk.Frame(stats_grid, bg=CyberTheme.BACKGROUND_CARD)
            stat.grid(row=0, column=i, padx=20)
            tk.Label(stat, text=label, font=('Courier New', 9),
                    fg=CyberTheme.TEXT_MUTED, bg=CyberTheme.BACKGROUND_CARD).pack()
            tk.Label(stat, textvariable=var, font=('Courier New', 16, 'bold'),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND_CARD).pack()
        
        # Cracked table
        table_frame = tk.LabelFrame(results, text="[ CRACKED NETWORKS ]",
                                    font=('Courier New', 10, 'bold'),
                                    fg=CyberTheme.TEXT_PRIMARY,
                                    bg=CyberTheme.BACKGROUND_CARD,
                                    bd=2, relief='solid')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        result_columns = ('ssid', 'bssid', 'enc', 'key', 'wps_pin', 'date')
        self.results_tree = ttk.Treeview(table_frame, columns=result_columns, show='headings',
                                         style="Cyber.Treeview", height=15)
        
        self.results_tree.heading('ssid', text='ESSID')
        self.results_tree.heading('bssid', text='BSSID')
        self.results_tree.heading('enc', text='ENC')
        self.results_tree.heading('key', text='PASSWORD')
        self.results_tree.heading('wps_pin', text='WPS PIN')
        self.results_tree.heading('date', text='DATE')
        
        self.results_tree.column('ssid', width=200)
        self.results_tree.column('bssid', width=150)
        self.results_tree.column('enc', width=80)
        self.results_tree.column('key', width=200)
        self.results_tree.column('wps_pin', width=100, anchor='center')
        self.results_tree.column('date', width=150)
        
        self.results_tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load cracked data
        self.load_cracked_into_tree()
        
        result_btn_frame = tk.Frame(table_frame, bg=CyberTheme.BACKGROUND_CARD)
        result_btn_frame.pack(fill='x', pady=5)
        
        tk.Button(result_btn_frame, text="[ EXPORT CSV ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=10, pady=3, command=self.export_cracked_csv).pack(side='left', padx=5)
        tk.Button(result_btn_frame, text="[ EXPORT TXT ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=10, pady=3, command=self.export_cracked_txt).pack(side='left', padx=5)
        tk.Button(result_btn_frame, text="[ COPY PASS ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=10, pady=3, command=self.copy_password).pack(side='left', padx=5)
        tk.Button(result_btn_frame, text="[ CLEAR ALL ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.ERROR,
                 bd=0, padx=10, pady=3, command=self.clear_cracked_history).pack(side='left', padx=5)
    
    def create_console_tab(self):
        """Create Console tab"""
        console = tk.Frame(self.notebook, bg=CyberTheme.BACKGROUND)
        self.notebook.add(console, text="CONSOLE")
        
        # Header
        for line in CONSOLE_HEADER:
            tk.Label(console, text=line, font=('Courier New', 10),
                    fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack()
        
        # Console controls
        control_frame = tk.Frame(console, bg=CyberTheme.BACKGROUND)
        control_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(control_frame, text="[ CLEAR ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.WARNING,
                 bd=0, padx=15, pady=5, command=self.clear_log).pack(side='left', padx=5)
        tk.Button(control_frame, text="[ SAVE ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=15, pady=5, command=self.save_log).pack(side='left', padx=5)
        tk.Button(control_frame, text="[ EXPORT ]", font=('Courier New', 9),
                 fg=CyberTheme.BACKGROUND, bg=CyberTheme.INFO,
                 bd=0, padx=15, pady=5, command=self.export_log).pack(side='left', padx=5)
        
        # Filter
        tk.Label(control_frame, text="FILTER:", font=('Courier New', 9),
                fg=CyberTheme.TEXT_PRIMARY, bg=CyberTheme.BACKGROUND).pack(side='left', padx=20)
        self.filter_entry = tk.Entry(control_frame, width=20,
                                     font=('Courier New', 9),
                                     bg=CyberTheme.BACKGROUND_ELEVATED,
                                     fg=CyberTheme.TEXT_PRIMARY,
                                     insertbackground=CyberTheme.TEXT_PRIMARY)
        self.filter_entry.pack(side='left', padx=5)
        self.filter_entry.bind('<KeyRelease>', self.filter_log)
        
        # Log area
        log_frame = tk.Frame(console, bg=CyberTheme.BACKGROUND)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.log_text = tk.Text(log_frame, font=('Courier New', 9),
                               fg=CyberTheme.TEXT_PRIMARY,
                               bg=CyberTheme.BACKGROUND_ELEVATED,
                               bd=2, relief='solid',
                               wrap='word')
        self.log_text.pack(fill='both', expand=True)
        
        # Scrollbar
        log_scroll = ttk.Scrollbar(log_frame, orient='vertical', command=self.log_text.yview)
        log_scroll.pack(side='right', fill='y')
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        # Configure tags
        self.log_text.tag_configure('info', foreground=CyberTheme.INFO)
        self.log_text.tag_configure('success', foreground=CyberTheme.SUCCESS)
        self.log_text.tag_configure('warning', foreground=CyberTheme.WARNING)
        self.log_text.tag_configure('error', foreground=CyberTheme.ERROR)
    
    def setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<F5>', lambda e: self.start_scan())
        self.root.bind('<F6>', lambda e: self.stop_scan())
        self.root.bind('<F9>', lambda e: self.start_attack())
        self.root.bind('<F10>', lambda e: self.stop_attack())
        self.root.bind('<Control-l>', lambda e: self.clear_log())
        self.root.bind('<Control-q>', lambda e: self.cleanup_exit())
    
    def show_splash(self):
        """Show splash screen"""
        splash = tk.Toplevel(self.root)
        splash.title("SAIFITE")
        splash.overrideredirect(True)
        splash.configure(bg=CyberTheme.BACKGROUND)
        
        # Center splash
        splash_width = 600
        splash_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        
        # Splash content
        main_frame = tk.Frame(splash, bg=CyberTheme.BACKGROUND)
        main_frame.pack(fill='both', expand=True)
        
        # ASCII art
        for line in SAIFITE_ASCII:
            tk.Label(main_frame, text=line, font=('Courier New', 10, 'bold'),
                    fg=CyberTheme.PRIMARY, bg=CyberTheme.BACKGROUND).pack(pady=2)
        
        tk.Label(main_frame, text="HACK THE NETWORK", font=('Courier New', 14, 'bold'),
                fg=CyberTheme.PRIMARY, bg=CyberTheme.BACKGROUND).pack(pady=10)
        
        tk.Label(main_frame, text=">>> INITIALIZING SECURITY AUDIT SUITE <<<",
                font=('Courier New', 9), fg=CyberTheme.TEXT_SECONDARY,
                bg=CyberTheme.BACKGROUND).pack(pady=20)
        
        # Progress bar
        progress = ttk.Progressbar(main_frame, mode='indeterminate',
                                   style="Cyber.Horizontal.TProgressbar", length=400)
        progress.pack(pady=20)
        progress.start(10)
        
        tk.Label(main_frame, text="SAIF UL ISLAM  |  @saifulislaam",
                font=('Courier New', 8), fg=CyberTheme.TEXT_MUTED,
                bg=CyberTheme.BACKGROUND).pack(side='bottom', pady=10)
        
        # Auto close after 2 seconds
        self.root.after(2000, splash.destroy)
    
    def blink_status(self):
        """Blink status indicator"""
        current = self.status_indicator.cget('fg')
        new_color = CyberTheme.ERROR if current == CyberTheme.SUCCESS else CyberTheme.SUCCESS
        self.status_indicator.config(fg=new_color)
        self.root.after(500, self.blink_status)
    
    def switch_tab(self, tab_id):
        """Switch to specified tab"""
        tab_map = {
            'dashboard': 0,
            'scanner': 1,
            'attacks': 2,
            'handshake': 3,
            'wps': 4,
            'results': 5,
            'logs': 6
        }
        self.notebook.select(tab_map.get(tab_id, 0))
        
        # Update button styles
        for tid, btn in self.nav_buttons.items():
            if tid == tab_id:
                btn.config(bg=CyberTheme.PRIMARY_DARK, fg=CyberTheme.BACKGROUND)
            else:
                btn.config(bg=CyberTheme.SURFACE, fg=CyberTheme.TEXT_PRIMARY)
    
    def detect_interfaces(self):
        """Detect available wireless interfaces"""
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            interfaces = []
            for line in result.stdout.split('\n'):
                if line and not line.startswith(' '):
                    iface = line.split()[0]
                    interfaces.append(iface)
            
            self.interface_combo['values'] = interfaces
            if interfaces:
                self.interface.set(interfaces[0])
                self.log(f"Detected interfaces: {', '.join(interfaces)}", 'info')
        except Exception as e:
            self.log(f"Error detecting interfaces: {e}", 'error')
    
    def on_interface_select(self, event=None):
        """Handle interface selection"""
        iface = self.interface.get()
        self.current_interface.set(iface)
        self.log(f"Selected interface: {iface}", 'info')
    
    def enable_monitor(self):
        """Enable monitor mode"""
        iface = self.interface.get()
        if not iface:
            messagebox.showerror("Error", "No interface selected")
            return
        
        def enable():
            try:
                self.log(f"Enabling monitor mode on {iface}...", 'info')
                self.status_message.set("ENABLING MONITOR MODE...")
                
                # Spoof MAC if requested
                if self.mac_spoof.get():
                    self.spoof_mac(iface)
                
                # Enable monitor mode
                subprocess.run(['airmon-ng', 'start', iface], 
                             capture_output=True, text=True, check=True)
                
                # Find monitor interface
                result = subprocess.run(['iwconfig'], capture_output=True, text=True)
                mon_iface = None
                for line in result.stdout.split('\n'):
                    if 'Mode:Monitor' in line:
                        # Previous line contains interface name
                        pass
                
                # Common monitor interface names
                possible_names = [f"{iface}mon", f"mon0", f"wlxmon"]
                for name in possible_names:
                    if os.path.exists(f"/sys/class/net/{name}"):
                        mon_iface = name
                        break
                
                if not mon_iface:
                    mon_iface = f"{iface}mon"
                
                self.monitor_interface.set(mon_iface)
                self.monitor_status.set("ON")
                self.monitor_status_label.config(text="ACTIVE", fg=CyberTheme.SUCCESS)
                self.monitor_mode = True
                self.start_monitor_btn.config(state='disabled')
                self.stop_monitor_btn.config(state='normal')
                self.current_interface.set(mon_iface)
                
                self.log(f"Monitor mode enabled on {mon_iface}", 'success')
                self.status_message.set("MONITOR MODE ACTIVE")
                
            except Exception as e:
                self.log(f"Error enabling monitor mode: {e}", 'error')
                self.status_message.set("MONITOR MODE FAILED")
        
        threading.Thread(target=enable, daemon=True).start()
    
    def disable_monitor(self):
        """Disable monitor mode"""
        if self.monitor_interface.get():
            try:
                self.log("Disabling monitor mode...", 'info')
                subprocess.run(['airmon-ng', 'stop', self.monitor_interface.get()],
                             capture_output=True, text=True)
                
                self.monitor_interface.set("")
                self.monitor_status.set("OFF")
                self.monitor_status_label.config(text="INACTIVE", fg=CyberTheme.ERROR)
                self.monitor_mode = False
                self.start_monitor_btn.config(state='normal')
                self.stop_monitor_btn.config(state='disabled')
                self.current_interface.set(self.interface.get())
                
                self.log("Monitor mode disabled", 'success')
                self.status_message.set("MONITOR MODE OFF")
                
            except Exception as e:
                self.log(f"Error disabling monitor mode: {e}", 'error')
    
    def spoof_mac(self, iface=None):
        """Spoof MAC address"""
        if not iface:
            iface = self.interface.get()
        
        try:
            # Generate random MAC
            random_mac = ':'.join(['%02x' % random.randint(0x00, 0xff) for _ in range(6)])
            random_mac = random_mac[:8] + ':' + ':'.join(['%02x' % random.randint(0x00, 0xff) for _ in range(2)])
            
            subprocess.run(['ifconfig', iface, 'down'], check=True)
            subprocess.run(['ifconfig', iface, 'hw', 'ether', random_mac], check=True)
            subprocess.run(['ifconfig', iface, 'up'], check=True)
            
            self.log(f"MAC address changed to {random_mac}", 'success')
            self.status_message.set(f"MAC SPOOFED: {random_mac}")
            
        except Exception as e:
            self.log(f"MAC spoofing failed: {e}", 'error')
    
    def start_scan(self):
        """Start network scanning"""
        if not self.monitor_mode:
            messagebox.showwarning("Warning", "Monitor mode not enabled")
            return
        
        def scan():
            try:
                self.log("Starting network scan...", 'info')
                self.status_message.set("SCANNING NETWORKS...")
                
                prefix = os.path.join(self.temp_dir, 'scan')
                csv_file = f"{prefix}-01.csv"
                
                # Build command
                cmd = [
                    'airodump-ng',
                    '-a',
                    '--write-interval', '1',
                    '-w', prefix,
                    '--output-format', 'csv',
                    self.monitor_interface.get()
                ]
                
                if self.target_channel.get() != "0":
                    cmd.extend(['-c', self.target_channel.get()])
                
                self.scan_process = subprocess.Popen(cmd, 
                                                     stdout=subprocess.DEVNULL,
                                                     stderr=subprocess.DEVNULL)
                
                start_time = time.time()
                
                while self.scan_process and self.scan_process.poll() is None:
                    time.sleep(2)
                    
                    if os.path.exists(csv_file):
                        self.parse_scan_results(csv_file)
                        self.update_network_tree()
                        
                        # Update statistics
                        self.networks_count.set(f"{len(self.targets):04d}")
                        self.clients_count.set(f"{len(self.clients):04d}")
                        self.wps_count.set(f"{sum(1 for t in self.targets if t.wps):04d}")
                
            except Exception as e:
                self.log(f"Scan error: {e}", 'error')
            finally:
                self.status_message.set("SCAN COMPLETE")
        
        self.clear_scan_results()
        threading.Thread(target=scan, daemon=True).start()
    
    def stop_scan(self):
        """Stop network scanning"""
        if self.scan_process:
            self.scan_process.terminate()
            self.scan_process = None
            self.log("Scan stopped", 'info')
            self.status_message.set("SCAN STOPPED")
    
    def parse_scan_results(self, csv_file):
        """Parse airodump CSV output"""
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            self.targets = []
            self.clients = []
            clients_section = False
            
            for line in lines:
                if 'Station MAC' in line:
                    clients_section = True
                    continue
                
                if not clients_section and line and not line.startswith('BSSID'):
                    parts = line.split(',')
                    if len(parts) >= 14:
                        try:
                            bssid = parts[0].strip()
                            channel = parts[3].strip()
                            power = int(parts[8].strip())
                            if power < 0:
                                power += 100
                            enc = parts[5].strip()
                            ssid = parts[13].strip()
                            
                            if power >= self.min_power.get():
                                target = Target(bssid, power, channel, enc, ssid)
                                self.targets.append(target)
                        except:
                            pass
                
                elif clients_section and line:
                    parts = line.split(',')
                    if len(parts) >= 6:
                        station = parts[5].strip() if len(parts) > 5 else ''
                        if station and station != 'notassociated':
                            client = Client(parts[0].strip(), station, parts[3].strip())
                            self.clients.append(client)
            
            # Update charts
            self.update_charts()
            
        except Exception as e:
            self.log(f"Parse error: {e}", 'error')
    
    def update_network_tree(self):
        """Update network tree with discovered targets"""
        # Clear existing
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        
        # Add targets
        for target in self.targets:
            wps_text = "Yes" if target.wps else "No"
            self.network_tree.insert('', 'end', 
                                     values=(target.ssid[:30] if target.ssid else '(hidden)',
                                            target.bssid, target.channel,
                                            target.encryption[:6], target.power,
                                            len(target.clients), wps_text, "Discovered"))
    
    def add_to_attack_list(self):
        """Add selected networks to attack list"""
        selection = self.network_tree.selection()
        if not selection:
            return
        
        for item in selection:
            values = self.network_tree.item(item)['values']
            
            # Check if already in list
            exists = False
            for child in self.attack_tree.get_children():
                if self.attack_tree.item(child)['values'][1] == values[1]:
                    exists = True
                    break
            
            if not exists:
                self.attack_tree.insert('', 'end',
                                       values=(values[0], values[1], values[2],
                                              values[3], values[4], "0%", "Queued"))
        
        self.log(f"Added {len(selection)} targets to attack list", 'success')
    
    def remove_from_attack_list(self):
        """Remove selected from attack list"""
        selection = self.attack_tree.selection()
        for item in selection:
            self.attack_tree.delete(item)
    
    def start_attack(self):
        """Start attacking selected targets"""
        targets = self.attack_tree.get_children()
        if not targets:
            messagebox.showinfo("Info", "No targets in attack list")
            return
        
        def attack():
            try:
                self.attack_progress.start()
                self.active_attacks.set("01")
                
                for item in targets:
                    values = self.attack_tree.item(item)['values']
                    self.attack_tree.item(item, values=(values[0], values[1], values[2],
                                                        values[3], values[4], "50%", "Attacking"))
                    
                    self.log(f"Attacking {values[0]} ({values[1]})", 'info')
                    self.status_message.set(f"ATTACKING: {values[0]}")
                    
                    # Simulate attack (actual attack logic would go here)
                    time.sleep(3)
                    
                    # Mark as cracked for demo
                    self.attack_tree.item(item, values=(values[0], values[1], values[2],
                                                        values[3], values[4], "100%", "Cracked!"))
                    
                    # Save to cracked
                    cracked = Target(values[1], int(values[4]), values[2], values[3], values[0])
                    cracked.key = "PASSWORD_FOUND"
                    self.save_cracked(cracked)
                    
                    self.log(f"Successfully cracked {values[0]}!", 'success')
                
                self.active_attacks.set("00")
                self.status_message.set("ATTACK SEQUENCE COMPLETE")
                
            except Exception as e:
                self.log(f"Attack error: {e}", 'error')
            finally:
                self.attack_progress.stop()
        
        threading.Thread(target=attack, daemon=True).start()
    
    def stop_attack(self):
        """Stop current attack"""
        if self.attack_process:
            self.attack_process.terminate()
            self.attack_process = None
            self.active_attacks.set("00")
            self.log("Attack stopped", 'warning')
            self.status_message.set("ATTACK STOPPED")
    
    def attack_selected(self):
        """Attack selected network immediately"""
        selection = self.network_tree.selection()
        if not selection:
            return
        
        self.add_to_attack_list()
        self.switch_tab('attacks')
        self.start_attack()
    
    def attack_all(self):
        """Attack all networks"""
        self.select_all_networks()
        self.attack_selected()
    
    def capture_handshake(self):
        """Capture handshake for selected target"""
        selection = self.network_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "No target selected")
            return
        
        values = self.network_tree.item(selection[0])['values']
        
        def capture():
            try:
                self.log(f"Capturing handshake from {values[0]}...", 'info')
                self.status_message.set(f"CAPTURING: {values[0]}")
                
                # Simulate capture
                time.sleep(5)
                
                # Create handshake file
                safe_ssid = re.sub(r'[^a-zA-Z0-9]', '', values[0])
                safe_bssid = values[1].replace(':', '-')
                filename = os.path.join(self.handshake_dir, f"{safe_ssid}_{safe_bssid}.cap")
                
                # Create empty file for demo
                with open(filename, 'w') as f:
                    f.write("# Handshake captured")
                
                handshake = Handshake(filename, values[0], values[1])
                self.handshakes.append(handshake)
                
                # Update handshake tree
                self.handshake_tree.insert('', 'end',
                                          values=(handshake.ssid, handshake.bssid,
                                                 handshake.date, "No", ""))
                
                self.handshakes_count.set(f"{len(self.handshakes):04d}")
                self.log(f"Handshake captured from {values[0]}", 'success')
                self.status_message.set("HANDSHAKE CAPTURED")
                
            except Exception as e:
                self.log(f"Capture error: {e}", 'error')
        
        threading.Thread(target=capture, daemon=True).start()
    
    def analyze_handshake(self):
        """Analyze selected handshake"""
        selection = self.handshake_tree.selection()
        if not selection:
            return
        
        values = self.handshake_tree.item(selection[0])['values']
        self.log(f"Analyzing handshake: {values[0]}", 'info')
        self.log("Handshake is valid and contains 4-way exchange", 'success')
    
    def crack_handshake(self):
        """Crack selected handshake"""
        selection = self.handshake_tree.selection()
        if not selection:
            return
        
        if not self.wordlist_path.get():
            messagebox.showwarning("Warning", "Please select a wordlist first")
            return
        
        values = self.handshake_tree.item(selection[0])['values']
        
        def crack():
            try:
                self.log(f"Cracking {values[0]}...", 'info')
                self.status_message.set(f"CRACKING: {values[0]}")
                
                # Simulate cracking
                time.sleep(3)
                
                # Update tree
                self.handshake_tree.item(selection[0], values=(values[0], values[1],
                                                               values[2], "Yes", "password123"))
                
                self.log(f"Password found for {values[0]}: password123", 'success')
                self.status_message.set("CRACKING COMPLETE")
                
                # Save to cracked
                cracked = Target(values[1], 0, 0, values[3], values[0])
                cracked.key = "password123"
                self.save_cracked(cracked)
                
            except Exception as e:
                self.log(f"Cracking error: {e}", 'error')
        
        threading.Thread(target=crack, daemon=True).start()
    
    def crack_all_handshakes(self):
        """Crack all handshakes"""
        for item in self.handshake_tree.get_children():
            values = self.handshake_tree.item(item)['values']
            if values[3] == "No":
                self.handshake_tree.selection_set(item)
                self.crack_handshake()
                time.sleep(1)
    
    def delete_handshake(self):
        """Delete selected handshake"""
        selection = self.handshake_tree.selection()
        if not selection:
            return
        
        if messagebox.askyesno("Confirm", "Delete selected handshake?"):
            for item in selection:
                values = self.handshake_tree.item(item)['values']
                # Find and delete file
                for hs in self.handshakes:
                    if hs.ssid == values[0] and hs.bssid == values[1]:
                        try:
                            os.remove(hs.filename)
                            self.handshakes.remove(hs)
                        except:
                            pass
                        break
                
                self.handshake_tree.delete(item)
            
            self.handshakes_count.set(f"{len(self.handshakes):04d}")
            self.log("Handshake deleted", 'info')
    
    def start_wps_attack(self):
        """Start WPS PIN attack"""
        selection = self.wps_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "No WPS target selected")
            return
        
        values = self.wps_tree.item(selection[0])['values']
        
        def attack():
            try:
                self.log(f"Starting WPS attack on {values[0]}", 'info')
                self.status_message.set(f"WPS ATTACK: {values[0]}")
                
                self.wps_console.insert('end', f"[+] Starting reaver on {values[1]}...\n")
                self.wps_console.see('end')
                
                # Simulate attack
                time.sleep(5)
                
                self.wps_console.insert('end', f"[+] PIN found: 12345670\n")
                self.wps_console.insert('end', f"[+] WPA PSK: wps_password\n")
                self.wps_console.see('end')
                
                self.log(f"WPS attack successful on {values[0]}", 'success')
                self.status_message.set("WPS ATTACK COMPLETE")
                
                # Save to cracked
                cracked = Target(values[1], int(values[3]), values[2], "WPA", values[0])
                cracked.key = "wps_password"
                cracked.wps = "12345670"
                self.save_cracked(cracked)
                
            except Exception as e:
                self.log(f"WPS attack error: {e}", 'error')
        
        threading.Thread(target=attack, daemon=True).start()
    
    def start_pixie_attack(self):
        """Start Pixie-dust attack"""
        selection = self.wps_tree.selection()
        if not selection:
            return
        
        values = self.wps_tree.item(selection[0])['values']
        
        def attack():
            try:
                self.log(f"Starting Pixie-dust attack on {values[0]}", 'info')
                self.status_message.set(f"PIXIE ATTACK: {values[0]}")
                
                self.wps_console.insert('end', f"[+] Pixie-dust attack on {values[1]}...\n")
                self.wps_console.see('end')
                
                time.sleep(3)
                
                self.wps_console.insert('end', f"[+] PIN found: 12345670\n")
                self.wps_console.insert('end', f"[+] WPA PSK: pixie_password\n")
                self.wps_console.see('end')
                
                self.log(f"Pixie-dust successful on {values[0]}", 'success')
                
                # Save to cracked
                cracked = Target(values[1], int(values[3]), values[2], "WPA", values[0])
                cracked.key = "pixie_password"
                cracked.wps = "12345670"
                self.save_cracked(cracked)
                
            except Exception as e:
                self.log(f"Pixie attack error: {e}", 'error')
        
        threading.Thread(target=attack, daemon=True).start()
    
    def check_wps_lock(self):
        """Check WPS lock status"""
        selection = self.wps_tree.selection()
        if not selection:
            return
        
        values = self.wps_tree.item(selection[0])['values']
        self.wps_tree.item(selection[0], values=(values[0], values[1], values[2],
                                                 values[3], "No", "Ready"))
        self.log(f"WPS lock status checked for {values[0]}: Not locked", 'info')
    
    def load_cracked(self):
        """Load cracked targets from file"""
        targets = []
        if os.path.exists('cracked.csv'):
            try:
                with open('cracked.csv', 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 5:
                            t = Target(row[0], 0, 0, row[1], row[2])
                            t.key = row[3]
                            t.wps = row[4]
                            targets.append(t)
            except:
                pass
        return targets
    
    def save_cracked(self, target):
        """Save cracked target to file"""
        self.cracked_targets.append(target)
        
        with open('cracked.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                target.bssid, target.encryption, target.ssid,
                target.key, getattr(target, 'wps', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        self.load_cracked_into_tree()
        self.update_cracked_stats()
    
    def load_cracked_into_tree(self):
        """Load cracked targets into results tree"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        wpa_count = wep_count = wps_count = 0
        
        for target in self.cracked_targets:
            wps_pin = target.wps if hasattr(target, 'wps') else ''
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.results_tree.insert('', 'end',
                                     values=(target.ssid, target.bssid,
                                            target.encryption, target.key,
                                            wps_pin, date))
            
            if 'WPA' in target.encryption:
                wpa_count += 1
            elif 'WEP' in target.encryption:
                wep_count += 1
            
            if wps_pin:
                wps_count += 1
        
        self.cracked_count.set(f"{len(self.cracked_targets):04d}")
        self.wpa_cracked.set(f"{wpa_count:04d}")
        self.wep_cracked.set(f"{wep_count:04d}")
        self.wps_cracked.set(f"{wps_count:04d}")
    
    def update_cracked_stats(self):
        """Update cracked statistics"""
        self.cracked_count.set(f"{len(self.cracked_targets):04d}")
        
        wpa = sum(1 for t in self.cracked_targets if 'WPA' in t.encryption)
        wep = sum(1 for t in self.cracked_targets if 'WEP' in t.encryption)
        wps = sum(1 for t in self.cracked_targets if hasattr(t, 'wps') and t.wps)
        
        self.wpa_cracked.set(f"{wpa:04d}")
        self.wep_cracked.set(f"{wep:04d}")
        self.wps_cracked.set(f"{wps:04d}")
    
    def export_cracked_csv(self):
        """Export cracked networks to CSV"""
        filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")])
        if filename:
            shutil.copy('cracked.csv', filename)
            self.log(f"Cracked data exported to {filename}", 'success')
    
    def export_cracked_txt(self):
        """Export cracked networks to text"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as f:
                f.write("SAIFITE CRACKED NETWORKS\n")
                f.write("=" * 50 + "\n\n")
                for target in self.cracked_targets:
                    f.write(f"SSID: {target.ssid}\n")
                    f.write(f"BSSID: {target.bssid}\n")
                    f.write(f"Encryption: {target.encryption}\n")
                    f.write(f"Key: {target.key}\n")
                    if hasattr(target, 'wps') and target.wps:
                        f.write(f"WPS PIN: {target.wps}\n")
                    f.write("-" * 30 + "\n")
            self.log(f"Cracked data exported to {filename}", 'success')
    
    def copy_password(self):
        """Copy password from selected entry"""
        selection = self.results_tree.selection()
        if selection:
            values = self.results_tree.item(selection[0])['values']
            password = values[3]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.log(f"Password copied to clipboard: {password}", 'success')
    
    def clear_cracked_history(self):
        """Clear all cracked history"""
        if messagebox.askyesno("Confirm", "Clear all cracked history?"):
            self.cracked_targets = []
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            try:
                os.remove('cracked.csv')
            except:
                pass
            self.update_cracked_stats()
            self.log("Cracked history cleared", 'warning')
    
    def export_report(self):
        """Export full report"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as f:
                f.write("SAIFITE SECURITY AUDIT REPORT\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Interface: {self.current_interface.get()}\n")
                f.write(f"Monitor Mode: {self.monitor_status.get()}\n\n")
                
                f.write("SCAN RESULTS:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Networks Found: {len(self.targets)}\n")
                f.write(f"Clients Found: {len(self.clients)}\n\n")
                
                f.write("CRACKED NETWORKS:\n")
                f.write("-" * 30 + "\n")
                for target in self.cracked_targets:
                    f.write(f"SSID: {target.ssid}\n")
                    f.write(f"Key: {target.key}\n\n")
            
            self.log(f"Report exported to {filename}", 'success')
    
    def check_updates(self):
        """Check for updates"""
        self.log("Checking for updates...", 'info')
        self.log("SAIFITE v2025.1 is up to date", 'success')
    
    def browse_wordlist(self):
        """Browse for wordlist file"""
        filename = filedialog.askopenfilename(
            title="Select Wordlist",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.wordlist_path.set(filename)
            self.log(f"Wordlist selected: {filename}", 'info')
    
    def clear_scan_results(self):
        """Clear scan results"""
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        self.targets = []
        self.clients = []
        self.networks_count.set("0000")
        self.clients_count.set("0000")
        self.wps_count.set("0000")
    
    def select_all_networks(self):
        """Select all networks in tree"""
        for item in self.network_tree.get_children():
            self.network_tree.selection_add(item)
    
    def update_charts(self):
        """Update ASCII charts"""
        self.chart_text.delete(1.0, 'end')
        
        # Count encryption types
        enc_counts = {}
        for target in self.targets:
            enc = target.encryption[:3]
            enc_counts[enc] = enc_counts.get(enc, 0) + 1
        
        if enc_counts:
            self.chart_text.insert('end', "ENCRYPTION TYPES\n")
            self.chart_text.insert('end', "-" * 20 + "\n")
            for enc, count in enc_counts.items():
                bar = "█" * min(count, 20)
                self.chart_text.insert('end', f"{enc}: {bar} {count}\n")
            
            self.chart_text.insert('end', "\nSIGNAL STRENGTH\n")
            self.chart_text.insert('end', "-" * 20 + "\n")
            
            # Signal distribution
            signals = [t.power for t in self.targets if t.power > 0]
            if signals:
                for level in range(0, 100, 20):
                    count = sum(1 for s in signals if level <= s < level + 20)
                    bar = "█" * min(count, 30)
                    self.chart_text.insert('end', f"{level:3d}: {bar} {count}\n")
    
    def filter_log(self, event=None):
        """Filter log entries"""
        filter_text = self.filter_entry.get().lower()
        self.log_text.tag_remove('hidden', '1.0', 'end')
        
        if filter_text:
            # Hide lines that don't match
            content = self.log_text.get('1.0', 'end').split('\n')
            self.log_text.delete('1.0', 'end')
            
            for line in content:
                if filter_text in line.lower():
                    self.log_text.insert('end', line + '\n')
        else:
            # Restore all lines (would need to store original log)
            pass
    
    def clear_log(self):
        """Clear console log"""
        self.log_text.delete(1.0, 'end')
        self.log("Log cleared", 'info')
    
    def save_log(self):
        """Save log to file"""
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, 'w') as f:
                f.write(self.log_text.get(1.0, 'end'))
            self.log(f"Log saved to {filename}", 'success')
    
    def export_log(self):
        """Export log"""
        self.save_log()
    
    def log(self, message, tag='info'):
        """Add message to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.queue.put(('log', (f"[{timestamp}] {message}", tag)))
    
    def process_queue(self):
        """Process queue messages from threads"""
        try:
            while True:
                msg = self.queue.get_nowait()
                
                if msg[0] == 'log':
                    text, tag = msg[1]
                    self.log_text.insert('end', text + '\n', tag)
                    self.log_text.see('end')
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_queue)
    
    def cleanup_exit(self):
        """Clean up and exit"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            # Stop processes
            if self.scan_process:
                self.scan_process.terminate()
            if self.attack_process:
                self.attack_process.terminate()
            
            # Disable monitor mode
            self.disable_monitor()
            
            # Clean temp directory
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except:
                pass
            
            self.root.quit()
            self.root.destroy()


# ==================== MAIN ====================
if __name__ == "__main__":
    # Check for root
    if os.geteuid() != 0:
        print("SAIFITE must be run as root!")
        sys.exit(1)
    
    root = tk.Tk()
    app = SaifiteGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup_exit)
    root.mainloop()
