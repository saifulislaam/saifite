# SAIFITE - Professional Wireless Security Auditor

<p align="center">
  <img src="https://raw.githubusercontent.com/saifulislaam/saifite/assets/logo.png" alt="SAIFITE Logo" width="200">
</p>

<p align="center">
  <strong>⚡ HACK THE NETWORK ⚡</strong>
</p>

<p align="center">
  <a href="https://github.com/saifulislaam/saifite">
    <img src="https://img.shields.io/badge/GitHub-saifulislaam%2Fsaifite-brightgreen?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://github.com/saifulislaam/saifite/releases">
    <img src="https://img.shields.io/github/v/release/saifulislaam/saifite?style=for-the-badge&color=00FF41" alt="Version">
  </a>
  <a href="https://github.com/saifulislaam/saifite/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/saifulislaam/saifite?style=for-the-badge&color=00FF41" alt="License">
  </a>
  <a href="https://github.com/saifulislaam/saifite/issues">
    <img src="https://img.shields.io/github/issues/saifulislaam/saifite?style=for-the-badge&color=00FF41" alt="Issues">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-00FF41?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Linux-Kali%20%7C%20Ubuntu%20%7C%20Parrot-00FF41?style=flat-square&logo=linux" alt="Linux">
  <img src="https://img.shields.io/badge/Tools-aircrack--ng%20%7C%20reaver-00FF41?style=flat-square" alt="Tools">
</p>

---

## 📌 **Description**

**SAIFITE** is a **professional, automated wireless network security auditing tool** designed for security professionals and ethical hackers. It provides a complete suite of tools to assess Wi-Fi network security through various attack vectors including WPA/WPA2 handshake capture, WEP cracking, and WPS PIN brute-force attacks.

### 🎯 **Key Features**

| Feature | Description |
|---------|-------------|
| 🔍 **Network Discovery** | Real-time scanning of wireless networks with signal strength analysis |
| 🤝 **WPA Handshake Capture** | Capture 4-way handshake using deauthentication attacks |
| 🔑 **WPA Cracking** | Dictionary-based password cracking with aircrack-ng |
| 🔓 **WEP Attacks** | Multiple attack methods (ARP replay, Chop-chop, Fragmentation, Caffe-latte) |
| 📍 **WPS Attacks** | PIN brute-force and Pixie-Dust attacks using reaver |
| 💾 **Cracked Database** | Persistent storage of cracked networks in CSV format |
| 🖥️ **Dual Interface** | Both CLI and GUI versions available |
| 🎨 **Cyber Theme** | Hacker-style green-on-black interface |

### 🛠️ **Attack Methods**

#### WPA/WPA2
- Deauthentication attack for handshake capture
- Dictionary-based cracking
- Multi-tool handshake verification (aircrack, tshark, pyrit, cowpatty)

#### WEP
- ARP replay attack
- Chop-chop attack
- Fragmentation attack
- Caffe-latte attack
- P0841 attack
- Hirte attack

#### WPS
- PIN brute-force (reaver)
- Pixie-Dust attack (vulnerable routers)
- WPS lock status detection

---

