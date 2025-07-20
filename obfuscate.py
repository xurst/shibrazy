import os
import shutil
import subprocess
import glob
import re

def obfuscate():
    if os.path.exists("dist"):
        shutil.rmtree("dist")

    temp_src = "temp_src"
    if os.path.exists(temp_src):
        shutil.rmtree(temp_src)
    os.makedirs(temp_src, exist_ok=True)
    
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith(".py") and file != ".env":

                rel_dir = os.path.relpath(root, "src")
                target_dir = os.path.join(temp_src, rel_dir)
                os.makedirs(target_dir, exist_ok=True)
                
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)

                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                modified_content = re.sub(r'from src\.', 'from ', content)
                modified_content = re.sub(r'import src\.', 'import ', modified_content)
                if file == "constants.py" or file == "template_constants.py":
                    modified_content = re.sub(
                        r'os\.path\.join\(os\.path\.dirname\(os\.path\.dirname\(os\.path\.dirname\(__file__\)\)\)\s*,\s*"sounds"\s*,\s*"keyword_find"\)',
                        'os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds", "keyword_find")',
                        modified_content
                    )

                with open(dst_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
    
    os.makedirs("dist", exist_ok=True)
    files_to_obfuscate = []
    for root, _, files in os.walk(temp_src):
        for file in files:
            if file.endswith(".py") and file != "constants.py" and file != "template_constants.py":
                files_to_obfuscate.append(os.path.join(root, file))

    for file in files_to_obfuscate:
        rel_path = os.path.relpath(file, temp_src)
        output_dir = os.path.join("dist", os.path.dirname(rel_path))
        os.makedirs(output_dir, exist_ok=True)
        
        cmd = [
            "pyarmor", "gen",
            "--output", output_dir,
            file
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"error obfuscating {file}: {e}")

    for root, _, files in os.walk(temp_src):
        for file in files:
            if file == "template_constants.py":
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, temp_src)
                dst_dir = os.path.join("dist", os.path.dirname(rel_path))
                dst_file = os.path.join(dst_dir, "constants.py")
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"template_constants.py copied and renamed to constants.py in {dst_dir}")
            elif file == "constants.py" and not any(f == "template_constants.py" for f in os.listdir(root)):
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, temp_src)
                dst_file = os.path.join("dist", rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
                print(f"constants.py copied to {os.path.dirname(dst_file)}")
    for root, _, files in os.walk("src"):
        for file in files:
            if not file.endswith(".py"):
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, "src")
                dst_file = os.path.join("dist", rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)
    if os.path.exists("main.py"):
        with open("main.py", 'r', encoding='utf-8') as f:
            content = f.read()

        modified_content = re.sub(r'from src\.', 'from ', content)
        modified_content = re.sub(r'import src\.', 'import ', modified_content)

        with open(os.path.join("dist", "main.py"), 'w', encoding='utf-8') as f:
            f.write(modified_content)
    
    if os.path.exists("bot_state.py"):
        shutil.copy2("bot_state.py", os.path.join("dist", "bot_state.py"))
    
    if os.path.exists("sounds"):
        os.makedirs(os.path.join("dist", "sounds"), exist_ok=True)
        for root, dirs, files in os.walk("sounds"):
            rel_dir = os.path.relpath(root, ".")
            target_dir = os.path.join("dist", rel_dir)
            os.makedirs(target_dir, exist_ok=True)
            
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
        
        keyword_find_dir = os.path.join("dist", "sounds", "keyword_find")
        if os.path.exists(keyword_find_dir):
            shutil.rmtree(keyword_find_dir)
            print("keyword_find directory removed from dist/sounds")
        
        readme_path = os.path.join("dist", "sounds", "README.txt")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("no default sounds")
        print("'no default sounds' message created in dist/sounds")
        
        print("sounds directory copied to dist folder")
    else:
        print("warning: sounds directory not found in project root")
    
    if os.path.exists("requirements.txt"):
        shutil.copy2("requirements.txt", os.path.join("dist", "requirements.txt"))
        print("requirements.txt copied to dist folder")
    else:
        print("note: requirements.txt not found in project root")
    
    if os.path.exists(temp_src):
        shutil.rmtree(temp_src)
    
    for extra_dir in glob.glob("dist-*"):
        if os.path.isdir(extra_dir):
            shutil.rmtree(extra_dir)
    
    print("obfuscation complete. files ready in 'dist' directory.")
    print("note: template_constants.py was copied as constants.py but not obfuscated")
    print("note: import paths have been adjusted to work when dist becomes the root")
    print("note: sounds directory have been copied to dist")

if __name__ == "__main__":
    obfuscate()