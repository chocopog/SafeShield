from hashing import getHash
from sigcheck import checksig
from virustotalcheck import checkVT
from extensioncheck import checkDouble, isDangerExt
from config import dangerScore, doubleScore, sigScore, vtFlagScore, vtUnknownScore, riskThresholds

import os
def riskAnalyze(isDangerous, isDouble, sigStatus, vtStatus):
    score = 0
    if isDangerous:
        if sigStatus=="Valid":
            pass
        else:
            score += dangerScore
    if isDouble:
        score += doubleScore
    if sigStatus and sigStatus.startswith("N/A"):
        pass
    elif "Valid" not in sigStatus:
        score+= sigScore
    if "Flagged" in vtStatus:
        score+=vtFlagScore
    elif "Unknown file" in vtStatus:
        score+= vtUnknownScore
    
    for maxScore, label in riskThresholds:
        if score <= maxScore:
            return label
    return "Extreme"

def analyzeFolder(folderPath, output=print):
    results = []
    def reportWalkError(error):
        output(f"Error reading folder: {error}")

    for root, _, files in os.walk(folderPath, onerror=reportWalkError):
        for name in files:
            filePath = os.path.join(root, name)
            try:
                risk = analyzeFile(filePath, output=output)
            except OSError as error:
                output(f"Error scanning {name}: {error}")
                risk = None
            results.append((name, risk))

    output("\nBatch results")
    for name, risk in results:
        output(f"{name}: {risk if risk else 'Error'}")
    return results



def analyzeFile(filePath, output=print):
    output("\n--- File Analyzer ---")

    if not os.path.exists(filePath):
        output("Error, file not found")
        return
    if not os.path.isfile(filePath):
        output("Error, path is not a file")
        return
    name = os.path.basename(filePath)
    isDouble = checkDouble(name)

    output("\n Scanning...")
    output(f"File: {name}")
    try:
        fileSize = os.path.getsize(filePath)
    except OSError as error:
        output(f"Error, could not read file metadata: {error}")
        return

    output(f"Size: {fileSize} bytes")
    output(f"Double extension: {'DETECTED!!' if isDouble else 'None'}")
    output(f"Dangerous file type: {'Yes' if isDangerExt(name) else 'No'}")
    

    filehash = getHash(filePath)
    output(f"SHA-256 hash: {filehash if filehash else 'Could not compute!'}")

    sigStatus = checksig(filePath)
    output(f"Digital signature status: {sigStatus}")

    if filehash:
        vtStatus = checkVT(filehash, 2)
    else: 
        vtStatus = "Skipped, no hash available"
    output(f"Global threat DB: {vtStatus}")

    riskLevel = riskAnalyze(isDangerExt(name), isDouble, sigStatus, vtStatus)
    output(f"\nOverall Risk Level: {riskLevel}")

    output("\nDone. This tool only reads and reports; no files were changed.")
    return riskLevel
if __name__ == "__main__":
    path = input("Please enter file or folder path:   ").strip().strip('"')

    if os.path.isdir(path):
        analyzeFolder(path)
    else:
        analyzeFile(path)
