# Kabot Script Execution and Error Handling

This document summarizes the changes made to the kabot-hmi-mockup application regarding Python script execution, connection reliability, error handling, and UI reporting.

## 1. Connection Reliability & Ghost States
Previously, the UI could enter a "ghost state" where the robot was disconnected, but the plot continued updating, and the robot remained selected in the dropdown. 
- **Active Ping Mechanism**: A Bonjour ping loop was introduced in `backend/main.py` (`udp_ping_loop`). The backend continuously sends discovery sweep pings. If a robot stops responding to pings (timeout threshold), it is actively deregistered.
- **WebSocket Disconnection Cleanup**: If all frontend WebSockets disconnect, the backend automatically releases its claim on any connected robot by resetting `udp_target_ip` and broadcasting a release packet.
- **Frontend State Cleanup**: On receiving a `robot_disconnected` or `robot_lost` event containing the robot's IP, the frontend explicitly removes it from `discoveredRobots`, resets `selectedRobotSerial`, and drops the `connectedRobot` state, ensuring the UI accurately reflects a fully disconnected state.

## 2. Robust Script Execution & Failure Handling
When users inject errors into their scripts, the system needs to gracefully handle the failure without entering an invalid state.
- **Clearing Stale Callables**: The backend `_build_user_callable` is wrapped in an exception handler. If `compile` or `exec` fails due to syntax or runtime errors at the module level, the global `current_user_callable` is immediately set to `None`. This stops the runtime loop (`udp_loop`) from executing a broken script and implicitly halts plotting/control updates.
- **Clearing Frontend Logs**: The frontend automatically flushes the terminal logs (`setLogs([])`) when the user clicks 'Run', preventing old, stale output from masking new script execution failures.
- **Automatic Script Termination**: If a robot disconnects due to a ping timeout while a script is running, the backend natively intercepts the disconnect, drops the script (`current_user_callable = None`), stops the execution loop, and forces a broadcast of `runtime_status: active: False`. This cleanly synchronizes the frontend, stopping the script without ghost states.
- **Run Button Guard**: The frontend "Run" button dynamically guards against execution attempts when a robot is not actively connected (`disabled={!isRunning || robotConnectionStatus !== 'connected'}`).
- **Traceback Broadcasting**: Upon any syntax error or runtime exception, the backend captures the full Python traceback (`traceback.format_exc()`) and broadcasts it over the WebSocket as a `log` event prefixed with "Error parsing script" or "Runtime Error". This automatically flips the frontend `isRunning` state back to `false` and unlocks the Run button.

## 3. Monaco Editor Inline Error Highlighting
To improve the developer experience, the frontend features advanced parsing of backend Python tracebacks to provide inline visual feedback directly inside the Monaco Editor.
- **Traceback Parsing**: When the frontend receives a traceback string over the WebSocket, it scans backwards for the pattern `File "<user_code>", line X`. This maps 1-to-1 with the user's code in the editor.
- **Dual Monaco Decorations**:
  1. **Whole-Line Highlight**: A red background is applied across the entire code line (`isWholeLine: true`) using a standard `rgba` color to ensure high-visibility and cross-theme compatibility.
  2. **Inline Squiggle & Text Injection**: A secondary decoration targets the exact text range (from column 1 to the end of the line). It applies a red wavy underline (`.error-squiggle`) to the code and uses Monaco's `after` pseudo-element injection to append the raw Python exception string (e.g., `NameError: name 'asd' is not defined`) to the very end of the line.
- **Custom CSS Styling**: The injected text is styled using a dedicated CSS class (`.error-inline-text`) forcing it to render as bold, red, monospace text. 
- **Read-Only Mode & Visual Feedback**: While the script is successfully running, the `<Editor>` component automatically shifts into `readOnly` mode. The editor container's opacity is reduced to 50%, pointer events are disabled, and it pulses softly (`animate-pulse`) to signal execution state. All decorations are instantly cleared the moment the user hits "Run" again.

## 4. Versioning Strategy Update
- The development version string was updated from `0.1.2-dev` to `0.1.1-next` across `package.json`, `tauri.conf.json`, and `Cargo.toml`. This aligns with the new convention where development builds carry the `-next` suffix appended to the *most recently tagged version* rather than anticipating the scope of the next release.
