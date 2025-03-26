import os
import json
import time
import sys
import subprocess
import pkg_resources
import shutil
import requests
from packaging import version as packaging_version
import random

CONFIG_FILE = "config.json"
version = "0.18.4"
build = "beta"
count_lines = 0

def gitpakall(script_dir):

    # URL for the root directory of the repository
    url = "https://api.github.com/repos/mralfiem591/alf-dos-paks/contents"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            paks = response.json()
            pak_names = [pak['name'] for pak in paks if pak['name'].endswith('PAK.json')]
            if pak_names:
                print("Downloading available PAKs:")
                for pak_name in pak_names:
                    pak_url = f"https://raw.githubusercontent.com/mralfiem591/alf-dos-paks/main/{pak_name}"
                    pak_response = requests.get(pak_url)
                    if pak_response.status_code == 200:
                        pak_content = pak_response.text
                        paks_dir = os.path.join(script_dir, "Paks")
                        os.makedirs(paks_dir, exist_ok=True)
                        pak_path = os.path.join(paks_dir, pak_name)
                        with open(pak_path, 'w', encoding='utf-8') as file:
                            file.write(pak_content)
                        print(f"Downloaded: {pak_name}")
                    else:
                        print(f"Failed to download {pak_name}. Status code: {pak_response.status_code}")
            else:
                print("No PAKs found in the repository.")
        else:
            print(f"Failed to list PAKs. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while downloading PAKs: {e}")

def check_updates(current_version, system):
    url = "https://raw.githubusercontent.com/mralfiem591/alf-dos/main/version.txt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
                latest_version = response.text.strip()
                if packaging_version.parse(latest_version) > packaging_version.parse(current_version):
                    if not system:
                        return f"{Colours.BOLD}{Colours.YELLOW}ALF-DOS v{latest_version} is available. Run 'update' to update.{Colours.RESET}"
                    else:
                        return True
                elif packaging_version.parse(latest_version) < packaging_version.parse(current_version):
                    if not system:
                        return f"{Colours.BOLD}ALF-DOS v{current_version} is {Colours.RED}past{Colours.RESET}{Colours.BOLD} the latest version. {Colours.UNDERLINE}This is a development build.{Colours.RESET}"
                    else:
                        return False
                else:
                    if not system:
                        return f"{Colours.BOLD}{Colours.GREEN}ALF-DOS is up to date.{Colours.RESET}"
                    else:
                        return False
        else:
            return "Failed to check for updates."
    except Exception as e:
         return f"An error occurred finding updates: {e}"
    
def view_pak_details(pak_name):
    url = f"https://raw.githubusercontent.com/mralfiem591/alf-dos-paks/main/{pak_name}.json"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            pak_details = json.loads(response.text)
            print(f"Details for {pak_name}:")
            print(json.dumps(pak_details, indent=4))
        else:
            print(f"Failed to fetch details for {pak_name}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching PAK details: {e}")

def search_paks(keyword):
    url = "https://api.github.com/repos/mralfiem591/alf-dos-paks/contents"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            paks = response.json()
            matching_paks = [pak['name'] for pak in paks if keyword.lower() in pak['name'].lower()]
            if matching_paks:
                print("Matching PAKs:")
                for pak in matching_paks:
                    print(pak.replace("PAK.json", ""))
            else:
                print("No matching PAKs found.")
        else:
            print(f"Failed to search PAKs. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while searching for PAKs: {e}")

def update(script_dir):
    repo_url = "https://api.github.com/repos/mralfiem591/alf-dos/contents"
    exclude_files = ["key.env", "config.json", "version.txt", "theme.json", "template.json"]
    exclude_dirs = ["Commands", "Paks"]

    try:
        response = requests.get(repo_url)
        if response.status_code == 200:
            files = response.json()
            for file in files:
                file_path = file['path']
                if file_path in exclude_files or any(file_path.startswith(dir) for dir in exclude_dirs):
                    continue

                file_url = file['download_url']
                if file_url:
                    file_response = requests.get(file_url)
                    if file_response.status_code == 200:
                        local_path = os.path.join(script_dir, file_path)
                        os.makedirs(os.path.dirname(local_path), exist_ok=True)
                        with open(local_path, 'w', encoding='utf-8') as local_file:
                            local_file.write(file_response.text)
                        print(f"Updated {file_path}")
                    else:
                        print(f"Failed to download {file_path}. Status code: {file_response.status_code}")
            # Fetch the latest changelog.txt
            changelog_url = "https://raw.githubusercontent.com/mralfiem591/alf-dos/main/changelog.txt"
            changelog_response = requests.get(changelog_url)
            if changelog_response.status_code == 200:
                changelog_path = os.path.join(script_dir, "changelog.txt")
                with open(changelog_path, 'w', encoding='utf-8') as changelog_file:
                    changelog_file.write(changelog_response.text)
                print("Updated changelog.txt")
            else:
                print("Failed to download changelog.txt. Status code:", changelog_response.status_code)
            print("Update successful. Please restart the script.")
            update_changelog(script_dir)
            data_write("reboot_needed", True, script_dir)
        else:
            print("Failed to list repository contents.")
    except Exception as e:
        print(f"An error occurred during the update: {e}")
