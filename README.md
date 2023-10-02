# RoboMFG_Dynamixel_Integration
Klipper integration of Robotis Dynamixel servos 

# Install Dynamixel Integration

-update klipper
-clone the Dynamixel repo
```
cd ~/
git clone https://github.com/Advanced-Manufacturing-at-UoL/RoboMFG_Dynamixel_Integration.git
bash ~/RoboMFG_Dynamixel_Integration/install.sh
```
-add the update manager entry to the moonraker.conf file in your config folder
```
[update_manager IDEX]
type: git_repo
primary_branch: main
path: ~/vcore-idex
origin: https://github.com/HelgeKeck/vcore-idex.git
managed_services:
	klipper
```
-reboot the host controller (typically a Raspberry Pi)
