import math


class Vector3f:

# constructor
    def __init__(self, x=0, y=0, z=0): 
        self._x = self.__cast(x) 
        self._y = self.__cast(y) 
        self._z = self.__cast(z) 

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

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, new_z):
        self._z = self.__cast(new_z)

    def __str__(self):
        return "("+str(self._x)+","+str(self._y)+","+str(self._z)+")"

    def __cast(self,component):
        return float(component)
        
# Binary Operators
    ### +
    def __add__(self, other): 
        if isinstance(other, Vector3f):
            return Vector3f(self.x+other.x,self.y+other.y,self.z+other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x+other,self.y+other,self.z+other)
        elif isinstance(other, Vector2f):
            return Vector3f(self.x+other.x,self.y+other.y,self.z)
    def __radd__(self, other): 
       return Vector3f.__add__(self,other)

    ### -
    def __sub__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x-other.x,self.y-other.y,self.z-other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x-other,self.y-other,self.z-other)
        elif isinstance(other, Vector2f):
            return Vector3f(self.x-other.x,self.y-other.y,self.z)
    def __rsub__(self, other): 
       if isinstance(other, Vector3f):
           return Vector3f(-self.x+other.x,-self.y+other.y,-self.z+other.z)
       elif isinstance(other, (int,float)):
           return Vector3f(-self.x+other,-self.y+other,-self.z+other)
       elif isinstance(other, Vector2f):
            return Vector3f(-self.x+other.x,-self.y+other.y,-self.z)
       
    ### *
    def __mul__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x*other.x,self.y*other.y,self.z*other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x*other,self.y*other,self.z*other)
        elif isinstance(other, Vector2f):
            return Vector3f(self.x*other.x,self.y*other.y,self.z)
    def __rmul__(self, other):
        return Vector3f.__mul__(self,other)

    ### /
    def __truediv__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x/other.x,self.y/other.y,self.z/other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x/other,self.y/other,self.z/other)
    def __rtruediv__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(other.x/self.x,other.y/self.y,other.z/self.z)
        elif isinstance(other, (int,float)):
            return Vector3f(other/self.x,other/self.y,other/self.z)
    ### //
    def __floordiv__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x//other.x,self.y//other.y,self.z//other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x//other,self.y//other,self.z//other)
    ### %
    def __mod__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x/other.x,self.y/other.y,self.z/other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x/other,self.y/other,self.z/other)
    ### **
    def __pow__(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.x**other.x,self.y**other.y,self.z**other.z)
        elif isinstance(other, (int,float)):
            return Vector3f(self.x**other,self.y**other,self.z**other)

    ### ==
    def __eq__(self, other):
        return isinstance(other, Vector3f) and self.x == other.x and self.y == other.y and self.z == other.z

    def dot(self, other):
        if isinstance(other, Vector3f):
            return self.x*other.x+self.y*other.y+self.z*other.z
    
    def cross(self, other):
        if isinstance(other, Vector3f):
            return Vector3f(self.y*other.z - self.z*other.y,
                            self.z*other.x - self.x*other.z,
                            self.x*other.y - self.y*other.x)

# Unary Operators    
    def __neg__(self):
        return Vector3f(-self.x, -self.y, -self.z)

    @property    
    def magnitude(self):
        return math.sqrt(self.magnitudeSqr)
    @property
    def magnitudeSqr(self):
        return self.x*self.x+self.y*self.y+self.z*self.z

    @property
    def normalized(self):
        mag = self.magnitude()
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            self.x /= mag
            self.y /= mag
            self.z /= mag

    def normalize(self):
        mag = self.magnitude()
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            return Vector3f(self.x/mag,self.y/mag,self.z/mag)

# Commodity constructors
    @property
    def zero(self):
        return Vector3f(0,0,0)

    @property
    def one(self):
        return Vector3f(1,1,1)







class Vector3i:

