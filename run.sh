#!/bin/bash
# Update system and install requirements
sudo apt update -y && sudo apt install -y python3 wget

# Download the ultimate multi-tunnel script
sudo wget -O /usr/local/bin/app_cli.py https://raw.githubusercontent.com/Mikronet-plus/netplan-gre-tunnel-wizard/main/app_cli.py
sudo chmod +x /usr/local/bin/app_cli.py

# Ensure permanent alias exists
if ! grep -q "alias mikronet=" ~/.bashrc; then
    echo "alias mikronet='sudo python3 /usr/local/bin/app_cli.py'" >> ~/.bashrc
    echo "alias mikronet='sudo python3 /usr/local/bin/app_cli.py'" >> /root/.bashrc
fi

export PATH=$PATH:/usr/local/bin
alias mikronet='sudo python3 /usr/local/bin/app_cli.py'
sudo python3 /usr/local/bin/app_cli.py
