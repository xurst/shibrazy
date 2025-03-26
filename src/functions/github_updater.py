import os
import sys
import requests
import shutil
from packaging import version
import subprocess
from pathlib import Path
import tempfile
import zipfile
from colorama import Fore, Style  # Add this import

class GitHubUpdater:
    """handles checking for and applying updates from github."""
    
    def __init__(self, repo_owner, repo_name, current_version):
        """
        initialize the updater with repository details.
        
        args:
            repo_owner (str): github repository owner
            repo_name (str): github repository name
            current_version (str): current version of the application
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
        self.release_info = None
        
    def check_for_update(self):
        """
        check if an update is available.
        
        returns:
            bool: true if an update is available, false otherwise
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            self.release_info = response.json()
            
            latest_version = self.release_info['tag_name'].lstrip('v')
            return version.parse(latest_version) > version.parse(self.current_version)
        except Exception as e:
            print(f"{Fore.YELLOW}warning: could not check for updates: {e}{Style.RESET_ALL}")
            return False
            
    def prompt_for_update(self):
        """
        display update prompt and handle user response.
        
        returns:
            bool: true if user chose to update, false otherwise
        """
        if not self.release_info:
            return False
            
        latest_version = self.release_info['tag_name'].lstrip('v')
        
        print(f"\n{Fore.CYAN}=== update available ==={Style.RESET_ALL}")
        print(f"current version: {Fore.RED}v{self.current_version}{Style.RESET_ALL}")
        print(f"latest version: {Fore.GREEN}v{latest_version}{Style.RESET_ALL}")
        
        if 'body' in self.release_info and self.release_info['body']:
            print(f"\n{Fore.CYAN}release notes:{Style.RESET_ALL}")
            print(f"{self.release_info['body'][:200]}...")
            
        print(f"\n{Fore.YELLOW}this application requires the latest version to run.{Style.RESET_ALL}")
        print(f"1. update now")
        print(f"2. exit")
        
        while True:
            choice = input(f"\n{Fore.YELLOW}select option (1-2): {Style.RESET_ALL}").strip()
            if choice == "1":
                return True
            elif choice == "2":
                return False
            else:
                print(f"{Fore.RED}invalid choice. please select 1-2.{Style.RESET_ALL}")
                
    def download_and_install_update(self):
        """
        download and install the latest update.
        
        returns:
            bool: true if update was successful, false otherwise
        """
        if not self.release_info:
            return False
            
        try:
            # get download url for zip file
            zip_url = None
            for asset in self.release_info.get('assets', []):
                if asset['name'].endswith('.zip'):
                    zip_url = asset['browser_download_url']
                    break
                    
            # fall back to source code if no zip asset found
            if not zip_url:
                zip_url = self.release_info['zipball_url']
                
            print(f"{Fore.CYAN}downloading update...{Style.RESET_ALL}")
            
            # download the update
            response = requests.get(zip_url, stream=True, timeout=60)
            response.raise_for_status()
            
            # create a temporary directory for the download
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "update.zip")
                
                # save the zip file
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                # create the new directory for the update
                current_dir = Path(os.path.abspath(__file__)).parent
                parent_dir = current_dir.parent
                new_dir_name = f"{self.repo_name}-{self.release_info['tag_name'].lstrip('v')}"
                new_dir = os.path.join(parent_dir, new_dir_name)
                
                # extract the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # get the root directory in the zip
                    root_dir = zip_ref.namelist()[0].split('/')[0]
                    zip_ref.extractall(temp_dir)
                    
                    # move files to the new directory
                    extracted_dir = os.path.join(temp_dir, root_dir)
                    if os.path.exists(new_dir):
                        shutil.rmtree(new_dir)
                    shutil.copytree(extracted_dir, new_dir)
                    
            print(f"{Fore.GREEN}update downloaded successfully to: {new_dir}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}starting new version...{Style.RESET_ALL}")
            
            # launch the new version
            new_main_py = os.path.join(new_dir, "main.py")
            subprocess.Popen([sys.executable, new_main_py])
            
            # exit the current instance
            sys.exit(0)
            
        except Exception as e:
            print(f"{Fore.RED}error during update: {e}{Style.RESET_ALL}")
            input("press enter to exit...")
            return False