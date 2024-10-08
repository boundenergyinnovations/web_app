#!/bin/bash
set -e

# Update the package list
sudo apt update

# Install Nginx
sudo apt install -y nginx

# Allow Nginx HTTP through the firewall
sudo ufw allow 'Nginx HTTP'

# Check the firewall status
sudo ufw status

# Check the status of Nginx service
sudo systemctl status nginx

# Create the Nginx configuration file for gradio
sudo bash -c 'cat > /etc/nginx/sites-available/gradio <<EOF
server {
    listen 80;
    server_name your_domain.com; # Replace with your domain or IP address

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF'

# Enable the new site by creating a symbolic link
sudo ln -s /etc/nginx/sites-available/gradio /etc/nginx/sites-enabled/

# Test Nginx configuration for syntax errors
sudo nginx -t

# Reload Nginx to apply changes
sudo systemctl reload nginx

# Install Python 3 pip and venv
sudo apt install -y python3-pip
sudo apt install -y python3.10-venv

# Create a Python virtual environment
python3 -m venv venv

wget -O web_app_no_sheet.py https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/web_app_no_sheet.py
wget -O web_app_gsheet.py https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/web_app_gsheet.py
wget -O web_app_localmsg.py https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/web_app_localmsg.py
wget -O beartheme.json https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/beartheme.json
wget -O requirements.txt https://raw.githubusercontent.com/boundenergyinnovations/web_app/main/requirements.txt
