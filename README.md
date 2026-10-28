# BeeCV

OpenCV webcam app that detects red, orange, yellow, green, blue, and purple
blocks, then draws a labelled bounding box around each one.

## Getting started (Windows)

Follow these steps once to download and run the project.

### 1. Install Python

Install Python 3 from [python.org/downloads](https://www.python.org/downloads/).
During installation, tick **Add Python to PATH** before choosing **Install Now**.

After it finishes, open PowerShell and check that it is available:

```powershell
py --version
```

You should see a version number such as `Python 3.12.x`. If PowerShell says
that `py` is not recognized, close and reopen it, then try again.

### 2. Install Git

If you do not already have Git, install it from [git-scm.com/download/win](https://git-scm.com/download/win).

### 3. Clone this project

In PowerShell, move to the folder where you keep projects, then run:

```powershell
git clone https://github.com/vanshS66/beecv.git
cd beecv
```

### 4. Create a project environment

This keeps BeeCV's packages separate from other Python projects:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is successful, `(.venv)` appears at the beginning of your
PowerShell prompt.

### 5. Install the required packages

```powershell
py -m pip install -r requirements.txt
```

### 6. Run BeeCV

```powershell
py main.py
```

Press `q` or `Esc` to close the preview. Use a different camera with
`py main.py --camera 1`.

The next time you use the project, open PowerShell in the `beecv` folder and
run these two commands:

```powershell
.\.venv\Scripts\Activate.ps1
py main.py
```

## Detection tuning

The detector ignores regions below 1,000 pixels to avoid noise. For smaller
blocks or a higher-resolution camera, lower this threshold:

```powershell
py main.py --min-area 300
```

It works best with a plain, contrasting background and even lighting. The HSV
colour ranges are defined near the top of `main.py` if your blocks need tuning.
