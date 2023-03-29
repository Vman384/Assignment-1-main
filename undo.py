from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    def __init__(self) -> None:
        self.undo_tracker = ArrayStack(10000)
        self.redo_tracker = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if self.undo_tracker.is_full():
            return
        self.undo_tracker.push(action)

        self.redo_tracker.clear()

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.undo_tracker.is_empty():
            return None
        undo_action = self.undo_tracker.pop()
        self.redo_tracker.push(undo_action)
        undo_action.undo_apply(grid)
        return undo_action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.redo_tracker.is_empty():
            return
        redo_action = self.redo_tracker.pop()
        self.undo_tracker.push(redo_action)
        redo_action.redo_apply(grid)
        return redo_action
