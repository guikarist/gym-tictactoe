from tictactoe import TicTacToeEnv

# Enable symmetrical view and action mask.
env = TicTacToeEnv(symmetrical_view=True, use_action_mask=True)

state = env.reset()
done = False
print('Initial state:', state)
env.render(show_number=True)

while not done:
    action = int(input())
    state, reward, done, info = env.step(action)
    print('Current State:', state)
    env.render(show_number=True)
