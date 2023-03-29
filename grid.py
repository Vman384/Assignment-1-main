from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore


class Grid():
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (DRAW_STYLE_SET, DRAW_STYLE_ADD, DRAW_STYLE_SEQUENCE)

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0
    def __init__(self, draw_style: str, x: int, y: int,brush_size = DEFAULT_BRUSH_SIZE) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.x = x
        self.y = y
        self.draw_style = draw_style
        self.brush_size = brush_size
        self.grid = self.create_grid(draw_style, x, y)

    def create_grid(self, draw_style: str, x: int, y: int) -> ArrayR(ArrayR()):
        """
            makes a nested list with lists of length y storing layerstore object repeated in list of length x
            example with x and y 3[[Layerstore,Layerstore,Layerstore],[Layerstore,Layerstore,Layerstore],[Layerstore,Layerstore,Layerstore]]


            Args:
            - 2 ints, x and y
            - 1 string, which is the draw style

            Raises:
            - type Error: if draw style is invalid

            Returns:
            - result: a nested array with layerstore objects for each element 

            Complexity:
            - Worst case and Best: O(N^2), assuming x and y are same length
        """
        self.grid = ArrayR(x)
        for i in range(x):
            temp_list = ArrayR(y)
            for j in range(y):
                if draw_style == self.DRAW_STYLE_SET:
                    temp_list[j] = SetLayerStore()
                elif draw_style == self.DRAW_STYLE_ADD:
                    temp_list[j] = AdditiveLayerStore()
                elif draw_style == self.DRAW_STYLE_SEQUENCE:
                    temp_list[j] = SequenceLayerStore()
                else:
                    raise TypeError('Invalid Draw Style Invalid')
            self.grid[i] = temp_list
        return self.grid

    #using the magic method to return the layerstore value at that coordinate, technically getitem is called twice
    def __getitem__(
        self, index: int
    ) -> SetLayerStore or AdditiveLayerStore or SequenceLayerStore:
        """
            gets the layer store object at the x and y coordinate

            Args:
            - 2 ints, x and y

            Raises:
            - Index Error: if the x or y input is out of range

            Returns:
            - result: Layer store object, the type hint

            Complexity:
            - Worst case and Best: O(1), getting an element from refrential array is always constant
        """
        return self.grid[index]

    def increase_brush_size(self) -> int:
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        Args:
            None

        Raises:
            None just says if the brush size is invalid

        Returns:
            - the new brush size

        time complexity = O(1)
        """
        # checks to see if brush size is less than max brush size, otherwise returns the increased brush size
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size += 1
            print(f'increased brush size to {self.brush_size}')
        else:
            print('brush size is already max')
        return self.brush_size

    def decrease_brush_size(self) -> int:
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.

        Args:
            None

        Raises:
            None, just says if the brush size is invalid

        Returns:
            - the new brush size

        time complexity = O(1)
        """
        # checks to see if brush size is more than min brush size, otherwise returns the decreased brush size
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size -= 1
            print(f'decreased brush size to {self.brush_size}')
        else:
            print('brush size is already min')
        return self.brush_size

    def special(self) -> None:
        """
        Activate the special affect on all grid squares.
        Args:
            None

        Raises:
            None but the special function in the layer store will raise something depending on which one, could be 
            index error 

        Returns:
            - Nothing

        time complexity = O(N^2) best and worst as it is nested for loop, ignoring the time complexity of special as that is different for each 
        layer store type
        """
        for i in range(self.x):
            for j in range(self.y):
                self.grid[i][j].special()
