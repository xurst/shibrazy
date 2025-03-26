import sys
import time
import keyboard
import threading
import subprocess
import requests
from packaging import version
from src.core.constants import (
    INTERFACE,
    ANIMATION,
    NOTIFICATIONS,
    SERVERS,
    TIMING,
    FUZZY,
    PROCESSING,
    OUTPUT,
    EMULATOR,
    SOUND, SHIBRAZY_VERSION
)
from src.functions.client.browser.browser_handler import BrowserHandler
from src.functions.client.discord.discord_handler import DiscordHandler
from src.functions.client.message_handler import MessageChecker
from src.functions.client.emulator import EmulatorHandler
from src.functions.github_updater import GitHubUpdater
from bot_state import BotState
import os
from dotenv import load_dotenv
import colorama
from colorama import Fore, Style
from plyer import notification
from src.functions.animations import (
    startup_sequence,
    loading_animation,
    clear_screen,
    print_banner
)

# Initialize colorama
colorama.init()

def create_default_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        default_env_content = "DISCORD_TOKEN="
        try:
            with open(env_path, 'w') as f:
                f.write(default_env_content)
            print(f"{Fore.GREEN}✓ .env file created at {env_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}error creating .env file: {e}{Style.RESET_ALL}")

def select_mode():
    print(f"\n{Fore.CYAN}=== mode Selection ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}available modes:{Style.RESET_ALL}")
    print(f"1. monitor - real-time monitoring and joining")
    print(f"2. afk - {Fore.RED}[in development]{Style.RESET_ALL}")
    print(f"3. overnight - {Fore.RED}[in development]{Style.RESET_ALL}")

    while True:
        try:
            choice = input(f"\n{Fore.YELLOW}select mode (1-3): {Style.RESET_ALL}").strip()
            if choice == "1":
                return "monitor"
            elif choice in ["2", "3"]:
                print(f"{Fore.RED}invalid choice dummy. please select 1-3.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}invalid choice dummy. please select 1-3.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}. please try again.{Style.RESET_ALL}")

class MainRunner:
    def __init__(self):
        self.running = True
        self.toggle_event = threading.Event()
        self.discord_handler = DiscordHandler()
        self.emulator = EmulatorHandler()
        self.browser_handler = BrowserHandler(self.emulator)
        self.message_checker = MessageChecker()

    def toggle_bot(self):
        try:
            last_toggle_time = 0
            while not self.toggle_event.is_set():
                current_time = time.time()
                if keyboard.is_pressed(OUTPUT["toggle_hotkey"]) and (current_time - last_toggle_time) > 0.5:
                    BotState.set_bot_enabled(not BotState.get_bot_enabled())
                    status = f"{Fore.GREEN}ENABLED{Style.RESET_ALL}" if BotState.get_bot_enabled() else f"{Fore.RED}DISABLED{Style.RESET_ALL}"
                    print(f"\nbot functionality {status}")

                    if NOTIFICATIONS["enabled"]:
                        notification.notify(
                            title="shibrazy warning",
                            message=f"bot has been {'enabled' if BotState.get_bot_enabled() else 'disabled'}",
                            app_name="shibrazy",
                            timeout=NOTIFICATIONS["timeouts"]["toggle"]
                        )

                    last_toggle_time = current_time
                    while keyboard.is_pressed(OUTPUT["toggle_hotkey"]):
                        time.sleep(0.1)
                time.sleep(0.1)
        except Exception as e:
            print(f"{Fore.RED}error in toggle thread: {e}{Style.RESET_ALL}")

    def run(self):
        startup_sequence(ANIMATION)

        if NOTIFICATIONS["startup_test"]:
            notification.notify(
                title="shibrazy debug",
                message="notification system test",
                app_name="shibrazy",
                timeout=5
            )
            print(f"{Fore.GREEN}✓ test notification sent{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ test notification skipped (disabled in settings){Style.RESET_ALL}")

        stop_loading = threading.Event()
        loading_thread = threading.Thread(target=loading_animation, args=(stop_loading, ANIMATION))
        loading_thread.start()

        time.sleep(2)
        stop_loading.set()
        loading_thread.join()
        print('\n')

        print(f"\n{Fore.CYAN}shibrazy v{SHIBRAZY_VERSION}{Style.RESET_ALL}")

        print(f"\n{Fore.YELLOW}monitoring:{Style.RESET_ALL}")
        for server_id, server_config in SERVERS.items():
            print(f"\n{Fore.BLUE}{server_config['name']} ({server_id}){Style.RESET_ALL}")
            for channel_id, channel in server_config['channels'].items():
                channel_name = channel.get('name', f'Channel {channel_id}')
                print(f"  {Fore.WHITE}• {channel_name}:{Style.RESET_ALL}")
                print(f"    - whitelisted keywords: {', '.join(channel['whitelist']['keywords'])}")
                print(f"    - blacklisted keywords: {', '.join(channel['blacklist']['keywords'])}")
                print(f"    - match mode: {'any keyword' if channel['whitelist']['match_any'] else 'all keywords'}")
                webhook_mode = 'keywords only' if channel.get('webhook_only_keywords', False) else 'all messages'
                print(f"    - webhook Mode: {webhook_mode}")

        print(f"\n{Fore.YELLOW}controls:{Style.RESET_ALL}")
        print(f"• {OUTPUT['toggle_hotkey']} - toggle bot")
        print(f"• printing mode: {'whitelisted keywords only' if OUTPUT['print_whitelisted_only'] else 'all messages'}")
        print(f"• print when disabled: {'yes' if OUTPUT['print_when_disabled'] else 'no'}")
        print(f"\n{Fore.GREEN}bot is running...{Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA}-{Style.RESET_ALL}" * 50)

        toggle_thread = threading.Thread(target=self.toggle_bot, daemon=True)
        toggle_thread.start()

        last_message_ids = {}
        while self.running:
            try:
                for server_id, server_config in SERVERS.items():
                    for channel_id in server_config['channels'].keys():
                        msg = self.discord_handler.get_latest_message(channel_id)
                        if msg and msg.get('id') != last_message_ids.get(channel_id):
                            self.message_checker.process_message(
                                msg,
                                self.browser_handler,
                                server_id,
                                channel_id,
                                server_config['channels'][channel_id],
                                discord_handler=self.discord_handler
                            )
                            last_message_ids[channel_id] = msg.get('id')

                time.sleep(TIMING["check_delay"])
            except Exception as e:
                time.sleep(TIMING["rate_limit_delay"])

    def __del__(self):
        print(f"\n{Fore.YELLOW}cleaning up...{Style.RESET_ALL}")
        self.running = False
        if hasattr(self, 'toggle_event'):
            self.toggle_event.set()

if __name__ == "__main__":
    updater = GitHubUpdater(
        repo_owner="xurst",
        repo_name="shibrazy",
        current_version=SHIBRAZY_VERSION
    )
    
    if updater.check_for_update():
        if updater.prompt_for_update():
            updater.download_and_install_update()
        else:
            print(f"{Fore.RED}update required to run the application. exiting...{Style.RESET_ALL}")
            sys.exit(1)

    if not INTERFACE.get("mode") == "terminal" or "CHILD_PROCESS" in sys.argv:
        create_default_env()

        selected_mode = select_mode()
        runner = MainRunner()
        runner.run()
    else:
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', python_exe, script_path, 'CHILD_PROCESS'])
        sys.exit(0)