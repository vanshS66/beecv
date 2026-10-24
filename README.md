# BeeCV

Minimal OpenCV webcam preview project.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

## Run

```powershell
py main.py
```

Press `q` or `Esc` to close the preview. Use a different camera with
`py main.py --camera 1`.
