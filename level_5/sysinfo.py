"""
Your Challenge:
1 . use 'uv init' to cfreate a package structure.
2 . Configure 'pyproject.toml' for the package with the necessary metadata.
3 . Add a command-line entry point so you can run a 'sysinfo' command from the terminal.
4 . Use 'uv build' to build the package and distribute it.
5 . (Bonus) Add a '--json' option to display the system information in JSON format.


"""


import socket
from datetime import datetime
import platform


def get_system_info():
    """Gather system information"""
    info = {
        "Platform": platform.system(),
        "Platform Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": socket.gethostname(),
        "Python Version": platform.python_version(),
        "Current Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return info


def display_info():
    """Display system information"""
    print("=" * 50)
    print("System Information".center(50))
    print("=" * 50)
    info = get_system_info()
    for key, value in info.items():
        print(f"{key:<20}: {value}")
    print("=" * 50)
