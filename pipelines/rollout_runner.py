def run_episode(env, planner):
    state = env.reset()
    planner.reset()

    done = False
    info = {}

    while not done:
        action = planner.act(state)
        state, _, done, info = env.step(action)

    return info
