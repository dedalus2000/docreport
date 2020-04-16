# -*- coding: utf-8 -*-

from .localreportlab import MyParagraph
from .pagedata import styleN

# class Pdf(object):
#     def __init__(self, canvas):
#         self.canvas = canvas

#     def draw(self):
#         for ww in self.addWrappable:
#             self.drawOn

#     def drawOn(self, wrappable, x, y):
#         wrappable.drawOn(self.canvas, x, y)


class WrappableInterface(object):
    border = None
    height = None
    width = None

    def drawAt(self, x=None, y=None):
        raise Exception('Not defined')
        #return self

    # def add(self, wrappable):
    #     raise Exception('Not defined')
    #     #return self

    def __str__(self):
        return "<{} {}x{} >".format(
                getattr(self, 'name', self.__class__.__name__),
                self.width,
                self.height
            )
    __repr__=__str__


class Wrappable(WrappableInterface):
    """ un paragrafo con una larghezza predefinita e un altezza variabile in base al contenuto
    """
    style = styleN

    border_cb = None
    height = None
    _pheight = None
    width = None

    def __init__(self, txt, width, ctx, height=None, min_height=None, fill=None, style=None, border_cb=None):
        self.ctx = ctx
        self.width = width

        if fill is None:
            self.pb = MyParagraph(txt, style or self.style, ctx=self.ctx)

        if height is None:
            height = 200000  # serve?
        self.width, self.height = self.pb.wrap(max(width-2*self.ctx.x_padding, 1), height*300)  # verticalmente ignoriamo..
        self.width += 2*self.ctx.x_padding  # la larghezza minima è 1+2*x_padding
        self.height += 2*self.ctx.y_padding
        self._pheight = self.height
        self.border_cb = border_cb
        if min_height and self.height<min_height:
            self.height = min_height

    def drawAt(self, x, y):
        # ci sommo height perché scrive all'insu'..
        self.pb.drawAt(x+self.ctx.x_padding, y+self._pheight -self.ctx.y_padding)
        if self.border_cb:
            self.border_cb(self.ctx.canvas, x,y, self)
        return self


class _Path(object):
    def __init__(self, ww, x,y, idx=None):
        self.wrappable = ww
        self.x = x
        self.y = y
        self.idx = idx

    @property
    def height(self):
        return self.wrappable.height

    @property
    def width(self):
        return self.wrappable.width

    def drawAt(self, *args, **kwargs):
        return self.wrappable.drawAt(*args, **kwargs)


class Composition(WrappableInterface):
    paths = None
    height = None
    width = None
    border_cb = None
    ctx = None
    def __init__(self, ctx, border_cb=None):
        self.ctx = ctx
        self.border_cb = border_cb
        self.paths = []
        self.height = 0
        self.width = 0

    def hAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        path = _Path(wrappable, self.width, 0)
        self._beforeAddingPath(path)
        self.paths.append(path)
        self.width += wrappable.width
        self.height = max(self.height, wrappable.height)
        return self

    def _beforeAddingPath(self, path):
        pass

    def vAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        path = _Path(wrappable, 0, self.height)
        self._beforeAddingPath(path)
        self.paths.append(path)
        self.height += wrappable.height
        self.width = max(self.width, wrappable.width)
        return self

    def add(self, wrappable, x, y, resize=True):
        if x<0 or y<0:
            print ("Warning: [{}, {}]".format(x,y))
        assert isinstance(wrappable, WrappableInterface)
        path = _Path(wrappable, x,y)
        self._beforeAddingPath(path)
        self.paths.append(path)
        if resize:
            self.width = max(self.width, x+wrappable.width)
            self.height = max(self.height, y+wrappable.height)
        return self

    def __len__(self):
        return len(self.paths) if self.paths else 0

    def drawAt(self, x, y):
        for path in self.paths:
            path.drawAt(x+path.x, y+path.y)

        if self.border_cb:
            self.border_cb(self.ctx.canvas, x,y, self)

        return self
