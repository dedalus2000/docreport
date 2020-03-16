# -*- coding: utf-8 -*-

from .localreportlab import MyParagraph
from .pagedata import styleN, mm


class WrappableInterface(object):
    border = None
    height = None
    width = None

    def drawOn(self, canvas, x, y):
        raise Exception('Not defined')
        #return self

    def vAdd(self, wrappable):
        raise Exception('Not defined')
        #return self

    def hAdd(self, wrappable):
        raise Exception('Not defined')
        #return self

    def add(self, wrappable):
        raise Exception('Not defined')
        #return self

    def __str__(self):
        return "<Wrappable {}x{} >".format(
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
        self.width = width
        
        self.pb = MyParagraph(txt, style or self.style, escape=escape)

        if height is None:
            height = 9999*mm  # serve?
        self.width, self.height = self.pb.wrap(max(width-2*self.x_padding, 1), height*300)  # verticalmente ignoriamo..
        self.width += 2*self.x_padding  # la larghezza minima è 1+2*x_padding
        self.height += 2*self.y_padding
        self._pheight = self.height
        if min_height and self.height<min_height:
            self.height = min_height

    def drawOn(self, canvas, x, y):
        # ci sommo height perché scrive all'insu'..
        self.pb.drawOn(canvas, x+self.x_padding, y+self._pheight -self.y_padding)
        if self.border_cb:
            self.border_cb(canvas, x,y, self)

    def vAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        hh = VerticalWrappable()
        hh.add(self)
        hh.add(wrappable)
        return hh

    def hAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        hh = HorizzontalWrappable()
        hh.add(self)
        hh.add(wrappable)
        return hh


class HorizzontalWrappable(WrappableInterface):
    wrappables = None
    height = None
    width = None
    border = None

    def __init__(self, border=None):
        self.border = border
        self.wrappables = []
        self.height = 0
        self.width = 0

    def __len__(self):
        return len(self.wrappables or [])

    def hAdd(self, wrappable, border=None):
        assert isinstance(wrappable, WrappableInterface)
        self.wrappables.append(wrappable)

        self.height = max(self.height, wrappable.height)
        self.width += wrappable.width
        if border is not None:
            wrappable.border = border
        return self
    add = hAdd

    def vAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        hh = VerticalWrappable()
        hh.add(self)
        hh.add(wrappable)
        return hh

    def drawOn(self, canvas, x, y):
        curx = x
        for obj in self.wrappables:
            obj.drawOn(canvas, curx, y)
            curx += obj.width
           
        if self.border:
            canvas.rect(x,y, self.width,self.height)


class VerticalWrappable(WrappableInterface):
    wrappables = None
    height = None
    width = None
    border = None

    def __init__(self, border=None):
        self.border = border
        self.wrappables = []
        self.height = 0
        self.width = 0

    def __len__(self):
        return len(self.wrappables or [])
        
    def vAdd(self, wrappable, border=None):
        assert isinstance(wrappable, WrappableInterface)
        self.wrappables.append(wrappable)

        self.height += wrappable.height
        self.width = max(self.width, wrappable.width)
        if border is not None:
            wrappable.border = border
        return self
    add = vAdd

    def hAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        hh = HorizzontalWrappable()
        hh.add(self)
        hh.add(wrappable)
        return hh

    def drawOn(self, canvas, x, y):
        cury = y
        for obj in self.wrappables:
            obj.drawOn(canvas, x, cury)
            cury += obj.height
           
        if self.border:
            canvas.rect(x,y, self.width,self.height)