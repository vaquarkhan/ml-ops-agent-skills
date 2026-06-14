---
name: distributed-gpu-training-and-scheduling
description: Configures Kubernetes Volcano gang scheduling and fractional GPU training jobs. Use for distributed PyTorch training, PodGroup CRDs, queue specs, and dry-run manifest validation.
---

# Distributed GPU Training and Scheduling

## Overview

Provision gang-scheduled GPU worker pods with Volcano, configure fractional GPU sharing (MIG/HAMi), and validate manifests before cluster apply.

## When to Use

- authoring or reviewing K8s training manifests
- configuring Volcano PodGroup minMember and queue specs
- validating YAML before deployment
- debugging resource deadlocks in distributed training

## Workflow

1. Review Volcano Queue in `k8s/volcano/queue.yaml`.
2. Configure PodGroup gang scheduling in `k8s/volcano/podgroup.yaml`.
3. Set fractional GPU requests in `k8s/volcano/training-job.yaml`.
4. Dry-run validate with `python training/validate_k8s.py`.
5. Run tests: `pytest tests/test_k8s_validation.py -v`.

## Verification

- [ ] PodGroup minMember ensures simultaneous worker provisioning
- [ ] Queue capability includes GPU quota
- [ ] Job uses `schedulerName: volcano` and fractional GPU keys
- [ ] Python validator returns PASS for all manifests
