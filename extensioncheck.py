dangerExt = ['.exe', '.bat', '.dll', '.cmd', '.sh', '.js', '.vbs', '.scr', '.ps1', '.msi']
safeExt = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.txt', '.xls', '.xlsx']

def checkDouble(filename):
    parts = filename.lower().split('.')
    if len(parts)<3:
        return False
    prevExt = f".{parts[-2]}"
    finalExt = f".{parts[-1]}"
    return prevExt in safeExt and finalExt in dangerExt

def getFinalExt(filename):
    parts = filename.lower().split('.')
    return f".{parts[-1]}" if len(parts)>1 else ""

def isDangerExt(filename):
    return getFinalExt(filename) in dangerExt

