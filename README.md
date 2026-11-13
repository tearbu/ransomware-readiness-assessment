# Ransomware Readiness Assessment

A self-assessment CLI, with a simple structure. It scores how ready an organisation is to withstand a ransomware incident, detect it, and recover from it. The control categories come from NIST CSF and CISA's ransomware guidance.

## The problem it solves

"We think we're okay on ransomware" is not an assessment.

Readiness reviews stall for a familiar reason. A long questionnaire. No scoring. No clear output at the end, and nothing prioritised. This tool works differently. You give it a small set of honest maturity ratings (0 to 5), with evidence notes, across the ten control categories that decide real ransomware outcomes. What you get back is what a review needs: a scorecard for each category mapped to NIST CSF functions, an overall maturity figure, the critical gaps, and a remediation list in priority order that an owner can actually act on.

## Categories assessed

Backup isolation & restore testing · Immutable/offline backups · MFA
coverage · Patch cadence · EDR coverage · Network segmentation · Least
privilege · Email filtering & phishing defence · Incident response plan
& exercises · Logging & central monitoring.

Maturity scale: **0** not implemented · **1** ad hoc · **2** partially implemented · **3** defined · **4** managed · **5** optimised/measured.

Any category scoring **below 2** is flagged as a **critical gap**. In practice, incidents turn on exactly those categories: backups attackers can delete, standing admin rights, an untested IR plan.

## How to run

```bash
# Demo mode — assesses the bundled fictional sample company
python3 assess.py --demo

# Assess your own organisation: copy sample_answers.json, edit the
# scores and evidence notes honestly, then:
python3 assess.py --file answers.json
```

Python 3, standard library only. The answers format is simple JSON: an organisation name plus, for each category, a `score` (0 to 5) and an `evidence` note that says what the score is based on.

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

The sample company is fictional. Its maturity is mixed on purpose. Detection looks decent (EDR 4/5, email filtering 4/5), but recovery and privilege let it down. You see that profile behind a lot of real incidents.

## Design notes and limitations

- **Self-assessment, not an audit.** Scores are only as honest as the input. That is why the `evidence` field is there: a reviewer can challenge a score. In a real engagement, each rating should be tied to an artefact (a restore-test report, an MFA coverage export, a tabletop record).
- **Unassessed categories** are reported as NOT ASSESSED and left out of the average, instead of being silently scored zero. They still show up in the output, because "we never looked" is itself a finding.
- The overall figure is an unweighted mean of the category scores. The critical-gap flag is kept separate from it on purpose, so a good average cannot hide a fatal weakness.
- Framework mapping is at the NIST CSF function level (Protect / Detect / Respond / Recover) for reporting. It is not a formal CSF assessment.

## License

MIT. See `LICENSE`.
