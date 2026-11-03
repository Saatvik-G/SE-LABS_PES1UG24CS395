# Lab 6: Code and Branch Coverage Analysis — Coupon Validator

**Student Name:** Saatvik Gupta  
**SRN:** PES1UG24CS395  
**Section:** G  
**Course:** Software Engineering Laboratory  
**Assigned Original Repository:** [SETAPESU26/L6_L7_31_coupon_validator](https://github.com/SETAPESU26/L6_L7_31_coupon_validator.git)  
**Personal Lab Repository:** [Saatvik-G/SE-LABS_PES1UG24CS395](https://github.com/Saatvik-G/SE-LABS_PES1UG24CS395.git)  

---

## Deliverables & Submission Assets

| Deliverable | Description | File Link |
| :--- | :--- | :--- |
| **Module Under Test** | Core coupon validation and calculation logic | [`coupon_validator.py`](coupon_validator.py) |
| **Code Coverage Test Suite** | Test cases achieving 100% statement coverage (15 tests) | [`CodeCoverageTest_coupon_validator.py`](CodeCoverageTest_coupon_validator.py) |
| **Branch Coverage Test Suite** | Test cases achieving 100% decision branch coverage (22 tests) | [`BranchCoverageTest_coupon_validator.py`](BranchCoverageTest_coupon_validator.py) |
| **Consolidated Lab 6 PDF** | Formatted academic report containing concepts, summary, terminal screenshots, and branch matrix | [`Lab6_PES1UG24CS395_G.pdf`](Lab6_PES1UG24CS395_G.pdf) |
| **Terminal Screenshots** | Authentic Windows PowerShell coverage output screenshots | [`screenshots/code_coverage_terminal.png`](screenshots/code_coverage_terminal.png), [`screenshots/branch_coverage_terminal.png`](screenshots/branch_coverage_terminal.png) |
| **Coverage Reports (.txt)** | Raw terminal coverage reports | [`code_coverage_report.txt`](code_coverage_report.txt), [`branch_coverage_report.txt`](branch_coverage_report.txt) |

---

## Coverage Metrics & Analysis

| Test Suite File | Test Count | Statements | Missed | Statement (Line) Coverage | Branches (Total / Covered) | Branch Coverage | Target Met? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Starter Test** (`test_coupon_validator.py`) | 2 | 32 | 23 | **28%** | 24 / 4 | **23%** | Baseline |
| **Code Coverage Test** (`CodeCoverageTest_...py`) | 15 | 32 | 0 | **100%** | 24 / 23 | **98%** | **YES** (Req >= 90%) |
| **Branch Coverage Test** (`BranchCoverageTest_...py`) | 22 | 32 | 0 | **100%** | 24 / 24 | **100%** | **YES** (Req >= 70%) |

---

## Required Minimum 2 Commits

Per the lab manual instructions, separate commits were created for code coverage and branch coverage:

1. **Commit 1 (`4c97ee9`):**  
   `test(coverage): add test cases in CodeCoverageTest for 100% line coverage`  
   - Implemented 15 comprehensive unit tests exercising every executable statement in `coupon_validator.py` (`coupon_discount`, `best_discount`, and `is_expired`).
   - Line coverage achieved: **100%** (exceeding >= 90% requirement).

2. **Commit 2 (`5838bf6`):**  
   `test(coverage): add test cases in BranchCoverageTest for 100% branch coverage`  
   - Added 7 additional targeted decision-branch tests covering boundary conditions, cart caps, and multi-coupon sorting comparisons.
   - Closed partial branch `25->23` (`value > best` evaluating to False) by passing mixed discount lists.
   - Branch coverage achieved: **100%** (24/24 branches, exceeding >= 70% requirement).

---

## How to Run & Verify Coverage

```powershell
# 1. Run line coverage
coverage run -m pytest CodeCoverageTest_coupon_validator.py
coverage report -m

# 2. Run branch coverage
coverage run --branch -m pytest BranchCoverageTest_coupon_validator.py
coverage report -m
```
