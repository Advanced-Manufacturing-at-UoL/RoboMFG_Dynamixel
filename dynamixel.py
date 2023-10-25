# Support for Dynamixel MX-28 servos #

from time import sleep
import dynio

class Dynamixel:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.port = config.get('port')
        self.dmx_id = config.getint('dynamixel_id')
        self.velocity = config.getint('velocity',50)
        self.direction = config.getint('direction',1)
        self.accel = config.getint('acceleration',0)
        self.offset = config.getfloat('offset',0)
        self.name = config.get_name().split(' ')[-1]
        config_gear_ratio = config.getlists('gear_ratio', (), seps=(':', ','), count=2, parser=float)
        self.moving = False

        self.gear_ratio = self.parse_gear_ratio(config_gear_ratio)

        dxl_io = dynio.dxl.DynamixelIO(self.port, 1000000) # your port for U2D2 or other serial device

        self.dxl = dxl_io.new_mx28(self.dmx_id,2)  # MX-28 protocol 2 with ID x)
        self.dxl.torque_disable()
        self.dxl.set_extended_position_mode()
        self.dxl.set_velocity(int(self.velocity))
        self.dxl.set_acceleration(int(self.accel))
        self.dxl.write_control_table("Homing_Offset", int(self.offset/0.087891))
        self.dxl.write_control_table("LED", 1)
        sleep(0.2)
        self.dxl.write_control_table("LED", 0)

        gcode = self.printer.lookup_object('gcode')
        gcode.register_mux_command('DYNAMIXEL', 'DXL', self.name,
                                   self.cmd_DYNAMIXEL,
                                   desc=self.cmd_DYNAMIXEL_help)


    cmd_DYNAMIXEL_help = "Command a Dynamixel servo"
    def cmd_DYNAMIXEL(self, gcmd):
        while self.check_movement is True:
            pass

        enable = gcmd.get_int('ENABLE', None)
        if enable is not None:
            self.do_enable(enable)

        if gcmd.get_float('VELOCITY', None) is not None:
            velocity = gcmd.get_float('VELOCITY')
            if self.check_velocity(velocity) is False:
                self.set_velocity(velocity)
            else:
                raise gcmd.error(self.name + "Velocity is greater than its limit")
            
        if gcmd.get_float('ACCEL', None) is not None:
            acceleration = gcmd.get_float('ACCEL')
            self.set_accel(acceleration)

        if gcmd.get_float('MOVE', None) is not None:
            enabled = self.dxl.read_control_table("Torque_Enable")
            if int(enabled) == 1:
                movepos = gcmd.get_float('MOVE')
                self.do_move(movepos,gcmd)
            else:
                raise gcmd.error('Dynamixel ' + str(self.name) + ' torque is not enabled')


    def do_enable(self, enable):
        if enable:
            self.dxl.torque_enable()
            self.dxl.write_control_table("LED", 1)
        else:
            self.dxl.torque_disable()
            self.dxl.write_control_table("LED", 0)

    def check_movement(self):
        if self.dxl.read_control_table("Moving") == 1:
            self.moving = True
        else:
            self.moving = False

    def do_move(self, movepos, gcmd):
        movepos = movepos * self.gear_ratio * self.direction
        self.dxl.set_angle(movepos)
        sleep(0.2)
        self.check_movement()
        # moving = int(self.dxl.read_control_table("Moving")) == 1
        gcmd.respond_info("Moving ...")
        gcmd.respond_info(str(self.moving))
        while self.moving is True:
        # while moving == 1:
            gcmd.respond_info("Checking Movement ...")
            self.check_movement()
            # moving = int(self.dxl.read_control_table("Moving")) == 1
            # pass
        gcmd.respond_info("Done")

    def check_velocity(self, velocity):
        velocity_limit = self.dxl.read_control_table("Velocity_Limit")
        if velocity > velocity_limit:
            V_lim_exceed = True
        else:
            V_lim_exceed = False
        return V_lim_exceed

    def set_velocity(self, velocity):
        self.dxl.set_velocity(int(velocity))
        self.velocity = velocity

    def set_accel(self, accel):
        self.dxl.set_acceleration(int(accel))
        self.accel = accel

    def parse_gear_ratio(self, gear_ratio):
        
        result = 1.
        for g1, g2 in gear_ratio:
            result *= g1 / g2
        return float(result)

def load_config_prefix(config):
    return Dynamixel(config)
