# 301 UDP Socket Reuse & Orphan Cleanup

In `kabot-hmi`, the backend communicates with the robot via UDP state packets on a specific port.

## The "Address already in use" Problem
When testing the Tauri application, exiting the window might leave the Python sidecar process running as an orphan in the background. The next time the app runs, the Python backend crashes because the old process is still holding the UDP port lock.

## Solutions
1. **Rust Process Management**: As described in [200 Tauri Sidecar Pattern](./200-tauri-sidecar-pattern.md), we implemented the Rust `Drop` trait to explicitly kill the sidecar when the application quits.
2. **Socket Reuse (SO_REUSEADDR)**: To make the backend completely bulletproof against zombie processes, we configured the Python UDP receiving socket with `SO_REUSEADDR` and `SO_REUSEPORT`. This allows the new instance to bind to the port and continue functioning even if an old orphaned instance is silently holding the same port.

```python
sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    pass
sock_recv.bind(('0.0.0.0', UDP_STATE_PORT))
```

---
#python #networking #sockets #bugs #tauri
