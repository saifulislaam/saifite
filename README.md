{
  "saifite_readme": {
    "metadata": {
      "project": "SAIFITE",
      "version": "2024.1",
      "author": "SAIF UL ISLAM",
      "github": "@saifulislaam",
      "tagline": "HACK THE NETWORK",
      "repo_url": "https://github.com/saifulislaam/saifite"
    },
    
    "badges": [
      {
        "label": "GitHub",
        "url": "https://github.com/saifulislaam/saifite",
        "color": "brightgreen",
        "style": "for-the-badge",
        "logo": "github"
      },
      {
        "label": "Version",
        "url": "https://github.com/saifulislaam/saifite/releases",
        "color": "00FF41",
        "style": "for-the-badge",
        "text": "v2024.1"
      },
      {
        "label": "License",
        "url": "https://github.com/saifulislaam/saifite/blob/main/LICENSE",
        "color": "00FF41",
        "style": "for-the-badge",
        "text": "GPLv2"
      },
      {
        "label": "Python",
        "url": null,
        "color": "00FF41",
        "style": "flat-square",
        "text": "3.8+"
      },
      {
        "label": "Linux",
        "url": null,
        "color": "00FF41",
        "style": "flat-square",
        "text": "Kali|Ubuntu|Parrot"
      }
    ],

    "ascii_art": [
      "  ███████╗ █████╗ ██╗███████╗██╗████████╗███████╗",
      "  ██╔════╝██╔══██╗██║██╔════╝██║╚══██╔══╝██╔════╝",
      "  ███████╗███████║██║█████╗  ██║   ██║   █████╗  ",
      "  ╚════██║██╔══██║██║██╔══╝  ██║   ██║   ██╔══╝  ",
      "  ███████║██║  ██║██║██║     ██║   ██║   ███████╗",
      "  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝"
    ],

    "description": {
      "short": "Professional automated wireless network security auditing tool",
      "long": "SAIFITE is a professional, automated wireless network security auditing tool designed for security professionals and ethical hackers. It provides a complete suite of tools to assess Wi-Fi network security through various attack vectors including WPA/WPA2 handshake capture, WEP cracking, and WPS PIN brute-force attacks."
    },

    "features": [
      {
        "icon": "🔍",
        "name": "Network Discovery",
        "description": "Real-time scanning of wireless networks with signal strength analysis"
      },
      {
        "icon": "🤝",
        "name": "WPA Handshake Capture",
        "description": "Capture 4-way handshake using deauthentication attacks"
      },
      {
        "icon": "🔑",
        "name": "WPA Cracking",
        "description": "Dictionary-based password cracking with aircrack-ng"
      },
      {
        "icon": "🔓",
        "name": "WEP Attacks",
        "description": "Multiple attack methods (ARP replay, Chop-chop, Fragmentation, Caffe-latte)"
      },
      {
        "icon": "📍",
        "name": "WPS Attacks",
        "description": "PIN brute-force and Pixie-Dust attacks using reaver"
      },
      {
        "icon": "💾",
        "name": "Cracked Database",
        "description": "Persistent storage of cracked networks in CSV format"
      },
      {
        "icon": "🖥️",
        "name": "Dual Interface",
        "description": "Both CLI and GUI versions available"
      },
      {
        "icon": "🎨",
        "name": "Cyber Theme",
        "description": "Hacker-style green-on-black interface"
      }
    ],

    "attack_methods": {
      "wpa": {
        "enabled": true,
        "techniques": [
          "Deauthentication attack for handshake capture",
          "Dictionary-based cracking",
          "Multi-tool handshake verification (aircrack, tshark, pyrit, cowpatty)"
        ]
      },
      "wep": {
        "enabled": true,
        "techniques": [
          "ARP replay attack",
          "Chop-chop attack",
          "Fragmentation attack",
          "Caffe-latte attack",
          "P0841 attack",
          "Hirte attack"
        ]
      },
      "wps": {
        "enabled": true,
        "techniques": [
          "PIN brute-force (reaver)",
          "Pixie-Dust attack (vulnerable routers)",
          "WPS lock status detection"
        ]
      }
    },

    "installation": {
      "method_1": {
        "name": "Direct Download",
        "commands": [
          "git clone https://github.com/saifulislaam/saifite.git",
          "cd saifite",
          "chmod +x saifite.py saifite_gui.py",
          "sudo python3 saifite.py"
        ]
      },
      "method_2": {
        "name": "One-Line Install",
        "commands": [
          "git clone https://github.com/saifulislaam/saifite.git && cd saifite && sudo python3 saifite.py"
        ]
      },
      "method_3": {
        "name": "Install Dependencies",
        "commands": [
          "sudo apt-get update",
          "sudo apt-get install -y aircrack-ng reaver tshark python3-tk",
          "pip3 install matplotlib numpy",
          "sudo python3 saifite.py"
        ]
      }
    },

    "quick_start": {
      "cli": {
        "commands": [
          {
            "description": "Basic scan and attack",
            "command": "sudo python3 saifite.py"
          },
          {
            "description": "Target specific network",
            "command": "sudo python3 saifite.py -e \"MyNetwork\" -b 00:11:22:33:44:55"
          },
          {
            "description": "WPS Pixie-dust only",
            "command": "sudo python3 saifite.py --wps --pixie"
          },
          {
            "description": "Capture WPA handshake with cracking",
            "command": "sudo python3 saifite.py --wpa --crack /usr/share/wordlists/rockyou.txt"
          },
          {
            "description": "Show previously cracked networks",
            "command": "sudo python3 saifite.py --cracked"
          }
        ]
      },
      "gui": {
        "commands": [
          {
            "description": "Launch GUI",
            "command": "sudo python3 saifite_gui.py"
          }
        ],
        "hotkeys": [
          { "key": "F5", "action": "Start Scan" },
          { "key": "F6", "action": "Stop Scan" },
          { "key": "F9", "action": "Start Attack" },
          { "key": "F10", "action": "Stop Attack" },
          { "key": "Ctrl+L", "action": "Clear Log" },
          { "key": "Ctrl+Q", "action": "Exit" }
        ]
      }
    },

    "cli_commands": {
      "global": [
        {
          "command": "-i, --interface",
          "description": "Wireless interface",
          "example": "-i wlan0"
        },
        {
          "command": "-c, --channel",
          "description": "Channel to scan",
          "example": "-c 6"
        },
        {
          "command": "-e, --essid",
          "description": "Target ESSID",
          "example": "-e \"MyWiFi\""
        },
        {
          "command": "-b, --bssid",
          "description": "Target BSSID",
          "example": "-b 00:11:22:33:44:55"
        },
        {
          "command": "--all",
          "description": "Attack all targets",
          "example": "--all"
        },
        {
          "command": "--showb",
          "description": "Show BSSIDs in scan",
          "example": "--showb"
        },
        {
          "command": "--power",
          "description": "Minimum power level",
          "example": "--power 50"
        },
        {
          "command": "--mac",
          "description": "Spoof MAC address",
          "example": "--mac"
        },
        {
          "command": "--quiet",
          "description": "Quiet mode",
          "example": "--quiet"
        }
      ],
      "wpa": [
        {
          "command": "--wpa",
          "description": "Enable WPA attacks",
          "default": "On"
        },
        {
          "command": "--wpat",
          "description": "Attack timeout (seconds)",
          "default": "500"
        },
        {
          "command": "--wpadt",
          "description": "Deauth timeout (seconds)",
          "default": "10"
        },
        {
          "command": "--crack",
          "description": "Crack handshakes",
          "default": "Off"
        },
        {
          "command": "--dict",
          "description": "Dictionary file",
          "default": "auto"
        },
        {
          "command": "--strip",
          "description": "Strip handshake",
          "default": "On"
        }
      ],
      "wep": [
        {
          "command": "--wep",
          "description": "Enable WEP attacks",
          "default": "On"
        },
        {
          "command": "--pps",
          "description": "Packets per second",
          "default": "600"
        },
        {
          "command": "--wept",
          "description": "Attack timeout",
          "default": "600"
        },
        {
          "command": "--wepca",
          "description": "IVs to start cracking",
          "default": "10000"
        },
        {
          "command": "--chopchop",
          "description": "Chop-chop attack",
          "default": "On"
        },
        {
          "command": "--arpreplay",
          "description": "ARP replay attack",
          "default": "On"
        }
      ],
      "wps": [
        {
          "command": "--wps",
          "description": "Enable WPS attacks",
          "default": "On"
        },
        {
          "command": "--pixie",
          "description": "Pixie-dust only",
          "default": "Off"
        },
        {
          "command": "--wpst",
          "description": "Attack timeout",
          "default": "660"
        },
        {
          "command": "--wpsratio",
          "description": "Success ratio threshold",
          "default": "0.01"
        }
      ]
    },

    "gui_tabs": [
      {
        "name": "Dashboard",
        "features": [
          "Interface control (enable/disable monitor mode)",
          "MAC spoofing toggle",
          "Real-time statistics",
          "ASCII charts for network analysis",
          "Quick command buttons"
        ]
      },
      {
        "name": "Network Scanner",
        "features": [
          "Channel selection",
          "Signal strength filtering",
          "Target discovery",
          "Client association display",
          "Add to attack list"
        ]
      },
      {
        "name": "Attack Center",
        "features": [
          "Attack mode selection (WPA/WEP/WPS)",
          "Target queue management",
          "Attack settings configuration",
          "Progress tracking",
          "Attack console output"
        ]
      },
      {
        "name": "Handshake Lab",
        "features": [
          "Handshake capture with BSSID targeting",
          "Captured handshakes list",
          "Handshake analysis",
          "Dictionary cracking",
          "Delete functionality"
        ]
      },
      {
        "name": "WPS Cracker",
        "features": [
          "WPS-enabled targets list",
          "Lock status checking",
          "PIN brute-force attack",
          "Pixie-dust attack",
          "WPS console output"
        ]
      },
      {
        "name": "Cracked DB",
        "features": [
          "Statistics banner",
          "Cracked networks database",
          "Export to CSV/TXT",
          "Copy password to clipboard",
          "Clear history"
        ]
      },
      {
        "name": "Console",
        "features": [
          "Real-time logging",
          "Color-coded messages",
          "Filter functionality",
          "Save/export logs"
        ]
      }
    ],

    "requirements": {
      "system": {
        "os": "Linux (Kali, Ubuntu, Parrot, Debian)",
        "python": "3.8 or higher",
        "ram": "512MB minimum (2GB recommended)",
        "disk_space": "500MB for tools + wordlists"
      },
      "hardware": {
        "wireless_adapter": "Must support monitor mode and packet injection",
        "recommended": ["Alfa AWUS036ACH", "TP-Link TL-WN722N v1"],
        "chipsets": ["Atheros AR9271", "RTL8187", "RTL8812AU"]
      },
      "software": {
        "required": [
          "aircrack-ng",
          "reaver",
          "tshark",
          "iwconfig"
        ],
        "optional": [
          "pyrit",
          "cowpatty",
          "hashcat"
        ]
      },
      "wordlists": [
        "/usr/share/wordlists/rockyou.txt",
        "/usr/share/wordlists/fasttrack.txt"
      ]
    },

    "troubleshooting": {
      "common_issues": [
        {
          "issue": "No wireless interfaces found",
          "solution": "Plug in wireless adapter, check `iwconfig`"
        },
        {
          "issue": "Monitor mode failed",
          "solution": "Run `sudo airmon-ng check kill` first"
        },
        {
          "issue": "reaver: command not found",
          "solution": "Install reaver: `sudo apt-get install reaver`"
        },
        {
          "issue": "Handshake not captured",
          "solution": "Move closer to target, increase deauth count"
        },
        {
          "issue": "WPS locked",
          "solution": "Wait 5-10 minutes, target may have anti-hammering"
        },
        {
          "issue": "Dictionary not found",
          "solution": "Download rockyou.txt or specify custom wordlist"
        },
        {
          "issue": "Permission denied",
          "solution": "Must run as root: `sudo python3 saifite.py`"
        }
      ],
      "debug_commands": [
        "sudo python3 saifite.py --verbose",
        "sudo python3 saifite.py --check",
        "sudo aireplay-ng --test wlan0mon"
      ],
      "performance_tips": [
        "Use a powerful wireless adapter (Alfa cards recommended)",
        "Position antenna properly for better signal",
        "Close unnecessary programs to free resources",
        "Use GPU acceleration (pyrit/hashcat) for faster cracking",
        "Target networks with clients for WPA handshake capture"
      ]
    },

    "legal_disclaimer": {
      "title": "⚠️ FOR AUTHORIZED SECURITY TESTING ONLY ⚠️",
      "message": "This tool is designed for legitimate security assessments on networks you OWN or have EXPLICIT WRITTEN PERMISSION to test.",
      "warnings": [
        "Unauthorized access to computer networks is ILLEGAL in most jurisdictions",
        "Unauthorized access is UNETHICAL and violates privacy",
        "Unauthorized access is subject to criminal prosecution"
      ],
      "agreement": [
        "Only test networks you own or have permission for",
        "Comply with all applicable laws",
        "Accept full responsibility for your actions"
      ],
      "liability": "The author assumes NO LIABILITY for misuse of this tool."
    },

    "contributing": {
      "steps": [
        "Fork the repository",
        "Create a feature branch: `git checkout -b feature/amazing-feature`",
        "Commit changes: `git commit -m 'Add amazing feature'`",
        "Push to branch: `git push origin feature/amazing-feature`",
        "Open a Pull Request"
      ],
      "development_setup": [
        "git clone https://github.com/YOUR_USERNAME/saifite.git",
        "cd saifite",
        "python3 -m venv venv",
        "source venv/bin/activate",
        "pip3 install -r requirements-dev.txt",
        "python3 -m pytest tests/"
      ]
    },

    "license": {
      "name": "GNU General Public License v2.0",
      "copyright": "Copyright (C) 2024 SAIF UL ISLAM (@saifulislaam)",
      "description": "This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.",
      "warranty": "This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.",
      "full_text_link": "https://www.gnu.org/licenses/gpl-2.0.txt"
    },

    "contact": {
      "github": "github.com/saifulislaam/saifite",
      "issues": "github.com/saifulislaam/saifite/issues",
      "discussions": "github.com/saifulislaam/saifite/discussions"
    },

    "repository_structure": {
      "files": [
        "saifite.py",
        "saifite_gui.py",
        "README.md",
        "LICENSE",
        "requirements.txt",
        "cracked.csv"
      ],
      "directories": [
        "handshakes/",
        "assets/",
        "docs/"
      ],
      "assets": [
        "assets/logo.png",
        "assets/footer.png"
      ],
      "docs": [
        "docs/installation.md",
        "docs/usage.md",
        "docs/api.md"
      ]
    },

    "footer": {
      "text": "Made with 💚 by SAIF UL ISLAM",
      "copyright": "© 2024 | Ethical Hacking | Security Research",
      "social": "@saifulislaam"
    }
  }
}
