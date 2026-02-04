# Team 11 - Photon Laser Tag

## How to run
Running this program requires the pre-configured Virtual Box VM located [here](http://turing.csce.uark.edu/~jps011). All following steps should be performed within the running virtual machine.

### 1. Download Repo
```bash
# Clone the repo
git clone https://github.com/LongGameLuke/Lasers11.git

# Enter repo directory
cd Lasers11/
```

### 2. Run the program
```bash
# Run script with sudo.
# Sudo is required for the event where pip needs to be installed
sudo ./run.sh
```

## Troubleshooting
In the event the auto install and run script doesn't work, you can perform the steps below manually.
```bash
# Make sure pip is installed
sudo apt update && sudo apt install pip

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run program
python3 run.py
```