## 📋 **Table of Contents**

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Commands Reference](#-commands-reference)
- [GUI Guide](#-gui-guide)
- [Requirements](#-requirements)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Legal Disclaimer](#-legal-disclaimer)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 **Installation**

### **Method 1: Direct Download**

```bash
# Clone the repository
git clone https://github.com/saifulislaam/saifite.git
cd saifite

# Make executable
chmod +x saifite.py saifite_gui.py

# Run CLI version
sudo python3 saifite.py

# Run GUI version
sudo python3 saifite_gui.py
```

### **Method 2: One-Line Install**

```bash
git clone https://github.com/saifulislaam/saifite.git && cd saifite && sudo python3 saifite.py
```

### **Method 3: Install Dependencies**

```bash
# Install required system tools
sudo apt-get update
sudo apt-get install -y aircrack-ng reaver tshark python3-tk

# Install Python dependencies
pip3 install matplotlib numpy

# Run the tool
sudo python3 saifite.py
```

---

## 🎮 **Quick Start**

### **CLI Version (saifite.py)**

```bash
# Basic scan and attack
sudo python3 saifite.py

# Target specific network
sudo python3 saifite.py -e "MyNetwork" -b 00:11:22:33:44:55

# WPS Pixie-dust only
sudo python3 saifite.py --wps --pixie

# Capture WPA handshake with cracking
sudo python3 saifite.py --wpa --crack /usr/share/wordlists/rockyou.txt

# Show previously cracked networks
sudo python3 saifite.py --cracked
```

### **GUI Version (saifite_gui.py)**

```bash
# Launch GUI
sudo python3 saifite_gui.py

# GUI Navigation:
# F5 - Start Scan
# F6 - Stop Scan
# F9 - Start Attack
# F10 - Stop Attack
# Ctrl+L - Clear Log
# Ctrl+Q - Exit
```

---

## 📖 **Usage Guide**

### **CLI Commands**

#### **Global Options**

| Command | Description | Example |
|---------|-------------|---------|
| `-i, --interface` | Wireless interface | `-i wlan0` |
| `-c, --channel` | Channel to scan | `-c 6` |
| `-e, --essid` | Target ESSID | `-e "MyWiFi"` |
| `-b, --bssid` | Target BSSID | `-b 00:11:22:33:44:55` |
| `--all` | Attack all targets | `--all` |
| `--showb` | Show BSSIDs in scan | `--showb` |
| `--power` | Minimum power level | `--power 50` |
| `--mac` | Spoof MAC address | `--mac` |
| `--quiet` | Quiet mode | `--quiet` |

#### **WPA/WPA2 Options**

| Command | Description | Default |
|---------|-------------|---------|
| `--wpa` | Enable WPA attacks | On |
| `--wpat` | Attack timeout (seconds) | 500 |
| `--wpadt` | Deauth timeout (seconds) | 10 |
| `--crack` | Crack handshakes | Off |
| `--dict` | Dictionary file | auto |
| `--strip` | Strip handshake | On |

#### **WEP Options**

| Command | Description | Default |
|---------|-------------|---------|
| `--wep` | Enable WEP attacks | On |
| `--pps` | Packets per second | 600 |
| `--wept` | Attack timeout | 600 |
| `--wepca` | IVs to start cracking | 10000 |
| `--chopchop` | Chop-chop attack | On |
| `--arpreplay` | ARP replay attack | On |

#### **WPS Options**

| Command | Description | Default |
|---------|-------------|---------|
| `--wps` | Enable WPS attacks | On |
| `--pixie` | Pixie-dust only | Off |
| `--wpst` | Attack timeout | 660 |
| `--wpsratio` | Success ratio threshold | 0.01 |

### **Attack Workflow**

```bash
# Step 1: Scan for networks
sudo python3 saifite.py -i wlan0

# Step 2: Select target (interactive)

# Step 3: Attack based on encryption type
# - WPA: Captures handshake, then cracks
# - WEP: Injects packets, collects IVs, cracks
# - WPS: Brute-forces PIN or uses Pixie-dust

# Step 4: Results saved to cracked.csv
```

---

## 🖥️ **GUI Guide**

### **Dashboard Tab**
- Interface control (enable/disable monitor mode)
- MAC spoofing toggle
- Real-time statistics
- ASCII charts for network analysis
- Quick command buttons

### **Network Scanner Tab**
- Channel selection
- Signal strength filtering
- Target discovery
- Client association display
- Add to attack list

### **Attack Center Tab**
- Attack mode selection (WPA/WEP/WPS)
- Target queue management
- Attack settings configuration
- Progress tracking
- Attack console output

### **Handshake Lab Tab**
- Handshake capture with BSSID targeting
- Captured handshakes list
- Handshake analysis
- Dictionary cracking
- Delete functionality

### **WPS Cracker Tab**
- WPS-enabled targets list
- Lock status checking
- PIN brute-force attack
- Pixie-dust attack
- WPS console output

### **Cracked DB Tab**
- Statistics banner
- Cracked networks database
- Export to CSV/TXT
- Copy password to clipboard
- Clear history

### **Console Tab**
- Real-time logging
- Color-coded messages
- Filter functionality
- Save/export logs

---

## 📦 **Requirements**

### **System Requirements**
- **OS**: Linux (Kali, Ubuntu, Parrot, Debian)
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (2GB recommended)
- **Disk Space**: 500MB for tools + wordlists

### **Hardware Requirements**
- **Wireless Adapter**: Must support monitor mode and packet injection
  - Recommended: Alfa AWUS036ACH, TP-Link TL-WN722N v1
  - Chipset: Atheros AR9271, RTL8187, RTL8812AU

### **Software Dependencies**

```bash
# Required (must have)
aircrack-ng        # Core wireless tools
reaver             # WPS attacks
tshark             # Packet analysis
iwconfig           # Wireless configuration

# Optional (recommended)
pyrit              # GPU acceleration
cowpatty           # Handshake verification
hashcat            # Advanced cracking
```

### **Wordlists**
- rockyou.txt (`/usr/share/wordlists/rockyou.txt`)
- fasttrack.txt (`/usr/share/wordlists/fasttrack.txt`)
- Custom wordlists supported

---

## 📸 **Screenshots**

### CLI Interface
```
  ███████╗ █████╗ ██╗███████╗██╗████████╗███████╗
  ██╔════╝██╔══██╗██║██╔════╝██║╚══██╔══╝██╔════╝
  ███████╗███████║██║█████╗  ██║   ██║   █████╗  
  ╚════██║██╔══██║██║██╔══╝  ██║   ██║   ██╔══╝  
  ███████║██║  ██║██║██║     ██║   ██║   ███████╗
  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝   ╚═╝   ╚══════╝

  HACK THE NETWORK
  v2024.1

  [+] scanning for wireless devices...
  [+] enabling monitor mode on wlan0... done

   NUM ESSID                 CH  ENCR  POWER  WPS?  CLIENT
   --- --------------------  --  ----  -----  ----  ------
    1  MyWiFi                 6  WPA2    75db  wps   client
    2  GuestNet              11  WPA     45db   no     
    3  TestWEP                3  WEP     60db   no    client
```

### GUI Dashboard
```
╔══════════════════════════════════════════════════════════════════╗
║                      SECURITY DASHBOARD                          ║
║                   Real-time Network Intelligence                  ║
╚══════════════════════════════════════════════════════════════════╝

[ INTERFACE CONTROL ]
$> SELECT INTERFACE: [wlan0    ▼] [START MONITOR] [STOP MONITOR] [SPOOF MAC]
$> MONITOR MODE: ACTIVE (blinking)
$> MAC SPOOF: [x] ENABLED

[ STATISTICS ]
NETWORKS: 0045    CLIENTS: 0012    HANDSHAKES: 0001
CRACKED: 0003     WPS: 0008        ACTIVE: 01
```

---

## 🔧 **Troubleshooting**

### **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| **"No wireless interfaces found"** | Plug in wireless adapter, check `iwconfig` |
| **"Monitor mode failed"** | Run `sudo airmon-ng check kill` first |
| **"reaver: command not found"** | Install reaver: `sudo apt-get install reaver` |
| **"Handshake not captured"** | Move closer to target, increase deauth count |
| **"WPS locked"** | Wait 5-10 minutes, target may have anti-hammering |
| **"Dictionary not found"** | Download rockyou.txt or specify custom wordlist |
| **"Permission denied"** | Must run as root: `sudo python3 saifite.py` |

### **Debug Mode**

```bash
# Run with verbose output
sudo python3 saifite.py --verbose

# Check tool dependencies
sudo python3 saifite.py --check

# Test interface injection
sudo aireplay-ng --test wlan0mon
```

### **Performance Tips**

1. **Use a powerful wireless adapter** (Alfa cards recommended)
2. **Position antenna properly** for better signal
3. **Close unnecessary programs** to free resources
4. **Use GPU acceleration** (pyrit/hashcat) for faster cracking
5. **Target networks with clients** for WPA handshake capture

---

## ⚖️ **Legal Disclaimer**

```
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️  FOR AUTHORIZED SECURITY TESTING ONLY  ⚠️                    ║
║                                                                    ║
║  This tool is designed for legitimate security assessments on     ║
║  networks you OWN or have EXPLICIT WRITTEN PERMISSION to test.    ║
║                                                                    ║
║  Unauthorized access to computer networks is:                     ║
║  • ILLEGAL in most jurisdictions                                 ║
║  • UNETHICAL and violates privacy                                 ║
║  • Subject to criminal prosecution                               ║
║                                                                    ║
║  By using this tool, you agree to:                               ║
║  • Only test networks you own or have permission for              ║
║  • Comply with all applicable laws                                ║
║  • Accept full responsibility for your actions                    ║
║                                                                    ║
║  The author assumes NO LIABILITY for misuse of this tool.         ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## 🤝 **Contributing**

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### **Development Setup**

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/saifite.git
cd saifite

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip3 install -r requirements-dev.txt

# Run tests
python3 -m pytest tests/
```

---

## 📄 **License**

```
GNU General Public License v2.0

Copyright (C) 2024 SAIF UL ISLAM (@saifulislaam)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
```

---

## 📞 **Contact & Support**

| Platform | Link |
|----------|------|
| **GitHub** | [github.com/saifulislaam/saifite](https://github.com/saifulislaam/saifite) |
| **Issues** | [github.com/saifulislaam/saifite/issues](https://github.com/saifulislaam/saifite/issues) |
| **Discussions** | [github.com/saifulislaam/saifite/discussions](https://github.com/saifulislaam/saifite/discussions) |

---

## ⭐ **Show Your Support**

If you find SAIFITE useful, please consider:
- ⭐ Starring the repository on GitHub
- 🐛 Reporting issues and bugs
- 🔧 Contributing code or documentation
- 📢 Sharing with fellow security professionals

---

<p align="center">
  <strong>created by SAIF UL ISLAM</strong><br>
  <strong>© 2025-26 | Ethical Hacking | Security Research</strong>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/saifulislaam/saifite/assets/footer.png" alt="Footer" width="400">
</p>

---

## 📁 **Repository Structure**

```
saifite/
├── saifite.py              # CLI version
├── saifite_gui.py          # GUI version
├── README.md               # This file
├── LICENSE                 # GPL v2 license
├── requirements.txt        # Python dependencies
├── cracked.csv             # Cracked networks database
├── handshakes/             # Captured handshakes directory
├── assets/                 # Images and assets
│   ├── logo.png
│   └── footer.png
└── docs/                   # Documentation
    ├── installation.md
    ├── usage.md
    └── api.md
```

---

**Happy Ethical Hacking! **
