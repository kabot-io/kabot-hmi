# Developer Workflow

## Common commands

Start full stack:

```bash
./start.sh
```

Backend only:

```bash
cd backend
source venv/bin/activate
python3 main.py
```

Frontend only:

```bash
cd frontend
npm run dev
```

## Typical edit loop

1. Change frontend/backend code.
2. Restart with `./start.sh` if backend protocol/runtime changed.
3. Verify no compile/lint/type errors.
4. Validate manual controls and scope behavior in browser.

## When protobuf changes

1. Update `backend/state_control_msg.proto` from source repo.
2. Regenerate Python binding:

```bash
cd backend
protoc -I. --python_out=. state_control_msg.proto
```

3. Update decode/encode paths if field semantics changed.

## Git hygiene for this repo

- Do not commit virtualenvs.
- Do not commit build outputs (`.next`, `node_modules`, `__pycache__`).
- Commit source, docs, and lockfiles only.

## Known current follow-up

- Next planned work is improving code editor behavior and UX.
