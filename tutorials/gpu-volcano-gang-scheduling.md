# GPU Volcano Gang Scheduling

## Goal

Provision all distributed training workers simultaneously.

## Steps

1. Configure `k8s/volcano/podgroup.yaml` minMember.
2. Set fractional GPU in `k8s/volcano/training-job.yaml`.
3. Validate: `python training/validate_k8s.py`.

Skill: `skills/distributed-gpu-training-and-scheduling/SKILL.md`
