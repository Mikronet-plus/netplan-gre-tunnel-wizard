# =================================================================
# 🛡️ PROJECT: MikroNetPlus Linux-to-MikroTik GRE Tunnel CLI Wizard
# 👤 DEVELOPER: Mikronet_plus Channel (YouTube)
# 📄 LICENSE: GNU GPLv3 (Copyright © 2026)
# 🔗 Description: Interactive CLI tool for Netplan GRE Tunnels
# =================================================================
# #MikroNetPlus: این اسکریپت تعاملی خط فرمان، تونل GRE را روی اوبونتو پیکربندی می‌کند.

import os
import subprocess
import sys

def run_wizard():
    # بررسی دسترسی روت (Root) برای ویرایش فایل‌های سیستم
    if os.getuid() != 0:
        print("\n❌ [MikroNetPlus] خطا: این اسکریپت برای تغییرات شبکه باید با دسترسی sudo اجرا شود!")
        print("💡 دستور اجرا: sudo python3 app_cli.py\n")
        sys.exit(1)

    print("="*65)
    print(" 🚀 به اسکریپت تعاملی MikroNetPlus خوش آمدید (Linux to MikroTik)")
    print(" 📺 کاری از کانال یوتیوب Mikronet_plus")
    print("="*65)
    print("لطفاً اطلاعات زیر را برای پیکربندی تونل GRE وارد کنید:\n")

    # دریافت اطلاعات از کاربر
    local_ip = input("۱. آی‌پي عمومی همین سرور لینوکس (مثلاً ایران): ").strip()
    remote_ip = input("۲. آی‌پي عمومی سرور مقابل (میکروتیک خارج): ").strip()
    tunnel_ip = input("۳. آی‌پي داخلی تونل برای این سرور همراه با ساب‌نت (مثلاً 10.10.10.1/30): ").strip()

    # تایید نهایی از کاربر
    print("\n" + "-"*40)
    print(f"📊 اطلاعات وارد شده:")
    print(f"🔹 آی‌پي این سرور: {local_ip}")
    print(f"🔹 آی‌پي میکروتیک: {remote_ip}")
    print(f"🔹 آی‌پي داخل تونل: {tunnel_ip}")
    print("-"*40)
    
    confirm = input("🤔 آیا از صحت اطلاعات اطمینان دارید؟ (y/n): ").strip().lower()
    if confirm != 'y':
        print("\n❌ عملیات توسط کاربر لغو شد.")
        sys.exit(0)

    # #MikroNetPlus Core Engine: ساخت ساختار YAML نت‌پلان
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

    print("\n⏳ در حال نوشتن فایل نت‌پلان و اعمال تغییرات شبکه...")

    try:
        # #MikroNetPlus File Manager: ذخیره در فایل اختصاصی برای امنیت شبکه اصلی
        yaml_path = "/etc/netplan/60-mikronet-tunnel.yaml"
        with open(yaml_path, "w") as f:
            f.write(netplan_yaml)
        
        # #MikroNetPlus Network Executor: اجرای دستور نت‌پلان در لینوکس
        result = subprocess.run(["netplan", "apply"], capture_output=True, text=True, timeout=12)
        
        if result.returncode == 0:
            print("\n" + "="*65)
            print(" ✅ [MikroNetPlus] تونل GRE با موفقیت ساخته و در اوبونتو اعمال شد!")
            print(" 🌐 شبکه شما بدون قطعی اینترنت اصلی به‌روزرسانی شد.")
            print(" 📢 برای آموزش‌های بیشتر کانال Mikronet_plus را در یوتیوب دنبال کنید.")
            print("="*65 + "\n")
        else:
            print(f"\n❌ خطایی در حین اعمال نت‌پلان رخ داد:\n{result.stderr}")
            
    except Exception as e:
        print(f"\n❌ خطای سیستم پایتون: {str(e)}")

if __name__ == "__main__":
    run_wizard()
