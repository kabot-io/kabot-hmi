# Runtime Data Flow

## Control path

1. Operator presses manual control or runs code.
2. Frontend sends WebSocket action (`control` or `run` flow).
3. Backend builds protobuf `Control`.
4. Backend transmits UDP datagram to control target (`ip:30010`).

## State path

1. Firmware publishes protobuf `State` snapshots.
2. Backend receives UDP packets on `30011`.
3. Backend decodes message and stamp fields.
4. Backend broadcasts `state` JSON over WebSocket.
5. Frontend updates live state and channel buffers.
6. Scope plot renders latest buffer window.

## Frequency/Hz behavior

- Hz is derived from stamp delta history.
- Window size is five stamp samples.
- Non-monotonic stamps are treated defensively.

## Scope interactions

- Pause freezes new samples into plotting window.
- Trigger mode waits for configured threshold condition.
- Auto layout computes scale/offset from visible data.

## Editor constraints

- Function signature line is enforced.
- Function body remains editable.
