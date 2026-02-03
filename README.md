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

### 2. Install the python virtual environment
```bash
# Create the virtual environment
python3 -m venv env

# Switch to virtual environment
source env/bin/activate
```

### 3. Install python dependencies
```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 4. Run the program
```bash
# Run python script
python3 run.py
```

### After running
If you want to disconnect from the python virtual environment and return to your regular terminal do the following:
```bash
# Disconect from the python virtual environment
deactivate
```