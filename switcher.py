import os
import json
import shutil
import subprocess
import sys
import signal
from colorama import init, Fore, Style

init(autoreset=True)

# ─────────────────────
# Color helpers
# ─────────────────────

def info(msg):
    print(Fore.CYAN + msg)

def success(msg):
    print(Fore.GREEN + msg)

def warn(msg):
    print(Fore.YELLOW + msg)

def error(msg):
    print(Fore.RED + msg)

def dim(msg):
    print(Style.DIM + msg + Style.RESET_ALL)


# ─────────────────────
# Paths & config
# ─────────────────────

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()
CONFIG_PATH = os.path.join(BASE_PATH, "config.json")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        error("config.json not found!")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────
# Addons / symlink
# ─────────────────────

def clear_existing_addons(path):
    if os.path.islink(path):
        dim("[*] Removing existing symlink...")
        os.unlink(path)
    elif os.path.exists(path):
        dim("[*] Removing existing addons folder...")
        shutil.rmtree(path)


def create_symlink(target, link_path):
    try:
        os.symlink(target, link_path, target_is_directory=True)
        success("[+] Symlink created (python)")
    except OSError:
        warn("[!] Python symlink failed, trying mklink...")

        cmd = f'cmd /c mklink /D "{link_path}" "{target}"'
        result = subprocess.run(cmd, shell=True)

        if result.returncode != 0:
            error("[X] mklink failed. Try running as Administrator or enable Developer Mode.")
            raise
        else:
            success("[+] Symlink created (mklink)")


# ─────────────────────
# Menu
# ─────────────────────

def show_menu(servers):
    info("What to run?\n")
    names = list(servers.keys())

    for i, name in enumerate(names, start=1):
        print(f"{Fore.WHITE}{i}. {Style.BRIGHT}{name}{Style.RESET_ALL}")

    print()
    choice = input(Fore.BLUE + Style.BRIGHT + "Select server: " + Style.RESET_ALL)
    return names[int(choice) - 1]


# ─────────────────────
# Server start logic
# ─────────────────────

def resolve_start_command(config, server):
    exe = server.get("start_exe", config.get("start_exe"))

    if not exe:
        raise RuntimeError("start_exe is not defined")

    global_args = config.get("start_args", [])
    server_args = server.get("start_args", [])

    args = [*global_args, *server_args]

    return exe, args


def start_server(config, server):
    if "start_bat" in server:
        info("[*] Running BAT file...")
        subprocess.Popen(server["start_bat"], shell=True)
        return

    try:
        exe, args = resolve_start_command(config, server)
    except RuntimeError as e:
        error(f"[X] {e}")
        return

    info("\n[*] Starting server (watchdog mode)...")

    while True:
        info("[*] srcds started.")

        exe_name = os.path.basename(exe)
        dim(f"[*] Command: {exe_name} {' '.join(args)}")

        try:
            proc = subprocess.Popen(
                [exe, *args],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            proc.wait()

            warn("\n[!] srcds stopped.")
            answer = input(Fore.BLUE + Style.BRIGHT + "Restart server? [Y/N]: " + Style.RESET_ALL).strip().lower()

            if answer != "y":
                info("[*] Exiting.")
                break

        except KeyboardInterrupt:
            warn("\n[*] Shutdown requested.")

            try:
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            except Exception:
                proc.kill()

            break


# ─────────────────────
# Main
# ─────────────────────

def main():
    config = load_config()
    servers = config["servers"]
    addons_path = config["gmod_addons_path"]

    try:
        selected = show_menu(servers)
    except (ValueError, IndexError):
        error("Invalid choice.")
        return

    server = servers[selected]

    success(f"\n[+] Selected: {selected}")

    clear_existing_addons(addons_path)
    create_symlink(server["addons"], addons_path)

    start_server(config, server)

    success("[+] Done.")


if __name__ == "__main__":
    main()