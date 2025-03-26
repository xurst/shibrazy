import os
import json
import uuid
import requests
import subprocess

class KeySystem:
    def __init__(self):
        self.api_endpoint = "https://server-side-keys-3fe93bb399f2.herokuapp.com/validate"
        self.save_file = 'saved_key.json'

    def get_hwid(self):
        try:
            system_uuid = str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip()
            disk_serial = str(subprocess.check_output('wmic diskdrive get serialnumber')).split('\\r\\n')[1].strip()
            cpu_id = str(subprocess.check_output('wmic cpu get processorid')).split('\\r\\n')[1].strip()
            combined = f"{system_uuid}-{disk_serial}-{cpu_id}"
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, combined))
        except:
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(uuid.getnode())))

    def validate_key(self, key, check_saved=False):
        try:
            current_hwid = self.get_hwid()

            # First, check with the server about existing keys for this HWID
            response = requests.post(
                self.api_endpoint,
                json={
                    'key': key,
                    'hwid': current_hwid,
                    'check_only': True  # New parameter to just check without validating
                },
                headers={
                    'Content-Type': 'application/json'
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                existing_key = data.get('existing_key')

                # If there's an existing different key and this isn't a saved key check
                if existing_key and existing_key != key and not check_saved:
                    print(f"\nwarning: you already have a key ({existing_key}) registered on this hardware.")
                    while True:
                        choice = input("do you want to use the new key instead? (y/n): ").lower().strip()
                        if choice in ['y', 'n']:
                            if choice == 'n':
                                self.save_key(existing_key)
                                return True, "using existing key"
                            break
                        print("enter 'y' or 'n'")

                # Only proceed with validation if we don't have an existing key
                # or if the user chose to use the new key
                validation_response = requests.post(
                    self.api_endpoint,
                    json={
                        'key': key,
                        'hwid': current_hwid,
                        'force_new': True  # Add force_new flag when user chooses new key
                    },
                    headers={
                        'Content-Type': 'application/json'
                    },
                    timeout=10
                )

                if validation_response.status_code == 200:
                    validation_data = validation_response.json()
                    if validation_data.get('valid'):
                        self.save_key(key)
                        return True, validation_data.get('message', 'key validated successfully')
                    return False, validation_data.get('message', 'invalid key')

            return False, "error connecting to validation server"

        except requests.exceptions.Timeout:
            return False, "validation server timeout - please try again"
        except requests.exceptions.ConnectionError:
            return False, "could not connect to validation server"
        except Exception as e:
            return False, f"error validating key: {str(e)}"

    def save_key(self, key):
        """Save a validated key to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump({
                    'key': key,
                    'hwid': self.get_hwid()
                }, f)
        except Exception as e:
            print(f"warning: could not save key - {e}")

    def load_saved_key(self):
        """Load a previously saved key"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    if data.get('hwid') == self.get_hwid():
                        return data.get('key')
        except Exception as e:
            print(f"warning: could not load saved key - {e}")
        return None