def pak_tree(script_dir):
    # Locate the Paks directory
    paks_dir = os.path.join(script_dir, "Paks")
    
    # Check if the Paks directory exists
    if not os.path.exists(paks_dir):
        print("Paks directory not found.")
        return
    
    # Build the dependency tree
    dependency_tree = {}
    
    for pak_file in os.listdir(paks_dir):
        if pak_file.endswith(".json"):
            pak_path = os.path.join(paks_dir, pak_file)
            with open(pak_path, "r") as file:
                try:
                    pak_data = json.load(file)
                    pak_name = pak_file[:-5]  # Remove .json extension
                    dependencies = pak_data.get("dependencies", [])
                    dependency_tree[pak_name] = dependencies
                except json.JSONDecodeError:
                    print(f"Error parsing {pak_file}")
    
    # Recursive function to print the tree
    def print_tree(pak_name, indent=""):
        print(f"{indent}- {pak_name}")
        for dependency in dependency_tree.get(pak_name, []):
            print_tree(dependency, indent + "  ")
    
    # Print the tree for all top-level Paks
    print("Pak Dependency Tree:")
    for pak_name in dependency_tree:
        if not any(pak_name in dependencies for dependencies in dependency_tree.values()):
            print_tree(pak_name)
def count_lines(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for line in file)
    
def clear_screen():
    # Clear the console screen
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Unix-based systems
        os.system('clear')

def update_changelog(script_dir):
    changelog_path = os.path.join(script_dir, "changelog.txt")
    try:
        with open(changelog_path, 'r', encoding='utf-8') as file:
            print(file.read())
    except FileNotFoundError:
        print("changelog.txt file not found.")

def load_command(command_name, script_dir):
    # Check for command in the current directory
    command_file_path = os.path.join(os.getcwd(), "Commands", f"{command_name}.json")
    if os.path.exists(command_file_path):
        with open(command_file_path, 'r') as file:
            return json.load(file)
    
    # Check for command in the script directory
    command_file_path = os.path.join(script_dir, "Commands", f"{command_name}.json")
    if os.path.exists(command_file_path):
        with open(command_file_path, 'r') as file:
            return json.load(file)
    
    return None

def execute_command(command):
    exec(command['code'])

def display_requirements_and_dependencies(cmdpak):
    requirements = cmdpak.get("requirements", "None")
    dependencies = cmdpak.get("dependencies", [])
    print(f"Requirements: {requirements}")
    print(f"Dependencies: {', '.join(dependencies)}")

def create_command_file(command, script_dir):
    command_name = command["name"]
    command_file_path = os.path.join(script_dir, "Commands", f"{command_name}.json")
    with open(command_file_path, 'w') as command_file:
        json.dump(command, command_file, indent=4)
    print(f"Created command file: {command_file_path}")

def read_cmdpak(file_path, script_dir):
    # Read the cmdpak file and create individual command JSON files
    with open(file_path, 'r') as file:
        cmdpak = json.load(file)
        commands = cmdpak.get("commands", [])
        command_names = [command["name"] for command in commands]
        command_count = len(commands)
        
        # Display requirements and dependencies
        display_requirements_and_dependencies(cmdpak)
        
        # Prompt for confirmation
        print(f"Are you sure you would like to download {command_count} commands?")
        print(f"Commands in this CMDPAK: {', '.join(command_names)}")
        confirmation = input("Type 'yes' to confirm: ").strip().lower()
        
        if confirmation == 'yes':
            for command in commands:
                create_command_file(command, script_dir)
        else:
            print("Operation cancelled.")

