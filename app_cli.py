#!/bin/bash
# =================================================================
# 🛡️ PROJECT: MikroNetPlus Linux-to-MikroTik GRE Tunnel CLI Manager
# 👤 DEVELOPER: Mikronet_plus Channel (YouTube)
# 📄 LICENSE: GNU GPLv3 (Copyright © 2026)
# 🔗 Description: Auto-install Python & Interactive Netplan Wizard
# =================================================================

# #MikroNetPlus: بخش اول - بررسی هوشمند و نصب خودکار پایتون ۳ توسط لینوکس
if ! command -v python3 &> /dev/null; then
    echo "⚠️ [MikroNetPlus] پایتون ۳ روی سرور شما یافت نشد!"
    echo "⏳ در حال نصب خودکار پایتون و ابزارهای مورد نیاز..."
    sudo apt update -y && sudo apt install -y python3
    if [ $? -ne 0 ]; then
        echo "❌ خطا: نصب پایتون با مشکل مواجه شد. لطفاً مخازن سرور را بررسی کنید."
        exit 1
    fi
    echo "✅ پایتون ۳ با موفقیت نصب شد."
fi

# #MikroNetPlus: بخش دوم - اجرای هسته اصلی مدیریت تونل با پایتون
python3 - << 'EOF'
import os
import subprocess
import sys

YAML_PATH = "/etc/netplan/60-mikronet-tunnel.yaml"

def check_root():
    if os.getuid() != 0:
        print("\n❌ [MikroNetPlus] خطا: این اسکریپت باید با دسترسی sudo اجرا شود!")
        print("💡 دستور اجرا: sudo ./app_manager.sh\n")
        sys.exit(1)

def show_menu():
    print("="*65)
    print(" 🚀 مدیریت هوشمند تونل MikroNetPlus (Linux to MikroTik)")
    print(" 📺 کاری از کانال یوتیوب Mikronet_plus")
    print("="*65)
    print("1) ساخت یا اصلاح (Modify) تونل GRE")
    print("2) بررسی وضعیت (Status) زنده بودن تونل")
    print("3) خروج")
    print("="*65)
    return input("👉 یک گزینه را انتخاب کنید (1-3): ").strip()

def configure_tunnel():
    print("\n[+] لطفا اطلاعات زیر را برای ساخت یا اصلاح تونل وارد کنید:")
    local_ip = input("۱. آی‌پي عمومی همین سرور لینوکس: ").strip()
    remote_ip = input("۲. آی‌پي عمومی سرور مقابل (میکروتیک): ").strip()
    tunnel_ip = input("۳. آی‌پي داخلی تونل برای این سرور (مثلاً 10.10.10.1/30): ").strip()

    print("\n" + "-"*40)
    print(f"📊 اطلاعات جدید:")
    print(f"🔹 آی‌پي این سرور: {local_ip}")
    print(f"🔹 آی‌پي میکروتیک: {remote_ip}")
    print(f"🔹 آی‌پي داخل تونل: {tunnel_ip}")
    print("-"*40)
    
    confirm = input("🤔 آیا از اعمال این تغییرات اطمینان دارید؟ (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ عملیات لغو شد.")
        return

    netplan_yaml = f"""network:
  version: 2
  tunnels:
    gre-to-mikro:
      mode: gre
      local: {local_ip}
      remote: {remote_ip}
      addresses:
        - {tunnel_ip}
"""

    print("\n⏳ در حال بازنویسی نت‌پلان و اعمال تغییرات جدید شبکه...")
    try:
        with open(YAML_PATH, "w") as f:
            f.write(netplan_yaml)
        
        result = subprocess.run(["netplan", "apply"], capture_output=True, text=True, timeout=12)
        
        if result.returncode == 0:
            print("\n✅ [MikroNetPlus] تغییرات با موفقیت اصلاح و روی شبکه اعمال شد!")
        else:
            print(f"\n❌ خطای نت‌پلان:\n{result.stderr}")
    except Exception as e:
        print(f"\n❌ خطای سیستم: {str(e)}")

def check_status():
    print("\n" + "="*50)
    print(" 🔍 گزارش وضعیت تونل MikroNetPlus")
    print("="*50)
    
    if not os.path.exists(YAML_PATH):
        print("❌ وضعیت کانفیگ: هیچ تونلی از قبل ساخته نشده است!")
        print("="*50 + "\n")
        return
    else:
        print("✅ فایل کانفیگ نت‌پلان: موجود و فعال است.")

    print("\n⚙️ وضعیت کارت شبکه مجازی (GRE Interface):")
    if_result = subprocess.run(["ip", "link", "show", "gre-to-mikro"], capture_output=True, text=True)
    if if_result.returncode == 0:
        if "UP" in if_result.stdout:
            print("   🟢 وضعیت اینترفیس: [UP] تونل در سیستم‌عامل روشن است.")
        else:
            print("   🟡 وضعیت اینترفیس: [DOWN] تونل ساخته شده اما خاموش است.")
    else:
        print("   🔴 وضعیت اینترفیس: یافت نشد! (احتمالاً نت‌پلان به درستی اعمال نشده).")

    print("\n⚡ تست ارتباط زنده:")
    check_ping = input("🤔 آیا مایلید پینگ داخل تونل را تست کنید? (y/n): ").strip().lower()
    if check_ping == 'y':
        target_ping = input("🎯 آی‌پي داخل تونلِ سمت میکروتیک را وارد کنید: ").strip()
        print(f"⏳ در حال ارسال ۴ پینگ به {target_ping}...")
        ping_result = subprocess.run(["ping", "-c", "4", target_ping], capture_output=True, text=True)
        if ping_result.returncode == 0:
            print("   ✅ ارتباط برقرار است! پینگ با موفقیت انجام شد.")
            print(ping_result.stdout)
        else:
            print("   ❌ عدم پاسخگویی! تونل متصل است اما سرور مقابل پاسخ نمی‌دهد.")
            
    print("="*50 + "\n")

if __name__ == "__main__":
    check_root()
    while True:
        choice = show_menu()
        if choice == '1':
            configure_tunnel()
        elif choice == '2':
            check_status()
        elif choice == '3':
            print("\n👋 خروج از ابزار MikroNetPlus. موفق باشید!\n")
            break
        else:
            print("\n❌ گزینه نامعتبر! لطفاً عددی بین 1 تا 3 وارد کنید.\n")
EOF
