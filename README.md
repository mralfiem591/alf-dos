# ALF-DOS Project

ALF-DOS is a command execution system that allows users to run predefined commands through a simple interface. Each command is defined in a separate JSON file, making it easy to add or modify commands without changing the core system.

> *"The modular OS to rule them all"*

## Project Structure

```plaintext
ALF-DOS
├── Commands
│   ├── template.txt
│   ├── command1.json
│   ├── command2.json
│   └── command3.json
├── Paks
│   ├── pak1.json
│   ├── pak2.json
│   ├── pak3.json
│   └── pak4.json
├── main.py
├── README.md
├── config.json
├── .gitignore
├── changelog.txt
└── requirements.txt
```

## Getting Started

To set up and run the ALF-DOS system, follow these steps:

**PLEASE NOTE: Only cd and cmdpak are available right after install. Other commands must be downloaded via CMDPAK. Also note that the dependencies of a PAK may be wrong. Please check the PAK file, as it contains all the commands.**

1. **Download**:
   Download ALF-DOS-installer to your main system.

2. **Run the Installer**
   Execute the main installer:

   ```bash
   python ALF-DOS-installer
   ```

3. **Install Dependencies**:
   If there are any dependencies required for the main project, install them using:

   ```bash
   pip install -r requirements.txt
   ```

   Please note some Paks may have dependencies. You will be notified at Pak install.

4. **Run the System**:
   Execute the main program:

   ```bash
   python main.py
   ```

   You will get an output like this if it worked:

   ```bash
   ALF-DOS Command Line Interface v{Version}
   Type 'help' help finding commands, 'exit' to exit, or a command to execute.

   $ {Your ALF-DOS Directory} >
   ```

## Commands

The following commands are available in the ALF-DOS system:

- **cd**: Lets you open a directory to run commands from. Usage: cd {dir}
- **readme**: Open this file
- **cmdpak-read**: Lets you download a CMDPAK. Usage: cmdpak-read {cmdpak JSON}
- **cmdpak-one**: Same as cmdpak-read but for 1 command only.
- **cmdpak-all**: Download all paks in one directory.
- **cmdpak-refresh**: Refresh all paks in the "Paks" directory. Useful for if you are not interested in an advanced install.
- **cmdpak-dep**: Automatically download required dependencies for all Paks.
- **cmdpak-grab**: Clones all Paks from your current cded directory into your installation.
- **pak-rm**: Delete a Pak.
- **gitpakget**: Download a GitHub Pak.
- **gitpaklist**: List all GitHub paks.
- **gitpakall**: Download all GitHub paks.
- **github-repo**: Open the GitHub repository
- **update**: Updates ALF-DOS.
- **update-changelog**: Open update changelog. (v0.15.5+ only)
- **reboot**: Reboots ALF-DOS.
- **setup**: Open setup.
- **theme-refresh**: Refresh theme.json (More details soon)
- **pak-details**: Find details on GitHub for a Pak
- **pak-search**: Search for a Pak on GitHub
Other commands can be downloaded from CMDPAKs.

Each command can be executed by invoking its name in the ALF-DOS interface.

## Custom Themes

ALF-DOS supports custom themes. To do this, create a themes.json file in your ALF-DOS directory and put the theme data in it using ANSI escape codes. for example:

```bash
{
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "BACKGROUND_RED": "\033[41m",
    "BACKGROUND_GREEN": "\033[42m",
    "BACKGROUND_YELLOW": "\033[43m",
    "BACKGROUND_BLUE": "\033[44m",
    "BACKGROUND_MAGENTA": "\033[45m",
    "BACKGROUND_CYAN": "\033[46m",
    "BACKGROUND_WHITE": "\033[47m"
}
```

This will be loaded at startup and when you run

```bash
theme-refresh
```

## Adding New Commands

To add a new command, create a new JSON file in the `Commands` folder with the following structure:

```json
{
    "name": "new_command",
    "description": "Description of the new command.",
    "code": "print('Hello from new_command!')"
}
```

Make sure to replace `new_command`, the description, and the code with your desired values.
