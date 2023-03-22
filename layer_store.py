from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
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
        self.layers_store = ArrayStack(1)
        self.special_state = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        O(1)
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

    def get_color(self, start, timestamp, x, y)  -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        O(1)
        """
        color = start

        if not self.layers_store.is_empty():
            current_layer = self.layers_store.peek()
            color = current_layer.apply(start, timestamp, x, y)

        if self.special_state:
            color = layers.invert.apply(color,timestamp, x, y)

        return color


    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        O(1)
        """
        if self.layers_store.is_empty():
            return False
        self.layers_store.pop()
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        O(1)
        """
        if self.special_state == False:
            self.special_state = True
            return self.special_state
        elif self.special_state == True:
            self.special_state = False
            return self.special_state
        

        
        



class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self) -> None:
        #O(1)
        self.layers_store = CircularQueue(100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        O(1)
        """
        self.layers_store.append(layer)
        return True

    def get_color(self, start, timestamp, x, y)  -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        O(N)
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
        O(1)
        """
        if self.layers_store.is_empty():
            return False
        self.layers_store.serve()
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        reverses the store of layers and is O(N)
        """
        self.reversed_queue = ArrayStack(100)
        for _ in range(len(self.layers_store)): #O(N)
            self.reversed_queue.push(self.layers_store.serve())
        for _ in range(len(self.reversed_queue)): #(N)
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
        self.layers_store = ArraySortedList(100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        O(Log(N))
        """
        layer_to_insert = ListItem(layer, layer.index)
        self.layers_store.add(layer_to_insert)
        return True
                


        return True

    def get_color(self, start :tuple , timestamp: float, x:int, y: int)  -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        O(N)
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
        O(N)
        best case of one is worst case of other 
        """
        deleted = False
        offset = 0
        if self.layers_store.is_empty():
            return deleted
        for i in  range(len(self.layers_store)):
            if self.layers_store[i].value == layer:
                self.layers_store.delete_at_index(i+offset)
                offset -=1
                deleted = True
        return deleted

    def special(self):
        """
        Special mode. Different for each store implementation.
        reverses the store of layers and is O(NLog(N))
        """
        self.alphabetical_layers_store = ArraySortedList(len(self.layers_store))
        for i in range(len(self.layers_store)):
            current_layer = ListItem(self.layers_store[i], self.layers_store[i].value.name)
            self.alphabetical_layers_store.add(current_layer)
        self.layers_store.delete_at_index(self.layers_store.index(self.alphabetical_layers_store[(len(self.alphabetical_layers_store)-1)//2].value))

                
