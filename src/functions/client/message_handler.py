import re
from core.constants import (
    SOUND,
    OUTPUT,
    TIMING,
    FUZZY,
    NOTIFICATIONS,
    PROCESSING,
    SERVERS,
    VIP,
)
import os
import logging
import pygame
import random
import colorama
from colorama import Fore, Back, Style
import time
from plyer import notification
import html
from fuzzywuzzy import fuzz
from bot_state import BotState

colorama.init()

class MessageChecker:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageChecker, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not MessageChecker._initialized:
            print(f"\n{Fore.CYAN}initializing shibrazy macro...{Style.RESET_ALL}")
            self.processed_messages = set()  # Track processed message IDs
            self.start_time = time.time()  # Track when the script started
            try:
                pygame.mixer.quit()  # Ensure clean state
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                print(f"{Fore.GREEN}✓ pygame mixer initialized: {pygame.mixer.get_init()}{Style.RESET_ALL}")
                self.sound_objects = []
                self.load_sound_files()
            except Exception as e:
                print(f"{Fore.RED}✗ error initializing pygame mixer: {e}{Style.RESET_ALL}")
            MessageChecker._initialized = True

    def load_sound_files(self):
        self.sound_objects = []
        if SOUND["enabled"] and os.path.exists(SOUND["directory"]):
            print(f"\n{Fore.YELLOW}loading sound files from: {SOUND['directory']}{Style.RESET_ALL}")
            files = os.listdir(SOUND["directory"])
            print(f"{Fore.GREEN}found files: {', '.join(files)}{Style.RESET_ALL}")

            for file in files:
                if file.endswith('.mp3'):
                    try:
                        sound_path = os.path.join(SOUND["directory"], file)
                        print(f"{Fore.GREEN}loaded: {file} ", end='')
                        sound = pygame.mixer.Sound(sound_path)
                        sound.set_volume(SOUND["volume"])
                        self.sound_objects.append(sound)
                        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}✗ error: {e}{Style.RESET_ALL}")
        else:
            print(
                f"{Fore.YELLOW}sound directory not found or SOUND enabled is False. dir: {SOUND['directory']}, enabled: {SOUND['enabled']}{Style.RESET_ALL}")

    def play_keyword_sound(self, keyword):
        if SOUND["enabled"] and keyword in SOUND["keyword_sounds"]["keywords"]:
            sound_file = SOUND["keyword_sounds"]["keywords"].get(keyword)
            sound_path = os.path.join(SOUND["directory"], sound_file)
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(SOUND["volume"])
                sound.play()
                print(f"{Fore.GREEN}✓ playing sound for keyword: {keyword}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}✗ error playing keyword sound: {e}{Style.RESET_ALL}")

    def check_keywords(self, content, keyword_config, match_any, is_blacklist=False):
        if not content:
            return False, []

        content_lower = content.lower() if FUZZY["blacklist" if is_blacklist else "whitelist"][
            "ignore_case"] else content
        keywords_found = []
        match_config = FUZZY["blacklist" if is_blacklist else "whitelist"]

        if not match_config["enabled"]:
            return False, []

        # Get fuzzy exclusions from channel configuration
        fuzzy_exclusions = keyword_config.get('fuzzy_exclusions', [])

        # Handle word splitting based on FUZZY config
        word_handling = match_config["word_handling"]
        words = content_lower.split()

        if word_handling["split_compound_words"]:
            split_words = []
            for word in words:
                for char in word_handling["split_characters"]:
                    word = word.replace(char, ' ')
                split_words.extend(word.split())
            words = split_words

        # Remove special characters if configured
        if word_handling["remove_special_chars"]:
            cleaned_words = []
            for word in words:
                cleaned_word = word
                for char in word_handling["special_chars"]:
                    cleaned_word = cleaned_word.replace(char, '')
                if cleaned_word and len(cleaned_word) >= match_config["min_length"]:
                    cleaned_words.append(cleaned_word)
            words = cleaned_words if cleaned_words else words

        # Check each word against keywords
        for word in words:
            # Skip word if it's in fuzzy exclusions
            if word in fuzzy_exclusions:
                continue

            for keyword in keyword_config["keywords"]:
                keyword_proc = keyword.lower() if match_config["ignore_case"] else keyword

                # Skip keyword if it's in fuzzy exclusions
                if keyword_proc in fuzzy_exclusions:
                    if word == keyword_proc:  # Allow direct matches for excluded words/keywords
                        keywords_found.append(keyword)
                        if is_blacklist or match_any:
                            return True, keywords_found
                    continue

                if match_config["match_type"] == "ratio":
                    ratio = fuzz.ratio(word, keyword_proc)
                elif match_config["match_type"] == "partial_ratio":
                    ratio = fuzz.partial_ratio(word, keyword_proc)
                elif match_config["match_type"] == "token_sort_ratio":
                    ratio = fuzz.token_sort_ratio(word, keyword_proc)
                elif match_config["match_type"] == "token_set_ratio":
                    ratio = fuzz.token_set_ratio(word, keyword_proc)

                # Also check if the keyword is contained within the word
                contains_keyword = keyword_proc in word

                if ratio >= match_config["match_ratio"] or contains_keyword:
                    keywords_found.append(keyword)
                    if is_blacklist or match_any:
                        return True, keywords_found

        if not match_any:
            return len(keywords_found) == len(keyword_config["keywords"]), keywords_found

        return bool(keywords_found), keywords_found

    def extract_roblox_url(self, content, channel_config):
        if not content or not channel_config:
            return None

        if channel_config["format"] == "old":
            # Match exactly: https://www.roblox.com/share?code=<alphanumeric>&type=Server
            match = re.search(r"https://www\.roblox\.com/share\?code=[a-f0-9]+&type=Server", content)
            if match:
                return match.group(0).strip()
        else:  # new format
            # Match exactly: https://www.roblox.com/games/<game_id>/<name>?privateServerLinkCode=<numbers>
            expected_game_id = channel_config["game_id"]
            match = re.search(
                rf"https://www\.roblox\.com/games/{expected_game_id}/[^?\s]+\?privateServerLinkCode=\d+",
                content
            )
            if match:
                return match.group(0).strip()

        return None

    def process_message(self, msg, browser_handler, server_id, channel_id, channel_config, bot_enabled=True,
                        discord_handler=None):
        if not msg or not channel_config:
            return

        # Get message ID and check if already processed
        message_id = msg.get('id')
        if not message_id:
            return

        if message_id in self.processed_messages:
            print(f"\n{Fore.YELLOW}skipping already processed message: {message_id}{Style.RESET_ALL}")
            return

        # Add message to processed set
        self.processed_messages.add(message_id)

        bot_enabled = BotState.get_bot_enabled()

        # Only check timestamp if we're still processing the message
        timestamp = msg.get('timestamp')
        if timestamp:
            try:
                dt = time.strptime(timestamp.split('.')[0], '%Y-%m-%dT%H:%M:%S')
                msg_time = time.mktime(dt) - time.timezone
                if msg_time < self.start_time:
                    return
            except (ValueError, TypeError):
                return

        content = msg.get('content', '')
        url = self.extract_roblox_url(content, channel_config)
        author = msg.get('author', {})
        author_id = author.get('id')
        username = author.get('username', 'Unknown')
        server_name = SERVERS[server_id]["name"]
        channel_name = channel_config["name"]
        game_name = channel_config.get("game_name", "Unknown Game")

        # Check if user is VIP
        is_vip = VIP["enabled"] and author_id in VIP["users"]

        # Play VIP sound if enabled
        if is_vip and VIP["benefits"]["play_vip_sound"] and url and SOUND["enabled"]:
            try:
                sound_path = os.path.join(SOUND["directory"], "vip.mp3")
                if os.path.exists(sound_path):
                    if not pygame.mixer.get_init():
                        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(SOUND["volume"])
                    sound.play()
                    print(f"{Fore.GREEN}✓ playing VIP alert sound{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}✗ error playing VIP sound: {e}{Style.RESET_ALL}")

        # Remove the URL from content to get actual message
        message_content = content
        if url:
            message_content = content.replace(url, '').strip()

        # Check blacklist first, but skip for VIP users with blacklist bypass
        if not (is_vip and VIP["benefits"]["bypass_blacklist"]):
            blacklist_match, blacklist_found = self.check_keywords(message_content, channel_config['blacklist'],
                                                                   channel_config['blacklist']['match_any'],
                                                                   is_blacklist=True)
            if blacklist_match:
                # Format blacklist details with fuzzy matching info
                blacklist_details = []
                for word in message_content.lower().split():
                    for keyword in channel_config['blacklist']['keywords']:
                        ratio = fuzz.ratio(word.lower(), keyword.lower())
                        if ratio >= FUZZY["blacklist"]["match_ratio"]:
                            details = keyword
                            if ratio < 100:  # Only add the original word if it wasn't an exact match
                                details += f" (matched '{word}' at {ratio}%)"
                            blacklist_details.append(details)

                print(f"\n{Fore.RED}blacklisted message from {username}:{Style.RESET_ALL}")
                print(f"{Fore.RED}message: {message_content}{Style.RESET_ALL}")
                if url:
                    print(f"{Fore.RED}link: {url}{Style.RESET_ALL}")
                print(f"{Fore.RED}matched keywords: {', '.join(blacklist_details)}{Style.RESET_ALL}")

                if NOTIFICATIONS["enabled"]:
                    try:
                        notification.notify(
                            title=f"⚠️ blacklisted Message - {server_name}",
                            message=f"from: {username}\nchannel: {channel_name}\nkeywords: {', '.join(blacklist_details)}",
                            app_icon=None,
                            timeout=NOTIFICATIONS["timeouts"]["keyword"]
                        )
                    except Exception as e:
                        print(f"{Fore.RED}failed to send notification: {e}{Style.RESET_ALL}")
                return

        # Check whitelist unless VIP user has whitelist bypass
        if is_vip and VIP["benefits"]["bypass_whitelist"]:
            whitelist_match = True
            whitelist_found = ["VIP User"]
        else:
            whitelist_match, whitelist_found = self.check_keywords(message_content, channel_config['whitelist'],
                                                                   channel_config['whitelist']['match_any'],
                                                                   is_blacklist=False)

        if url and (whitelist_match or (is_vip and VIP["benefits"]["bypass_whitelist"])):
            if not bot_enabled:
                print(
                    f"\n{Fore.YELLOW}⚠️ link found but bot is currently DISABLED! "
                    f"use {OUTPUT['toggle_hotkey']} to enable the bot.{Style.RESET_ALL}"
                )
                print(f"{Fore.CYAN}game: {Style.BRIGHT}{game_name}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}link: {Style.BRIGHT}{url}{Style.RESET_ALL}")

            elif OUTPUT["actual_joining"]:
                # Logging and notification setup
                print(f"\n{Fore.GREEN}found a link: {Style.BRIGHT}{url}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}game: {Style.BRIGHT}{game_name}{Style.RESET_ALL}")

                if is_vip:
                    print(f"{Fore.CYAN}VIP user detected - automatically joining game{Style.RESET_ALL}")
                elif whitelist_found:
                    print(f"{Fore.CYAN}matched whitelist keywords: {', '.join(whitelist_found)}{Style.RESET_ALL}")

                for keyword in whitelist_found:
                    self.play_keyword_sound(keyword)

                browser_handler.open_url(url)

                if NOTIFICATIONS["enabled"]:
                    try:
                        title = "🎮 VIP Game Link" if is_vip else "🎮 Game Link Found"
                        notification.notify(
                            title=f"{title} - {server_name}",
                            message=(
                                f"from: {username}\n"
                                f"channel: {channel_name}\n"
                                f"keywords: {', '.join(whitelist_found)}"
                            ),
                            app_icon=None,
                            timeout=NOTIFICATIONS["timeouts"]["keyword"]
                        )
                    except Exception as e:
                        print(f"{Fore.RED}failed to send notification: {e}{Style.RESET_ALL}")

                # Disable bot after joining
                if OUTPUT["disable_bot_on_join"]:
                    BotState.set_bot_enabled(False)
                    print(
                        f"\n{Fore.YELLOW}bot automatically disabled after joining game. "
                        f"Use {OUTPUT['toggle_hotkey']} to re-enable.{Style.RESET_ALL}"
                    )

                    if NOTIFICATIONS["enabled"]:
                        notification.notify(
                            title="shibrazy",
                            message="bot has been automatically disabled after joining game",
                            app_name="shibrazy",
                            timeout=NOTIFICATIONS["timeouts"]["toggle"]
                        )

            else:
                print(
                    f"\n{Fore.YELLOW}found a link but actual_joining is disabled (debug mode): "
                    f"{Style.BRIGHT}{url}{Style.RESET_ALL}"
                )

                if whitelist_found:
                    print(f"{Fore.CYAN}matched whitelist keywords: {', '.join(whitelist_found)}{Style.RESET_ALL}")
                    for keyword in whitelist_found:
                        self.play_keyword_sound(keyword)

        # Determine if we should process output (terminal and webhook)
        should_process = False
        if bot_enabled or OUTPUT["print_when_disabled"]:
            if OUTPUT["print_whitelisted_only"]:
                should_process = whitelist_match
            else:
                should_process = True

        # Handle webhook messages based on should_process
        if should_process and OUTPUT["webhook"] and discord_handler:
            if OUTPUT["print_whitelisted_only"]:
                if whitelist_match:
                    discord_handler.send_webhook_message(channel_config['name'], msg, whitelist_found)
            else:
                discord_handler.send_webhook_message(channel_config['name'], msg,
                                                     whitelist_found if whitelist_match else None)

        # Handle terminal output based on should_process
        if should_process:
            author = msg.get('author', {})
            username = author.get('username', 'Unknown')
            user_id = author.get('id', 'Unknown')
            server_name = SERVERS[server_id]["name"]
            channel_name = channel_config["name"]

            print(f"\n{Fore.MAGENTA}═══ New Message ═══{Style.RESET_ALL}")
            print(f"{Fore.CYAN}server:{Style.RESET_ALL} {server_name}")
            print(f"{Fore.CYAN}channel:{Style.RESET_ALL} {channel_name}")
            print(f"{Fore.CYAN}user:{Style.RESET_ALL} {username} ({user_id})")
            print(f"{Fore.CYAN}time:{Style.RESET_ALL} {time.strftime('%H:%M:%S')} on {time.strftime('%d/%m/%Y')}")
            print(f"{Fore.CYAN}message:{Style.RESET_ALL} {message_content}")
            if url:
                print(f"{Fore.CYAN}link:{Style.RESET_ALL} {url}")
            print(f"{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}")