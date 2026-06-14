# Volcano Gang Scheduling Checklist

> **Provenance:** Volcano Scheduler documentation; Kubernetes batch scheduling patterns; NVIDIA MIG GPU sharing guides.

- [ ] PodGroup `minMember` matches required worker count
- [ ] Queue declares GPU capability quota
- [ ] Job `schedulerName` is `volcano`
- [ ] Job `minAvailable` >= 2 for gang scheduling
- [ ] Fractional GPU keys present (`nvidia.com/gpu`, MIG partitions)
- [ ] Shared memory volume mounted for distributed training
- [ ] Dry-run validation passes: `python training/validate_k8s.py`
