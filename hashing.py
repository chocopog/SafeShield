
import hashlib

def getHash(path):
    hashVal = hashlib.sha256()
    try:
        with open(path, "rb") as file:
            while True:
                    chunk = file.read(4096)
                    if not chunk:
                        break
                    hashVal.update(chunk)
        return hashVal.hexdigest()
    except FileNotFoundError:
        return None
    except PermissionError:
        return None
    except OSError as e:
        print(f"Could not read file: {e}")
        return None

     