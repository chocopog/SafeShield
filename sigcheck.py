import platform
import subprocess

def checksig(path):
    if not path.lower().endswith('.exe'):
        return "N/A Not an exe"
    if platform.system() != "Windows":
        return "NA, signature check only works on windows systems"
    psCmd = f"(Get-AuthenticodeSignature '{path}').Status.ToString()"
    try:
        res = subprocess.run(
            ["powershell", "-Command", psCmd],
            capture_output=True,
            text=True,
            timeout=15,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        output = res.stdout.strip()
        return output if output else "Unknown"
    except subprocess.TimeoutExpired:
        return "Error: signature check took too long"
    except Exception as e:
        return f"Error: {e}"
    