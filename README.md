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
   Download ALF-DOS-installer.portable.py to your main system.

2. **Run the Installer**:
   Execute the main installer:

   ```bash
   python ALF-DOS-installer
   ```

3. **CD into main directory**:
   CD into main directory:

   ```bash
   cd ALF-DOS
   ```

4. **Install Dependencies**:
   If there are any dependencies required for the main project, install them using:

   ```bash
   pip install -r requirements.txt
   ```

   Please note some Paks may have dependencies. You will be notified at Pak install.

5. **Run the System**:
   Execute the main program:

   ```bash
   python main.py
   ```

   You will get an output like this if it worked:

   ```bash
   ALF-DOS Command Line Interface v{version}-{build}
   **ALF-DOS is up to date.**
   Type 'help' for help finding commands, 'exit' to exit, or a command to execute.

   $ {your ALF-DOS directory} >
   ```

## Supported Versions

* `✅` - Supported  
* `❌` - Not Supported
* `=↑` - Greater than or equal to
* `=↓` - Lower than or equal to
* `x` - Anything

| Version | Build | Supported |
|:--------|:-----:|:---------:|
| 0.x.x   | beta  | ✅ |
| 0.10.x=↑| alpha | ✅ |
| 0.9.x=↓ | alpha | ❌ |

**If your version is unsupported, please update ALF-DOS. Unsupported versions no longer get security updates.**
You can check your version from the ALF-DOS home screen. It'll look something like this:
```bash
ALF-DOS Command Line Interface v0.10.2-alpha  # Example of a supported version
```
```bash
ALF-DOS Command Line Interface v0.8.1-alpha  # Example of a unsupported version
```

## Commands

The following commands are available in the ALF-DOS system:

- **cd**: Lets you open a directory to run commands from. Usage: cd {dir}
- **readme**: Open this file.
- **cmdpak-read**: Lets you download a CMDPAK. Usage: cmdpak-read {cmdpak JSON}
- **cmdpak-one**: Same as cmdpak-read but for 1 command only.
- **cmdpak-all**: Download all paks in one directory.
- **cmdpak-refresh**: Refresh all paks in the "Paks" directory. Useful for if you are not interested in an advanced install.
- **cmdpak-dep**: Automatically download required dependencies for all Paks.
- **cmdpak-grab**: Clones all Paks from your current cded directory into your installation.
- **cmdpak-tree**: Shows you a dependency tree for all Paks.
- **pak-rm**: Delete a Pak.
- **gitpakget**: Download a GitHub Pak.
- **gitpaklist**: List all GitHub paks.
- **gitpakall**: Download all GitHub paks.
- **github-repo**: Open the GitHub repository
- **update**: Updates ALF-DOS.
- **update-changelog**: Open update changelog. (v0.15.5+ only)
- **reboot**: Reboots ALF-DOS.
- **setup**: Open setup.
- **pak-details**: Find details on GitHub for a Pak
- **pak-search**: Search for a Pak on GitHub.
- **settings**: Open settings menu. Useful for colour-blindness.
Other commands can be downloaded from CMDPAKs.

Each command can be executed by invoking its name in the ALF-DOS interface.

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
Also make sure you don't actually take new lines, instead replace them with `\n`.
