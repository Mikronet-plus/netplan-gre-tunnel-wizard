#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =================================================================
# 🚀 MIKRONETPLUS - MULTI-TUNNEL HUB (TRUE EDIT MODE & KEEPALIVE)
# 📺 Presented by: Mikronet_plus YouTube Channel (2026)
# =================================================================

import os
import subprocess
import sys
import time
import re

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

def slow_print(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def play_animated_intro():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}╔" + "═"*58 + "╗")
    print("║  ⚡ INITIALIZING MIKRONETPLUS CORE SYSTEM...             ║")
    print("╚" + "═"*58 + f"╝{C_END}\n")
    time.sleep(0.3)
    
    slow_print(f"{C_GREEN}{C_BOLD}📢 FOLLOW US ON SOCIAL MEDIA FOR UPDATES:{C_END}", 0.03)
    print(f"{C_CYAN}─{C_END}"*60)
    slow_print(f"📺 YouTube : {C_YELLOW}{C_BOLD}https://www.youtube.com/@Mikronet_plus{C_END}", 0.04)
    slow_print(f"🚀 Telegram: {C_YELLOW}{C_BOLD}https://t.me/Mikronet_plus{C_END}", 0.04)
    print(f"{C_CYAN}─{C_END}"*60)
    
    slow_print(f"\n{C_GREEN}⌛ Loading Core Components, Please Wait...{C_END}", 0.02)
    time.sleep(1.2)

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

def parse_yaml_fields(path):
    """استخراج پیشرفته اطلاعات فایل نت‌پلان برای بخش ادیت"""
    data = {"name": "Regular_GRE", "local": "", "remote": "", "tunnel_cidr": ""}
    if not os.path.exists(path):
        return data
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        name_match = re.search(r"# NAME:\s*(.*)", content)
        if name_match: data["name"] = name_match.group(1).strip()
        
        local_match = re.search(r"local:\s*([\d\.]+|[a-fA-F\d\:]+)", content)
        if local_match: data["local"] = local_match.group(1).strip()
        
        remote_match = re.search(r"remote:\s*([\d\.]+|[a-fA-F\d\:]+|any)", content)
        if remote_match: data["remote"] = remote_match.group(1).strip()
        
        cidr_match = re.search(r"-\s*([\d\.]+/\d+|[a-fA-F\d\:]+/\d+)", content)
        if cidr_match: data["tunnel_cidr"] = cidr_match.group(1).strip()
    return data

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

def get_input_with_default(prompt, default_val):
    """گرفتن ورودی همراه با مقدار پیش‌فرض برای حالت ادیت"""
    if default_val:
        res = input(f"{prompt} {C_CYAN}(Default: {default_val}){C_END}: ").strip()
        return res if res else default_val
    else:
        return input(f"{prompt}: ").strip()

