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

### 2. Install python dependencies
```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt

# TROUBLESHOOTING
# If pip is not installed do the following and try the above again
sudo apt update && sudo apt install pip
```

### 3. Run the program
```bash
# Run python script
python3 run.py
```