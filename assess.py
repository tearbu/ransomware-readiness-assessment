#!/usr/bin/env python3
"""Ransomware Readiness Assessment.

Scores an organisation against ransomware-readiness controls aligned to
NIST CSF functions and CISA ransomware guidance. Input is a JSON answers
file giving a maturity rating (0-5) and evidence note per category.

    0 = not implemented   1 = ad hoc        2 = partially implemented
    3 = defined           4 = managed       5 = optimised / measured

Usage:
    python3 assess.py --demo                 # bundled fictional sample
    python3 assess.py --file answers.json    # your own answers file

Standard library only.
"""

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CRITICAL_THRESHOLD = 2.0  # any category below this is a critical gap

# id -> (display name, NIST CSF function, remediation if weak)
CATEGORIES = {
    "backup_isolation": (
        "Backup isolation & restore testing", "Recover (RC)",
        "Isolate backup infrastructure from production credentials and test full restores quarterly."),
    "immutable_backups": (
        "Immutable / offline backups", "Recover (RC)",
        "Keep at least one immutable or offline (air-gapped) copy of critical data that production admins cannot delete."),
    "mfa_coverage": (
        "MFA coverage", "Protect (PR)",
        "Enforce phishing-resistant MFA on remote access, email, admin and backup consoles first, then all users."),
    "patch_cadence": (
        "Patch cadence (internet-facing first)", "Protect (PR)",
        "Patch internet-facing and known-exploited vulnerabilities within 14 days; track exceptions formally."),
    "edr_coverage": (
        "EDR coverage", "Detect (DE)",
        "Deploy EDR to servers as well as workstations and alert on tampering / disabled agents."),
    "segmentation": (
        "Network segmentation", "Protect (PR)",
        "Segment backups, servers and user networks; block workstation-to-workstation lateral movement."),
    "least_privilege": (
        "Least privilege / privileged access", "Protect (PR)",
        "Remove standing local admin, tier admin accounts, and review privileged group membership monthly."),
    "email_filtering": (
        "Email filtering & phishing defence", "Protect (PR)",
        "Block executable/macro attachments, enforce DMARC, and run regular phishing simulations."),
    "ir_plan": (
        "Incident response plan & exercises", "Respond (RS)",
        "Maintain a ransomware-specific playbook (isolate, preserve evidence, restore order) and tabletop it twice a year."),
    "logging": (
        "Logging & central monitoring", "Detect (DE)",
        "Centralise logs off-host for at least 90 days, including authentication, EDR and backup job results."),
}


def load_answers(path):
    data = json.loads(Path(path).read_text())
    return data.get("organization", "(unnamed)"), data.get("responses", {})


def assess(org, responses):
    print(f"\nRansomware Readiness Assessment — {org}")
    print("=" * 78)
    print(f"{'Category':<42}{'CSF':<13}{'Score':>6}  Status")
    print("-" * 78)
    rows, missing = [], []
    for cid, (name, csf, _fix) in CATEGORIES.items():
        entry = responses.get(cid)
        if entry is None:
            missing.append(name)
            rows.append((cid, name, csf, None))
            continue
        rows.append((cid, name, csf, float(entry.get("score", 0))))
    for _cid, name, csf, score in rows:
        if score is None:
            print(f"{name:<42}{csf:<13}{'  n/a':>6}  NOT ASSESSED")
        else:
            status = "CRITICAL GAP" if score < CRITICAL_THRESHOLD else "ok" if score >= 3 else "weak"
            print(f"{name:<42}{csf:<13}{score:>6.1f}  {status}")
    scored = [s for *_x, s in rows if s is not None]
    overall = sum(scored) / len(scored) if scored else 0.0
    print("-" * 78)
    print(f"Overall maturity: {overall:.2f} / 5.00  "
          f"({'Initial' if overall < 1.5 else 'Developing' if overall < 2.5 else 'Defined' if overall < 3.5 else 'Managed' if overall < 4.5 else 'Optimised'})")
    if missing:
        print(f"Not assessed (treated as risk, excluded from average): {', '.join(missing)}")

    gaps = sorted((r for r in rows if r[3] is not None), key=lambda r: r[3])
    critical = [g for g in gaps if g[3] < CRITICAL_THRESHOLD]
    print(f"\nCritical gaps (score < {CRITICAL_THRESHOLD:.0f}): {len(critical)}")
    for _cid, name, _csf, score in critical:
        print(f"  !! {name} — {score:.1f}/5")

    print("\nPrioritised remediation list (lowest maturity first):")
    for i, (cid, name, _csf, score) in enumerate(gaps[:5], 1):
        print(f"  {i}. [{score:.1f}/5] {name}")
        print(f"     -> {CATEGORIES[cid][2]}")
    return overall


def main():
    ap = argparse.ArgumentParser(description="Ransomware Readiness Assessment")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--demo", action="store_true", help="Assess the bundled fictional sample answers")
    g.add_argument("--file", help="Path to your own answers JSON file")
    args = ap.parse_args()
    path = HERE / "sample_answers.json" if args.demo else Path(args.file)
    org, responses = load_answers(path)
    assess(org, responses)
    return 0


if __name__ == "__main__":
    sys.exit(main())
