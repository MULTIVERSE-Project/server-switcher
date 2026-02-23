# ServerSwitcher

**ServerSwitcher** is a lightweight console launcher for **Garry's Mod servers**.  
It allows you to quickly switch between different server setups by changing the `addons` folder via symlinks, and start your server with either a `.bat` file or direct executable command. Perfect for developers and server admins who frequently run multiple local servers.

---

## Features

- **Select server setup**: Easily choose which server configuration to run.
- **Automatic symlink management**: Updates the `addons` folder with a symlink to the selected server’s addons. Removes any existing symlink before creating a new one.
- **Watchdog mode**: Restarts your server after it stops, with confirmation before restart.
- **Flexible start command**: Run a `.bat` file or directly start `srcds.exe` with custom arguments.
- **Colorful console output**: Easy-to-read, colored status messages.
- **Configurable and portable**: `config.json` stays editable even after building the `.exe`.

---

> [!WARNING]
> Administrator / Developer Mode Requirement
>
> **ServerSwitcher must be run as an Administrator or with Windows Developer Mode enabled**.

**Why?**

- On Windows, creating **symbolic links** (symlinks) requires elevated privileges.
- The app creates a symlink from your global `addons` folder to the selected server’s addons folder.
- Without admin rights, symlink creation will fail, and the launcher cannot switch server setups properly.

**Tip:**

- Right-click `ServerSwitcher.exe` → _Run as administrator_
- Or enable **Developer Mode** in Windows Settings → _Update & Security → For developers → Developer Mode_ (this allows creating symlinks without full admin rights).

---

## Getting Started

### Prerequisites

- Windows 10/11
- Python 3.13+ (for building from source)
- Administrator privileges or Developer Mode enabled

### Configuration (`config.json`)

Create a `config.json` in the same folder as `ServerSwitcher.exe` (or edit the one in the repo). Example:

```json
{
  "gmod_addons_path": "absolut/path/to/garrysmod/addons",
  "start_exe": "absolute/path/to/srcds.exe",
  "start_args": [
    "-console",
    "-game garrysmod",
    "+map gm_flatgrass",
    "+maxplayers 20"
  ],
  "servers": {
    "StarwarsRP": {
      "addons": "absolute/path/to/catalyst/addons",
      "start_args": [
        "+gamemode starwarsrp",
        "+host_workshop_collection 3368186821"
      ]
    },
    "DarkRP": {
      "addons": "absolute/path/to/starwars/addons2",
      "start_bat": "absolute/path/to/darkrp_start.bat"
    }
  }
}
```

Explanation:

- `gmod_addons_path`: Path where the addons symlink is created.
- `start_exe`: Global path to srcds.exe (can be overridden per server).
- `start_args`: Global arguments for the executable.
- `servers`: Server-specific configurations.
- `addons`: Path to the server’s addon folder.
- `start_exe` / start_args: Optional, overrides global defaults.
- `start_bat`: Optional, path to a .bat file instead of direct exe.

### Usage

1. Run `ServerSwitcher.exe` as Administrator or with Developer Mode enabled.
2. Select the server setup you want to run:

```
   What to run?

   1. StarwarsRP
   2. DarkRP
   ...

   Select server:
```

3. The launcher will update the `addons` symlink and start the server with the specified command or .bat file.

---

## Building from Source

If you want to compile `ServerSwitcher` yourself (for example, to include your own icon or modify the script), follow these steps:

### Install Python 3.13+

Download and install Python 3.13+ from [python.org](https://www.python.org/downloads/windows/). Make sure to **check "Add Python to PATH"** during installation.

### Install required packages

Open a terminal or PowerShell in your project folder and run:

```powershell
python -m pip install --upgrade pip
pip install pyinstaller colorama
```

## Build the executable

Run this command from your project folder:

```powershell
python -m PyInstaller --onefile --clean --icon=icon.ico --name=ServerSwitcher switcher.py
```

- Output .exe will be in dist/ServerSwitcher.exe
- Keep config.json next to the .exe for editing
