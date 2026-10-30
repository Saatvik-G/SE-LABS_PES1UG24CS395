# Lab 5: Static Code Analysis — Event Management System

**Student Name:** Saatvik Gupta  
**SRN:** PES1UG24CS395  
**Section:** G  
**Course:** Software Engineering Laboratory  
**Assigned Original Repository:** [SETAPESU26/L5_31_event_manager](https://github.com/SETAPESU26/L5_31_event_manager.git)  
**Personal Lab Repository:** [Saatvik-G/SE-LABS_PES1UG24CS395](https://github.com/Saatvik-G/SE-LABS_PES1UG24CS395.git)  

---

## Deliverables & Submission Assets

| Deliverable | Description | File Link |
| :--- | :--- | :--- |
| **Final Corrected Code** | Cleaned and validated Python script meeting 10.00/10 Pylint score, 0 Bandit vulnerabilities, and 0 Flake8 issues | [`event_manager.py`](event_manager.py) |
| **Consolidated Lab Report (PDF)** | Formatted report containing Introduction, Issue Table, Screenshots, Report Contents, and Reflection Answers | [`Lab5_PES1UG24CS395_G.pdf`](Lab5_PES1UG24CS395_G.pdf) |
| **Issue Documentation (Markdown)** | Detailed analysis table of all 8 identified issues and remediation approaches | [`issues.md`](issues.md) |
| **Reflection Answers (Markdown)** | Comprehensive answers to all 4 static analysis reflection questions | [`reflection.md`](reflection.md) |
| **Analysis Reports (Before & After)** | Text logs for Pylint, Bandit, and Flake8 executions | [`pylint_report_before.txt`](pylint_report_before.txt), [`pylint_report_after.txt`](pylint_report_after.txt), [`bandit_report_before.txt`](bandit_report_before.txt), [`bandit_report_after.txt`](bandit_report_after.txt), [`flake8_report_before.txt`](flake8_report_before.txt), [`flake8_report_after.txt`](flake8_report_after.txt) |

---

## Static Code Analysis Summary

### Tool Roles & Metrics

| Static Analysis Tool | Role | Before Fixes | After Fixes | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Pylint** | Code quality, design smells, naming conventions, docstrings | **4.64 / 10** | **10.00 / 10** | **100% Resolved** (Target > 9.5 exceeded) |
| **Bandit** | Python security vulnerability scanner (CWE mapping) | **4 Issues** (1 High, 1 Medium, 2 Low) | **0 Issues** (No issues identified) | **100% Clean** |
| **Flake8** | PEP 8 style, layout, operator padding, line length | **4 Violations** | **0 Violations** (Clean exit code 0) | **100% Clean** |

---

## 3 Separate Git Commits for Tool Fixes

Per lab instructions, all changes were committed in distinct, focused commits:

1. **Commit 1 (Bandit Fixes):**  
   `fix(bandit): replace insecure pickle and shell command with json and safe file writing`  
   - Replaced `os.system` command injection vulnerability (`B605`) with safe in-process badge file generation.
   - Replaced insecure object deserialization with `pickle` (`B301`, `B403`) by adopting structured `json.dump` / `json.load`.
   - Replaced weak PRNG `random.choice` (`B311`) with cryptographically secure `secrets.choice`.

2. **Commit 2 (Pylint Fixes):**  
   `fix(pylint): resolve mutable default argument, docstrings, unused argument and naming conventions`  
   - Fixed mutable default argument bug `guests=[]` (`W0102`) by adopting `guests=None` and local instantiation, resolving cross-event data corruption.
   - Converted all function and parameter identifiers from `camelCase` to PEP 8 standard `snake_case` (`C0103`).
   - Added descriptive PEP 257 docstrings for module and all public functions (`C0114`, `C0116`).
   - Leveraged previously unused argument `sortOrder` in `guest_report()` (`W0613`).
   - Raised Pylint score to **10.00 / 10**.

3. **Commit 3 (Flake8 Fixes):**  
   `style(flake8): fix PEP 8 formatting whitespace line lengths and entry point`  
   - Corrected missing whitespace after commas (`E231`), missing whitespace around operators (`E225`), and inline comment spacing (`E261`).
   - Wrapped long lines under 79 characters (`E501`).
   - Added two blank lines before top-level definitions and encapsulated program execution under `if __name__ == "__main__":` (`E305`).

---

## How to Run & Verify

```bash
# 1. Run the corrected program
python event_manager.py

# 2. Run static analysis tools
python -m pylint event_manager.py
python -m bandit -r event_manager.py
python -m flake8 event_manager.py
```
