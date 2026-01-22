def aggregate(metrics, key):
    return sum(m[key] for m in metrics) / len(metrics)
