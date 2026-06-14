# Fairness Gate Checklist

Use before promoting models to production or publishing Model Cards.

> **Provenance:** Fairlearn documentation; Microsoft Responsible AI Standard; NIST AI RMF fairness considerations.

- [ ] Sensitive feature identified and documented
- [ ] Demographic parity difference computed via Fairlearn
- [ ] Equalized odds difference logged
- [ ] DP threshold configured (default 0.05)
- [ ] Model Card generated with metrics and lineage
- [ ] CI gate fails pipeline when threshold exceeded
- [ ] Intended use and limitations documented in Model Card

## Sources

| Source | URL | Last reviewed |
|--------|-----|---------------|
| Fairlearn — Metrics | https://fairlearn.org/main/user_guide/assessment/common_fairness_metrics.html | 2026-06-14 |
| Fairlearn — MetricFrame | https://fairlearn.org/main/user_guide/assessment/general_purpose_metrics.html | 2026-06-14 |
| Microsoft Responsible AI Standard v2 | https://www.microsoft.com/en-us/ai/responsible-ai | 2026-06-14 |
| NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | 2026-06-14 |
| Model Cards for Model Reporting (Mitchell et al.) | https://arxiv.org/abs/1810.03993 | 2026-06-14 |
| Runnable reference | `governance/fairness.py` | 2026-06-14 |