def read_cmdpak_one(file_path, script_dir):
    # Read the cmdpak file and create a single command JSON file
    with open(file_path, 'r') as file:
        cmdpak = json.load(file)
        commands = cmdpak.get("commands", [])
        command_names = [command["name"] for command in commands]
        
        # Display requirements and dependencies
        display_requirements_and_dependencies(cmdpak)
        
        # Prompt for command selection
        print(f"Commands in this CMDPAK: {', '.join(command_names)}")
        selected_command_name = input("Enter the name of the command you want to download: ").strip()
        
        # Find the selected command
        selected_command = next((command for command in commands if command["name"] == selected_command_name), None)
        
        if selected_command:
            # Prompt for confirmation
            print(f"Are you sure you would like to download the command '{selected_command_name}'?")
            confirmation = input("Type 'yes' to confirm: ").strip().lower()
            
            if confirmation == 'yes':
                create_command_file(selected_command, script_dir)
            else:
                print("Operation cancelled.")
        else:
            print(f"Command '{selected_command_name}' not found in the CMDPAK.")

def read_all_cmdpaks(directory, script_dir):
    # Read all cmdpak files in the specified directory and create individual command JSON files
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                cmdpak = json.load(file)
                commands = cmdpak.get("commands", [])
                command_names = [command["name"] for command in commands]
                command_count = len(commands)
                
                # Display requirements and dependencies
                display_requirements_and_dependencies(cmdpak)
                
                # Prompt for confirmation
                print(f"Are you sure you would like to download {command_count} commands from {filename}?")
                print(f"Commands in this CMDPAK: {', '.join(command_names)}")
                confirmation = input("Type 'yes' to confirm: ").strip().lower()
                
                if confirmation == 'yes':
                    for command in commands:
                        create_command_file(command, script_dir)
                else:
                    print(f"Operation cancelled for {filename}.")

