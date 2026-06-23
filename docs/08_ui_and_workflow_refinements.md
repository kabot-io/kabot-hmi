# UI and Workflow Refinements

This document summarizes the user interface and workflow improvements made to the Kabot HMI mockup.

## Robot Selection & Auto-Discovery

The Robot Selector was heavily refactored to provide a more intuitive and automated user experience:
- **Componentization:** The robot selection dropdown, along with its status indicators and action buttons (Claim, Unclaim, Scan), was extracted into a reusable `renderRobotSelector` component. This component is now consistently used across the application (e.g., in the Code Editor header and the Settings panel).
- **Auto-Discovery Loop:** If the list of discovered robots is empty, the application automatically enters an aggressive scanning loop (triggering a scan every 3.5 seconds). During this phase, the dropdown is disabled with a "Searching..." placeholder, and the search button continuously spins to visually indicate the background activity.
- **Visual Connection Indicators:** The connection dot dynamically updates to reflect the current state:
  - **Pulsating Blue:** A discovery scan is currently in progress.
  - **Green:** Connected to a claimed robot.
  - **Yellow:** Warning state / Connection lost.
  - **Red:** Disconnected.
- **Claim & Unclaim Improvements:** 
  - The UI now immediately reflects the "Claimed by us" state without requiring a secondary manual scan to update the robot's claimed status.
  - Manually unclaiming a robot no longer clears its selection from the dropdown, allowing for quick "Unclaim -> Re-claim" cycles without needing to re-select the robot from the list.

## Settings & Workspace Optimization

- **Default Workspace:** The application now defaults to the "Code" workspace upon startup, rather than the "Firmware" workspace, reflecting the primary user focus.
- **Settings Streamlining:** The standalone "Configurations" section (which included manual IP overrides and scripts folder paths) was completely removed from the Settings panel. All robot status information is now driven by the dynamic `renderRobotSelector` component.

## Release & Versioning Strategy

A new versioning strategy was adopted for Git tags:
- **Releases:** Official releases use standard semantic versioning tags (e.g., `v0.1.2`, `v0.2.0`).
- **Development Tags:** Ongoing development builds between official releases are tagged with a `-next` suffix (e.g., `v0.1.2-next`). This prevents premature patch version bumps and accommodates unpredictable release scopes (such as unexpected minor or major bumps).
