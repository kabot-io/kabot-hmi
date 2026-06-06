# Protocol Reference

## Source of truth

- `backend/state_control_msg.proto`

## Control message used by this HMI

Message: `Control`

Fields currently sent:

- `effort.state.x`
- `effort.state.y`

Transport:

- UDP destination port: `30010`
- UDP destination IP: configurable from UI (default `172.20.10.2`)

## State message consumed by this HMI

Message: `State`

Primary groups currently surfaced in UI:

- `distance`
- `effort`
- `linear_acceleration`
- `angular_velocity`
- `magnetic_field`
- `light_left`, `light_right`
- `current_left`, `bus_voltage_left`, `power_left`
- `current_right`, `bus_voltage_right`, `power_right`
- `current_supply`, `bus_voltage_supply`, `power_supply`

Transport:

- UDP bind/listen port: `30011`

## WebSocket messages between UI and backend

From UI to backend:

- `validate` - compile code and return status.
- `run` - set active user code.
- `stop` - clear active user code.
- `control` - send immediate manual effort frame.
- `set_control_target_ip` - update UDP control target IP.

From backend to UI:

- `state` - decoded state payload + stamps.
- `log` - runtime/validation/control status text.
