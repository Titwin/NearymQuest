import math
  
class Vector2f:
# constructor
    def __init__(self, x=0.0, y=0.0): 
        self.x, self.y = x, y

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def __cast(self,component):
        return float(component)

# Binary Operators
    ### +
    def __add__(self, other): 
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x+other.x,self.y+other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x+other,self.y+other)
    def __radd__(self, other): 
       return Vector2f.__add__(self,other)

    ### -
    def __sub__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x-other.x,self.y-other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x-other,self.y-other)
    def __rsub__(self, other): 
       return Vector2f.__add__(-self,other)
       
    ### *
    def __mul__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x*other.x,self.y*other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x*other,self.y*other)
    def __rmul__(self, other):
        return Vector2f.__mul__(self,other)

    ### /
    def __truediv__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x/other.x,self.y/other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x/other,self.y/other)
    def __rtruediv__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(other.x/self.x,other.y/self.y)
        elif isinstance(other, (int,float)):
            return Vector2f(other/self.x,other/self.y)
    ### //
    def __floordiv__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x//other.x,self.y//other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x//other,self.y//other)
    ### %
    def __mod__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x/other.x,self.y/other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x/other,self.y/other)
    ### **
    def __pow__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2f(self.x**other.x,self.y**other.y)
        elif isinstance(other, (int,float)):
            return Vector2f(self.x**other,self.y**other)

    ### ==
    def __eq__(self, other):
        return isinstance(other, (Vector2f,Vector2i)) and self.x == other.x and self.y == other.y

    def dot(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return self.x*other.x+self.y*other.y

# Unary Operators    
    def __neg__(self):
        return Vector2f(-self.x, -self.y)

    @property    
    def magnitude(self):
        return math.sqrt(self.magnitudeSqr)
    @property
    def magnitudeSqr(self):
        return self.x*self.x+self.y*self.y

    @property
    def normalized(self):
        mag = self.magnitude
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            self.x /= mag
            self.y /= mag

    def normalize(self):
        mag = self.magnitude
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            return Vector2f(self.x/mag,self.y/mag)

# Commodity constructors
    #@property
    #def zero(self):
    #    global __zero
    #    return __zero

    #@property
    #def one(self):
    #    return Vector2f(1,1)
#__zero = Vector2f(0,0)


  
class Vector2i:

# constructor
    def __init__(self, x=0, y=0): 
        self._x = self.__cast(x) 
        self._y = self.__cast(y)

# getters and setters 
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = self.__cast(new_x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = self.__cast(new_y)

    def __str__(self):
        return "("+str(self._x)+","+str(self._y)+")"

    def __cast(self,component):
        return int(component)

# Binary Operators
    ### +
    def __add__(self, other): 
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x+other.x,self.y+other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x+other,self.y+other)
    def __radd__(self, other): 
       return Vector2i.__add__(self,other)

    ### -
    def __sub__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x-other.x,self.y-other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x-other,self.y-other)
    def __rsub__(self, other): 
       return Vector2i.__add__(-self,other)
       
    ### *
    def __mul__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x*other.x,self.y*other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x*other,self.y*other)
    def __rmul__(self, other):
        return Vector2i.__mul__(self,other)

    ### /
    def __truediv__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x/other.x,self.y/other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x/other,self.y/other)
    def __rtruediv__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(other.x/self.x,other.y/self.y)
        elif isinstance(other, (int,float)):
            return Vector2i(other/self.x,other/self.y)
    ### //
    def __floordiv__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x//other.x,self.y//other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x//other,self.y//other)
    ### %
    def __mod__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x/other.x,self.y/other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x/other,self.y/other)
    ### **
    def __pow__(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return Vector2i(self.x**other.x,self.y**other.y)
        elif isinstance(other, (int,float)):
            return Vector2i(self.x**other,self.y**other)

    ### ==
    def __eq__(self, other):
        return isinstance(other, (Vector2f,Vector2i)) and self.x == other.x and self.y == other.y

    def dot(self, other):
        if isinstance(other, (Vector2f,Vector2i)):
            return self.x*other.x+self.y*other.y

# Unary Operators    
    def __neg__(self):
        return Vector2i(-self.x, -self.y)

    @property    
    def magnitude(self):
        return math.sqrt(self.magnitudeSqr)
    @property
    def magnitudeSqr(self):
        return self.x*self.x+self.y*self.y

    @property
    def normalized(self):
        mag = self.magnitude()
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            self.x /= mag
            self.y /= mag

    def normalize(self):
        mag = self.magnitude()
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            return Vector2f(self.x/mag,self.y/mag)

# Commodity constructors
    @property
    def zero(self):
        return Vector2i(0,0)

    @property
    def one(self):
        return Vector2i(1,1)
        
        

