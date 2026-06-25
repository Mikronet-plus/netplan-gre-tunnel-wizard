#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =================================================================
# 🚀 MIKRONETPLUS - ULTIMATE MULTI-TUNNEL HUB (WAKE-UP ASSURED)
# 📺 Presented by: Mikronet_plus YouTube Channel (2026)
# =================================================================

import os
import subprocess
import sys
import time
import re

YAML_REGULAR_PATH = "/etc/netplan/60-mikronet-tunnel.yaml"
YAML_6TO4_PATH = "/etc/netplan/70-mikronet-6to4-gre6.yaml"

# Terminal Colors
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_CYAN = "\033[96m"
C_BOLD = "\033[1m"
C_END = "\033[0m"

if os.getuid() != 0:
    print(f"\n{C_RED}{C_BOLD}❌ [Error] Access Denied! Please run with sudo.{C_END}\n")
    sys.exit(1)

def clear_screen():
    os.system('clear')

def ipv4_to_6to4(ipv4_str):
    try:
        parts = [int(x) for x in ipv4_str.split('.')]
        return f"2002:{parts[0]:02x}{parts[1]:02x}:{parts[2]:02x}{parts[3]:02x}::1"
    except:
        return None

def get_tunnel_metadata(path):
    if not os.path.exists(path):
        return None
    
    tunnel_name = "Unnamed_Tunnel"
    tunnel_ip = "Unknown"
    
    with open(path, "r") as f:
        content = f.read()
        name_match = re.search(r"# NAME:\s*(.*)", content)
        if name_match:
            tunnel_name = name_match.group(1).strip()
            
        ip_match = re.search(r"-\s*([\d\.]+)/?\d*", content)
        if ip_match:
            tunnel_ip = ip_match.group(1).strip()
            
    return {"name": tunnel_name, "ip": tunnel_ip}

def force_up_interface(iface_name, remote_tunnel_ip):
    """بیدار کردن اینترفیس و اجرای اولین پینگ زنده برای پایداری روتینگ لینوکس"""
    subprocess.run(["ip", "link", "set", "dev", iface_name, "up"])
    subprocess.run(["ip", "link", "set", "dev", iface_name, "arp", "off"])
    subprocess.run(["sysctl", "-w", f"net.ipv4.conf.{iface_name}.disable_policy=1"], capture_output=True)
    subprocess.run(["sysctl", "-w", f"net.ipv4.conf.{iface_name}.disable_xfrm=1"], capture_output=True)
    
    if remote_tunnel_ip:
        print(f"\n{C_CYAN}⚡ Initializing Network Route & Testing Connection...{C_END}")
        print(f"{C_YELLOW}⏳ Triggering tunnel with 4 live verification packets to {remote_tunnel_ip}:{C_END}\n")
        # اجرای پینگ مستقیم در ترمینال اصلی برای شکستن قفل لینوکس
        subprocess.run(["ping", "-c", "4", remote_tunnel_ip])

