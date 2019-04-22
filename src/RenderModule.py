import pyxel

class Renderer:
    RESOLUTION_WIDTH = 256
    RESOLUTION_HEIGHT = 256
    SPRITE_W = 16
    SPRITE_H = 16

    #class Mode:
    #    OPAQUE = 0
    #    TRANSPARENT = 1
    #    TRANSLUSCENT = 2

    @staticmethod    
    def SetResolution(width,height):
        Renderer.RESOLUTION_WIDTH = width
        Renderer.RESOLUTION_HEIGHT = height

    @staticmethod
    def DrawSpriteOpaque(palette,idx,x,y,w,h,material):
        if(Renderer.clip(x,y,h,w)):
            ## do something
            ## to render
            ## the sprite
            Renderer.DrawSpriteTransparent(x, y, palette, \
                (material.indexX)*Renderer.SPRITE_W, (material.indexY)*Renderer.SPRITE_H, \
                w*material.flipX,h*material.flipY)
            

    @staticmethod
    def DrawSpriteTransparent(palette,material,x,y,w,h):
        if(Renderer.clip(x,y,h,w)):
            ## do something
            ## to render
            ## the sprite
            pyxel.blt(x, y, palette, \
                (material.indexX)*Renderer.SPRITE_W, (material.indexY)*Renderer.SPRITE_H, \
                w*material.flipX,h*material.flipY,\
                material.transparency)

    @staticmethod
    def DrawSpriteDithering(palette,idx,x,y,w,h, ditherPattern, ditherX, ditherY):
        if(Renderer.clip(x,y,h,w)):
            ## do something
            ## to render
            ## the sprite
            ## including the transparent color
            print("nothing!")
            

    @staticmethod
    # returns True if at least one of the corners is part of the screen
    # could be improved to check center and other extremes, but not sure how expensive it would get
    def clip(x,y,w,h): 
        return True or (x>=0 and x < Renderer.RESOLUTION_WIDTH) \
        or  (x+w>=0 and x+w < Renderer.RESOLUTION_WIDTH) \
        or  (y>=0 and y < Renderer.RESOLUTION_HEIGHT)\
        or  (y+h>=0 and y+h < Renderer.RESOLUTION_HEIGHT)
        