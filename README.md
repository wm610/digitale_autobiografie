# digitale_autobiografie

### create virtual environment
python3 -m venv erzaehlomat
python3 -m venv --system-site-packages erzaehlomat
source ./erzaehlomat/bin/activate

### installation on Linux
maybe not needed: sudo apt-get install python3-rpi.gpiovi
curl -fsSL https://ollama.com/install.sh | sh
pip install -r requirements.txt --timeout=120

### start the programm
sudo python3 script/controller.py

### UI
change wayland to X11 inside the Raspberry Pi Software Configuration Tool
execute: sudo raspi-config -> Advanced Options -> switch from Wayland to X11