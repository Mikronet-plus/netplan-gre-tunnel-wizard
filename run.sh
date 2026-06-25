#!/bin/bash

# 1. Update system and install requirements
sudo apt update -y && sudo apt install -y python3 wget

# 2. Download the core script to a safe system binary path
sudo wget -O /usr/local/bin/app_cli.py https://raw.githubusercontent.com/Mikronet-plus/netplan-gre-tunnel-wizard/main/app_cli.py
sudo chmod +x /usr/local/bin/app_cli.py

# 3. Create a permanent system shortcut (Alias) for 'mikronet' command
if ! grep -q "alias mikronet=" ~/.bashrc; then
    echo "alias mikronet='sudo python3 /usr/local/bin/app_cli.py'" >> ~/.bashrc
    echo "alias mikronet='sudo python3 /usr/local/bin/app_cli.py'" >> /root/.bashrc
fi

# 4. Refresh current environment path
export PATH=$PATH:/usr/local/bin
alias mikronet='sudo python3 /usr/local/bin/app_cli.py'

# 5. Run it instantly for the first time
sudo python3 /usr/local/bin/app_cli.py
