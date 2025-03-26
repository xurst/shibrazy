import os
import sys
import shutil
import subprocess
from pathlib import Path

def obfuscate():
    """Obfuscate source code and prepare for GitHub push"""
    # Clean previous build
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Create output directory
    os.makedirs("dist", exist_ok=True)
    
    # Get list of Python files to obfuscate
    files_to_obfuscate = []
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py") and file != "constants.py":
                files_to_obfuscate.append(os.path.join(root, file))
    
    # Obfuscate each file
    for file in files_to_obfuscate:
        # Determine output path
        rel_path = os.path.relpath(file, "src")
        output_dir = os.path.join("dist", os.path.dirname(rel_path))
        os.makedirs(output_dir, exist_ok=True)
        
        # Run PyArmor
        cmd = [
            "pyarmor", "obfuscate",
            "--exact",           # Obfuscate exactly this file
            "--output", output_dir,
            file
        ]
        subprocess.run(cmd, check=True)
    
    # Copy non-Python files and constants.py
    for root, _, files in os.walk("src"):
        for file in files:
            if not file.endswith(".py") or file == "constants.py":
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, "src")
                dst_file = os.path.join("dist", rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
    
    print("obfuscation complete. files ready in 'dist' directory.")
    print("note: constants.py was copied as-is (not obfuscated)")

if __name__ == "__main__":
    obfuscate()