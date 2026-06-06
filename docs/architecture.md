# Architecture Overview

## Runtime topology

1. Browser UI connects to backend via WebSocket (`/ws`).
2. Backend receives robot state from UDP `30011` and broadcasts state to UI.
3. UI sends run/stop/validate/control actions to backend over WebSocket.
4. Backend forwards control commands to robot over UDP `30010`.

## Backend responsibilities

- Decode protobuf `State` frames from UDP.
- Encode protobuf `Control` frames to UDP.
- Broadcast decoded state and stamp metadata to all active WebSocket clients.
- Execute user `control(...)` function when run mode is active.
- Accept manual control messages from UI and send immediate control frames.
- Keep control target IP configurable at runtime.

## Frontend responsibilities

- Maintain scope state channels and plotting config.
- Render telemetry tree and UPlot-based charts.
- Offer pause/trigger/autolayout plotting controls.
- Provide code editor for user control function body.
- Keep first code line locked to required function signature.
- Provide compact manual control strip and target IP input.

## Important runtime notes

- State channel discovery is dynamic: numeric fields are flattened and auto-added.
- Control messages are sent only when direction state changes.
- UI arrow-key control handling is active in Scope view.
