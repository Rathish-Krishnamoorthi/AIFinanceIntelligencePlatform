def optimize(allocated, utilization):
    return allocated * (1.08 if utilization >= .85 else .92)
