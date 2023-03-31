from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer, LAYERS
from data_structures.stack_adt import ArrayStack
import layers
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem




class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass


class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        #O(1)
        '''
        I used a stack here instead of just making it a layer object as there is no time complexity disadvantages and really no difference
        in how the code works or making it less efficient or anything, using a stack just made it easier to know whats going on
        and allowed me to make the code more robust

        self.layers_store is where the layers are stored and is a stack
        self.special_state is if special is active for the layer or not and is initially false
        '''
        self.layers_store = ArrayStack(1)
        self.special_state = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        checks if the layer is already in the store and if so it doesnt add it and returns false
        Args:
            - 1 layer 

            Raises:
            - type Error: if the layer is not actually a type Layer

            Returns:
            - result: a boolean if the layer was changed or not 

            Complexity:
            - Worst case and Best: O(1)
        """
        if self.layers_store.is_empty():
            self.layers_store.push(layer)
            return True
        current_layer = self.layers_store.peek()
        if layer == current_layer: #checking if the adding the layer will change the stack
            return False
        self.layers_store.pop() #if it will then remove the layer already there and push the new one
        self.layers_store.push(layer)
        return True

    def get_color(self, start: tuple, timestamp: float, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
            - 2 ints, x and y
            - the start value of the color which is a tuple
            - the timestamp as a float

            Raises:
            - type Error: if any of the inputs are not correct type

            Returns:
            - result: a tuple with the rgb values of the color

            Complexity:
            - Worst case and Best: O(1)
        """
        color = start

        if not self.layers_store.is_empty():
            current_layer = self.layers_store.peek()
            color = current_layer.apply(
                start, timestamp, x, y
            )  #apply is constant as it is max 3 iterations for any given layer

        if self.special_state: #if the special state is true then we do the special method which is invert
            color = layers.invert.apply(color, timestamp, x, y)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        
        Args:
            - 1 layer object

            Raises:
            - type Error: layer is not a Layer

            Returns:
            - result: a bolean if the layer was changed or not

            Complexity:
            - Worst case and Best: O(1)
        """
        if self.layers_store.is_empty():
            return False
        self.layers_store.pop() #removes the layer no matter what the arguement is
        return True

    def special(self) -> None:
        """
        Special mode. Different for each store implementation.
        changes the state of speical 
        Args:
            - None

            Raises:
            - None

            Returns:
            - None

            Complexity:
            - Worst case and Best: O(1)
        """
        self.special_state = ~self.special_state #bitwise operation to flip the state


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        '''
        creates a circualr queue to store the layers as we need first in first out principal
        '''
        self.layers_store = CircularQueue(100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        Args:
            - layer object

        Raises:
        - Exception, queue is full if it is

        Returns:
        - Boolean

        Complexity:
        - Worst case and Best: O(1)
        """
        try:
            self.layers_store.append(layer)
            return True
        except:
            return False

    def get_color(self,  start: tuple, timestamp: float, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers. 
        iterates through the queue serves each layer and applies it then adds the layer back into the queue
        Args:
            - 2 ints, x and y
            - the start value of the color which is a tuple
            - the timestamp as a float

        Raises:
        - type Error: if any of the inputs are not correct type

        Returns:
        - result: a tuple with the rgb values of the color

        Complexity:
        - Worst case and Best: O(N) N is the length of the self.layer_store
        """
        if self.layers_store.is_empty():
            return start

        current_color = start

        for _ in range(len(self.layers_store)):
            current_layer = self.layers_store.serve()
            current_color = current_layer.apply(current_color, timestamp, x, y) #O(1) as its maxed at 3
            self.layers_store.append(current_layer)

        return current_color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        serves the first element in the queue 
        Args:
            - layer object

        Raises:
        - None

        Returns:
        - Boolean

        Complexity:
        - Worst case and Best: O(1)
        """
        if self.layers_store.is_empty():
            return False
        self.layers_store.serve()
        return True

    def special(self) -> None:
        """
        Special mode. Different for each store implementation.
        reverses the store of layers and is O(N)
        Args:
            - layer object

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case and Best: O(N) N is the length of the self.layer_store
        """
        self.reversed_queue = ArrayStack(len(self.layers_store))
        for _ in range(len(self.layers_store)):  #O(N)
            self.reversed_queue.push(self.layers_store.serve())
        for _ in range(len(self.reversed_queue)):  #(N)
            self.layers_store.append(self.reversed_queue.pop())



class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.

        create a bitset that checks if the layer at that index is applying or not, 1 if it is and 0 if its not
    """
    #can use a bitset to represent if the layers are applying or not todo if i have time
    def __init__(self) -> None:
        #O(1)
        self.layers_store = BSet(len(LAYERS))

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.

        Args:
            - layer object

        Raises:
        - Type error is item input into add is not integer

        Returns:
        - Boolean

        Complexity:
        - Worst case: O(1) 
        - Best case: O(1) 
        """
        self.temp_layer_store = self.layers_store
        self.layers_store.add(layer.index+1)
        if self.layers_store.intersection(self.temp_layer_store):
            return False
        else:
            return True
                

    def get_color(self, start :tuple , timestamp: float, x:int, y: int)  -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
            - 2 ints, x and y
            - the start value of the color which is a tuple
            - the timestamp as a float

        Raises:
            - type Error: if any of the inputs are not correct type or if layer[i] is not int or input into contains is not int

        Returns:
            - result: a tuple with the rgb values of the color

        Complexity:
            - Worst case and Best: O(N)
        """
        if self.layers_store.is_empty():
            return start

        current_color = start

        for i in range(len(LAYERS)):
            try:
                if type(LAYERS[i].index) == int:
                    print(LAYERS[i].index)
                    if self.layers_store.__contains__(LAYERS[i].index+1):
                        current_layer = LAYERS[i]
                        current_color = current_layer.apply(current_color, timestamp, x, y)
            except:
                break

        return current_color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        creates a temp layer store that is the origninal unchanged layer store then
        removes layer from layer store and checks against temp layer store to see if it was changed
        Args:
            - 1 layer

        Raises:
            - type Error: if any of the inputs are not correct type

        Returns:
            - result: a bolean if the layer was changed
        Complexity:
            - Worst case and Best: O(1)
        
        """
        if self.layers_store.is_empty():
            return False
        self.temp_layer_store = self.layers_store
        self.layers_store.remove(layer.index+1)
        if self.layers_store.intersection(self.temp_layer_store):
            return False
        else:
            return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        removes the alphabetically middle layer
        Args:
        - None

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case and Best: O(N log (N))
        """
        self.alphabetical_layers_store = ArraySortedList(len(LAYERS))
        for i in range(len(LAYERS)): #O(N)
            try:
                if self.layers_store.__contains__(LAYERS[i].index+1):
                    current_layer = ListItem(LAYERS[i], LAYERS[i].name)
                    self.alphabetical_layers_store.add(current_layer) #O(log N)
            except:
                break
        if self.alphabetical_layers_store.is_empty():
            return
        middle_layer = self.alphabetical_layers_store[(len(self.alphabetical_layers_store)-1)//2].value
        self.layers_store.remove(middle_layer.index+1) #O(1)
