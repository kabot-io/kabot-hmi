# 301 UDP Socket Reuse & Conflict Handling

In `kabot-hmi`, the backend communicates with the robot via UDP state packets on a specific port.

## The "Address already in use" Problem
When testing the Tauri application, exiting the window might leave the Python sidecar process running as an orphan in the background. The next time the app runs, the Python backend traditionally crashed because the old process was still holding the UDP port lock.

## Solutions

### 1. Rust Process Management
As described in [200 Tauri Sidecar Pattern](./200-tauri-sidecar-pattern.md), we implemented the Rust `Drop` trait to explicitly kill the sidecar when the application quits. This is the primary defense against zombie processes.

### 2. Explicit Conflict Detection (No `SO_REUSEPORT`)
Previously, we attempted to use `SO_REUSEPORT` to force binding. However, this caused silent failures and packet splitting between the zombie process and the new process, resulting in erratic telemetry.

We removed `SO_REUSEPORT`. Instead, we now explicitly catch the `OSError` during the bind phase. If the port is in use, the backend continues to boot but flags the conflict. The frontend polls this state and immediately presents a blocking modal to the user, instructing them to kill the orphaned instance.

```python
backend_port_conflict = None

sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock_recv.bind(('0.0.0.0', UDP_STATE_PORT))
except OSError:
    backend_port_conflict = UDP_STATE_PORT
sock_recv.setblocking(False)
```

---
#python #networking #sockets #bugs #tauri
