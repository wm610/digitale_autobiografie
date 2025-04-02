# digitale_autobiografie

### create virtual environment
python3 -m venv erzaehlomat
source ./erzaehlomat/bin/activate

### installation on Linux
sudo apt-get install python3-rpi.gpiovi
pip install -r requirements.txt --timeout=120

### start the programm
python3 script/controller.py