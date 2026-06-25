from dataclasses import dataclass

@dataclass
class Vector2:
    x: float
    y: float

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Stamps:
    state: float = 0.0
    distance: float = 0.0
    effort: float = 0.0
    accel: float = 0.0
    gyro: float = 0.0
    mag: float = 0.0
    light_left: float = 0.0
    light_right: float = 0.0
    current_left: float = 0.0
    bus_voltage_left: float = 0.0
    power_left: float = 0.0
    current_right: float = 0.0
    bus_voltage_right: float = 0.0
    power_right: float = 0.0
    current_supply: float = 0.0
    bus_voltage_supply: float = 0.0
    power_supply: float = 0.0

@dataclass
class RobotState:
    distance: float
    effort: Vector2
    linear_acceleration: Vector3
    angular_velocity: Vector3
    magnetic_field: Vector3
    light_left: float = 0.0
    light_right: float = 0.0
    current_left: float = 0.0
    bus_voltage_left: float = 0.0
    power_left: float = 0.0
    current_right: float = 0.0
    bus_voltage_right: float = 0.0
    power_right: float = 0.0
    current_supply: float = 0.0
    bus_voltage_supply: float = 0.0
    power_supply: float = 0.0
    stamps: Stamps = None

@dataclass
class RobotControl:
    effort: Vector2
