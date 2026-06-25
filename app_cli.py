#!/usr/bin/env python3
import os, subprocess, sys

YAML_PATH = "/etc/netplan/60-mikronet-tunnel.yaml"

if os.getuid() != 0:
    print("\n❌ دسترسی sudo نیاز است!"); sys.exit(1)

while True:
    print("\n" + "="*50 + "\n🚀 MikroNetPlus Menu:\n1) Build/Modify Tunnel\n2) Check Status\n3) Exit\n" + "="*50)
    choice = input("👉 Option (1-3): ").strip()
    
    if choice == '1':
        local = input("1. Local Public IP: ").strip()
        remote = input("2. Remote Public IP: ").strip()
        tunnel = input("3. Tunnel Internal IP (e.g. 10.10.10.1/30): ").strip()
        
        yaml_content = f"network:\n  version: 2\n  tunnels:\n    gre-to-mikro:\n      mode: gre\n      local: {local}\n      remote: {remote}\n      addresses:\n        - {tunnel}\n"
        with open(YAML_PATH, "w") as f: f.write(yaml_content)
        
        if subprocess.run(["netplan", "apply"]).returncode == 0:
            print("\n✅ تونل با موفقیت اعمال/اصلاح شد!")
        else: print("\n❌ خطای نت‌پلان!")
        
    elif choice == '2':
        if not os.path.exists(YAML_PATH):
            print("\n❌ هیچ تونلی ساخته نشده است."); continue
        print("\n⚙️ Interface Status:")
        subprocess.run(["ip", "link", "show", "gre-to-mikro"])
        if input("\n🤔 Test Ping? (y/n): ").strip().lower() == 'y':
            target = input("🎯 Target Tunnel IP: ").strip()
            subprocess.run(["ping", "-c", "4", target])
            
    elif choice == '3':
        print("\n👋 Bye!"); break
