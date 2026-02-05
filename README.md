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

### 2. Install Dependencies
```bash
# Install the required dependencies
sudo ./install.sh
# This script will launch the Photon Laser Tag program after installing
```

### 3. Running the Program
```bash
# After installing the first time, you can run the program regularly with:
python3 run.py
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