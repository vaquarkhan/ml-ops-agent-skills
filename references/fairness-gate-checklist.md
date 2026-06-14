# Fairness Gate Checklist

> **Provenance:** Fairlearn documentation; Microsoft Responsible AI Standard; NIST AI RMF fairness considerations.

- [ ] Sensitive feature identified and documented
- [ ] Demographic parity difference computed via Fairlearn
- [ ] Equalized odds difference logged
- [ ] DP threshold configured (default 0.05)
- [ ] Model Card generated with metrics and lineage
- [ ] CI gate fails pipeline when threshold exceeded
- [ ] Intended use and limitations documented in Model Card
