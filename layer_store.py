from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.stack_adt import ArrayStack
import layers
from data_structures.queue_adt import CircularQueue

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
        self.layers_store = ArrayStack(1)
        self.special_state = False

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
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
        """
        if self.layers_store.is_empty():
            return start
        current_layer = self.layers_store.peek()
        color = current_layer.apply(start, timestamp, x, y)
        if self.special_state:
            color = layers.invert.apply(color,timestamp, x, y)
        return color


    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.layers_store.is_empty():
            return False
        self.layers_store.pop()
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
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
        self.layers_store = CircularQueue(100)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        self.layers_store.append(layer)
        return True

    def get_color(self, start, timestamp, x, y)  -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
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
        """
        if self.layers_store.is_empty():
            return False
        self.layers_store.serve()
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        self.reversed_queue = ArrayStack(100)
        for _ in range(len(self.layers_store)):
            self.reversed_queue.push(self.layers_store.serve())
        for _ in range(len(self.reversed_queue)):
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
    #stack of layers
    pass
