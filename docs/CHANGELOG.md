# Changelog & Session Notes

## UI & Discovery Overhaul (Session Notes)

This document tracks a major sequence of architectural and UI improvements made to the KABOT HMI mockup. 

### 1. Robot Discovery & Network Security
- **Dynamic Discovery:** Completely removed the hardcoded target IP (`172.20.10.2`) across the frontend, backend, and documentation. 
- **Auto-Claiming:** The Python backend now performs a 3-pass network discovery sweep. If a robot is found and claimed by our IP, it is automatically connected and set as the active target.
- **Unclaimed Packet Dropping:** Modified the Python `udp_loop` to actively filter out incoming telemetry UDP packets unless they originate from the explicitly selected (claimed) robot. This prevents the UI from randomly bouncing or displaying data from unselected robots on the network.
- **Auto Search Toggle:** Added a checkbox to disable automatic periodic robot discovery sweeps.

### 2. Teleoperation Controls
- **Continuous Actuation:** Fixed a bug where holding down the teleop arrow keys only sent a single initial command. `sendManualControl` now accepts a `force` flag, allowing a `setInterval` hook to periodically send the control vector every 100ms, bypassing the previous deduplication logic.

### 3. Settings Workspace Overhaul
- **Default Landing Page:** The application now boots directly into the Settings menu instead of the plotter.
- **HMI & Robot Dashboards:** Completely redesigned the settings page. Replaced the generic "Settings and Firmware Configurations" with two live dashboards:
  - **HMI Status:** Displays the live WebSocket connection state to the Python backend, HMI version, and external resource links.
  - **Robot Status:** Extracts and displays live Bonjour discovery data for the connected robot (IP, Serial, Human Name, Firmware Version, Port, and Claim Status).
- **Cleanup:** Removed unused Serial/Baud rate and Motor Type dropdowns. Hid the "Device Shell Output" panel.
- **WIP Features:** The "Connect Robot" and "Firmware Update" dialogs were disabled and replaced with temporary alerts ("This functionality will be available soon. Sorry.").
- **Updated Links:** Added direct links to the `kabot-zephyr` repository, `kabot-hmi` repository, and the KABOT Discord channel.

### 4. Plotter & Signal Browser Improvements
- **Layout Persistence:** Implemented local storage caching for the plotter. The visibility, y-offset, y-scale, and trigger settings for all channels are now seamlessly saved to `localStorage("plot_layout")` and restored on application boot. 
- **SSR Hydration Fix:** Resolved a Next.js hydration mismatch error by moving the `localStorage` payload initialization into a `useEffect` mount hook.
- **Default View:** By default, only the `effort`, `distance`, and `gyro` plots are visible. The IP input field was removed from the plots panel, and the signal browser width was increased by 1.5x to accommodate longer channel names.

### 5. General QoL Improvements
- **Window Maximization:** Updated `tauri.conf.json` to launch the application maximized by default.
- **Action Buttons:** Renamed the "Start" script button to "Run script". Standardized the width of the Run and Stop buttons to prevent UI jitter, and added a glowing red breathing animation to the "Stop" button.
- **Verify Button:** Restored the "Verify" button next to the Run button. It triggers a static type check (via `mypy`) on the backend and displays the results in the log console.
- **Logs Console:** Implemented auto-scrolling to the bottom of the logs console when new messages arrive.
### 6. Connection State Refactoring & Active Ping Loop
- **Bug Fix for Auto-Claiming:** The frontend now explicitly sends a `claim_robot` message back to the backend when an already-claimed robot is discovered. This allows the backend to appropriately bind its target IP and ensures the telemetry stream starts correctly (un-freezing the plots).
- **Active Ping Loop:** Introduced a new background `continuous_ping` polling task. The backend now actively pings the connected robot every 1 second via Bonjour.
- **Dynamic 3-State Connection Dot:** 
  - The UI now features a robust connection indicator that immediately reacts to ping successes and failures.
  - The dot turns Yellow ("Connection Lost") immediately if 1 or 2 pings are missed.
  - The dot turns Red ("Disconnected") and drops the connection state entirely if 3 consecutive pings fail (a window of ~3 seconds).
  - The dot returns to Green ("Connected") immediately upon a successful ping recovery.

### 7. Script Path Context & Documentation
- **Dataclass Semantics in Backend:** Upgraded the `RobotState` timestamp tracker to utilize a fully typed `Stamps` dataclass in `models.py` instead of a plain Python dictionary. This seamlessly enables users to use natural dot-notation (e.g., `state.stamps.light_right`) natively inside their Python `control()` scripts without encountering `AttributeError` exceptions.
- **Rich Unit Trees in UI:** Restructured the Script Paths helper into an interactive, deeply-nested component tree (`ScriptTreeNode`). It now leverages embedded JSX to visually differentiate values and render complex physical units (like $m/s^2$ fractions and $rad/s$) elegantly.
- **Hover Tooltips:** Injected standard HTML `title` tooltips natively into every schema property. Mouseovers now expose explicit hardware boundaries (e.g., `0.0-1.0`), sensor chip models (`DRV8837`, `INA219`), and detailed behavioral definitions for each state and control dimension.

### 8. Build System & Version Automation
- **Git-Aware Release Tags:** Fully automated versioning inside `build_appimage.sh`. The build process now dynamically queries `git describe --tags --always` prior to triggering the Tauri/Next.js toolchains. 
- **Automated Manifest Injection:** If commits have occurred since the last tag, a `-next` suffix is explicitly applied (e.g., `0.2.0-next`); otherwise, the clean base tag is preserved. This derived string is seamlessly injected into `package.json`, `tauri.conf.json`, and `Cargo.toml`, ensuring completely hands-free version syncing across local tests and CI actions.
