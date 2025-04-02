# digitale_autobiografie

### create virtual environment on Raspberry Pi OS
python3 -m venv --system-site-packages erzaehlomat
source ./erzaehlomat/bin/activate

### installation on Linux
pip install -r requirements.txt --timeout=120
curl -fsSL https://ollama.com/install.sh | sh
maybe not needed: sudo apt-get install python3-rpi.gpiovi

### start the programm
sudo python3 script/controller.py

### UI
change wayland to X11 inside the Raspberry Pi Software Configuration Tool
execute: sudo raspi-config -> Advanced Options -> switch from Wayland to X11