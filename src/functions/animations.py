import os
import time
import random
import shutil
import itertools
import sys
import colorama
from colorama import Fore, Style

colorama.init()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_glitch_text(text, config):
    """Print text with a glitch effect"""
    glitch_chars = config["title"]["glitch_chars"]
    prob = config["title"]["glitch_probability"]
    iterations = config["title"]["glitch_iterations"]

    for _ in range(iterations):
        glitched = ''.join(random.choice(glitch_chars) if random.random() < prob else char for char in text)
        print(f"\r{getattr(Fore, config['title']['color'])}{glitched}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(0.05)
    print(f"\r{getattr(Fore, config['title']['color'])}{text}{Style.RESET_ALL}")


def matrix_effect(config):
    """Enhanced matrix effect with varying densities and colors"""
    clear_screen()
    width = shutil.get_terminal_size().columns - 1
    density = config["matrix"]["density_chars"]
    colors = [getattr(Fore, color) for color in config["matrix"]["colors"]]
    primary_color = getattr(Fore, config["matrix"]["primary_color"])
    start_time = time.time()
    duration = config["matrix"]["duration"]

    while time.time() - start_time < duration:
        line = ''
        for _ in range(width):
            char = random.choice(density) if random.random() < 0.7 else random.choice('01')
            color = random.choice(colors) if random.random() < 0.1 else primary_color
            line += f"{color}{char}{Style.RESET_ALL}"
        print(line)
        time.sleep(config["matrix"]["delay"])
    clear_screen()


def loading_bar(text, config, duration=1.0):
    """Animated loading bar with percentage"""
    width = config["loading"]["bar_width"]
    bar_char = config["loading"]["bar_char"]
    empty_char = config["loading"]["empty_char"]
    color = getattr(Fore, config["loading"]["color"])

    for i in range(width + 1):
        progress = i / width
        bar = bar_char * i + empty_char * (width - i)
        percentage = int(progress * 100)
        print(f'\r{color}{text} [{bar}] {percentage}%{Style.RESET_ALL}', end='')
        time.sleep(duration / width)
    print()


def fake_system_check(config):
    """Simulated system check with technical details"""
    systems = config["system_check"]["systems"]
    statuses = config["system_check"]["statuses"]
    min_delay, max_delay = config["system_check"]["delay_range"]
    color = getattr(Fore, config["system_check"]["color"])

    for system in systems:
        status = random.choice(statuses)
        print(f"{color}[+]{Style.RESET_ALL} checking {Fore.CYAN}{system}{Style.RESET_ALL}... ", end='', flush=True)
        time.sleep(random.uniform(min_delay, max_delay))
        print(f"{color}{status}{Style.RESET_ALL}")


def print_banner(config):
    color = getattr(Fore, config["banner"]["color"])
    banner = f"{color}{''.join(config['banner']['text'])}{Style.RESET_ALL}"
    print(banner)

def typewriter(text, config):
    """Enhanced typewriter effect with color glitches"""
    delay = config["typewriter"]["delay"]
    colors = [getattr(Fore, color) for color in config["typewriter"]["glitch_colors"]]
    main_color = getattr(Fore, config["typewriter"]["color"])
    prob = config["typewriter"]["glitch_probability"]

    for char in text:
        if random.random() < prob:
            print(f"{random.choice(colors)}{char}{Style.RESET_ALL}", end='', flush=True)
        else:
            print(f"{main_color}{char}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(delay)
    print()


def loading_animation(stop_event, config):
    frames = config["spinner"]["frames"]
    delay = config["spinner"]["delay"]
    color = getattr(Fore, config["spinner"]["color"])

    spinner = itertools.cycle(frames)
    while not stop_event.is_set():
        sys.stdout.write(f'\r{color}initializing {next(spinner)} {Style.RESET_ALL}')
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\r')
    sys.stdout.flush()
    clear_screen()


def startup_sequence(config):
    """Enhanced startup animation sequence"""
    try:
        if not config["enabled"]:
            clear_screen()
            print_banner(config)
            return

        clear_screen()
        print_glitch_text(config["title"]["text"], config)
        time.sleep(0.5)

        matrix_effect(config)

        print(f"\n{getattr(Fore, 'CYAN')}[SYSTEM INITIALIZATION]{Style.RESET_ALL}")
        loading_bar("Loading core systems", config, 1.0)

        print(f"\n{getattr(Fore, 'YELLOW')}[SECURITY CHECK]{Style.RESET_ALL}")
        fake_system_check(config)

        print(f"\n{getattr(Fore, 'MAGENTA')}[FINAL SETUP]{Style.RESET_ALL}")
        for message in config["typewriter"]["messages"]:
            typewriter(message, config)
            time.sleep(0.3)

        print(f"\n{getattr(Fore, 'GREEN')}[SYSTEM READY]{Style.RESET_ALL}")
        time.sleep(0.5)

        matrix_effect(config)
        clear_screen()
        print_banner(config)
    except Exception as e:
        print(f"{Fore.RED}animation error: {e}{Style.RESET_ALL}")
        print_banner(config)  # Fallback to regular banner