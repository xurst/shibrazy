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
    "enabled": False,  # Master toggle for all animations

    "title": {
        "text": f"shibrazy v{SHIBRAZY_VERSION}",  # Use f-string for dynamic version
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
    1186570213077041233: {
        "name": "Sol's RNG",
        "channels": {
            "1282542323590496277": {
                "name": "biomes",
                "webhook_url": os.getenv('SOLS_RNG_BIOMES_WEBHOOK'),
                "format": "new",  # Can be "old" or "new"
                "game_id": "15532962292",
                "game_name": "Sol's RNG [Eon1-1]",
                "whitelist": {
                    "keywords": ["glitch", "glitched"],
                    "match_any": True,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": ["bait", "pls", "fake", "scam", "where", "not", "baiters", "unreal", "totally", "astrald", "hunting", "hunt", "was", "aura", "when", "waiting", "no", "macro"],
                    "match_any": True,
                    "fuzzy_exclusions": []
                }
            },
            "1282543762425516083": {
                "name": "merchants",
                "webhook_url": os.getenv('SOLS_RNG_MERCHANTS_WEBHOOK'),
                "format": "new",  # Can be "old" or "new"
                "game_id": "15532962292",
                "game_name": "Sol's RNG [Eon1-1]",
                "whitelist": {
                    "keywords": ["mari", "void", "coin", "lucky", "penny", "gear", "trash", "vc", "lp", "jester", "oblivion"],
                    "match_any": True,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": [],
                    "match_any": True,
                    "fuzzy_exclusions": []
                }
            },
        }
    },
    1284692110242746441: {
        "name": "Radiant Team",
        "channels": {
            "1287614809705021470": {
                "name": "glitch-ping-radiant",
                "webhook_url": os.getenv('RADIANT_TEAM_GLITCH_WEBHOOK'),
                "format": "new",
                "game_id": "15532962292",
                "game_name": "Sol's RNG [Eon1-1]",
                "whitelist": {
                    "keywords": ["glitch", "glitched", "<@&1287615051888594944>"],
                    "match_any": True,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": [],
                    "match_any": True,
                    "fuzzy_exclusions": []
                }
            }
        }
    },
    1313799612263305238: {
        "name": "shibrazy testing",
        "channels": {
            "1315241732316729455": {
                "name": "biomes-debug",
                "webhook_url": os.getenv('SOLS_RNG_BIOMES_WEBHOOK'),
                "format": "new",  # Can be "old" or "new"
                "game_id": "15532962292",
                "game_name": "Sol's RNG [Eon1-1]",
                "whitelist": {
                    "keywords": [],
                    "match_any": True,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": [],
                    "match_any": True,
                    "fuzzy_exclusions": []
                }
            },
            "1318129882378534974": {
                "name": "merchants-debug",
                "webhook_url": os.getenv('SOLS_RNG_MERCHANTS_WEBHOOK'),
                "format": "new",  # Can be "old" or "new"
                "game_id": "15532962292",
                "game_name": "Sol's RNG [Eon1-1]",
                "whitelist": {
                    "keywords": [],
                    "match_any": True,
                    "fuzzy_exclusions": []
                },
                "blacklist": {
                    "keywords": [],
                    "match_any": True,
                    "fuzzy_exclusions": []
                }
            },
        }
    },
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
        "play_vip_sound": True,
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
    "use_emulator": True,
}

# Sound configuration table
SOUND = {
    "enabled": True,
    "directory": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sounds", "keyword_find"),
    "volume": 0.8,
    "keyword_sounds": {
        # Specific keyword to sound mappings
        "keywords": {
            "glitch": "screaming.mp3",
            "glitched": "screaming.mp3",
            "jester": "screaming.mp3",
            "oblivion": "screaming.mp3",
            "mari": "screaming.mp3",
            "lucky": "screaming.mp3",
            "penny": "screaming.mp3",
            "vc": "screaming.mp3",
            "lp": "screaming.mp3",
            "void": "screaming.mp3",
            "coin": "screaming.mp3",
            "gear": "screaming.mp3",
            "trash": "screaming.mp3",
        }
    }
}