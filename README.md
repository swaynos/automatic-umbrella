# automatic-umbrella
Web automation for EA FC25.

# automatic-umbrella
Web automation for EA FC25.

## Setup

To set up the project, you will need to have [pyenv](https://github.com/pyenv/pyenv) and [Poetry](https://python-poetry.org/) installed.

### Installing Python with Pyenv

1. First, install pyenv if you haven't already. Follow the installation instructions from the [pyenv repository](https://github.com/pyenv/pyenv#installation).

2. Once you have pyenv installed, you can install the required version of Python (according to `pyproject.toml`):
   ```bash
   pyenv install 3.10.16
   ```

3. Set the local Python version for the project: 
    ```bash
    pyenv local 3.10.16
    ```

### Installing Poetry
You can install Poetry by following the official installation instructions here.<br>
After installing Poetry, navigate to your project directory and install the dependencies defined in pyproject.toml: 
```bash
poetry install
```

### Setting Up Visual Studio Code
1. Open your project folder in Visual Studio Code.

2. Ensure that the correct Python interpreter is selected:

    - Press ```Ctrl+Shift+P``` (or ```Cmd+Shift+P``` on macOS) to open the command palette.
    Type ```Python: Select Interpreter``` and select the Python version managed by pyenv (3.10.16) and local to the project from the list.
3. Once the interpreter is set, you should be able to run and debug the project without issues.

## .env
This file will be used to store sensitive information such as email and password, as well as user configuration settings. Create this file, and here are the minimum expected variables:
```
APP_URL=https://www.ea.com/ea-sports-fc/ultimate-team/web-app/
EMAIL = "your_email@example.com"
PASSWORD = "your_password"
COOKIES_FILE=cookies.json
DAILY_SIMPLE_BRONZE_SBC_NAMES=Daily Bronze Upgrade,Daily Login Upgrade
DAILY_SIMPLE_SILVER_SBC_NAMES=Daily Silver Upgrade
PACK_NAMES=BRONZE PLAYERS PREMIUM,SMALL BRONZE PLAYERS,SILVER PLAYERS PREMIUM,Small Silver Players Pack,Super Bronze Pack
GOLD_PACK_NAMES=x11 Gold Players Pack
```
<br>

These variables can be used to toggle the flow control of the application:
```
# Step 1. Solve SBC's
SOLVE_DAILY_CHALLENGES=True
GOLD_UPGRADE=False
SPECIAL_UPGRADE=False
TOTY_CRAFTING_UPGRADE=False

# Step 2. Open Packs
OPEN_CHEAP_PACKS=False
OPEN_GOLD_PACKS=False

# Gold Upgrade Parameters
GOLD_UPGRADE_COUNT=1
GOLD_UPGRADE_USE_SBC_STORAGE=True

# Special Upgrade Parameters
SPECIAL_UPGRADE_NAME="82+ Combo Upgrade"
SPECIAL_UPGRADE_COUNT=2
SPECIAL_UPGRADE_RARE_COUNT=0
SPECIAL_UPGRADE_USE_SBC_STORAGE=True
```

Please see ```config.py``` for other configuration options.

## setup.py
This script was written when moving code to a new machine. It will help resolve issues with webdriver-manager. On macOS there may be an additional step outside of the IDE to allow execution of the binaries through the operating system | Security settings.