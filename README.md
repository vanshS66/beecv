# BeeCV

OpenCV webcam app that detects red, orange, yellow, green, blue, and purple
blocks, then draws a labelled bounding box around each one.

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

## Detection tuning

The detector ignores regions below 1,000 pixels to avoid noise. For smaller
blocks or a higher-resolution camera, lower this threshold:

```powershell
py main.py --min-area 300
```

It works best with a plain, contrasting background and even lighting. The HSV
colour ranges are defined near the top of `main.py` if your blocks need tuning.
