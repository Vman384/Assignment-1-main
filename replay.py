from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue


class ReplayTracker:

    def __init__(self) -> None:
        self.replay_tracker = CircularQueue(1000)

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Args:
        - Bolean
        - Paintaction

        Raises:
        - Exception if is full

        Returns:
        - None.

        Complexity:
        - Worst case and Best: O(N)
        """
        self.replay_tracker.append((action, is_undo))

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Args:
        - Grid object

        Raises:
        - None

        Returns:
        - Bolean

        Complexity:
        - Worst case and Best: O(N)
        """
        if self.replay_tracker.is_empty():
            return True
        redo_layer = self.replay_tracker.serve()
        redo_layer, is_undo = redo_layer
        if is_undo:
            redo_layer.undo_apply(grid) #O(N)
        else:
            redo_layer.redo_apply(grid) #O(N)
        return False


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g)  # action 1, special
    f2 = r.play_next_action(g)  # action 2, draw
    f3 = r.play_next_action(g)  # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)
