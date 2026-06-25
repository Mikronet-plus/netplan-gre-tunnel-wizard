#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =================================================================
# 🚀 MIKRONETPLUS - ULTIMATE MULTI-TUNNEL HUB (CINEMATIC EDITION)
# 📺 Presented by: Mikronet_plus YouTube Channel (2026)
# 🌐 GitHub Repository: https://github.com/Mikronet-plus/netplan-gre-tunnel-wizard
# =================================================================

import os
import subprocess
import sys
import time
import re
import shutil

# Netplan and Keepalive Config Paths
YAML_REGULAR_PATH = "/etc/netplan/60-mikronet-tunnel.yaml"
YAML_6TO4_PATH = "/etc/netplan/70-mikronet-6to4-gre6.yaml"
KEEPALIVE_SCRIPT_PATH = "/usr/local/bin/mikronet_keepalive.sh"

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

def get_terminal_width():
    """محاسبه عرض ترمینال برای وسط‌چین کردن دقیق متون"""
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def slow_print(text, speed=0.03, center=False):
    """چاپ کاراکتر به کاراکتر با قابلیت هوشمند وسط‌چین کردن متن"""
    if center:
        width = get_terminal_width()
        # حذف کدهای رنگی برای محاسبه دقیق طول واقعی متن
        plain_text = re.sub(r'\033\[[0-9;]*m', '', text)
        padding = max(0, (width - len(plain_text)) // 2)
        sys.stdout.write(" " * padding)
        
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def play_animated_intro():
    clear_screen()
    width = get_terminal_width()
    
    # طراحی باکس ماتریکسی وسط‌چین
    box_title = "⚡ INITIALIZING MIKRONETPLUS CORE SYSTEM... ⚡"
    padding = max(0, (width - len(box_title)) // 2)
    
    print("\n" * 2)
    print(" " * padding + f"{C_CYAN}{C_BOLD}╔" + "═"*(len(box_title)+2) + "╗")
    print(" " * padding + f"║ {box_title} ║")
    print(" " * padding + f"╚" + "═"*(len(box_title)+2) + f"╝{C_END}\n")
    time.sleep(0.4)
    
    # خط جداکننده وسط چین
    sep = "─" * 68
    sep_pad = max(0, (width - 68) // 2)
    
    slow_print(f"{C_GREEN}{C_BOLD}📢 OFFICIAL PROJECT LINKS & SOCIAL MEDIA:{C_END}", 0.02, center=True)
    print(" " * sep_pad + f"{C_CYAN}{sep}{C_END}")
    
    slow_print(f"🐙 GitHub  : {C_GREEN}{C_BOLD}https://github.com/Mikronet-plus/netplan-gre-tunnel-wizard{C_END}", 0.02, center=True)
    slow_print(f"📺 YouTube : {C_YELLOW}{C_BOLD}https://www.youtube.com/@Mikronet_plus{C_END}", 0.02, center=True)
    slow_print(f"🚀 Telegram: {C_YELLOW}{C_BOLD}https://t.me/Mikronet_plus{C_END}", 0.02, center=True)
    
    print(" " * sep_pad + f"{C_CYAN}{sep}{C_END}")
    
    slow_print(f"\n{C_GREEN}⌛ Loading Core Matrix Components, Please Wait...{C_END}", 0.01, center=True)
    time.sleep(1.5)

def play_cinematic_outro():
    """افکت خروج فوق‌العاده اسلو موشن و سایبرپانکی"""
    clear_screen()
    width = get_terminal_width()
    
    print("\n" * 3)
    slow_print(f"{C_RED}{C_BOLD}🛑 DISCONNECTING FROM MIKRONETPLUS HUB CORE...{C_END}", 0.04, center=True)
    time.sleep(0.4)
    
    # شبیه‌سازی لودینگ خروج ماتریکسی
    bar_width = 40
    bar_pad = max(0, (width - bar_width - 10) // 2)
    for i in range(1, bar_width + 1):
        percent = int((i / bar_width) * 100)
        sys.stdout.write("\r" + " " * bar_pad + f"{C_CYAN}[{C_GREEN}" + "█"*i + " "*(bar_width-i) + f"{C_CYAN}] {C_YELLOW}{percent}%")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")
    
    time.sleep(0.3)
    slow_print(f"{C_GREEN}{C_BOLD}✨ Thank you for using MikroNetPlus CLI Manager! ✨{C_END}", 0.03, center=True)
    slow_print(f"{C_CYAN}📺 Remember to Subscribe & Like our videos on YouTube.{C_END}", 0.03, center=True)
    slow_print(f"{C_YELLOW}🚀 Stay secure, Stay connected.{C_END}", 0.04, center=True)
    
    print("\n" * 2)
    time.sleep(0.8)
    clear_screen()

def show_big_banner():
    banner = f"""
{C_CYAN}{C_BOLD}    __  ___ _ __              _   __     __     ____   __            
   /  |/  /(_) /__  _________  / | / /__  / /_   / __ \ / /_  ______ _ 
  / /|_/ // / //_/ / ___/ __ \/  |/ / _ \/ __/  / /_/ // / / / / ___/ / 
 / /  / // / ,<   / /  / /_/ / /|  /  __/ /_   / ____// / /_/ (__  )_/  
/_/  /_//_/_/|_| /_/   \____/_/ |_/\___/\__/  /_/    /_/\__,_/____(_)   {C_END}

{C_GREEN}{C_BOLD}                     🌐  ULTIMATE MULTI-TUNNEL HUB  🌐{C_END}
{C_YELLOW}              Presented by Mikronet_plus YouTube Channel{C_END}
"""
    print(banner)

def start_background_keepalive(remote_ip):
    stop_background_keepalive()
    script_content = f"""#!/bin/bash
while true; do
    ping -c 1 {remote_ip} > /dev/null 2>&1
    sleep 20
done
"""
    try:
        with open(KEEPALIVE_SCRIPT_PATH, "w") as f:
            f.write(script_content)
        os.chmod(KEEPALIVE_SCRIPT_PATH, 0o755)
        subprocess.Popen(["nohup", KEEPALIVE_SCRIPT_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setpgrp)
        print(f"{C_GREEN}🔄 Background Keepalive Core activated! (Pinging {remote_ip} every 20s){C_END}")
    except:
        pass

def stop_background_keepalive():
    try:
        os.system(f"pkill -f {KEEPALIVE_SCRIPT_PATH} > /dev/null 2>&1")
        if os.path.exists(KEEPALIVE_SCRIPT_PATH):
            os.remove(KEEPALIVE_SCRIPT_PATH)
    except:
        pass

def ipv4_to_6to4(ipv4_str):
    try:
        parts = [int(x) for x in ipv4_str.split('.')]
        return f"2002:{parts[0]:02x}{parts[1]:02x}:{parts[2]:02x}{parts[3]:02x}::1"
    except:
        return None

def parse_yaml_fields(path, tunnel_type):
    data = {"name": "", "local": "", "remote": "", "tunnel_cidr": ""}
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        name_match = re.search(r"# NAME:\s*(.*)", content)
        data["name"] = name_match.group(1).strip() if name_match else f"Unnamed_{tunnel_type}"
        
        if tunnel_type == "Regular":
            local_match = re.search(r"local:\s*([\d\.]+)", content)
            remote_match = re.search(r"remote:\s*([\d\.]+)", content)
            cidr_match = re.search(r"-\s*([\d\.]+/\d+)", content)
            if local_match: data["local"] = local_match.group(1).strip()
            if remote_match: data["remote"] = remote_match.group(1).strip()
            if cidr_match: data["tunnel_cidr"] = cidr_match.group(1).strip()
        else:
            sit_block = re.search(r"ip6to4:\s*mode:\s*sit\s*local:\s*([\d\.]+)", content)
            if sit_block: data["local"] = sit_block.group(1).strip()
            cidr_matches = re.findall(r"-\s*([\d\.]+/\d+)", content)
            if cidr_matches: data["tunnel_cidr"] = cidr_matches[-1].strip()
    return data

def get_input_with_default(prompt, default_val):
    if default_val:
        res = input(f"{prompt} {C_CYAN}(Default: {default_val}){C_END}: ").strip()
        return res if res else default_val
    else:
        return input(f"{prompt}: ").strip()

def force_up_interface(iface_name, remote_tunnel_ip):
    subprocess.run(["ip", "link", "set", "dev", iface_name, "up"])
    subprocess.run(["ip", "link", "set", "dev", iface_name, "arp", "off"])
    subprocess.run(["sysctl", "-w", f"net.ipv4.conf.{iface_name}.disable_policy=1"], capture_output=True)
    subprocess.run(["sysctl", "-w", f"net.ipv4.conf.{iface_name}.disable_xfrm=1"], capture_output=True)
    if remote_tunnel_ip:
        print(f"\n{C_CYAN}⚡ Initializing Network Route & Testing Connection...{C_END}")
        start_background_keepalive(remote_tunnel_ip)
        print(f"\n{C_YELLOW}⏳ Sending 4 live verification packets to {remote_tunnel_ip}:{C_END}\n")
        subprocess.run(["ping", "-c", "4", remote_tunnel_ip])

def extract_remote_ping_ip(tunnel_cidr):
    try:
        base_ip = tunnel_cidr.split('/')[0]
        ip_parts = base_ip.split('.')
        last_octet = int(ip_parts[3])
        return f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{last_octet + 1 if last_octet % 2 != 0 else last_octet - 1}"
    except:
        return ""

def menu_create_tunnel():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  CREATE NEW MULTI-TUNNEL ARCHITECTURE{C_END}")
    print("─"*60)
    print(f"  {C_GREEN}[1]{C_END} Regular IPv4 GRE Tunnel")
    print(f"  {C_GREEN}[2]{C_END} Hybrid 6to4 > GRE6 Tunnel (High Performance Infrastructure)")
    print(f"  {C_RED}[B]{C_END} Back to Main Menu")
    print("─"*60)
    choice = input(f"{C_BOLD}👉 Select Tunnel Type: {C_END}").strip()
    
    if choice == '1': wizard_build_tunnel(YAML_REGULAR_PATH, "Regular")
    elif choice == '2': wizard_build_tunnel(YAML_6TO4_PATH, "Hybrid")

def wizard_build_tunnel(path, tunnel_type, default_data=None):
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🚀 WIZARD: BUILDING {tunnel_type.upper()} TUNNEL INTERFACE{C_END}")
    print("─"*60)
    
    is_edit = default_data is not None
    d = default_data if is_edit else {"name": f"{tunnel_type}_GRE", "local": "", "remote": "", "tunnel_cidr": ""}
    
    t_name = get_input_with_default(f"{C_YELLOW}🏷️  Enter Tunnel Name{C_END}", d['name']).replace(" ", "_")
    local = get_input_with_default(f"{C_YELLOW}🔹 1. Local Linux Public IPv4{C_END}", d['local'])
    remote = get_input_with_default(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4{C_END}", d['remote'])
    tunnel_cidr = get_input_with_default(f"{C_YELLOW}🔹 3. Tunnel Internal IP (e.g., 10.10.10.1/30){C_END}", d['tunnel_cidr'])
    
    remote_tunnel_ip = extract_remote_ping_ip(tunnel_cidr)
    local_v6 = ipv4_to_6to4(local)
    remote_v6 = ipv4_to_6to4(remote)
    
    if not local_v6 or not remote_v6:
        print(f"\n{C_RED}❌ Invalid IPv4 Format!{C_END}"); input("\nPress Enter..."); return
            
    print(f"\n{C_BOLD}📊 Preview Configuration [{t_name}]:{C_END}")
    print(f"  ▫️ Local IP  : {C_GREEN}{local}{C_END}")
    print(f"  ▫️ Remote IP : {C_GREEN}{remote}{C_END}")
    print(f"  ▫️ Tunnel IP : {C_GREEN}{tunnel_cidr}{C_END}")
    print("─"*60)
    
    if input(f"{C_BOLD}🤔 Apply this configuration? (y/n): {C_END}").strip().lower() == 'y':
        if tunnel_type == "Regular":
            yaml_content = f"# NAME: {t_name}\nnetwork:\n  version: 2\n  tunnels:\n    gre-to-mikro:\n      mode: gre\n      local: {local}\n      remote: {remote}\n      addresses:\n        - {tunnel_cidr}\n"
            iface = "gre-to-mikro"
        else:
            yaml_content = f"""# NAME: {t_name}
network:
  version: 2
  tunnels:
    ip6to4:
      mode: sit
      local: {local}
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
            iface = "gre6-to-mikro"
            
        with open(path, "w", encoding="utf-8") as f: f.write(yaml_content)
        
        print(f"\n{C_YELLOW}⏳ Applying Netplan Configuration...{C_END}")
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            time.sleep(1)
            if tunnel_type == "Hybrid": subprocess.run(["ip", "link", "set", "dev", "ip6to4", "up"])
            force_up_interface(iface, remote_tunnel_ip)
            print(f"\n{C_GREEN}{C_BOLD}✅ Tunnel operation completed successfully!{C_END}")
        else: print(f"\n{C_RED}❌ Error! Netplan Apply Failed.{C_END}")
    input(f"\nPress Enter to return...")

def menu_edit_tunnel():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}📝 EDIT ACTIVE TUNNEL CORE INTERFACES{C_END}")
    print("═"*70)
    
    tunnels_pool = []
    reg_data = parse_yaml_fields(YAML_REGULAR_PATH, "Regular")
    if reg_data: tunnels_pool.append({"path": YAML_REGULAR_PATH, "type": "Regular", "data": reg_data})
    v6_data = parse_yaml_fields(YAML_6TO4_PATH, "Hybrid")
    if v6_data: tunnels_pool.append({"path": YAML_6TO4_PATH, "type": "Hybrid", "data": v6_data})
    
    if not tunnels_pool:
        print(f"{C_RED}{C_BOLD}❌ No tunnels detected on this system! Create a tunnel first.{C_END}")
        print("═"*70)
        input(f"\nPress Enter to return to main menu...")
        return
        
    print(f"{C_BOLD}🎯 System Detected the following active tunnels:{C_END}\n")
    for idx, item in enumerate(tunnels_pool, 1):
        print(f"  {C_GREEN}[{idx}]{C_END} Type: {C_CYAN}{item['type']}{C_END} | Name: {C_BOLD}{item['data']['name']}{C_END} | IP Pool: {item['data']['tunnel_cidr']}")
    print(f"  {C_RED}[B]{C_END} Cancel and return to menu")
    print("═"*70)
    
    choice = input(f"{C_BOLD}👉 Which tunnel do you want to edit? (1-{len(tunnels_pool)}): {C_END}").strip()
    if choice.lower() == 'b' or not choice: return
    
    try:
        selected_idx = int(choice) - 1
        if 0 <= selected_idx < len(tunnels_pool):
            target = tunnels_pool[selected_idx]
            wizard_build_tunnel(target['path'], target['type'], target['data'])
        else: print(f"{C_RED}❌ Invalid selection!{C_END}"); time.sleep(1)
    except ValueError: print(f"{C_RED}❌ Please enter a valid number!{C_END}"); time.sleep(1)

def menu_delete_tunnel():
    clear_screen()
    print(f"{C_RED}{C_BOLD}❌ REMOVE TUNNEL INTERFACES FROM NETPLAN{C_END}")
    print("─"*60)
    
    has_tunnel = False
    if os.path.exists(YAML_REGULAR_PATH):
        has_tunnel = True
        if input(f"{C_YELLOW}⚠️  Delete Regular GRE Tunnel? (y/n): {C_END}").lower() == 'y':
            os.remove(YAML_REGULAR_PATH)
            print(f"{C_RED}🗑️  Regular GRE config removed.{C_END}")
            
    if os.path.exists(YAML_6TO4_PATH):
        has_tunnel = True
        if input(f"{C_YELLOW}⚠️  Delete Hybrid 6to4 > GRE6 Tunnel? (y/n): {C_END}").lower() == 'y':
            os.remove(YAML_6TO4_PATH)
            print(f"{C_RED}🗑️  Hybrid 6to4 config removed.{C_END}")
            
    if has_tunnel:
        stop_background_keepalive()
        print(f"\n{C_YELLOW}⏳ Flashing Netplan Core Infrastructure...{C_END}")
        subprocess.run(["netplan", "apply"])
        print(f"{C_GREEN}✅ Systems flushed successfully!{C_END}")
    else: print(f"{C_YELLOW}ℹ️  No tunnels found to clear!{C_END}")
    input(f"\nPress Enter to return to main menu...")

def status_and_diagnostic_hub():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🔍  MIKRONETPLUS - INTERFACE STATUS & DIAGNOSTIC HUB{C_END}")
    print("═"*75)
    
    active_tunnels = {}
    index = 1
    
    meta_reg = parse_yaml_fields(YAML_REGULAR_PATH, "Regular")
    print(f"{C_BOLD}[Method 1] Regular IPv4 GRE:{C_END}")
    if meta_reg:
        if_check = subprocess.run(["ip", "link", "show", "gre-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP (Running){C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN{C_END}"
        print(f"  [{index}] Interface: {C_CYAN}gre-to-mikro{C_END} | Name: {C_BOLD}{meta_reg['name']}{C_END} | IP: {meta_reg['tunnel_cidr']} | Status: {status}")
        active_tunnels[str(index)] = {"name": meta_reg['name'], "ip": meta_reg['tunnel_cidr']}
        index += 1
    else: print(f"  ❌ {C_RED}Not Configured{C_END}")
        
    print("-" * 75)
    
    meta_6to4 = parse_yaml_fields(YAML_6TO4_PATH, "Hybrid")
    print(f"{C_BOLD}[Method 2] Hybrid 6to4 > GRE6:{C_END}")
    if meta_6to4:
        if_check = subprocess.run(["ip", "link", "show", "gre6-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP (Running){C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN{C_END}"
        print(f"  [{index}] Interface: {C_CYAN}gre6-to-mikro{C_END} | Name: {C_BOLD}{meta_6to4['name']}{C_END} | IP: {meta_6to4['tunnel_cidr']} | Status: {status}")
        active_tunnels[str(index)] = {"name": meta_6to4['name'], "ip": meta_6to4['tunnel_cidr']}
        index += 1
    else: print(f"  ❌ {C_RED}Not Configured{C_END}")
        
    print("═"*75)
    
    print(f"{C_BOLD}[Keepalive Daemon Status]:{C_END}")
    is_running = os.system(f"pgrep -f {KEEPALIVE_SCRIPT_PATH} > /dev/null 2>&1") == 0
    if is_running: print(f"  🟢 Keepalive Service: {C_GREEN}ACTIVE (Pinging every 20s in background){C_END}")
    else: print(f"  🔴 Keepalive Service: {C_RED}INACTIVE{C_END}")
    print("═"*75)

    print(f"  {C_GREEN}[1-2]{C_END} Select Tunnel number to Ping diagnostics")
    print(f"  {C_RED}[K]{C_END}   Stop Background Keepalive Service")
    print(f"  {C_YELLOW}[Enter]{C_END} Return to Main Menu")
    print("-" * 75)
    
    ping_choice = input(f"{C_BOLD}👉 Choice: {C_END}").strip()
    if ping_choice.lower() == 'k':
        stop_background_keepalive()
        print(f"\n{C_RED}🛑 Keepalive daemon stopped successfully!{C_END}"); time.sleep(1.5); return
        
    if ping_choice in active_tunnels:
        selected = active_tunnels[ping_choice]
        remote_ip = extract_remote_ping_ip(selected['ip'])
        print(f"\n🚀 Launching live diagnostics for [{C_BOLD}{selected['name']}{C_END}]...")
        target_ip = input(f"{C_YELLOW}🎯 Target Remote Tunnel IP [Default auto-detect: {remote_ip}]: {C_END}").strip()
        if not target_ip: target_ip = remote_ip
        print(f"\n⏳ Sending 4 live packets to {target_ip}...\n")
        subprocess.run(["ping", "-c", "4", target_ip])
        input(f"\nPress Enter to return to main menu...")

# TRIGGER METRIC INTRO
play_animated_intro()

# Main CLI Loop
while True:
    clear_screen()
    show_big_banner()
    
    print(f"{C_BOLD}📱 SELECT OPERATION CORE:{C_END}")
    print(f"  {C_GREEN}[1]{C_END} 🛠️  Create New Tunnel Interface (Regular / Hybrid)")
    print(f"  {C_GREEN}[2]{C_END} 📝  Edit / Modify Existing Tunnels")
    print(f"  {C_GREEN}[3]{C_END} ❌  Delete / Remove Active Tunnels")
    print(f"  {C_GREEN}[4]{C_END} 🔍  Check Status & Live Diagnostics (Ping Hub)")
    print(f"  {C_RED}[5]{C_END} ❌  Exit Hub")
    print(f"{C_CYAN}" + "─"*72 + f"{C_END}")
    
    choice = input(f"{C_BOLD}👉 Select an option (1-5): {C_END}").strip()
    
    if choice == '1': menu_create_tunnel()
    elif choice == '2': menu_edit_tunnel()
    elif choice == '3': menu_delete_tunnel()
    elif choice == '4': status_and_diagnostic_hub()
    elif choice == '5':
        play_cinematic_outro()
        break
