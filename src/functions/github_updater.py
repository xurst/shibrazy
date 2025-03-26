# src/functions/github_updater.py
import os
import sys
import requests
import tempfile
import zipfile
import shutil
import re
from packaging import version
from colorama import Fore, Style

class GitHubUpdater:
    def __init__(self, repo_owner, repo_name, current_version):
        self.repo_owner = repo_owner
        self.repo_name = repo_name  # Using the parameter value directly
        self.current_version = current_version
        # FIX 1: Using the correct repo_name from parameters instead of hardcoded value
        self.api_base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.latest_version = None
        self.latest_release_url = None

    def check_for_update(self):
        """
        Check for updates by examining the source code directly instead of using releases.
        This fixes both bugs:
        1. Not using releases endpoint which gives 404
        2. Checking actual source code, not just comparing version numbers
        """
        try:
            # Get repository information to find the default branch
            repo_response = requests.get(self.api_base_url)
            if repo_response.status_code != 200:
                print(f"{Fore.RED}warning: could not check for updates: {repo_response.status_code} {repo_response.reason} for url: {self.api_base_url}{Style.RESET_ALL}")
                if repo_response.status_code == 404:
                    print(f"{Fore.YELLOW}hint: repository '{self.repo_name}' not found. check the repository name{Style.RESET_ALL}")
                return False
            
            repo_data = repo_response.json()
            default_branch = repo_data.get('default_branch', 'main')
            
            # Try to find constants.py in the repository
            constants_url = f"{self.api_base_url}/contents/src/core/constants.py?ref={default_branch}"
            constants_response = requests.get(constants_url)
            
            # FIX 2: Check the remote version directly from constants.py in the repository
            # This way, even if someone changes their local version number, we compare with the actual remote version
            if constants_response.status_code == 200:
                constants_data = constants_response.json()
                if constants_data.get('type') == 'file' and constants_data.get('name') == 'constants.py':
                    # Get the raw content
                    constants_content = requests.get(constants_data.get('download_url')).text
                    
                    # Extract SHIBRAZY_VERSION from remote constants.py
                    version_match = re.search(r'SHIBRAZY_VERSION\s*=\s*([0-9.]+)', constants_content)
                    if version_match:
                        remote_version = float(version_match.group(1))
                        
                        # Compare versions
                        if remote_version > self.current_version:
                            print(f"{Fore.GREEN}update available: v{remote_version} (current: v{self.current_version}){Style.RESET_ALL}")
                            self.latest_version = remote_version
                            self.latest_release_url = f"{self.api_base_url}/zipball/{default_branch}"
                            return True
                        else:
                            print(f"{Fore.GREEN}you're running the latest version (v{self.current_version}){Style.RESET_ALL}")
                            return False
            
            # If we couldn't find or parse constants.py, fall back to checking latest commit
            commits_url = f"{self.api_base_url}/commits/{default_branch}"
            commits_response = requests.get(commits_url)
            
            if commits_response.status_code == 200:
                commit_data = commits_response.json()
                latest_commit_sha = commit_data.get('sha')
                commit_date = commit_data.get('commit', {}).get('author', {}).get('date')
                
                if latest_commit_sha:
                    print(f"{Fore.YELLOW}couldn't determine version from source code. checking latest commit.{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}latest commit: {latest_commit_sha[:7]} on {commit_date}{Style.RESET_ALL}")
                    
                    # Additional security by suggesting update based on latest commit
                    print(f"{Fore.YELLOW}potentially new code available. update recommended.{Style.RESET_ALL}")
                    self.latest_release_url = f"{self.api_base_url}/zipball/{default_branch}"
                    return True
            
            print(f"{Fore.RED}could not check for updates. please check manually.{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}error checking for updates: {e}{Style.RESET_ALL}")
            return False

    def prompt_for_update(self):
        response = input(f"{Fore.YELLOW}would you like to update now? (y/n): {Style.RESET_ALL}").strip().lower()
        return response == 'y'

    def download_and_install_update(self):
        if not self.latest_release_url:
            print(f"{Fore.RED}no update information available{Style.RESET_ALL}")
            return False
        
        try:
            print(f"{Fore.CYAN}downloading update...{Style.RESET_ALL}")
            response = requests.get(self.latest_release_url, stream=True)
            
            if response.status_code != 200:
                print(f"{Fore.RED}failed to download update: {response.status_code} {response.reason}{Style.RESET_ALL}")
                return False
            
            # Save the downloaded file
            temp_dir = tempfile.mkdtemp()
            temp_zip = os.path.join(temp_dir, "update.zip")
            
            with open(temp_zip, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Extract the update
            print(f"{Fore.CYAN}extracting update...{Style.RESET_ALL}")
            with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the extracted directory (it usually has the commit hash in the name)
            extracted_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)) and d != "__MACOSX"]
            if not extracted_dirs:
                print(f"{Fore.RED}failed to find extracted update files{Style.RESET_ALL}")
                return False
            
            extracted_dir = os.path.join(temp_dir, extracted_dirs[0])
            
            # Install the update by copying files
            print(f"{Fore.CYAN}installing update...{Style.RESET_ALL}")
            app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Copy all files except certain directories/files
            exclude = {'.git', 'venv', '__pycache__', 'dist', 'temp_src'}
            for item in os.listdir(extracted_dir):
                if item in exclude:
                    continue
                
                src_path = os.path.join(extracted_dir, item)
                dst_path = os.path.join(app_dir, item)
                
                if os.path.isdir(src_path):
                    # Copy directory
                    if os.path.exists(dst_path):
                        shutil.rmtree(dst_path)
                    shutil.copytree(src_path, dst_path)
                else:
                    # Copy file
                    shutil.copy2(src_path, dst_path)
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            print(f"{Fore.GREEN}update installed successfully. please restart the application.{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}error installing update: {e}{Style.RESET_ALL}")
            return False