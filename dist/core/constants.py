import os
from dotenv import load_dotenv

load_dotenv()

# Interface configuration table
INTERFACE = {
    "mode": "terminal"  # Options: "terminal" or "app"
}

SHIBRAZY_VERSION = 1.47

# Animation configuration tables
ANIMATION = {
    "enabled": True,  # Master toggle for all animations

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
        "text": [  # ASCII banner text
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

# Notification configuration table
NOTIFICATIONS = {
    "enabled": False,
    "startup_test": False,
    "timeouts": {
        "license": 5,
        "toggle": 5,
        "keyword": 5
    }
}

# Server configuration table
SERVERS = {
    0000000000000000000: {  # Placeholder server ID
        "name": "Placeholder Server",
        "channels": {
            000000000000000000: {  # Placeholder channel ID
                "name": "placeholder-channel",
                "webhook_url": os.getenv('PLACEHOLDER_WEBHOOK'),
                "format": "new",
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

# Timing configuration table
TIMING = {
    "check_delay": 0.01,  # Reduced from 0.05 for faster checking
    "rate_limit_delay": 0.05,  # Reduced from 0.1 for faster recovery
    "link_timer": 5,
    "overlapping": False
}

VIP = {
    "enabled": True,
    "users": [
        "994927455175458857",  # Original VIP user
        # Add more VIP user IDs here
    ],
    "benefits": {
        "bypass_blacklist": True,
        "bypass_whitelist": True,
        "play_vip_sound": False,
        "priority_processing": True
    }
}

# Fuzzy matching configuration table
FUZZY = {
    "whitelist": {
        "enabled": True,
        "match_ratio": 75,
        "match_type": "ratio",
        "ignore_case": True,
        "min_length": 0,
        "word_handling": {
            "split_compound_words": True,  # Enable splitting of compound words
            "split_characters": ["-", "_", "+", "."],  # Characters to split words on
            "remove_special_chars": True,  # Remove special characters before matching
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

# Processing configuration table
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

# Output configuration table
OUTPUT = {
    "actual_joining": True,
    "disable_bot_on_join": True,
    "print_whitelisted_only": False,
    "print_when_disabled": True,
    "webhook": True,
    "toggle_hotkey": 'ctrl+y',
}

# Emulator configuration table
EMULATOR = {
    "use_emulator": False,
}

# Sound configuration table
SOUND = {
    "enabled": True,
    "directory": os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds", "keyword_find"),
    "volume": 0.8,
    "keyword_sounds": {
        # Specific keyword to sound mappings
        "keywords": {
            "example_keyword": "example_sound.mp3",
        }
    }
}