def manage_regular_gre():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  METHOD 1: REGULAR IPv4 GRE TUNNEL CORE{C_END}")
    print("─"*60)
    
    existing = parse_yaml_fields(YAML_REGULAR_PATH)
    is_edit_mode = False
    
    if os.path.exists(YAML_REGULAR_PATH):
        print(f"{C_YELLOW}⚠️  An active Regular GRE tunnel [{C_BOLD}{existing['name']}{C_END}{C_YELLOW}] already exists!{C_END}")
        print(f"  {C_GREEN}[E]{C_END} Edit/Modify existing tunnel parameters")
        print(f"  {C_RED}[O]{C_END} Overwrite completely (Fresh setup)")
        print(f"  {C_BOLD}[C]{C_END} Cancel operation")
        mode_choice = input(f"\n{C_BOLD}👉 Action (E/O/C): {C_END}").strip().lower()
        
        if mode_choice == 'c' or not mode_choice:
            return
        elif mode_choice == 'e':
            is_edit_mode = True

    t_name = get_input_with_default(f"{C_YELLOW}🏷️  Enter Tunnel Name{C_END}", existing['name'] if is_edit_mode else "Regular_GRE").replace(" ", "_")
    local = get_input_with_default(f"{C_YELLOW}🔹 1. Local Linux Public IPv4{C_END}", existing['local'] if is_edit_mode else "")
    remote = get_input_with_default(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4{C_END}", existing['remote'] if is_edit_mode else "")
    tunnel_cidr = get_input_with_default(f"{C_YELLOW}🔹 3. Tunnel Internal IP (e.g., 10.10.10.1/30){C_END}", existing['tunnel_cidr'] if is_edit_mode else "")
    
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
    print("─"*60)
    
    if input(f"{C_BOLD}🤔 Apply this tunnel configuration? (y/n): {C_END}").strip().lower() == 'y':
        yaml_content = f"# NAME: {t_name}\nnetwork:\n  version: 2\n  tunnels:\n    gre-to-mikro:\n      mode: gre\n      local: {local}\n      remote: {remote}\n      addresses:\n        - {tunnel_cidr}\n"
        with open(YAML_REGULAR_PATH, "w", encoding="utf-8") as f: f.write(yaml_content)
        
        print(f"\n{C_YELLOW}⏳ Applying Netplan Configuration...{C_END}")
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            time.sleep(1)
            force_up_interface("gre-to-mikro", remote_tunnel_ip)
            print(f"\n{C_GREEN}{C_BOLD}✅ Tunnel '{t_name}' applied and synced successfully!{C_END}")
        else: print(f"\n{C_RED}❌ Error! Netplan Apply Failed.{C_END}")
    input(f"\nPress Enter to return to main menu...")

def manage_6to4_gre6():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🛠️  METHOD 2: HYBRID 6to4 > GRE6 TUNNEL CORE{C_END}")
    print("─"*60)
    
    # برای ۶تو۴، آی‌پی لوکال اصلی را از اینترفیس sit یا خود کامپوننت دیتای فایل در میاریم
    existing = parse_yaml_fields(YAML_6TO4_PATH)
    is_edit_mode = False
    
    if os.path.exists(YAML_6TO4_PATH):
        print(f"{C_YELLOW}⚠️  An active Hybrid 6to4 tunnel [{C_BOLD}{existing['name']}{C_END}{C_YELLOW}] already exists!{C_END}")
        print(f"  {C_GREEN}[E]{C_END} Edit/Modify existing tunnel parameters")
        print(f"  {C_RED}[O]{C_END} Overwrite completely (Fresh setup)")
        print(f"  {C_BOLD}[C]{C_END} Cancel operation")
        mode_choice = input(f"\n{C_BOLD}👉 Action (E/O/C): {C_END}").strip().lower()
        
        if mode_choice == 'c' or not mode_choice:
            return
        elif mode_choice == 'e':
            is_edit_mode = True

    t_name = get_input_with_default(f"{C_YELLOW}🏷️  Enter Tunnel Name{C_END}", existing['name'] if is_edit_mode else "Hybrid_6to4_GRE6").replace(" ", "_")
    local_v4 = get_input_with_default(f"{C_YELLOW}🔹 1. Local Linux Public IPv4{C_END}", existing['local'] if is_edit_mode else "")
    remote_v4 = get_input_with_default(f"{C_YELLOW}🔹 2. Remote MikroTik Public IPv4{C_END}", existing['remote'] if is_edit_mode else "")
    tunnel_cidr = get_input_with_default(f"{C_YELLOW}🔹 3. Tunnel Internal IPv4 (e.g., 10.20.20.1/30){C_END}", existing['tunnel_cidr'] if is_edit_mode else "")
    
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
    print("─"*60)
    
    if input(f"{C_BOLD}🤔 Apply this Hybrid Tunnel configuration? (y/n): {C_END}").strip().lower() == 'y':
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
        with open(YAML_6TO4_PATH, "w", encoding="utf-8") as f: f.write(yaml_content)
        
        print(f"\n{C_YELLOW}⏳ Applying Hybrid Netplan Architecture...{C_END}")
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            time.sleep(1)
            subprocess.run(["ip", "link", "set", "dev", "ip6to4", "up"])
            force_up_interface("gre6-to-mikro", remote_tunnel_ip)
            print(f"\n{C_GREEN}{C_BOLD}✅ Hybrid Tunnel '{t_name}' applied and synced successfully!{C_END}")
        else: print(f"\n{C_RED}❌ Error! Netplan Apply Failed.{C_END}")
    input(f"\nPress Enter to return to main menu...")

def status_and_diagnostic_hub():
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}🔍  MIKRONETPLUS - INTERFACE STATUS & DIAGNOSTIC HUB{C_END}")
    print("═"*75)
    
    active_tunnels = {}
    index = 1
    
    meta_reg = parse_yaml_fields(YAML_REGULAR_PATH) if os.path.exists(YAML_REGULAR_PATH) else None
    print(f"{C_BOLD}[Method 1] Regular IPv4 GRE:{C_END}")
    if meta_reg:
        if_check = subprocess.run(["ip", "link", "show", "gre-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP (Running){C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN{C_END}"
        print(f"  [{index}] Interface: {C_CYAN}gre-to-mikro{C_END} | Name: {C_BOLD}{meta_reg['name']}{C_END} | IP: {meta_reg['tunnel_cidr']} | Status: {status}")
        active_tunnels[str(index)] = {"name": meta_reg['name'], "ip": meta_reg['tunnel_cidr'], "type": "Regular"}
        index += 1
    else:
        print(f"  ❌ {C_RED}Not Configured{C_END}")
        
    print("-" * 75)
    
    meta_6to4 = parse_yaml_fields(YAML_6TO4_PATH) if os.path.exists(YAML_6TO4_PATH) else None
    print(f"{C_BOLD}[Method 2] Hybrid 6to4 > GRE6:{C_END}")
    if meta_6to4:
        if_check = subprocess.run(["ip", "link", "show", "gre6-to-mikro"], capture_output=True, text=True)
        status = f"{C_GREEN}UP (Running){C_END}" if ("UP" in if_check.stdout or "UNKNOWN" in if_check.stdout) else f"{C_YELLOW}DOWN{C_END}"
        print(f"  [{index}] Interface: {C_CYAN}gre6-to-mikro{C_END} | Name: {C_BOLD}{meta_6to4['name']}{C_END} | IP: {meta_6to4['tunnel_cidr']} | Status: {status}")
        active_tunnels[str(index)] = {"name": meta_6to4['name'], "ip": meta_6to4['tunnel_cidr'], "type": "Hybrid"}
        index += 1
    else:
        print(f"  ❌ {C_RED}Not Configured{C_END}")
        
    print("═"*75)
    
    print(f"{C_BOLD}[Keepalive Daemon Status]:{C_END}")
    is_running = os.system(f"pgrep -f {KEEPALIVE_SCRIPT_PATH} > /dev/null 2>&1") == 0
    if is_running:
        print(f"  🟢 Keepalive Service: {C_GREEN}ACTIVE (Pinging every 20s in background){C_END}")
    else:
        print(f"  🔴 Keepalive Service: {C_RED}INACTIVE{C_END}")
    print("═"*75)

    print(f"  {C_GREEN}[1-2]{C_END} Select Tunnel number to Ping diagnostics")
    print(f"  {C_RED}[K]{C_END}   Stop Background Keepalive Service")
    print(f"  {C_YELLOW}[Enter]{C_END} Return to Main Menu")
    print("-" * 75)
    
    ping_choice = input(f"{C_BOLD}👉 Choice: {C_END}").strip()
    
    if ping_choice.lower() == 'k':
        stop_background_keepalive()
        print(f"\n{C_RED}🛑 Keepalive daemon stopped successfully!{C_END}")
        time.sleep(1.5)
        return
        
    if ping_choice in active_tunnels:
        selected = active_tunnels[ping_choice]
        try:
            parts = selected['ip'].split('/')[0].split('.')
            last_octet = int(parts[3])
            remote_ip = f"{parts[0]}.{parts[1]}.{parts[2]}.{last_octet + 1 if last_octet % 2 != 0 else last_octet - 1}"
        except:
            remote_ip = selected['ip'].split('/')[0]
            
        print(f"\n🚀 Launching live diagnostics for [{C_BOLD}{selected['name']}{C_END}]...")
        target_ip = input(f"{C_YELLOW}🎯 Target Remote Tunnel IP [Default auto-detect: {remote_ip}]: {C_END}").strip()
        if not target_ip: target_ip = remote_ip
            
        print(f"\n⏳ Sending 4 live packets to {target_ip}...\n")
        subprocess.run(["ping", "-c", "4", target_ip])
        input(f"\nPress Enter to return to main menu...")

# Trigger Animated Intro
play_animated_intro()

# Main CLI Loop
while True:
    clear_screen()
    show_big_banner()
    
    print(f"{C_BOLD}📱 SELECT TUNNEL METHOD:{C_END}")
    print(f"  {C_GREEN}[1]{C_END} 🛠️  Create / Edit Regular IPv4 GRE Tunnel")
    print(f"  {C_GREEN}[2]{C_END} ⚡  Create / Edit Hybrid 6to4 > GRE6 Tunnel (Best Performance)")
    print(f"  {C_GREEN}[3]{C_END} 🔍  Check Status & Live Diagnostics (Ping Hub)")
    print(f"  {C_RED}[4]{C_END} ❌  Exit Hub")
    print(f"{C_CYAN}" + "─"*72 + f"{C_END}")
    
    choice = input(f"{C_BOLD}👉 Select an option (1-4): {C_END}").strip()
    
    if choice == '1': manage_regular_gre()
    elif choice == '2': manage_6to4_gre6()
    elif choice == '3': status_and_diagnostic_hub()
    elif choice == '4':
        clear_screen()
        print(f"\n{C_GREEN}{C_BOLD}👋 Thank you for using MikroNetPlus CLI Manager!{C_END}")
        print(f"{C_CYAN}📺 Don't forget to subscribe to Mikronet_plus on YouTube.{C_END}\n")
        break
