#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =================================================================
# 🚀 MIKRONETPLUS - ULTRA GRE TUNNEL HIERARCHY MANAGER
# 📺 Presented by: Mikronet_plus YouTube Channel (2026)
# =================================================================

import os
import subprocess
import sys
import time

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
    """تبدیل خودکار و ریاضی آی‌پی نسخه ۴ به سابنت استاندارد 6to4"""
    try:
        parts = [int(x) for x in ipv4_str.split('.')]
        return f"2002:{parts[0]:02x}{parts[1]:02x}:{parts[2]:02x}{parts[3]:02x}::1"
    except:
        return None

def manage_regular_gre():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  METHOD 1: REGULAR IPv4 GRE TUNNEL{C_END}")
    print("─"*50)
    local = input(f"{C_YELLOW}🔹 1. Local Linux Public IPv4: {C_END}").strip()
    remote = input(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4: {C_END}").strip()
    tunnel_cidr = input(f"{C_YELLOW}🔹 3. Tunnel Internal IP (e.g., 10.10.10.1/30): {C_END}").strip()
    
    print(f"\n{C_BOLD}📊 Preview Configuration:{C_END}")
    print(f"  ▫️ Mode      : IPv4 GRE")
    print(f"  ▫️ Local IP  : {C_GREEN}{local}{C_END}")
    print(f"  ▫️ Remote IP : {C_GREEN}{remote}{C_END}")
    print(f"  ▫️ Tunnel IP : {C_GREEN}{tunnel_cidr}{C_END}")
    print("─"*50)
    
    if input(f"{C_BOLD}🤔 Apply this tunnel? (y/n): {C_END}").strip().lower() == 'y':
        yaml_content = f"network:\n  version: 2\n  tunnels:\n    gre-to-mikro:\n      mode: gre\n      local: {local}\n      remote: {remote}\n      addresses:\n        - {tunnel_cidr}\n"
        with open(YAML_REGULAR_PATH, "w") as f: f.write(yaml_content)
        
        print(f"\n{C_YELLOW}⏳ Applying Netplan...{C_END}")
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            time.sleep(2)
            subprocess.run(["ip", "link", "set", "dev", "gre-to-mikro", "up"])
            print(f"\n{C_GREEN}{C_BOLD}✅ Regular GRE Tunnel is now UP & ONLINE!{C_END}")
        else: print(f"\n{C_RED}❌ Netplan Apply Failed!{C_END}")
    input(f"\nPress Enter to return to main menu...")

def manage_6to4_gre6():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  METHOD 2: HYBRID 6to4 > GRE6 TUNNEL (IPv6 Infrastructure){C_END}")
    print("─"*50)
    local_v4 = input(f"{C_YELLOW}🔹 1. Local Linux Public IPv4: {C_END}").strip()
    remote_v4 = input(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4: {C_END}").strip()
    tunnel_cidr = input(f"{C_YELLOW}🔹 3. Tunnel Internal IPv4 (e.g., 10.20.20.1/30): {C_END}").strip()
    
    # محاسبه خودکار IPv6 بر اساس استاندارد 6to4
    local_v6 = ipv4_to_6to4(local_v4)
    remote_v6 = ipv4_to_6to4(remote_v4)
    
    if not local_v6 or not remote_v6:
        print(f"\n{C_RED}❌ Invalid IPv4 Format!{C_END}")
        input("\nPress Enter...")
        return

    print(f"\n{C_GREEN}⚡ Auto-Generated 6to4 IPv6 Infrastructure:{C_END}")
    print(f"  ▫️ Linux Local v6  : {C_CYAN}{local_v6}/16{C_END}")
    print(f"  ▫️ MikroTik Remote v6: {C_CYAN}{remote_v6}/16{C_END}")
    print("─"*50)
    
    if input(f"{C_BOLD}🤔 Apply this Hybrid Tunnel? (y/n): {C_END}").strip().lower() == 'y':
        yaml_content = f"""network:
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
            time.sleep(2)
            # فعال‌سازی اجباری هر دو اینترفیس زیرساخت و تونل اصلی
            subprocess.run(["ip", "link", "set", "dev", "ip6to4", "up"])
            subprocess.run(["ip", "link", "set", "dev", "gre6-to-mikro", "up"])
            print(f"\n{C_GREEN}{C_BOLD}✅ Hybrid 6to4 > GRE6 Tunnel is now UP & RUNNING!{C_END}")
        else: print(f"\n{C_RED}❌ Netplan Apply Failed!{C_END}")
    input(f"\nPress Enter to return to main menu...")

def check_all_status():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🔍  MIKRONETPLUS SYSTEM STATUS REPORT{C_END}")
    print("═"*60)
    
    # چک کردن تونل معمولی
    print(f"{C_BOLD}[▶] Tunnel Method 1 (Regular GRE):{C_END}")
    if os.path.exists(YAML_REGULAR_PATH):
        if_check = subprocess.run(["ip", "link", "show", "gre-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP & RUNNING{C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN / IDLE{C_END}"
        if if_check.returncode != 0: status = f"{C_RED}NOT FOUND{C_END}"
        print(f"  ▫️ Config: Active | Interface Status: {status}")
    else:
        print(f"  ▫️ Config: {C_RED}Not Configured{C_END}")
        
    print("-" * 50)
    
    # چک کردن تونل ترکیبی
    print(f"{C_BOLD}[▶] Tunnel Method 2 (6to4 > GRE6):{C_END}")
    if os.path.exists(YAML_6TO4_PATH):
        if_check = subprocess.run(["ip", "link", "show", "gre6-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP & RUNNING{C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN / IDLE{C_END}"
        if if_check.returncode != 0: status = f"{C_RED}NOT FOUND{C_END}"
        print(f"  ▫️ Config: Active | Interface Status: {status}")
    else:
        print(f"  ▫️ Config: {C_RED}Not Configured{C_END}")
        
    print("═"*60)
    
    if input(f"\n{C_BOLD}⚡ Launch Live Diagnostic Ping? (y/n): {C_END}").strip().lower() == 'y':
        target = input(f"{C_YELLOW}🎯 Enter Target Internal Tunnel IP: {C_END}").strip()
        print(f"\n⏳ Pinging {target}...\n")
        subprocess.run(["ping", "-c", "4", target])
    input(f"\nPress Enter to return to main menu...")

# چرخه اصلی منو
while True:
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}╔" + "═"*58 + "╗")
    print("║ 🚀  MIKRONETPLUS - ULTIMATE TUNNEL CORE MANAGER         ║")
    print("║ 📺  Presented by: Mikronet_plus YouTube Channel         ║")
    print("╚" + "═"*58 + "╝" + f"{C_END}")
    
    print(f"{C_BOLD}📱 SELECT TUNNEL METHOD:{C_END}")
    print(f"  {C_GREEN}[1]{C_END} 🛠️  Regular IPv4 GRE Tunnel")
    print(f"  {C_GREEN}[2]{C_END} ⚡  Hybrid 6to4 > GRE6 Tunnel (Best for Restrictions)")
    print(f"  {C_GREEN}[3]{C_END} 🔍  Check Status & Live Diagnostics")
    print(f"  {C_RED}[4]{C_END} ❌  Exit Hub")
    print(f"{C_CYAN}" + "─"*60 + f"{C_END}")
    
    choice = input(f"{C_BOLD}👉 Select an option (1-4): {C_END}").strip()
    
    if choice == '1': manage_regular_gre()
    elif choice == '2': manage_6to4_gre6()
    elif choice == '3': check_all_status()
    elif choice == '4':
        clear_screen()
        print(f"\n{C_GREEN}{C_BOLD}👋 Thank you for using MikroNetPlus Ultimate Hub!{C_END}\n")
        break
