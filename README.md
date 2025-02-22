# automatic-umbrella
Web automation for EA FC25.

## .env
This file will be used to store sensitive information such as email and password, as well as user configuration settings. Create this file, and here are the minimum expected variables:
```
EMAIL = "your_email@email.com"
PASSWORD = "your_password"
DAILY_SIMPLE_BRONZE_SBC_NAMES=Daily Bronze Upgrade
DAILY_SIMPLE_SILVER_SBC_NAMES=Daily Silver Upgrade
PACK_NAMES=BRONZE PLAYERS PREMIUM,SMALL BRONZE PLAYERS,SILVER PLAYERS PREMIUM,Small Silver Players Pack,Super Bronze Pack
GOLD_PACK_NAMES=x11 Gold Players Pack
```
<br>

These variables can be used to toggle the flow control of the application:
```
OPEN_GOLD_PACKS=True
OPEN_CHEAP_PACKS=True
SOLVE_DAILY_CHALLENGES=True
GRASSROOT_GRIND=True
TOTY_CRAFTING_UPGRADE=True
EIGHTYONE_PLUS_PLAYER_PICK=True
```

Please see ```config.py``` for other configuration options.

## setup.py
This script was written when moving code to a new machine. It will help resolve issues with webdriver-manager. On macOS there may be an additional step outside of the IDE to allow execution of the binaries through the operating system | Security settings.