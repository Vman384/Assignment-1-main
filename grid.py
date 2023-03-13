from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import SetLayerStore, AdditiveLayerStore, SequenceLayerStore
from layer_util import Layer

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
        self.x=x
        self.y=y    
        self.draw_style=draw_style
        self.brush_size=brush_size
        self.grid = self.create_grid(draw_style, x, y)
       

    def create_grid(self, draw_style, x, y):
        #made a nested list with lists of length y storing layerstore object repeated in list of length x
        #example with x and y 3[[Layerstore,Layerstore,Layerstore],[Layerstore,Layerstore,Layerstore],[Layerstore,Layerstore,Layerstore]]
        #making the an instace of the grid object that is an array of length x (x or y doesnt matter)
        #O(n^2)
        self.grid = ArrayR(x)
        temp_list = ArrayR(y)
        for i in range(x):
            for j in range(y):
                if draw_style ==  'SET':
                    temp_list[j] = SetLayerStore()
                    print(temp_list[j])
                elif draw_style == 'ADD':
                    temp_list[j] = AdditiveLayerStore()
                elif draw_style == "SEQUENCE":
                    temp_list[j] = SequenceLayerStore()
                else:
                    raise TypeError('Invalid Draw Style Invalid')
            self.grid[i] = temp_list
            print(self.grid[0][0])
        return self.grid

    #using the magic method to return the layerstore value at that coordinate, technically getitem is called twice
    def __getitem__(self,index): 
        return self.grid[index]
    

    def increase_brush_size(self,MAX_BRUSH):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        # checks to see if brush size is less than max brush size, otherwise returns the increased brush size
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
        # checks to see if brush size is more than min brush size, otherwise returns the decreased brush size
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

