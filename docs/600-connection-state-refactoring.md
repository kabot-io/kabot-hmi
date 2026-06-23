# Connection State Refactoring & Watchdog

## Motivation
Previously, the HMI mockup relied on a basic mechanism for receiving UDP state packets indiscriminately. This was improved to drop unmatched packets, but it introduced a problem where turning off the robot did not update the HMI to a "Disconnected" state, and discovering an already-claimed robot failed to start the telemetry stream. 

## Architectural Changes

### 1. Fix for Auto-Claim Telemetry Stream
During the discovery phase, if a robot responds with `is_claimed = True` and its IP matches ours, the frontend automatically connects to it. However, the frontend was previously failing to notify the backend of this implicit claim.
- **Solution:** The frontend now explicitly sends a `claim_robot` message back to the backend whenever an auto-claimed robot is discovered. This allows the backend to bind its internal `udp_target_ip` and correctly process incoming state UDP packets from the robot, successfully un-freezing the plots.

### 2. Replacing Passive Watchdog with Active Ping Loop
An initial attempt was made to track the connection state via a passive watchdog monitoring the timestamp of the last received UDP telemetry packet (`last_state_time`). This proved unreliable and convoluted.
- **Solution:** Replaced the passive state tracking with an active, continuous Bonjour ping loop (`continuous_ping` background task).
- The HMI now pings the target robot every 1 second over port 30012.
- The UI features a real-time responsive 3-state connection dot:
  - **Green (Connected):** Ping successful.
  - **Yellow (Connection Lost):** The dot turns yellow as soon as 1 or 2 pings are missed. It immediately returns to green if a subsequent ping succeeds.
  - **Red (Disconnected):** If 3 consecutive pings fail, the backend considers the connection permanently dead, clears its active target, and forces the frontend into the disconnected state.

## Implementation Details
- `continuous_ping` in `backend/main.py`: Sends a Bonjour request (with `claim=False` and `release=False`) every 1 second with a 0.5s socket timeout.
- UI Indicator in `frontend/src/app/page.tsx`: Uses the `robotConnectionStatus` React state to conditionally render `bg-green-500`, `bg-yellow-500`, or `bg-red-500` CSS classes.
