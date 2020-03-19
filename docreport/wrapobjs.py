# -*- coding: utf-8 -*-

from .localreportlab import MyParagraph
from .pagedata import styleN, mm


class WrappableInterface(object):
    border = None
    height = None
    width = None
    _last = (None, None, None)  # canvas,x,y
    _wattached = None  # []

    def drawOn(self, canvas, x, y):
        raise Exception('Not defined')
        #return self

    def vAdd(self, wrappable):
        raise Exception('Not defined')
        #return self

    def hAdd(self, wrappable):
        raise Exception('Not defined')
        #return self

    def add(self, wrappable, x=0, y=0, resize=True):
        assert isinstance(wrappable, WrappableInterface)
        self._wattached.append( (wrappable, x, y) )
        # now we are going to update the size of the self wrappable
        if resize:
            self.width = max(self.width, x + wrappable.width)
            self.height = max(self.height, x + wrappable.height)
        return self

    
    def _call_wattachments(self):
        if self._wattached:
            for (obj, dx,dy) in self._wattached:
                obj.drawOn(self, dx, dy)

    def __str__(self):
        return "<{} {}x{} >".format(
                getattr(self, 'name', self.__class__.__name__),
                None if self.width is None else self.width/mm ,
                None if self.height is None else  self.height/mm
            )
    __repr__=__str__


class Wrappable(WrappableInterface):
    """ un paragrafo con una larghezza predefinita e un altezza variabile in base al contenuto
    """
    y_padding = 1*mm
    x_padding = 1*mm
    style = styleN

    border_cb = None
    height = None
    _pheight = None
    width = None

    def __init__(self, txt, width, height=None, min_height=None, style=None, escape=None, border_cb=None):
        self._wattached = []
        self.width = width
        
        self.pb = MyParagraph(txt, style or self.style, escape=escape)

        if height is None:
            height = 9999*mm  # serve?
        self.width, self.height = self.pb.wrap(max(width-2*self.x_padding, 1), height*300)  # verticalmente ignoriamo..
        self.width += 2*self.x_padding  # la larghezza minima è 1+2*x_padding
        self.height += 2*self.y_padding
        self._pheight = self.height
        self.border_cb = border_cb
        if min_height and self.height<min_height:
            self.height = min_height

    def vAdd(self, wrappable, *args, **kwargs):
        assert isinstance(wrappable, WrappableInterface)
        hh = VerticalWrappable(*args, **kwargs)
        hh.add(self)
        hh.add(wrappable)
        return hh

    def hAdd(self, wrappable, *args, **kwargs):
        assert isinstance(wrappable, WrappableInterface)
        hh = HorizzontalWrappable(*args, **kwargs)
        hh.add(self)
        hh.add(wrappable)
        return hh

    def drawOn(self, obj, x=None, y=None):
        """ obj: canvas or wrappable
            x: absolute x or delta-x from wrappable
            y: absolute y or delta-y from wrappable
        """
        if isinstance(obj, WrappableInterface):
            canvas, ox, oy = obj._last
            x = (x or 0)
            y = (y or 0)
            if canvas is None:
                # consider to update the "self" width and height (with a resize=True arg?)
                obj._wattached.append( (self, x, y) )
            else:
                self.drawOn(canvas, ox+x, oy+y  )
        else:
            canvas = obj
            if x is None or y is None:
                raise Exception("Coordinates x,y are mandatory")
            self._last = canvas, x, y
            # ci sommo height perché scrive all'insu'..
            self.pb.drawOn(canvas, x+self.x_padding, y+self._pheight -self.y_padding)
            if self.border_cb:
                self.border_cb(canvas, x,y, self)
            
            self._call_wattachments()


class HorizzontalWrappable(WrappableInterface):
    wrappables = None
    height = None
    width = None
    border_cb = None

    def __init__(self, border_cb=None):
        self._wattached = []
        self.border_cb = border_cb
        self.wrappables = []
        self.height = 0
        self.width = 0

    def __len__(self):
        return len(self.wrappables or [])

    def hAdd(self, wrappable):
        return self.add(wrappable, x=self.width)

    def vAdd(self, wrappable, *args, **kwargs):
        hh = VerticalWrappable(*args, **kwargs)
        hh.add(self)
        return hh.add(wrappable)

    def drawOn(self, obj, x=None, y=None):
        """ obj: canvas or wrappable
            x: absolute x or delta-x from wrappable
            y: absolute y or delta-y from wrappable
        """
        if isinstance(obj, WrappableInterface):
            canvas, ox, oy = obj._last
            x = (x or 0)
            y = (y or 0)
            if canvas is None:
                obj._wattached.append( (self, x, y) )
            else:
                self.drawOn(canvas, ox+x, oy+y)
        else:
            canvas = obj
            if x is None or y is None:
                raise Exception("Coordinates x,y are mandatory")
            self._last = canvas, x, y

            curx = x
            for obj in self.wrappables:
                obj.drawOn(canvas, curx, y)
                curx += obj.width

            if self.border_cb:
                self.border_cb(canvas, x,y, self)

            self._call_wattachments()


class VerticalWrappable(WrappableInterface):
    wrappables = None
    height = None
    width = None
    border_cb = None

    def __init__(self, border_cb=None):
        self._wattached = []
        self.border_cb = border_cb
        self.wrappables = []
        self.height = 0
        self.width = 0

    def __len__(self):
        return len(self.wrappables or [])
        
    def vAdd(self, wrappable, border=None):
        return self.add(wrappable, y=self.height)
    
    def hAdd(self, wrappable):
        hh = HorizzontalWrappable()
        hh.add(self)
        return hh.add(wrappable)
    
    def drawOn(self, obj, x=None, y=None):
        """ obj: canvas or wrappable
            x: absolute x or delta-x from wrappable
            y: absolute y or delta-y from wrappable
        """
        if isinstance(obj, WrappableInterface):
            canvas, ox, oy = obj._last
            x = (x or 0)
            y = (y or 0)
            if canvas is None:
                obj._wattached.append( (self, x, y) )
            else:
                self.drawOn(canvas, ox+x, oy+y)
        else:
            canvas = obj
            if x is None or y is None:
                raise Exception("Coordinates x,y are mandatory")
            self._last = canvas, x, y

            cury = y
            for obj in self.wrappables:
                obj.drawOn(canvas, x, cury)
                cury += obj.height
            
            if self.border_cb:
                self.border_cb(canvas, x,y, self)
            
            self._call_wattachments()