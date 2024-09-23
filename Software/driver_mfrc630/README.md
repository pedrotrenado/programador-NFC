# TycheTools MFRC630 controller in Python

//TODO

## Setup

- Install Raspberry OS Lite (recommended) using Raspbian in a SD
- Enable SSH
- Enable SPI with ```sudo raspi-config```
- Upload bitbuket keys (in heimdall repo) to ```~/.ssh/```, change permisions ```chmod 600 ~/.ssh/bitbucket*``` and create ```~/ssh/config```
- Install Pip, Vim, Tmux and Git ```sudo apt install git vim tmux python3-pip``` and reboot ```sudo reboot```
- Clone this repository ```git clone git@bitbucket.org:tychermo/mfrc522_python.git```
- Install requirements ```pip3 install -r requirements.txt```
- Run example ```python3 ttne-example.py```

## Wiring diagram

## Pin assignment

![](./resources/wiring.png)
