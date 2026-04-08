# SAIFITE Installation Guide

## System Requirements

### Minimum Requirements
- **OS**: Linux (Kali Linux, Ubuntu 20.04+, Parrot OS, Debian)
- **Python**: 3.8 or higher
- **RAM**: 512 MB (1 GB recommended)
- **Disk Space**: 500 MB for tools + wordlists
- **Wireless Adapter**: Must support monitor mode and packet injection

### Recommended Hardware
- **Wireless Adapter**: Alfa AWUS036ACH, TP-Link TL-WN722N v1
- **Chipset**: Atheros AR9271, RTL8187, RTL8812AU
- **RAM**: 2 GB or more
- **Processor**: Dual-core or better

---

## Installation Methods

### Method 1: Quick Install (Ubuntu/Debian/Kali)

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y git python3 python3-pip python3-tk \
    aircrack-ng reaver tshark wireshark \
    build-essential libssl-dev libffi-dev

# Clone repository
git clone https://github.com/saifulislaam/saifite.git
cd saifite

# Install Python dependencies
pip3 install -r requirements.txt

# Make executables
chmod +x saifite.py saifite_gui.py

# Run SAIFITE
sudo python3 saifite.py
