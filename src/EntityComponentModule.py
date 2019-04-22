
class Entity:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._w = 16
        self._h = 16
        self.__components = {}

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, new_x):
        self._x = float(new_x)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, new_y):
        self._y = float(new_y)

    @property
    def w(self):
        return self._w
    @w.setter
    def w(self, new_w):
        self._w = float(new_w)

    @property
    def h(self):
        return self._h
    @h.setter
    def h(self, new_h):
        self._h = float(new_h)

    def GetComponent(self, component):
        if components in self.__components:
            return self.__components[component]


class Component:
    #@abstractmethod
    #def start(self):
    #    print("start here")
    #@abstractmethod
    #def update(self):
    #    print("update here")
    #@abstractmethod    
    #def draw(self):
    #    print("draw here")    