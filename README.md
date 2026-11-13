# Ransomware Readiness Assessment

A structured self-assessment CLI that scores an organisation's readiness
to withstand, detect, and recover from a ransomware incident, using the
control categories in NIST CSF and CISA's ransomware guidance.

## The problem it solves

"We think we're okay on ransomware" is not an assessment. Readiness
reviews often stall because they are unstructured: a long questionnaire,
no scoring, and no prioritised output. This tool takes a small set of
honest maturity ratings (0–5) with evidence notes across the ten control
categories that decide real ransomware outcomes, and produces what a
review actually needs: a per-category scorecard mapped to NIST CSF
functions, an overall maturity figure, the critical gaps, and a
prioritised remediation list an owner can act on.

## Categories assessed

Backup isolation & restore testing · Immutable/offline backups · MFA
coverage · Patch cadence · EDR coverage · Network segmentation · Least
privilege · Email filtering & phishing defence · Incident response plan
& exercises · Logging & central monitoring.

Maturity scale: **0** not implemented · **1** ad hoc · **2** partially
implemented · **3** defined · **4** managed · **5** optimised/measured.
Any category scoring **below 2** is flagged as a **critical gap** —
experience shows incidents turn on exactly those categories (backups
attackers can delete, standing admin rights, an untested IR plan).

## How to run

```bash
# Demo mode — assesses the bundled fictional sample company
python3 assess.py --demo

# Assess your own organisation: copy sample_answers.json, edit the
# scores and evidence notes honestly, then:
python3 assess.py --file answers.json
```

Python 3, standard library only. The answers format is simple JSON:
an organisation name plus, per category, a `score` (0–5) and an
`evidence` note recording what the score is based on.

## Demo output (actual run)

```
Ransomware Readiness Assessment — Northwind Traders Ltd (fictional sample)
==============================================================================
Category                                  CSF           Score  Status
------------------------------------------------------------------------------
Backup isolation & restore testing        Recover (RC)    3.0  ok
Immutable / offline backups               Recover (RC)    1.0  CRITICAL GAP
MFA coverage                              Protect (PR)    3.0  ok
Patch cadence (internet-facing first)     Protect (PR)    2.0  weak
EDR coverage                              Detect (DE)     4.0  ok
Network segmentation                      Protect (PR)    2.0  weak
Least privilege / privileged access       Protect (PR)    1.0  CRITICAL GAP
Email filtering & phishing defence        Protect (PR)    4.0  ok
Incident response plan & exercises        Respond (RS)    1.0  CRITICAL GAP
Logging & central monitoring              Detect (DE)     2.0  weak
------------------------------------------------------------------------------
Overall maturity: 2.30 / 5.00  (Developing)

Critical gaps (score < 2): 3
  !! Immutable / offline backups — 1.0/5
  !! Least privilege / privileged access — 1.0/5
  !! Incident response plan & exercises — 1.0/5

Prioritised remediation list (lowest maturity first):
  1. [1.0/5] Immutable / offline backups
     -> Keep at least one immutable or offline (air-gapped) copy of critical data that production admins cannot delete.
  2. [1.0/5] Least privilege / privileged access
     -> Remove standing local admin, tier admin accounts, and review privileged group membership monthly.
  3. [1.0/5] Incident response plan & exercises
     -> Maintain a ransomware-specific playbook (isolate, preserve evidence, restore order) and tabletop it twice a year.
  4. [2.0/5] Patch cadence (internet-facing first)
     -> Patch internet-facing and known-exploited vulnerabilities within 14 days; track exceptions formally.
  5. [2.0/5] Network segmentation
     -> Segment backups, servers and user networks; block workstation-to-workstation lateral movement.
```

The sample company is fictional, with deliberately mixed maturity:
decent detection (EDR 4/5, email filtering 4/5) undermined by recovery
and privilege weaknesses — the profile behind many real incidents.

## Design notes and limitations

- **Self-assessment, not an audit.** Scores are only as honest as the
  input. The `evidence` field exists so a reviewer can challenge a
  score; in a real engagement each rating should be tied to an artefact
  (a restore-test report, an MFA coverage export, a tabletop record).
- **Unassessed categories** are reported as NOT ASSESSED and excluded
  from the average rather than silently scored zero — but they are
  still surfaced, because "we never looked" is itself a finding.
- The overall figure is an unweighted mean of category scores; the
  critical-gap flag is deliberately independent of it, so a good
  average cannot hide a fatal weakness.
- Framework mapping is at the NIST CSF function level (Protect /
  Detect / Respond / Recover) for reporting; it is not a formal CSF
  assessment.

## License

MIT — see `LICENSE`.
