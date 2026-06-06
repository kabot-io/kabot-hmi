import asyncio
import socket
import traceback
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import state_control_msg_pb2 as pb2
from models import RobotState, RobotControl, Vector2, Vector3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

UDP_STATE_PORT = 30011
UDP_CONTROL_PORT = 30010
UDP_TARGET_IP = '172.20.10.2'
udp_target_ip = UDP_TARGET_IP

current_user_code = None
active_connections = []

def decode_state(data: bytes) -> RobotState:
    msg = pb2.State()
    msg.ParseFromString(data)
    
    stamps = {
        'state': msg.header.stamp,
        'distance': msg.distance.header.stamp,
        'effort': msg.effort.header.stamp,
        'accel': msg.linear_acceleration.header.stamp,
        'gyro': msg.angular_velocity.header.stamp,
        'mag': msg.magnetic_field.header.stamp,
        'light_left': msg.light_left.header.stamp,
        'light_right': msg.light_right.header.stamp,
        'current_left': msg.current_left.header.stamp,
        'bus_voltage_left': msg.bus_voltage_left.header.stamp,
        'power_left': msg.power_left.header.stamp,
        'current_right': msg.current_right.header.stamp,
        'bus_voltage_right': msg.bus_voltage_right.header.stamp,
        'power_right': msg.power_right.header.stamp,
        'current_supply': msg.current_supply.header.stamp,
        'bus_voltage_supply': msg.bus_voltage_supply.header.stamp,
        'power_supply': msg.power_supply.header.stamp,
    }
    
    return RobotState(
        distance=msg.distance.state,
        effort=Vector2(x=msg.effort.state.x, y=msg.effort.state.y),
        linear_acceleration=Vector3(x=msg.linear_acceleration.state.x, y=msg.linear_acceleration.state.y, z=msg.linear_acceleration.state.z),
        angular_velocity=Vector3(x=msg.angular_velocity.state.x, y=msg.angular_velocity.state.y, z=msg.angular_velocity.state.z),
        magnetic_field=Vector3(x=msg.magnetic_field.state.x, y=msg.magnetic_field.state.y, z=msg.magnetic_field.state.z),
        light_left=msg.light_left.state,
        light_right=msg.light_right.state,
        current_left=msg.current_left.state,
        bus_voltage_left=msg.bus_voltage_left.state,
        power_left=msg.power_left.state,
        current_right=msg.current_right.state,
        bus_voltage_right=msg.bus_voltage_right.state,
        power_right=msg.power_right.state,
        current_supply=msg.current_supply.state,
        bus_voltage_supply=msg.bus_voltage_supply.state,
        power_supply=msg.power_supply.state,
        stamps=stamps
    )

def encode_control(ctrl: RobotControl) -> bytes:
    msg = pb2.Control()
    msg.effort.state.x = ctrl.effort.x
    msg.effort.state.y = ctrl.effort.y
    return msg.SerializeToString()

sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv.bind(('0.0.0.0', UDP_STATE_PORT))
sock_recv.setblocking(False)

sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

async def udp_loop():
    global current_user_code
    loop = asyncio.get_event_loop()
    while True:
        try:
            data, addr = sock_recv.recvfrom(2048)
            state = decode_state(data)
            
            state_dict = {
                'type': 'state',
                'data': {
                    'distance': state.distance,
                    'effort': {'x': state.effort.x, 'y': state.effort.y},
                    'accel': {'x': state.linear_acceleration.x, 'y': state.linear_acceleration.y, 'z': state.linear_acceleration.z},
                    'gyro': {'x': state.angular_velocity.x, 'y': state.angular_velocity.y, 'z': state.angular_velocity.z},
                    'mag': {'x': state.magnetic_field.x, 'y': state.magnetic_field.y, 'z': state.magnetic_field.z},
                    'light_left': state.light_left,
                    'light_right': state.light_right,
                    'current_left': state.current_left,
                    'bus_voltage_left': state.bus_voltage_left,
                    'power_left': state.power_left,
                    'current_right': state.current_right,
                    'bus_voltage_right': state.bus_voltage_right,
                    'power_right': state.power_right,
                    'current_supply': state.current_supply,
                    'bus_voltage_supply': state.bus_voltage_supply,
                    'power_supply': state.power_supply,
                },
                'stamps': state.stamps
            }
            for conn in active_connections:
                asyncio.create_task(conn.send_text(json.dumps(state_dict)))

            if current_user_code:
                local_env = {'RobotState': RobotState, 'RobotControl': RobotControl, 'Vector2': Vector2, 'Vector3': Vector3}
                try:
                    exec(current_user_code, local_env)
                    if 'control' in local_env:
                        user_func = local_env['control']
                        blank_ctrl = RobotControl(effort=Vector2(0, 0))
                        result_ctrl = user_func(state, blank_ctrl)
                        if result_ctrl:
                            out_data = encode_control(result_ctrl)
                            sock_send.sendto(out_data, (udp_target_ip, UDP_CONTROL_PORT))
                except Exception as e:
                    current_user_code = None
                    err_msg = {'type': 'log', 'data': f"Runtime Error: {e}"}
                    for conn in active_connections:
                        asyncio.create_task(conn.send_text(json.dumps(err_msg)))
                    
        except BlockingIOError:
            await asyncio.sleep(0.01)
        except Exception as e:
            await asyncio.sleep(0.01)

@app.on_event('startup')
async def startup_event():
    asyncio.create_task(udp_loop())

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    global current_user_code, udp_target_ip
    try:
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            
            if msg.get('type') == 'validate':
                code = msg.get('code', '')
                try:
                    compile(code, '<string>', 'exec')
                    await websocket.send_text(json.dumps({'type': 'log', 'data': 'Validation successful.'}))
                except Exception as e:
                    await websocket.send_text(json.dumps({'type': 'log', 'data': f'Validation error: {e}'}))
            
            elif msg.get('type') == 'run':
                code = msg.get('code', '')
                try:
                    compile(code, '<string>', 'exec')
                    current_user_code = code
                    await websocket.send_text(json.dumps({'type': 'log', 'data': 'Running...'}))
                except Exception as e:
                    await websocket.send_text(json.dumps({'type': 'log', 'data': f'Run error: {e}'}))
                    
            elif msg.get('type') == 'stop':
                current_user_code = None
                await websocket.send_text(json.dumps({'type': 'log', 'data': 'Stopped.'}))

            elif msg.get('type') == 'control':
                effort = msg.get('effort', {}) or {}
                try:
                    ctrl = RobotControl(
                        effort=Vector2(
                            x=float(effort.get('x', 0.0)),
                            y=float(effort.get('y', 0.0)),
                        )
                    )
                    out_data = encode_control(ctrl)
                    sock_send.sendto(out_data, (udp_target_ip, UDP_CONTROL_PORT))
                except Exception as e:
                    await websocket.send_text(json.dumps({'type': 'log', 'data': f'Control send error: {e}'}))

            elif msg.get('type') == 'set_control_target_ip':
                new_ip = (msg.get('ip', '') or '').strip()
                if not new_ip:
                    await websocket.send_text(json.dumps({'type': 'log', 'data': 'Control target IP update error: empty IP'}))
                else:
                    udp_target_ip = new_ip
                    await websocket.send_text(json.dumps({'type': 'log', 'data': f'Control target IP set to {udp_target_ip}:{UDP_CONTROL_PORT}'}))

    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