def cmdpak_refresh(script_dir):
    # Read all cmdpak files in the "Paks" directory and create individual command JSON files without confirmation
    paks_directory = os.path.join(script_dir, "Paks")
    all_dependencies = set()
    for filename in os.listdir(paks_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(paks_directory, filename)
            with open(file_path, 'r') as file:
                cmdpak = json.load(file)
                commands = cmdpak.get("commands", [])
                dependencies = cmdpak.get("dependencies", [])
                all_dependencies.update(dependencies)
                for command in commands:
                    create_command_file(command, script_dir)
    print(f"Dependencies: {', '.join(all_dependencies)}")
    print("Success!")

def cmdpak_dep(script_dir):
    # Create a paks-requirements.txt file with all dependencies for all PAKs in the "Paks" folder
    paks_directory = os.path.join(script_dir, "Paks")
    all_dependencies = set()
    built_in_modules = {
        'sys', 'os', 'json', 'time', 'subprocess', 'platform', 'shutil', 'zipfile', 
        'hashlib', 'base64', 'xml.dom.minidom', 'csv', 'socket', 're', 'datetime'
    }
    for filename in os.listdir(paks_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(paks_directory, filename)
            with open(file_path, 'r') as file:
                cmdpak = json.load(file)
                dependencies = cmdpak.get("dependencies", [])
                all_dependencies.update(dependencies)
    # Filter out built-in modules
    filtered_dependencies = [dep for dep in all_dependencies if dep not in built_in_modules]
    requirements_file_path = os.path.join(paks_directory, "paks-requirements.txt")
    with open(requirements_file_path, 'w') as requirements_file:
        for dependency in filtered_dependencies:
            requirements_file.write(dependency + '\n')
    print(f"Created {requirements_file_path}")
    
    # Automatically install the dependencies using pip
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', requirements_file_path], check=True)
        print("Dependencies installed successfully.")
        os.remove(requirements_file_path)
        print(f"Deleted {requirements_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
        print(f"Please manually install the dependencies listed in {requirements_file_path}")

def read_readme(script_dir):
    readme_path = os.path.join(script_dir, "README.md")
    try:
        with open(readme_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("README.md file not found.")

def data_read(value_name, script_dir):
    config_file_path = os.path.join(script_dir, "config.json")
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            config = json.load(file)
            return config.get(value_name, None)
    return None

def data_write(value_name, value, script_dir):
    config_file_path = os.path.join(script_dir, "config.json")
    config = {}
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as file:
            config = json.load(file)
    config[value_name] = value
    with open(config_file_path, 'w') as file:
        json.dump(config, file, indent=4)

script_dir = os.path.dirname(os.path.abspath(__file__))
class Colours:
    if data_read("theme", script_dir) is None or data_read("theme", script_dir) == "default":
        RESET = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
    elif data_read("theme", script_dir) == "dark":
        RESET = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        BLUE = "\033[34m"
        MAGENTA = "\033[35m"
        CYAN = "\033[36m"
        WHITE = "\033[37m"
    elif data_read("theme", script_dir) == "neon":
        RESET = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
    elif data_read("theme", script_dir) == "futuristic":
        RESET = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        RED = "\033[38;5;197m"
        GREEN = "\033[38;5;40m"
        YELLOW = "\033[38;5;226m"
        BLUE = "\033[38;5;12m"
        MAGENTA = "\033[38;5;201m"
        CYAN = "\033[38;5;51m"
        WHITE = "\033[38;5;255m"


def settings(script_dir):
    while True:
        clear_screen()
        print("SETTINGS")
        print("Please check back later for updates.")
        print("Options:")
        print("1. Open README")
        print("2. Change Directory")
        print("3. Open First Setup")
        print("4. Run Automated PAK Install")
        print("5. Run Automated Dependency Install")
        print("6. Run Automated PAK and Dependency Install")
        print("7. Update ALF-DOS")
        print("8. Choose Theme")
        print("0. Exit Settings")
        
        choice = input("Select an option: ").strip()
        if choice == '0':
            break
        if choice == '1':
            read_readme(script_dir)
        elif choice == '2':
            new_dir = input("Enter the new directory: ")
            try:
                os.chdir(new_dir)
                print("Directory changed successfully.")
            except FileNotFoundError:
                print("Directory not found.")
        elif choice == '3':
            data_write("first_run", True, script_dir)
            data_write("reboot_needed", True, script_dir)
        elif choice == '4':
            cmdpak_refresh(script_dir)
        elif choice == '5':
            cmdpak_dep(script_dir)
        elif choice == '6':
            cmdpak_refresh(script_dir)
            cmdpak_dep(script_dir)
        elif choice == '7':
            if check_updates(version, True):
                update(script_dir)
            else:
                print("No updates available.")
        elif choice == '8':
            print("Choose a theme:")
            print("1. Default")
            print("2. Dark")
            print("3. Neon")
            print("4. Futuristic")
            theme_choice = input("Select a theme: ").strip()
            if theme_choice == '1':
                data_write("theme", "default", script_dir)
            elif theme_choice == '2':
                data_write("theme", "dark", script_dir)
            elif theme_choice == '3':
                data_write("theme", "neon", script_dir)
            elif theme_choice == '4':
                data_write("theme", "futuristic", script_dir)
        else:
            print("Invalid option. Please try again.")
        
        input("Press Enter to continue...")

def gitpaklist():

    # URL for the root directory of the repository
    url = "https://api.github.com/repos/mralfiem591/alf-dos-paks/contents"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            paks = response.json()
            # Filter and list only PAK names
            pak_names = sorted([pak['name'] for pak in paks if pak['name'].endswith('PAK.json')])
            if pak_names:
                print("Available PAKs:")
                for pak_name in pak_names:
                    print(pak_name.replace("PAK.json", ""))  # Remove the ".PAK.json" extension for cleaner output
            else:
                print("No PAKs found in the repository.")
        else:
            print(f"Failed to list PAKs. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred while listing PAKs: {e}")

def gitpakget(script_dir):
    pak_name = input("Enter the name of the PAK to download: ").strip()
    if not pak_name.endswith("PAK.json"):
        pak_name += "PAK.json"

    # Correct URL for the root directory of the repository
    url = f"https://raw.githubusercontent.com/mralfiem591/alf-dos-paks/main/{pak_name}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pak_content = response.text
            paks_dir = os.path.join(script_dir, "Paks")
            os.makedirs(paks_dir, exist_ok=True)
            pak_path = os.path.join(paks_dir, pak_name)
            with open(pak_path, 'w', encoding='utf-8') as file:
                file.write(pak_content)
            print(f"Downloaded: {pak_name}")
        else:
            print(f"Failed to download {pak_name}. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    except Exception as e:
        print(f"An error occurred during the download: {e}")

def pak_rm(script_dir):
    pak_name = input("Enter the name of the PAK to remove (without .json extension): ").strip()
    if not pak_name.endswith("PAK.json"):
        pak_name += "PAK.json"
    paks_dir = os.path.join(script_dir, "Paks")
    pak_path = os.path.join(paks_dir, pak_name)
    if os.path.exists(pak_path):
        os.remove(pak_path)
        print(f"Removed {pak_name} from the Paks folder.")
    else:
        print(f"PAK file {pak_name} not found in the Paks folder.")

def checkpaks(script_dir):
    paks_dir = os.path.join(script_dir, "Paks")
    return os.path.exists(paks_dir)

def cmdpak_grab(script_dir):
    current_dir = os.getcwd()
    paks_dir = os.path.join(script_dir, "Paks")
    
    if not os.path.exists(paks_dir):
        os.makedirs(paks_dir, exist_ok=True)
    
    for filename in os.listdir(current_dir):
        if filename.endswith(".json"):
            source_path = os.path.join(current_dir, filename)
            destination_path = os.path.join(paks_dir, filename)
            shutil.copy(source_path, destination_path)
            print(f"Copied {filename} to Paks folder.")
    print("All JSON files have been copied to the Paks folder.")

def main():
    update_availible = False
    clear_screen()
    # Set the current working directory to the directory containing main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    data_write("reboot_needed", False, script_dir)
    if data_read("debug_mode", script_dir) is not True:
            if data_read("potential_issue", script_dir) is not None and data_read("potential_issue", script_dir):
                print("There was a problem loading ALF-DOS: Your config.json may be corrupt. It is HEAVILY reccomended to get the reapir utility from GitHub. ALF-DOS will now close.")
                exit()
    clear_screen()
    print(f"WELCOME TO {Colours.RED}A{Colours.GREEN}L{Colours.YELLOW}F{Colours.BLUE}-{Colours.MAGENTA}D{Colours.CYAN}O{Colours.WHITE}S{Colours.RESET}")
    time.sleep(1)
    print("INITIALIZING...")
    time.sleep(3)
    print("SETTING DIR...")
    time.sleep(2)
    print("READY")
    time.sleep(1)
    if data_read("first_run", script_dir) is None or data_read("first_run", script_dir):
        data_write("first_run", False, script_dir)
        data_write("potential_issue", False, script_dir)
        data_write("debug_mode", False, script_dir)
        data_write("theme", "default", script_dir)
        print("Preparing Setup...")
        print("Prepared Commands Folder")
        time.sleep(2)
        print("Prepared Paks Folder")
        time.sleep(2)
        print("Prepared Config File")
        time.sleep(2)
        print("Prepared ALF-DOS-PACKAGE-MANAGER V1.13")
        time.sleep(2)
        print("Prepared ALF-DOS-DEPENDENCY-MANAGER V1.2")
        print("Prepared Setup")
        print(f"Welcome to {Colours.RED}A{Colours.GREEN}L{Colours.YELLOW}F{Colours.BLUE}-{Colours.MAGENTA}D{Colours.CYAN}O{Colours.WHITE}S{Colours.RESET}! This is your first time running the program.")
        print("Please follow the setup and you will be ready in no time!")
        time.sleep(3)
        setupmode = input("Would you like to run (a)utomated setup, (m)anual setup, (r)epair previous install or (s)kip? (a/m/r/s)")
        if setupmode == "a":
            if os.path.exists(os.path.join(script_dir, "Commands")):
                shutil.rmtree(os.path.join(script_dir, "Commands"))
            print("Running automated setup...")
            print("Setting up Paks folder...")
            os.makedirs("Paks", exist_ok=True)
            print("Setting up Commands folder...")
            os.makedirs("Commands", exist_ok=True)
            print("Scanning for built-in Paks...")
            cmdpak_refresh(script_dir)
            print("Installing dependencies...")
            cmdpak_dep(script_dir)
            time.sleep(2)
            print("Setup complete!")
            time.sleep(1)
        elif setupmode == "m":
            if os.path.exists(os.path.join(script_dir, "Commands")):
                shutil.rmtree(os.path.join(script_dir, "Commands"))
            print("Running manual setup...")
            print("Please follow the instructions to set up the program.")
            makepaks = input("Would you like to create a Paks folder? (y/n) (Heavily recommended)")
            if makepaks == "y":
                print("Setting up Paks folder...")
                os.makedirs("Paks", exist_ok=True)
            makecmds = input("Would you like to create a Commands folder? (y/n) (Heavily recommended) (Required for Paks)")
            if makecmds == "y":
                print("Setting up Commands folder...")
                os.makedirs("Commands", exist_ok=True)
            getdependencies = input("Would you like to install dependencies for built-in Paks? (y/n) (Heavily recommended)")
            if getdependencies == "y":
                print("Installing dependencies...")
                cmdpak_dep(script_dir)
                time.sleep(2)
            getpaks = input("Would you like to scan for built-in Paks? (y/n) (Heavily recommended)")
            if getpaks == "y":
                print("Scanning for built-in Paks...")
                cmdpak_refresh(script_dir)
                time.sleep(2)
            print("Setup complete!")
            time.sleep(1)
        elif setupmode == "s":
            if os.path.exists(os.path.join(script_dir, "Commands")):
                shutil.rmtree(os.path.join(script_dir, "Commands"))
            data_write("potential_issue", True, script_dir)
            print(f"{Colours.RED}{Colours.BOLD}{Colours.UNDERLINE}You decided to skip setup. Please note that due to this there is not a 'Commands' folder and can cause MAJOR corruption. Please run 'setup' to redo setup or 'reboot' to attempt to recover the commands folder. Skipping the setup is for debug only.{Colours.RESET}")
            pass
        elif setupmode == "r":
            corrupted_fix(script_dir)
            return
        elif setupmode == "debug":
            data_write("debug_mode", True, script_dir)
            print("DEBUG MODE")
            print("This does the same as skip, but disables alerts and repair.")
            print("To return the system to normal, run 'setup'")
            input("Press Enter to continue to debug mode...")
        else:
            print("Invalid option. Assuming Automated Setup...")
            print("Running automated setup...")
            print("Setting up Paks folder...")
            os.makedirs("Paks", exist_ok=True)
            print("Setting up Commands folder...")
            os.makedirs("Commands", exist_ok=True)
            print("Scanning for built-in Paks...")
            cmdpak_refresh(script_dir)
            print("Installing dependencies...")
            cmdpak_dep(script_dir)
            time.sleep(2)
            print("Setup complete!")
            time.sleep(1)
        data_write("first_run", False, script_dir)
        if input("Would you like to read the README? (y/n)") == "y":
            read_readme(script_dir)
            input("Press Enter to continue")
        if checkpaks(script_dir):
            if input("Would you like to install all available PAKs? (y/n)") == "y":
                gitpakall(script_dir)
    while True:
        clear_screen()
        if data_read("debug_mode", script_dir):
            print(f"{Colours.RED}{Colours.BOLD}DEBUG MODE ENABLED. REPAIRS DISABLED. RUN SETUP TO DISABLE DEBUG.{Colours.RESET}")
        if data_read("reboot_needed", script_dir) is not None and data_read("reboot_needed", script_dir):
            data_write("reboot_needed", False, script_dir)
            print("Reboot needed. Please run 'reboot'.")
        if data_read("potential_issue", script_dir) is not None and data_read("potential_issue", script_dir):
            print(f"{Colours.RED}{Colours.BOLD}{Colours.UNDERLINE}WARNING: POTENTIAL ISSUE DETECTED. ALF-DOS may not function. Please run 'reboot' to automatically boot into repair mode. If the issue stays after repair, please run setup {Colours.BOLD}{Colours.UNDERLINE}IMMEDIATELY..{Colours.RESET}")
        print(f"{Colours.RED}A{Colours.GREEN}L{Colours.YELLOW}F{Colours.BLUE}-{Colours.MAGENTA}D{Colours.CYAN}O{Colours.WHITE}S{Colours.RESET} Command Line Interface v{version}")
        print(check_updates(version, False))
        print("Build: " + build)
        print("""Type 'help' help finding commands, 'exit' to exit, or a command to execute.
              """)
        command_name = input("$ " + os.getcwd() + " > ")
        if command_name.lower() == 'exit':
            break
        elif command_name.lower() == 'help':
            print("For help, run the following commands (In order):")
            print("  cd reset - Reset the current directory to the script directory")
            print("  cmd-list - List all available commands")
            print("  If you get an error from cmd-list, run the following command:")
            print("     cmdpak-one [path to cmdpak folder]/cmdmanagePAK.json, then enter cmd-list, and try cmd-list again")
            print("  desc, then command to enquire")
            print("  If you get an error from desc, run the following command:")
            print("     cmdpak-one [path to cmdpak folder]/essentialsPAK.json, then enter desc, and try desc again")
            print("")
            print("If you have a pak, run cmdpak-read [path to pak] to enable the pak")
            print("If you have a single command you want from a pak, run cmdpak-one [path to pak] then choose a command to enable that command")
            print("If you have a folder of paks, run cmdpak-all [path to folder] to enable all paks in the folder")
            print("If you want to refresh all paks in the 'Paks' folder, run cmdpak-refresh")
            print("If you want to create a requirements file for all paks in the 'Paks' folder, run cmdpak-dep")
            print("If you want to grab all JSON files in the current directory and copy them to the Paks folder, run cmdpak-grab")
            print("For more info, read the README.md file, OR to repoen this page, run help again")
        elif command_name.lower().startswith('cd '):
            new_dir = command_name[3:].strip()
            if new_dir == 'reset':
                os.chdir(script_dir)
                print("Waiting...")
                time.sleep(1)
            elif new_dir == 'back':
                os.chdir('..')
                print("Waiting...")
                time.sleep(1)
            else:
                try:
                    os.chdir(new_dir)
                except FileNotFoundError:
                    print(f"Directory '{new_dir}' not found.")
                print("Waiting...")
                time.sleep(1)
            continue
        elif command_name.lower() == 'reboot':
            print("Rebooting...")
            time.sleep(1)
            return
        elif command_name.lower() == 'setup':
            if input("Are you sure you want to run setup? (y/n)") == "y":
                data_write("first_run", True, script_dir)
                data_write("reboot_needed", True, script_dir)
            continue
        elif command_name.lower() == 'readme':
            read_readme(script_dir)
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'pak-rm':
            if checkpaks(script_dir):
                pak_rm(script_dir)
            else:
                print("Pak Directory Missing!")
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'gitpakall':
            if checkpaks(script_dir):
                gitpakall(script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == 'settings':
            settings(script_dir)
            input("Settings updated. Press Enter to continue...")
            continue
        elif command_name.lower().startswith('cmdpak-read '):
            if checkpaks(script_dir):
                file_path = command_name[12:].strip()
                read_cmdpak(file_path, script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower().startswith('cmdpak-one '):
            if checkpaks(script_dir):
                file_path = command_name[11:].strip()
                read_cmdpak_one(file_path, script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower().startswith('cmdpak-all '):
            if checkpaks(script_dir):
                directory = command_name[11:].strip()
                read_all_cmdpaks(directory, script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == 'cmdpak-refresh':
            if checkpaks(script_dir):
                cmdpak_refresh(script_dir)
            else:
                print("Pak Directory Missing!")
            input("Success! Press Enter to continue...")
            continue
        elif command_name.lower() == 'cmdpak-dep':
            if checkpaks(script_dir):
                cmdpak_dep(script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == 'cmdpak-grab':
            if checkpaks(script_dir):
                cmdpak_grab(script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == 'update':
            if check_updates(version, True):
                update(script_dir)
            else:
                print("No updates available.")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == 'gitpaklist':
            if checkpaks(script_dir):
                gitpaklist()
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == 'update-changelog':
            update_changelog(script_dir)
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'pak-details':
            view_pak_details(input("Enter the name of the PAK to view details: ").strip(), script_dir)
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'pak-search':
            search_paks(input("Enter the search term: ").strip(), script_dir)
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'gitpakget':
            if checkpaks(script_dir):
                gitpakget(script_dir)
            else:
                print("Pak Directory Missing!")
            input("Command finished. Press Enter to continue...")
            continue
        elif command_name.lower() == '42':
            print("Are YOU the meaning of Life, The Universe, And Everything?")
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == '7':
            print("Are YOU lucky?")
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'cmdpak-tree':
            pak_tree(script_dir)
            input("Press Enter to continue...")
            continue
        elif command_name.lower() == 'github-repo':
            print("https://github.com/mralfiem591/alf-dos")
            print("https://github.com/mralfiem591/alf-dos-paks")
            input("Press Enter to continue...")
        try:
            command = load_command(command_name, script_dir)
            if command:
                clear_screen()
                print(f"Executing {command['name']}: {command['description']}")
                execute_command(command)
            else:
                print(f"Command '{command_name}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        input("Command finished. Press Enter to continue...")

if __name__ == "__main__":
    clear_screen()
    if sys.version_info.major < 3:
        print("This script requires Python 3 or higher.")
        sys.exit(1)
    main()