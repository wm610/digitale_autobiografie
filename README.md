# digitale_autobiografie

### create virtual environment on Raspberry Pi OS
```bash
python3 -m venv --system-site-packages erzaehlomat
source ./erzaehlomat/bin/activate
```

### installation on Linux
```bash
sudo apt-get install portaudio19-dev
pip install -r requirements.txt --timeout=120
curl -fsSL https://ollama.com/install.sh | sh
sudo apt-get install python3-rpi.gpiovi # maybe not needed
```

### start the programm
```bash
sudo python3 script/controller.py
```

### UI
if the UI is not working: change wayland to X11 inside the Raspberry Pi Software Configuration Tool
```bash
sudo raspi-config -> Advanced Options -> switch from Wayland to X11
```

### AI
create ollama Models with
```bash
ollama create generate_question -f ./ollama/generate_question/models/Modelfile
ollama create profile -f ./ollama/profile/models/Modelfile
```