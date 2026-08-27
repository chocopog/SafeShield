# SafeShield File Analyzer

A simple Python command-line tool that analyzes a file and reports how risky it might be, without ever modifying, moving, or deleting anything. It's a read-only security scanner built for a college cybersecurity internship assignment.

## What it checks

- **Double extension spoofing** — flags files disguised like `invoice.pdf.exe`
- **Dangerous file types** — flags extensions like `.exe`, `.bat`, `.dll`, `.js`, etc.
- **SHA-256 hash** — generates a unique fingerprint of the file
- **Digital signature** — checks if a `.exe` is signed by a verified publisher (Windows only)
- **VirusTotal lookup** — checks if the file's hash has already been scanned and flagged by antivirus engines
- **Overall Risk Level** — combines all of the above into one rating: Low, Medium, High, or Extreme

## Project structure

```
main.py             # CLI entry point and scan pipeline
gui.py              # Tkinter graphical interface
hashing.py          # SHA-256 hashing
extensioncheck.py   # dangerous-extension and double-extension checks
sigcheck.py         # Windows digital signature check
virustotalcheck.py  # VirusTotal API lookup
config.py           # risk scores, thresholds, and GUI colors
.env                # local VirusTotal API key (create this; do not commit it)
```

`learningtkinter.py` is a local learning file and is excluded by `.gitignore`.

## Setup

### 1. Install dependencies

```
pip install requests python-dotenv
```

### 2. Get a free VirusTotal API key

1. Go to [virustotal.com](https://www.virustotal.com) and create a free account
2. Click your profile icon (top right) and open **API Key**
3. Copy the key shown there

The free tier is limited to about 4 requests per minute, which is plenty for scanning files one at a time.

### 3. Set up your `.env` file

In the same folder as `main.py`, create a file named exactly `.env` (no `.txt` extension, check Windows isn't hiding it) with this single line:

```
VT_API_KEY=your_actual_key_here
```

No quotes, no spaces around the `=`. Never commit this file to GitHub, it should stay private. Add a `.gitignore` with `.env` in it if you're pushing this project to a repo.

## Usage

Run the command-line scanner and enter a file or folder path when prompted:

```
python main.py
```

```
Please enter file or folder path: C:\Users\you\Downloads\somefile.exe
```

To use the graphical interface instead:

```
python gui.py
```

Choose a file or folder, then select **Start scan**. A folder scan displays the risk level for each file and the highest risk level found.

Example output:

```
--- File Analyzer ---

Scanning...
File: somefile.exe
Size: 152064 bytes
Double extension: None
Dangerous file type: Yes
SHA-256 hash: 3a7bd3e2360a3d...
Digital signature status: Valid
Global threat DB: Clean

Overall Risk Level: Medium

Done. This tool only reads and reports; no files were changed.
```

## Notes

- The digital signature check only works on Windows, since it relies on PowerShell's `Get-AuthenticodeSignature` cmdlet
- This tool is read-only: it never deletes, moves, quarantines, or modifies any file it scans
- A "Low" risk result doesn't guarantee a file is safe, it just means none of the checks above found anything suspicious
- VirusTotal lookups are skipped when `VT_API_KEY` is missing
- VirusTotal timeouts, connection failures, rate limits, invalid responses, and unexpected status codes are reported without stopping the whole scan
- If a file cannot be read, hashed, or inspected, the scanner reports the problem and continues with the next file during a folder scan

## Risk scoring

The scanner adds points for suspicious indicators:

- Dangerous file extension: 1 point, unless the executable has a valid signature
- Double extension: 2 points
- Missing or invalid executable signature: 2 points
- VirusTotal flagged result: 3 points
- VirusTotal unknown result: 1 point

The total score is reported as **Low** (0–1), **Medium** (2), **High** (3–5), or **Extreme** (6 or more).