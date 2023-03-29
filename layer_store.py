from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer, LAYERS
from data_structures.stack_adt import ArrayStack
import layers
from data_structures.queue_adt import CircularQueue
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
        if layer == current_layer:
            return False
        self.layers_store.pop()
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

        if self.special_state:
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
        self.layers_store.pop()
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
        self.special_state = ~self.special_state


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
        - Worst case and Best: O(N)
        """
        if self.layers_store.is_empty():
            return start

        current_color = start

        for _ in range(len(self.layers_store)):
            current_layer = self.layers_store.serve()
            current_color = current_layer.apply(current_color, timestamp, x, y)
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
        - Worst case and Best: O(N)
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
    """

    def __init__(self) -> None:
        #O(1)
        self.layers_store = ArraySortedList(10 * len(LAYERS))

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        contains didnt work with my implementation as it checks if the listitem object is the same, which it wont be if i create 
        a new instance of it to add so instead i go through and check the value of the listitem object in the layer store and see 
        if it is the same as the one i am trying to add in. This results in same time complexity so no loss, I would change
        the implementation of contains but am not allowed so rip.

        Args:
            - layer object

        Raises:
        - Exception, queue is full if it is

        Returns:
        - Boolean

        Complexity:
        - Worst case: O(N) if item is not in list
        - Best case: O(1) if item is the first item
        """
        for i in range(len(self.layers_store)):
            if self.layers_store[i].value == layer: #its just adding .value as contains checks for the same list item object
                #however contains takes the arguement of a list item object so we need to create one but then its not the same
                #as the others in the layer as its a new object therefore contains never finds it so i had to do it this way
                return False
        else:
            layer_to_insert = ListItem(layer, layer.index)
            self.layers_store.add(layer_to_insert)
        return True
                

    def get_color(self, start :tuple , timestamp: float, x:int, y: int)  -> tuple[int, int, int]:
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
            - Worst case and Best: O(N)
        """
        if self.layers_store.is_empty():
            return start

        current_color = start

        for i in range(len(self.layers_store)):
            current_layer = self.layers_store[i].value
            current_color = current_layer.apply(current_color, timestamp, x, y)

        return current_color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        best case of one is worst case of other, an improvement could be to instead change the start value instead of shuffling 
        everything left when we delete at the first index, this would get our best case down to O(1)
        Args:
            - 1 layer

        Raises:
            - type Error: if any of the inputs are not correct type

        Returns:
            - result: a bolean if the layer was changed
        Complexity:
            - Worst case and Best: O(N^2)
            I could also have had a tuple for the layer to check if it was applying however, I would 
            have had to make the sorted list initialised with all the layers and them applying false
            that just seemed very hard cody to me therefore i took this approach. It would have not been
            hard cody but LAYERS had a len of 20 when there is only 8 layers so is there more layers for later on????
        
        """
        if self.layers_store.is_empty():
            return False
        for i in range(len(self.layers_store)): #O(N)
            if self.layers_store[i].value == layer:
                self.layers_store.delete_at_index(i) #O(N) as has to shuffle
                return True
        return False

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
        - Worst case and Best: O(N^2)
        """
        self.alphabetical_layers_store = ArraySortedList(len(self.layers_store))
        for i in range(len(self.layers_store)): #O(N)
            current_layer = ListItem(self.layers_store[i], self.layers_store[i].value.name)
            self.alphabetical_layers_store.add(current_layer) #O(N)
        if self.alphabetical_layers_store.is_empty():
            return
        middle_layer = self.alphabetical_layers_store[(len(self.alphabetical_layers_store)-1)//2].value
        self.layers_store.delete_at_index(self.layers_store.index(middle_layer)) #O(N log(N))
