# RoboMFG_Dynamixel_Integration
Klipper integration of Robotis Dynamixel servos 

# Install Dynamixel Integration

- update klipper
- clone the Dynamixel repo
```
cd ~/
git clone https://github.com/Advanced-Manufacturing-at-UoL/RoboMFG_Dynamixel.git
bash ~/RoboMFG_Dynamixel/install.sh
```
- add the update manager entry to the moonraker.conf file in your config folder
```
[update_manager DYNAMIXEL]
type: git_repo
primary_branch: main
path: ~/RoboMFG_Dynamixel_Integration
origin: https://github.com/Advanced-Manufacturing-at-UoL/RoboMFG_Dynamixel.git
managed_services: klipper
```
- reboot the host controller (typically a Raspberry Pi)
