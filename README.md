# SafeShield File Analyzer

SafeShield is a read-only Python file-analysis tool. It combines filename checks, SHA-256 hashing, Windows Authenticode signature checks, and a VirusTotal hash lookup into an overall risk rating. It never modifies, deletes, moves, quarantines, or uploads the file itself.

## Features

- Detects suspicious double extensions such as `invoice.pdf.exe`
- Recognizes potentially dangerous final extensions such as `.exe`, `.bat`, `.dll`, `.js`, and `.ps1`
- Computes a SHA-256 hash by reading the file in 4096-byte chunks
- Checks `.exe` Authenticode status on Windows with PowerShell
- Queries VirusTotal using the SHA-256 hash
- Supports both command-line and Tkinter graphical operation
- Scans a complete folder and reports the highest calculated risk level

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Main scan pipeline, risk scoring, CLI, and folder scanning |
| `gui.py` | Tkinter interface for selecting files/folders and displaying results |
| `config.py` | Risk points, thresholds, GUI colors, and risk ordering |
| `extensioncheck.py` | Final-extension and double-extension checks |
| `hashing.py` | SHA-256 calculation |
| `sigcheck.py` | Windows Authenticode signature lookup |
| `virustotalcheck.py` | VirusTotal API request and response handling |
| `maketestfile.py` | Small helper that creates a test file named `test'file.exe` |
| `learningtkinter.py` | Earlier Tkinter learning version; not the current GUI |
| `.env` | Local API key; private and never committed |

## Setup

Create or activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` in this folder:

```text
VT_API_KEY=your_actual_key_here
```

The API key must remain private. Do not commit `.env`.

## Running the application

Command line:

```powershell
python main.py
```

The program asks for a path. If the path is a directory, every file below it is scanned; otherwise one file is scanned.

Graphical interface:

```powershell
python gui.py
```

Choose a file or folder, then press **Start scan**. The text area shows the individual checks. For a folder, the risk label shows the worst risk and a count for each level.

## Scan flow

1. `main.py` validates that the path exists and is a file.
2. `extensioncheck.py` checks the filename and final extension.
3. `hashing.py` reads the file as bytes and calculates SHA-256.
4. `sigcheck.py` checks Authenticode only for `.exe` files on Windows.
5. `virustotalcheck.py` sends the hash to `https://www.virustotal.com/api/v3/files/{hash}`.
6. `riskAnalyze()` adds points from the results and maps the total to a label.
7. The result is printed through the supplied `output` function. The GUI supplies `outputGui`, while the CLI uses `print`.

## VirusTotal result meanings

VirusTotal is a **hash lookup**, not a local scan of the Python source. It does not receive the file from this program.

| Response | Meaning in this project |
| --- | --- |
| `200`, malicious or suspicious count above zero | `Flagged` |
| `200`, malicious and suspicious counts are zero | `Clean` according to the latest VT analysis |
| `404` | `Unknown file`; the exact hash is not in VT's database |
| No API key | `Skipped (NO API KEY)` |
| Timeout, network failure, rate limit, invalid response, or other status | An `Error: ...` message |

`Unknown` must not be interpreted as clean. A newly created file can be unknown, but a fresh file may also return clean if the exact same bytes and hash have already been submitted to VirusTotal. The detailed `Global threat DB` line is the authoritative VT status; `Overall Risk Level: Low` is only the combined local score and is not a guarantee of safety.

## Risk scoring

The current values are defined in `config.py`:

| Indicator | Points |
| --- | ---: |
| Dangerous extension without a valid `.exe` signature | 1 |
| Double extension | 2 |
| Invalid/missing executable signature | 2 |
| VirusTotal flagged | 3 |
| VirusTotal unknown | 1 |

Scores are mapped as follows:

- **Low:** 0–1
- **Medium:** 2
- **High:** 3–5
- **Extreme:** 6 or more

An `.exe` with a valid signature avoids both the dangerous-extension point and the signature point. Non-executable files receive `N/A` for signature checking and are not penalized for lacking an executable signature.

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

## Error handling and limitations

- The signature check depends on Windows PowerShell and `Get-AuthenticodeSignature`.
- A VirusTotal result is based on the hash and available historical analysis; it is not a guarantee that a file is safe.
- VirusTotal requests can be skipped without an API key and may be limited by the free API quota.
- Hashing and metadata failures are reported. Folder scans continue with other files when possible.
- Extension checks are filename-based and do not inspect file contents.
- `maketestfile.py` creates text containing `dummy content` with an `.exe` name; it is not a real executable or malware sample.

## Example output

```text
File: somefile.exe
Size: 152064 bytes
Double extension: None
Dangerous file type: Yes
SHA-256 hash: 3a7bd3e2360a3d...
Digital signature status: Valid
Global threat DB: Clean

Overall Risk Level: Medium
```