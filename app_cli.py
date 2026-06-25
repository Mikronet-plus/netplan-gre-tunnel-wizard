#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =================================================================
# 🚀 MIKRONETPLUS - SMART GRE TUNNEL CLI MANAGER
# 📺 YouTube Channel: Mikronet_plus
# =================================================================

import os
import subprocess
import sys

YAML_PATH = "/etc/netplan/60-mikronet-tunnel.yaml"

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

while True:
    clear_screen()
    print(f"{C_CYAN}{C_BOLD}╔" + "═"*58 + "╗")
    print("║ 🚀  MIKRONETPLUS - SMART GRE TUNNEL CLI MANAGER          ║")
    print("║ 📺  Presented by: Mikronet_plus YouTube Channel         ║")
    print("╚" + "═"*58 + "╝" + f"{C_END}")
    
    print(f"{C_BOLD}📱 MAIN MENU:{C_END}")
    print(f"  {C_GREEN}[1]{C_END} 🛠️  Build / Modify GRE Tunnel")
    print(f"  {C_GREEN}[2]{C_END} 🔍  Check Tunnel Status & Live Ping")
    print(f"  {C_RED}[3]{C_END} ❌  Exit Manager")
    print(f"{C_CYAN}" + "─"*60 + f"{C_END}")
    
    choice = input(f"{C_BOLD}👉 Select an option (1-3): {C_END}").strip()
    
    if choice == '1':
        clear_screen()
        print(f"{C_CYAN}{C_BOLD}🛠️  TUNNEL WIZARD (CREATE / MODIFY){C_END}")
        print("─"*40)
        
        local = input(f"{C_YELLOW}🔹 1. Local Linux Public IP: {C_END}").strip()
        remote = input(f"{C_YELLOW}🔹 2. Remote MikroTik Public IP: {C_END}").strip()
        tunnel_with_cidr = input(f"{C_YELLOW}🔹 3. Tunnel Internal IP (e.g., 10.10.10.1/30): {C_END}").strip()
        
        print(f"\n{C_BOLD}📊 Preview Configuration:{C_END}")
        print(f"  ▫️ Local IP  : {C_GREEN}{local}{C_END}")
        print(f"  ▫️ Remote IP : {C_GREEN}{remote}{C_END}")
        print(f"  ▫️ Tunnel IP : {C_GREEN}{tunnel_with_cidr}{C_END}")
        print("─"*40)
        
        confirm = input(f"{C_BOLD}🤔 Apply these changes? (y/n): {C_END}").strip().lower()
        if confirm == 'y':
            yaml_content = f"network:\n  version: 2\n  tunnels:\n    gre-to-mikro:\n      mode: gre\n      local: {local}\n      remote: {remote}\n      addresses:\n        - {tunnel_with_cidr}\n"
            with open(YAML_PATH, "w") as f: 
                f.write(yaml_content)
            
            print(f"\n{C_YELLOW}⏳ Applying Netplan configuration...{C_END}")
            if subprocess.run(["netplan", "apply"]).returncode == 0:
                print(f"\n{C_GREEN}{C_BOLD}✅ Netplan applied successfully!{C_END}")
                
                # 🔥 ترفند طلایی جدید: حدس زدن آی‌پي سمت میکروتیک برای شلیک پینگ بیدارکننده
                # اگر کاربر وارد کرده ۱۰.۱۰.۱۰.۱، اسکریپت به ۱۰.۱۰.۱۰.۲ پینگ می‌زند تا مسیر فعال شود
                try:
                    base_ip = tunnel_with_cidr.split('/')[0]
                    ip_parts = base_ip.split('.')
                    last_octet = int(ip_parts[3])
                    # اگر آی‌پی سرور فرد بود (مثل .۱) به زوج (.۲) پینگ می‌زند و برعکس
                    remote_tunnel_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{last_octet + 1 if last_octet % 2 != 0 else last_octet - 1}"
                    
                    print(f"{C_YELLOW}⏳ Pinging remote peer ({remote_tunnel_ip}) to force wake GRE interface...{C_END}")
                    subprocess.run(["ping", "-c", "1", "-W", "1", remote_tunnel_ip], capture_output=True)
                except:
                    pass # اگر فرمت آی‌پی عجیب بود خطا ندهد
                
                print(f"{C_GREEN}{C_BOLD}🚀 Success! Tunnel configuration completed.{C_END}")
            else: 
                print(f"\n{C_RED}❌ Error! Failed to apply Netplan configuration.{C_END}")
        else:
            print(f"\n{C_YELLOW}⚠️ Operation cancelled by user.{C_END}")
        
        input(f"\n{C_BOLD}Press Enter to return to menu...{C_END}")
        
    elif choice == '2':
        clear_screen()
        print(f"{C_CYAN}{C_BOLD}🔍  MIKRONETPLUS LIVE STATUS REPORT{C_END}")
        print("═"*50)
        
        if not os.path.exists(YAML_PATH):
            print(f"{C_RED}❌ Configuration file not found. No tunnel built yet!{C_END}")
            print("═"*50)
            input(f"\n{C_BOLD}Press Enter to return to menu...{C_END}")
            continue
            
        print(f"{C_GREEN}✅ Netplan Config File: EXISTS & ACTIVE{C_END}")
        print(f"\n{C_BOLD}⚙️ Linux Interface Status:{C_END}")
        print("-" * 35)
        
        if_check = subprocess.run(["ip", "link", "show", "gre-to-mikro"], capture_output=True, text=True)
        if if_check.returncode == 0:
            # در لینوکس وضعیت لایه ۳ تونل معمولا UNKNOWN (یعنی آماده تبادل دیتای بدون استیت) یا UP است
            if "UP" in if_check.stdout or "UNKNOWN" in if_check.stdout: 
                print(f"  🟢 Interface [gre-to-mikro]: {C_GREEN}{C_BOLD}UP & READY{C_END}")
            else:
                print(f"  🟡 Interface [gre-to-mikro]: {C_YELLOW}DOWN / IDLE (Needs Traffic){C_END}")
        else:
            print(f"  🔴 Interface [gre-to-mikro]: {C_RED}NOT FOUND (Apply Failed){C_END}")
            
        print("-" * 35)
        
        ping_opt = input(f"\n{C_BOLD}⚡ Do you want to test ping? (y/n): {C_END}").strip().lower()
        if ping_opt == 'y':
            target = input(f"{C_YELLOW}🎯 Enter Target Tunnel IP (MikroTik side): {C_END}").strip()
            print(f"\n⏳ Sending 4 packets to {target}...\n")
            subprocess.run(["ping", "-c", "4", target])
            
        print("═"*50)
        input(f"\n{C_BOLD}Press Enter to return to menu...{C_END}")
            
    elif choice == '3':
        clear_screen()
        print(f"\n{C_GREEN}{C_BOLD}👋 Thank you for using MikroNetPlus CLI Manager!{C_END}")
        print(f"{C_CYAN}📺 Don't forget to subscribe to Mikronet_plus on YouTube.{C_END}\n")
        break
