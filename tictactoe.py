from gym import spaces
import gym

NULL_MARK = ' '
NOUGHT_MARK = 'O'
CROSS_MARK = 'X'

NULL_CODE = 0
NOUGHT_CODE = 1
CROSS_CODE = 2
MY_CODE = 1
ENEMY_CODE = 2

NO_REWARD = 0
WIN_REWARD = 1
LOSE_REWARD = -1

CODE_TO_MARK = {
    NULL_CODE: NULL_MARK,
    NOUGHT_CODE: NOUGHT_MARK,
    CROSS_CODE: CROSS_MARK
}


class TicTacToeEnv(gym.Env):
    def __init__(self, symmetrical_view=False, use_action_mask=False):
        self.symmetrical_view = symmetrical_view
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Discrete(9)
        self.use_action_mask = use_action_mask

        self.occupied_locations = set()
        self.board = None
        self.mark = None
        self.start_mark = None
        self.done = None

    def reset(self, start_mark=NOUGHT_MARK):
        self.occupied_locations.clear()
        self.board = [0] * 9
        self.mark = start_mark
        self.start_mark = start_mark
        self.done = False
        return self._get_state()

    def step(self, action):
        if self.done:
            return self._get_state(), 0, True, None

        location = action
        if location in self.occupied_locations:
            raise ValueError('Invalid action on an occupied position')
        self.occupied_locations.add(location)
        self.board[location] = to_code(self.mark)

        status = check_game_status(self.board)
        rewards = [NO_REWARD, NO_REWARD]
        if status >= 0:
            self.done = True
            if status in [1, 2]:
                if self.mark == self.start_mark:
                    rewards = [WIN_REWARD, LOSE_REWARD]
                else:
                    rewards = [LOSE_REWARD, WIN_REWARD]

        # Switch turn.
        self.mark = next_mark(self.mark)
        return self._get_state(), rewards, self.done, None

    def render(self, show_number=False):
        def mark(i):
            if not show_number or self.board[i] != 0:
                return to_mark(self.board[i])
            else:
                return str(i)

        if self.done:
            self._show_result()
            return

        for j in range(0, 9, 3):
            print('  ' + '|'.join([mark(i) for i in range(j, j + 3)]))
            if j < 6:
                print('  ' + '-----')
        print(f"{self.mark}'s turn.")
        print()

    def available_actions(self):
        return set(range(9)) - self.occupied_locations

    def _get_state(self):
        state = self.board.copy()
        if self.symmetrical_view:
            for loc in range(9):
                if to_mark(state[loc]) == self.mark:
                    state[loc] = MY_CODE
                elif state[loc] == NULL_CODE:
                    pass
                else:
                    state[loc] = ENEMY_CODE

        if self.use_action_mask:
            action_mask = [loc not in self.occupied_locations
                           for loc in range(9)]
            return state, action_mask
        else:
            return state

    def _show_result(self):
        status = check_game_status(self.board)
        if status == 0:
            print('==== Finished: Draw ====')
        else:
            msg = f"Winner is '{to_mark(status)}'!"
            print(f'==== Finished: {msg} ====')
        print()


def to_mark(code):
    return CODE_TO_MARK[code]


def to_code(mark):
    return NOUGHT_CODE if mark == NOUGHT_MARK else CROSS_CODE


def next_mark(mark):
    return CROSS_MARK if mark == NOUGHT_MARK else NOUGHT_MARK


def check_game_status(board):
    """Return game status by current board status.

    :param board: Current board state
    :return: Status code
            -1: game in progress
            0: draw game,
            1 or 2 for finished game(winner code).
    """
    for t in [NOUGHT_CODE, CROSS_CODE]:
        for j in range(0, 9, 3):
            if [t] * 3 == [board[i] for i in range(j, j + 3)]:
                return t
        for j in range(0, 3):
            if board[j] == t and board[j + 3] == t and board[j + 6] == t:
                return t
        if board[0] == t and board[4] == t and board[8] == t:
            return t
        if board[2] == t and board[4] == t and board[6] == t:
            return t

    for i in range(9):
        if board[i] == 0:
            # Still playing
            return -1

    # Draw
    return 0
