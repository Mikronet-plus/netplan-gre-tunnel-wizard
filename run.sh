#!/bin/bash
sudo apt update -y && sudo apt install -y python3 wget
wget -O app_cli.py https://raw.githubusercontent.com/Mikronet-plus/netplan-gre-tunnel-wizard/main/app_cli.py
sudo python3 app_cli.py
