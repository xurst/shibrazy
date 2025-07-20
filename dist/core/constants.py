import os
from dotenv import load_dotenv

load_dotenv()

# interface configuration table
INTERFACE = {
    "mode": "terminal"  # options: "terminal" or "app"
}

SHIBRAZY_VERSION = 1.48

# animation configuration tables
ANIMATION = {
    "enabled": True,  # master toggle for all animations

    "title": {
        "text": f"shibrazy v{SHIBRAZY_VERSION}",
        "color": "RED",
        "glitch_iterations": 3,
        "glitch_chars": "!@#$%^&*()_+-={}[]|;:,.<>?",
        "glitch_probability": 0.3
    },

    "matrix": {
        "duration": 1.5,
        "density_chars": "░▒▓█",
        "colors": ["GREEN", "CYAN", "WHITE"],
        "primary_color": "GREEN",
        "delay": 0.05
    },

    "loading": {
        "bar_width": 30,
        "bar_char": "█",
        "empty_char": "░",
        "color": "CYAN"
    },

    "system_check": {
        "color": "GREEN",
        "systems": [
            "MEMORY ALLOCATION",
            "NETWORK PROTOCOLS",
            "API ENDPOINTS",
            "SECURITY MODULES",
            "DISCORD GATEWAY",
            "WEBSOCKET CONNECTION",
            "DATABASE INTEGRITY",
            "MONITORING SYSTEMS"
        ],
        "statuses": ["OK", "VERIFIED", "ACTIVE", "STABLE"],
        "delay_range": [0.1, 0.3]
    },

    "banner": {
        "color": "MAGENTA",
        "text": [  # ascii banner text
            """
  ███████╗██╗  ██╗██╗██████╗ ██████╗  █████╗ ███████╗██╗   ██╗    ██╗
  ██╔════╝██║  ██║██║██╔══██╗██╔══██╗██╔══██╗╚══███╔╝╚██╗ ██╔╝    ██║
  ███████╗███████║██║██████╔╝██████╔╝███████║  ███╔╝  ╚████╔╝     ██║
  ╚════██║██╔══██║██║██╔══██╗██╔══██╗██╔══██║ ███╔╝    ╚██╔╝      ╚═╝
  ███████║██║  ██║██║██████╔╝██║  ██║██║  ██║███████╗   ██║       ██╗
  ╚══════╝╚═╝  ╚═╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝
"""
        ]
    },

    "typewriter": {
        "delay": 0.03,
        "color": "GREEN",
        "glitch_colors": ["GREEN", "CYAN", "WHITE", "MAGENTA"],
        "glitch_probability": 0.1,
        "messages": [
            "ESTABLISHING SECURE CONNECTION...",
            "INITIALIZING MONITORING PROTOCOLS..."
        ]
    },

    "spinner": {
        "frames": ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        "delay": 0.1,
        "color": "MAGENTA"
    }
}

# notification configuration table
NOTIFICATIONS = {
    "enabled": False,
    "startup_test": False,
    "timeouts": {
        "license": 5,
        "toggle": 5,
        "keyword": 5
    }
}

# server configuration table
SERVERS = {
    0000000000000000000: {  # placeholder server id
        "name": "Placeholder Server",
        "channels": {
            000000000000000000: {  # placeholder channel id
                "name": "placeholder-channel",
                "webhook_url": os.getenv('PLACEHOLDER_WEBHOOK'),
                "format": "new",  # can be "old" or "new"
                "game_id": "00000000000",
                "game_name": "Placeholder Game",
                "whitelist": {
                    "keywords": ["keyword1", "keyword2"],
                    "match_any": True,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": ["bait", "fake"],
                    "match_any": True,
                    "fuzzy_exclusions": []
                }
            }
        }
    }
}

# timing configuration table
TIMING = {
    "check_delay": 0.01,  # reduced from 0.05 for faster checking
    "rate_limit_delay": 0.05,  # reduced from 0.1 for faster recovery
    "link_timer": 5,
    "overlapping": False
}

VIP = {
    "enabled": True,
    "users": [
        "994927455175458857",  # original vip user
        # add more vip user ids here
    ],
    "benefits": {
        "bypass_blacklist": True,
        "bypass_whitelist": True,
        "play_vip_sound": False,
        "priority_processing": True
    }
}

# fuzzy matching configuration table
FUZZY = {
    "whitelist": {
        "enabled": True,
        "match_ratio": 75,
        "match_type": "ratio",
        "ignore_case": True,
        "min_length": 0,
        "word_handling": {
            "split_compound_words": True,  # enable splitting of compound words
            "split_characters": ["-", "_", "+", "."],  # characters to split words on
            "remove_special_chars": True,  # remove special characters before matching
            "special_chars": ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ",", "?"]
        }
    },
    "blacklist": {
        "enabled": True,
        "match_ratio": 80,
        "match_type": "ratio",
        "ignore_case": True,
        "min_length": 0,
        "word_handling": {
            "split_compound_words": True,
            "split_characters": ["-", "_", "+", "."],
            "remove_special_chars": True,
            "special_chars": ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ",", "?"]
        }
    }
}

# processing configuration table
PROCESSING = {
    "enable_stats": True,
    "stats_directory": "stats",
    "stats_metrics": {
        "messages_processed": True,
        "successful_joins": True,
        "failed_joins": True,
        "keywords_matched": True,
        "uptime": True
    }
}

# output configuration table
OUTPUT = {
    "actual_joining": True,
    "disable_bot_on_join": True,
    "print_whitelisted_only": False,
    "print_when_disabled": True,
    "webhook": True,
    "toggle_hotkey": 'ctrl+y',
}

# emulator configuration table
EMULATOR = {
    "use_emulator": False,
}

# sound configuration table
SOUND = {
    "enabled": True,
    "directory": os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds", "keyword_find"),
    "volume": 0.8,
    "keyword_sounds": {
        # specific keyword to sound mappings
        "keywords": {
            "example_keyword": "example_sound.mp3",
        }
    }
}