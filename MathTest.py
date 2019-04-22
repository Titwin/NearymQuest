import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')

# import modules
import pyxel
from Vector import *

class Test:
     def __init__(self):
        a = Vector2f(0.1,2.3)
        b = Vector2f(1,0.25)
        c = 3
        print("Vector2f operations")
        print(""+str(a)+" + "+str(b)+" = "+ str(a+b))
        print(""+str(a)+" + "+str(c)+" = "+ str(a+c))
        print(""+str(c)+" + "+str(a)+" = "+ str(c+a))
        
        print(""+str(a)+" - "+str(b)+" = "+ str(a-b))
        print(""+str(a)+" - "+str(c)+" = "+ str(a-c))
        print(""+str(c)+" - "+str(a)+" = "+ str(c-a))
        
        print(""+str(a)+" * "+str(b)+" = "+ str(a*b))
        print(""+str(a)+" * "+str(c)+" = "+ str(a*c))
        print(""+str(c)+" * "+str(a)+" = "+ str(c*a))
        
        print(""+str(a)+" / "+str(b)+" = "+ str(a/b))
        print(""+str(a)+" / "+str(c)+" = "+ str(a/c))
        print(""+str(c)+" / "+str(a)+" = "+ str(c/a))

        print(""+str(a)+" == "+str(b)+" = "+ str(a==b))
        print(""+str(a)+" == "+str(a)+" = "+ str(a==a))
        print(""+str(a)+" == "+str(c)+" = "+ str(a==c))
        print(""+str(c)+" == "+str(a)+" = "+ str(c==a))
        
        print("dot("+str(a)+","+str(b)+") = "+ str(a.dot(b)))
        print("----")
        
        print("Vector3f operations")
        a = 0
        b = 0

        a = Vector3f(1,2,3)
        a2 = Vector3f(2,1,3)
        b = Vector2f(0.25,0.5)
        c = 3
        print(""+str(a)+" + "+str(b)+" = "+ str(a+b))
        print(""+str(a)+" + "+str(c)+" = "+ str(a+c))
        print(""+str(c)+" + "+str(a)+" = "+ str(c+a))
        
        print(""+str(a)+" - "+str(b)+" = "+ str(a-b))
        print(""+str(a)+" - "+str(c)+" = "+ str(a-c))
        print(""+str(c)+" - "+str(a)+" = "+ str(c-a))
        
        print(""+str(a)+" * "+str(b)+" = "+ str(a*b))
        print(""+str(a)+" * "+str(c)+" = "+ str(a*c))
        print(""+str(c)+" * "+str(a)+" = "+ str(c*a))
        
        print(""+str(a)+" / "+str(b)+" = "+ str(a/b))
        print(""+str(a)+" / "+str(c)+" = "+ str(a/c))
        print(""+str(c)+" / "+str(a)+" = "+ str(c/a))

        print(""+str(a)+" == "+str(b)+" = "+ str(a==b))
        print(""+str(a)+" == "+str(a)+" = "+ str(a==a))
        print(""+str(a)+" == "+str(c)+" = "+ str(a==c))
        print(""+str(c)+" == "+str(a)+" = "+ str(c==a))

        print("dot("+str(a)+","+str(a2)+") = "+ str(a.dot(a2)))
        print("cross("+str(a)+","+str(a2)+") = "+ str(a.cross(a2)))


        a = Vector2i(2,3)
        b = Vector2i(1,5)
        c = 3
        print("Vector2i operations")
        print(""+str(a)+" + "+str(b)+" = "+ str(a+b))
        print(""+str(a)+" + "+str(c)+" = "+ str(a+c))
        print(""+str(c)+" + "+str(a)+" = "+ str(c+a))
        
        print(""+str(a)+" - "+str(b)+" = "+ str(a-b))
        print(""+str(a)+" - "+str(c)+" = "+ str(a-c))
        print(""+str(c)+" - "+str(a)+" = "+ str(c-a))
        
        print(""+str(a)+" * "+str(b)+" = "+ str(a*b))
        print(""+str(a)+" * "+str(c)+" = "+ str(a*c))
        print(""+str(c)+" * "+str(a)+" = "+ str(c*a))
        
        print(""+str(a)+" / "+str(b)+" = "+ str(a/b))
        print(""+str(a)+" / "+str(c)+" = "+ str(a/c))
        print(""+str(c)+" / "+str(a)+" = "+ str(c/a))

        print(""+str(a)+" == "+str(b)+" = "+ str(a==b))
        print(""+str(a)+" == "+str(a)+" = "+ str(a==a))
        print(""+str(a)+" == "+str(c)+" = "+ str(a==c))
        print(""+str(c)+" == "+str(a)+" = "+ str(c==a))
        
        print("dot("+str(a)+","+str(b)+") = "+ str(a.dot(b)))
        print("----")
        
        print("Vector3i operations")
        a = 0
        b = 0

        a = Vector3i(1,2,3)
        a2 = Vector3i(2,1,3)
        b = Vector2i(2,5)
        c = 3
        print(""+str(a)+" + "+str(b)+" = "+ str(a+b))
        print(""+str(a)+" + "+str(c)+" = "+ str(a+c))
        print(""+str(c)+" + "+str(a)+" = "+ str(c+a))
        
        print(""+str(a)+" - "+str(b)+" = "+ str(a-b))
        print(""+str(a)+" - "+str(c)+" = "+ str(a-c))
        print(""+str(c)+" - "+str(a)+" = "+ str(c-a))
        
        print(""+str(a)+" * "+str(b)+" = "+ str(a*b))
        print(""+str(a)+" * "+str(c)+" = "+ str(a*c))
        print(""+str(c)+" * "+str(a)+" = "+ str(c*a))
        
        print(""+str(a)+" / "+str(b)+" = "+ str(a/b))
        print(""+str(a)+" / "+str(c)+" = "+ str(a/c))
        print(""+str(c)+" / "+str(a)+" = "+ str(c/a))

        print(""+str(a)+" == "+str(b)+" = "+ str(a==b))
        print(""+str(a)+" == "+str(a)+" = "+ str(a==a))
        print(""+str(a)+" == "+str(c)+" = "+ str(a==c))
        print(""+str(c)+" == "+str(a)+" = "+ str(c==a))

        print("dot("+str(a)+","+str(a2)+") = "+ str(a.dot(a2)))
        print("cross("+str(a)+","+str(a2)+") = "+ str(a.cross(a2)))
               
Test()