# constructor
    def __init__(self, x=0, y=0, z=0): 
        self._x = self.__cast(x) 
        self._y = self.__cast(y) 
        self._z = self.__cast(z) 

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

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, new_z):
        self._z = self.__cast(new_z)

    def __str__(self):
        return "("+str(self._x)+","+str(self._y)+","+str(self._z)+")"

    def __cast(self,component):
        return int(component)

# Binary Operators
    ### +
    def __add__(self, other): 
        if isinstance(other, Vector3i):
            return Vector3i(self.x+other.x,self.y+other.y,self.z+other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x+other,self.y+other,self.z+other)
        elif isinstance(other, Vector2i):
            return Vector3i(self.x+other.x,self.y+other.y,self.z)
    def __radd__(self, other): 
       return Vector3i.__add__(self,other)

    ### -
    def __sub__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.x-other.x,self.y-other.y,self.z-other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x-other,self.y-other,self.z-other)
        elif isinstance(other, Vector2i):
            return Vector3i(self.x-other.x,self.y-other.y,self.z)
    def __rsub__(self, other): 
       if isinstance(other, Vector3i):
           return Vector3i(-self.x+other.x,-self.y+other.y,-self.z+other.z)
       elif isinstance(other, (int,float)):
           return Vector3i(-self.x+other,-self.y+other,-self.z+other)
       elif isinstance(other, Vector2i):
            return Vector3i(-self.x+other.x,-self.y+other.y,-self.z)
       
    ### *
    def __mul__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.x*other.x,self.y*other.y,self.z*other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x*other,self.y*other,self.z*other)
        elif isinstance(other, Vector2i):
            return Vector3i(self.x*other.x,self.y*other.y,self.z)
    def __rmul__(self, other):
        return Vector3i.__mul__(self,other)

    ### /
    def __truediv__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.x/other.x,self.y/other.y,self.z/other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x/other,self.y/other,self.z/other)
    def __rtruediv__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(other.x/self.x,other.y/self.y,other.z/self.z)
        elif isinstance(other, (int,float)):
            return Vector3i(other/self.x,other/self.y,other/self.z)
    ### //
    def __floordiv__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.x//other.x,self.y//other.y,self.z//other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x//other,self.y//other,self.z//other)
    ### %
    def __mod__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.x/other.x,self.y/other.y,self.z/other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x/other,self.y/other,self.z/other)
    ### **
    def __pow__(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.x**other.x,self.y**other.y,self.z**other.z)
        elif isinstance(other, (int,float)):
            return Vector3i(self.x**other,self.y**other,self.z**other)

    ### ==
    def __eq__(self, other):
        return isinstance(other, Vector3i) and self.x == other.x and self.y == other.y and self.z == other.z

    def dot(self, other):
        if isinstance(other, Vector3i):
            return self.x*other.x+self.y*other.y+self.z*other.z
    
    def cross(self, other):
        if isinstance(other, Vector3i):
            return Vector3i(self.y*other.z - self.z*other.y,
                            self.z*other.x - self.x*other.z,
                            self.x*other.y - self.y*other.x)

# Unary Operators    
    def __neg__(self):
        return Vector3i(-self.x, -self.y, -self.z)

    @property    
    def magnitude(self):
        return math.sqrt(self.magnitudeSqr)
    @property
    def magnitudeSqr(self):
        return self.x*self.x+self.y*self.y+self.z*self.z

    @property
    def normalized(self):
        mag = self.magnitude()
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            self.x /= mag
            self.y /= mag
            self.z /= mag

    def normalize(self):
        mag = self.magnitude()
        if mag == 0 :
            raise Exception('Magnitude is zero')
        else:
            return Vector3f(self.x/mag,self.y/mag,self.z/mag)

# Commodity constructors
    @property
    def zero(self):
        return Vector3i(0,0,0)

    @property
    def one(self):
        return Vector3i(1,1,1)
        

