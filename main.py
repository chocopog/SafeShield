from hashing import GetFileHash
from sigcheck import checksig
from virustotalcheck import checkVirusTotal
from extensioncheck import CheckDoubleExtension, isDangerExt
from config import score_danger_ext, score_double_ext, score_invalid_signature, score_VT_flag, score_VT_unknown, Risk_threshold

import os
def RiskAnalyzer(is_danger_ext, is_double_ext, sig_status, vt_status):
    score = 0
    if is_danger_ext:
        if sig_status=="Valid":
            pass
        else:
            score += score_danger_ext
    if is_double_ext:
        score += score_double_ext
    if sig_status.startswith("N/A"):
        pass
    elif "Valid" not in sig_status:
        score+= score_invalid_signature
    if "Flagged" in vt_status:
        score+=score_VT_flag
    elif "Unknown file" in vt_status:
        score+= score_VT_unknown
    
    for m_score, label in Risk_threshold:
        if score <= m_score:
            return label
    return "Extreme"

def analyzeFolder(folderpath):
    results = []
    for root, _, files in os.walk(folderpath):
        for filename in files:
            filepath = os.path.join(root, filename)
            risk_level = analyzeFile(filepath)
            results.append((filename, risk_level))

    print("\nBatch results")
    for filename, risk_level in results:
        print(f"{filename}: {risk_level if risk_level else 'Error'}")
    return results



def analyzeFile(filepath):
    print("\n--- File Analyzer ---")

    if not os.path.exists(filepath):
        print("Error, file not found")
        return
    if not os.path.isfile(filepath):
        print("Error, path is not a file")
        return
    filename = os.path.basename(filepath)
    isDoubleExt = CheckDoubleExtension(filename)

    print("\n Scanning...")
    print(f"File: {filename}")
    print(f"Size: {os.path.getsize(filepath)} bytes")
    print(f"Double extension: {'DETECTED!!' if isDoubleExt else 'None'}")
    print(f"Dangerous file type: {'Yes' if isDangerExt(filename) else 'No'}")
    

    file_hash = GetFileHash(filepath)
    print(f"SHA-256 hash: {file_hash if file_hash else 'Could not compute!'}")

    sig_status = checksig(filepath)
    print(f"Digital signature status: {sig_status}")

    if file_hash:
        vt_status = checkVirusTotal(file_hash, 2)
    else: 
        vt_status = "Skipped, no hash available"
    print(f"Global threat DB: {vt_status}")

    risk_level = RiskAnalyzer(isDangerExt(filename), isDoubleExt, sig_status, vt_status)
    print(f"\nOverall Risk Level: {risk_level}")

    print("\nDone. This tool only reads and reports; no files were changed.")
    return risk_level

path = input("Please enter file or folder path:   ").strip().strip('"')
if os.path.isdir(path):
    analyzeFolder(path)
else:
    analyzeFile(path)
