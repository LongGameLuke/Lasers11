# Team 11 - Photon Laser Tag
![Photon Logo](/assets/images/logo_small.png)

This is a project for the University of Arkansas to recreate the original commercial version of laser tag's ([Photon: The Ultimate Game on Planet Earth](https://en.wikipedia.org/wiki/Photon:_The_Ultimate_Game_on_Planet_Earth)) game control server.

**NOTE**: This program cannot be used directly with the original Photon hardware. Modified hardware that can communicate over UDP is required.

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
./install.sh
# This script will launch the Photon Laser Tag program after installing
```

### 3. Running the Program
```bash
# After installing the first time, you can run the program regularly with:
python3 run.py
```

### Troubleshooting
In the event the auto install and run script doesn't work, you can perform the steps below manually.
```bash
# Make sure pip is installed
sudo apt update && sudo apt install pip -y

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run program
python3 run.py
```

## Game Events & Codes
The game server will broadcast and receive several codes that can be used to communicate with the player clients. These signals are communicated by UDP on the ports and host specified in ```config.yml```.

### Game Start/Stop
After a countdown of a specified length in ```config.yml```, the game server will send the start code to the player clients. When the full game time has elapsed or the game is stopped manually, the game server will send the end code.
```
202 = Start game
221 = End game
```

### Tag Event
Tag events are sent from clients to the game server and follow the following format:
```
<tagger hardware id>:<tagged hardware id>
```
After the game server registers the tag event, the tagged player's hardware id will be broadcast back. This is used by the player client to know their unit should become shortly disabled.

### Base Tag Event
When a team's base is tagged, the player client will send the base tag code to the game server in the same format as a regular tag event. The game server will send back the id of the base that was tagged. The player client will remember this event and can only occur once per player per game.
```
43 = Green base tagged by red player
53 = Red base tagged by green player
```