def manage_regular_gre():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  METHOD 1: REGULAR IPv4 GRE TUNNEL{C_END}")
    print("─"*50)
    
    t_name = input(f"{C_YELLOW}🏷️  Enter a Custom Name for this tunnel (e.g., Tunnel_Asghar): {C_END}").strip().replace(" ", "_")
    if not t_name: t_name = "Regular_GRE"
        
    local = input(f"{C_YELLOW}🔹 1. Local Linux Public IPv4: {C_END}").strip()
    remote = input(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4: {C_END}").strip()
    tunnel_cidr = input(f"{C_YELLOW}🔹 3. Tunnel Internal IP (e.g., 10.10.10.1/30): {C_END}").strip()
    
    try:
        base_ip = tunnel_cidr.split('/')[0]
        ip_parts = base_ip.split('.')
        last_octet = int(ip_parts[3])
        remote_tunnel_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{last_octet + 1 if last_octet % 2 != 0 else last_octet - 1}"
    except:
        remote_tunnel_ip = ""

    print(f"\n{C_BOLD}📊 Preview Configuration [{t_name}]:{C_END}")
    print(f"  ▫️ Local IP  : {C_GREEN}{local}{C_END}")
    print(f"  ▫️ Remote IP : {C_GREEN}{remote}{C_END}")
    print(f"  ▫️ Tunnel IP : {C_GREEN}{tunnel_cidr}{C_END}")
    print("─"*50)
    
    if input(f"{C_BOLD}🤔 Apply this tunnel? (y/n): {C_END}").strip().lower() == 'y':
        yaml_content = f"# NAME: {t_name}\nnetwork:\n  version: 2\n  tunnels:\n    gre-to-mikro:\n      mode: gre\n      local: {local}\n      remote: {remote}\n      addresses:\n        - {tunnel_cidr}\n"
        with open(YAML_REGULAR_PATH, "w") as f: f.write(yaml_content)
        
        print(f"\n{C_YELLOW}⏳ Applying Netplan...{C_END}")
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            time.sleep(1)
            force_up_interface("gre-to-mikro", remote_tunnel_ip)
            print(f"\n{C_GREEN}{C_BOLD}✅ Tunnel '{t_name}' is active and synced with system routing table!{C_END}")
        else: print(f"\n{C_RED}❌ Netplan Apply Failed!{C_END}")
    input(f"\nPress Enter to return to main menu...")

def manage_6to4_gre6():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  METHOD 2: HYBRID 6to4 > GRE6 TUNNEL{C_END}")
    print("─"*50)
    
    t_name = input(f"{C_YELLOW}🏷️  Enter a Custom Name for this tunnel (e.g., Tunnel_6to4): {C_END}").strip().replace(" ", "_")
    if not t_name: t_name = "Hybrid_6to4_GRE6"
        
    local_v4 = input(f"{C_YELLOW}🔹 1. Local Linux Public IPv4: {C_END}").strip()
    remote_v4 = input(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4: {C_END}").strip()
    tunnel_cidr = input(f"{C_YELLOW}🔹 3. Tunnel Internal IPv4 (e.g., 10.20.20.1/30): {C_END}").strip()
    
    try:
        base_ip = tunnel_cidr.split('/')[0]
        ip_parts = base_ip.split('.')
        last_octet = int(ip_parts[3])
        remote_tunnel_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{last_octet + 1 if last_octet % 2 != 0 else last_octet - 1}"
    except:
        remote_tunnel_ip = ""

    local_v6 = ipv4_to_6to4(local_v4)
    remote_v6 = ipv4_to_6to4(remote_v4)
    
    if not local_v6 or not remote_v6:
        print(f"\n{C_RED}❌ Invalid IPv4 Format!{C_END}")
        input("\nPress Enter...")
        return

    print(f"\n{C_GREEN}⚡ Auto-Generated Infrastructure Profiles:{C_END}")
    print(f"  ▫️ Linux Local v6  : {C_CYAN}{local_v6}/16{C_END}")
    print(f"  ▫️ MikroTik Remote v6: {C_CYAN}{remote_v6}/16{C_END}")
    print("─"*50)
    
    if input(f"{C_BOLD}🤔 Apply this Hybrid Tunnel? (y/n): {C_END}").strip().lower() == 'y':
        yaml_content = f"""# NAME: {t_name}
network:
  version: 2
  tunnels:
    ip6to4:
      mode: sit
      local: {local_v4}
      remote: any
      addresses:
        - "{local_v6}/16"
    gre6-to-mikro:
      mode: ip6gre
      local: {local_v6}
      remote: {remote_v6}
      addresses:
        - {tunnel_cidr}
"""
        with open(YAML_6TO4_PATH, "w") as f: f.write(yaml_content)
        
        print(f"\n{C_YELLOW}⏳ Applying Hybrid Netplan Architecture...{C_END}")
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            time.sleep(1)
            subprocess.run(["ip", "link", "set", "dev", "ip6to4", "up"])
            force_up_interface("gre6-to-mikro", remote_tunnel_ip)
            print(f"\n{C_GREEN}{C_BOLD}✅ Hybrid Tunnel '{t_name}' is active and synced with system routing table!{C_END}")
        else: print(f"\n{C_RED}❌ Netplan Apply Failed!{C_END}")
    input(f"\nPress Enter to return to main menu...")

def status_and_diagnostic_hub():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🔍  MIKRONETPLUS - INTERFACE STATUS & DIAGNOSTIC HUB{C_END}")
    print("═"*70)
    
    active_tunnels = {}
    index = 1
    
    meta_reg = get_tunnel_metadata(YAML_REGULAR_PATH)
    print(f"{C_BOLD}[Method 1] Regular IPv4 GRE:{C_END}")
    if meta_reg:
        if_check = subprocess.run(["ip", "link", "show", "gre-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP (Running){C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN{C_END}"
        print(f"  [{index}] Interface: {C_CYAN}gre-to-mikro{C_END} | Name: {C_BOLD}{meta_reg['name']}{C_END} | IP: {meta_reg['ip']} | Status: {status}")
        active_tunnels[str(index)] = {"name": meta_reg['name'], "ip": meta_reg['ip'], "type": "Regular"}
        index += 1
    else:
        print(f"  ❌ {C_RED}Not Configured{C_END}")
        
    print("-" * 70)
    
    meta_6to4 = get_tunnel_metadata(YAML_6TO4_PATH)
    print(f"{C_BOLD}[Method 2] Hybrid 6to4 > GRE6:{C_END}")
    if meta_6to4:
        if_check = subprocess.run(["ip", "link", "show", "gre6-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP (Running){C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN{C_END}"
        print(f"  [{index}] Interface: {C_CYAN}gre6-to-mikro{C_END} | Name: {C_BOLD}{meta_6to4['name']}{C_END} | IP: {meta_6to4['ip']} | Status: {status}")
        active_tunnels[str(index)] = {"name": meta_6to4['name'], "ip": meta_6to4['ip'], "type": "Hybrid"}
        index += 1
    else:
        print(f"  ❌ {C_RED}Not Configured{C_END}")
        
    print("═"*70)
    
    if not active_tunnels:
        print(f"{C_YELLOW}⚠️ No active tunnels found to ping!{C_END}")
        input(f"\nPress Enter to return to menu...")
        return

    ping_choice = input(f"{C_BOLD}⚡ Select a Tunnel number to Ping, or press Enter to skip: {C_END}").strip()
    
    if ping_choice in active_tunnels:
        selected = active_tunnels[ping_choice]
        try:
            parts = selected['ip'].split('.')
            last_octet = int(parts[3])
            remote_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{last_octet + 1 if last_octet % 2 != 0 else last_octet - 1}"
        except:
            remote_ip = selected['ip']
            
        print(f"\n🚀 Launching live diagnostics for {C_BOLD}{selected['name']}{C_END}...")
        target_ip = input(f"{C_YELLOW}🎯 Target Remote Tunnel IP [Default auto-detect: {remote_ip}]: {C_END}").strip()
        if not target_ip: target_ip = remote_ip
            
        print(f"\n⏳ Sending 4 live packets to {target_ip}...\n")
        subprocess.run(["ping", "-c", "4", target_ip])
    
    input(f"\nPress Enter to return to main menu...")

while True:
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}╔" + "═"*58 + "╗")
    print("║ 🚀  MIKRONETPLUS - ULTIMATE TUNNEL CORE MANAGER         ║")
    print("║ 📺  Presented by: Mikronet_plus YouTube Channel         ║")
    print("╚" + "═"*58 + "╝" + f"{C_END}")
    
    print(f"{C_BOLD}📱 SELECT TUNNEL METHOD:{C_END}")
    print(f"  {C_GREEN}[1]{C_END} 🛠️  Regular IPv4 GRE Tunnel")
    print(f"  {C_GREEN}[2]{C_END} ⚡  Hybrid 6to4 > GRE6 Tunnel (Best for Restrictions)")
    print(f"  {C_GREEN}[3]{C_END} 🔍  Check Status & Live Diagnostics (Ping Hub)")
    print(f"  {C_RED}[4]{C_END} ❌  Exit Hub")
    print(f"{C_CYAN}" + "─"*60 + f"{C_END}")
    
    choice = input(f"{C_BOLD}👉 Select an option (1-4): {C_END}").strip()
    
    if choice == '1': manage_regular_gre()
    elif choice == '2': manage_6to4_gre6()
    elif choice == '3': status_and_diagnostic_hub()
    elif choice == '4':
        clear_screen()
        print(f"\n{C_GREEN}{C_BOLD}👋 Thank you for using MikroNetPlus Ultimate Hub!{C_END}\n")
        break
