import subprocess

class EmulatorHandler:
    def __init__(self):
        self.initialize_adb()

    def initialize_adb(self):
        try:
            # Kill existing ADB server
            subprocess.run('adb kill-server', shell=True)

            # Start ADB server
            subprocess.run('adb start-server', shell=True)

        except Exception as e:
            print(f"Error initializing ADB: {e}")

    def open_url_in_emulator(self, url):
        try:
            formatted_url = url.replace('&', r'\&')
            command = f'adb shell am start -a android.intent.action.VIEW -d "{formatted_url}"'
            subprocess.run(command, shell=True)
            print(f"Successfully opened URL in emulator: {url}")
            return True
        except Exception as e:
            print(f"Error opening URL in emulator: {e}")
            return False