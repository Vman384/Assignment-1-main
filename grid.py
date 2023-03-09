from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import LayerStore

class Grid():
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0
    def __init__(self, draw_style, x, y,brush_size = DEFAULT_BRUSH_SIZE) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.grid: ArrayR[ArrayR[str]] = ArrayR(x)
        self.grid[:] = [[LayerStore for i in range(y)] for j in range(x)]
        self.draw_style=draw_style
        self.brush_size=brush_size


    """def __getattr__(self):
        return getattr(self.brush_size)"""

    def __getitem__(self, index:tuple):
        x, y = index
        return self.grid[x][y]


    def increase_brush_size(self,MAX_BRUSH):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size<MAX_BRUSH:
            self.brush_size+=1
            print('increased brush size')
        else:
            print('brush size is already max')
        return self.brush_size

    def decrease_brush_size(self,MIN_BRUSH):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size<MIN_BRUSH:
            self.brush_size-=1
            print('decreased brush size')
        else:
            print('brush size is already min')
        return self.brush_size

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        raise NotImplementedError()
