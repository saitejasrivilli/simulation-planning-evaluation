def collision_occurred(info):
    """
    Returns 1 if a collision occurred, else 0.
    """
    return int(info.get("collision", False))
