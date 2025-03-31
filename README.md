# shibrazy macro

a discord monitoring and auto-join tool for roblox games, specifically designed for sols rng. (i made this README.md with the help of ChatGPT because im too lazy to make my own!!!)

## overview

shibrazy macro is a specialized tool that monitors discord channels for specific keywords and game links. when it detects a message containing both a whitelisted keyword and a roblox game link, it automatically opens the link to join the game.

## features

- real-time discord channel monitoring
- keyword filtering with whitelist and blacklist support
- fuzzy matching for keywords to catch misspellings
- automatic game joining when keywords are detected
- sound alerts for specific keywords
- discord webhook integration for notifications
- vip user system with special privileges
- toggle hotkey (ctrl+y) to enable/disable the bot
- support for android emulator integration

## installation

### prerequisites

- windows 10/11
- python 3.7+
- pip (python package installer)

### setup

1. clone this repository
2. install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. configure your settings in `dist/.env` file (will be created on first run)
4. run the application from the `dist` directory

## usage

### configuration

the application uses several configuration files:

1. `dist/.env` - contains discord token and webhook urls
2. `dist/core/constants.py` - contains all application settings

### running the application

1. navigate to the `dist` directory
2. run `main.py`
3. select operating mode (currently only "monitor" is fully implemented)
4. the application will start monitoring configured discord channels

### controls

- `ctrl+y` - toggle bot on/off
- will automatically disable after joining a game (configurable)

## configuration options

### servers and channels

configure the discord servers and channels to monitor in `constants.py`:

```python
SERVERS = {
    "server_id": {
        "name": "server_name",
        "channels": {
            "channel_id": {
                "name": "channel_name",
                "webhook_url": "webhook_url",
                "format": "new",  # can be "old" or "new"
                "game_id": "game_id",
                "game_name": "game_name",
                "whitelist": {
                    "keywords": ["keyword1", "keyword2"],
                    "match_any": true,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": ["bad1", "bad2"],
                    "match_any": true,
                    "fuzzy_exclusions": []
                }
            }
        }
    }
}
```

### keyword matching

the application supports both exact and fuzzy keyword matching:

- **whitelist**: messages must contain these keywords to trigger actions
- **blacklist**: messages containing these keywords will be ignored
- **fuzzy matching**: configurable to catch misspelled keywords

## webhook notifications

when enabled, the application can send notifications to discord webhooks when keywords are detected.

## sound alerts

different sound alerts can be configured for specific keywords in the `constants.py` file.

## project structure

- `dist/`: distribution directory
  - `core/`: core functionality and constants
  - `functions/`: utility functions and handlers
  - `sounds/`: sound effect files
  - `main.py`: entry point
- `tests/`: test stuff which i havent done nothing with so far. dont worry i might do something with it.

## development

- python version: 3.7+
- key dependencies:
  - discord api client
  - keyboard
  - pygame (for sound)
  - requests
  - fuzzy matching libraries

## notes

- this tool is designed for windows 10+ computers and has not been extensively tested on other operating systems
- emulator support is intended for android emulators with adb