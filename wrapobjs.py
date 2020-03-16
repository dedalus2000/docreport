# -*- coding: utf-8 -*-

from localreportlab import MyParagraph
from pagedata import styleN, mm


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

    border = None
    height = None
    _pheight = None
    width = None

    def __init__(self, txt, width, height=None, min_height=None, style=None, escape=None):
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
        if self.border:
            canvas.rect(x,y, self.width,self.height)

    def vAdd(self, wrappable):
        assert isinstance(wrappable, WrappableInterface)
        hh = VerticalWrappable()
        hh.add(self)
        hh.add(wrappable)
        return hh
    add = vAdd  # default

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



def _test_page(c):
    from filters import Filter

    class TmpFilter(Filter):
        def text(self, txt):
            txt = super(TmpFilter, self).text(txt)
            txt ="* "+txt
            return txt

    def _extern_lines(x1,y1, xlen,ylen, thikness=3):
        x2 = x1 + xlen
        y2 = y1 + ylen
        c.line( x1-thikness,y1, x1,y1) # - 
        c.line( x1,y1-thikness, x1,y1) # |

        c.line( x2,y1, x2+thikness,y1)  # -
        c.line( x2,y1, x2,y1-thikness)  # |

        c.line( x1-thikness,y2, x1, y2) # -
        c.line( x1,y2, x1,y2+thikness)  # |

        c.line( x2,y2, x2+thikness,y2)
        c.line( x2,y2, x2, y2+thikness)
        
    def print_txt(txt, xx=30, yy=None, ll=None, min_height=None, escape=None):
        w1 = Wrappable("[{}:{},{}] {}".format(xx,yy,ll,txt), ll*mm,
            min_height=min_height, escape=escape)
        w1.drawOn(c, xx*mm, yy*mm)
        _extern_lines(xx*mm,yy*mm, ll*mm, w1.height)
        return w1

    w1 = print_txt('1 riga breve', yy=30, ll=80)
    w2 = print_txt('1 riga spezzata a metà', yy=50, ll=50)
    w3 = print_txt('No <br/>escape <br/>    min 40', yy=70, ll=40, min_height=50)
    w3 = print_txt(' Escape\n    min 40', xx=140,yy=70, ll=40,
            min_height=50, escape=TmpFilter())

    ###########
    h1 = HorizzontalWrappable(border=True)
    h1.add(w1, border=True)
    h1.add(w2)
    h1.add(w3)
    h1.drawOn(c, 30*mm, 120*mm)

    def ww(nn):
        nn += 1
        pre = width = 0
        for ii in range(nn):
            obj = h1.wrappables[ii]
            pre = width
            width += obj.width
        return pre, obj.width, obj.height

    pre, w, h = ww(0)
    _extern_lines(30*mm+pre,120*mm, w, h)
    pre, w, h = ww(1)
    _extern_lines(30*mm+pre,120*mm, w, h)
    pre, w, h = ww(2)
    _extern_lines(30*mm+pre,120*mm, w, h)

    c.showPage()  ######################################
    v1 = VerticalWrappable(border=True)
    v1.add(w1)
    v1.add(w2)
    v1.add(w3)
    v1.add(h1)
    v1.drawOn(c, 30*mm, 30*mm)

    c.showPage()  ######################################
    ww = Wrappable("Txt1", 30*mm).\
            hAdd(Wrappable("Txt2", 20*mm)).\
            add(Wrappable("Txt3", 20*mm)).\
            vAdd(Wrappable("Txt4", 20*mm))
    ww.drawOn(c, 10*mm, 30*mm)

    c.showPage()  ######################################
    from filters import T
    ww = Wrappable("Test Markup System", 130*mm)
    ww.drawOn(c, 10*mm, 30*mm)

    ww1 = Wrappable(["This ", "is ", "a" , "list"], 120*mm).\
            vAdd(Wrappable(["To be wrapped (default escaping): ", '<b>example</b>'], 120*mm)).\
            vAdd(Wrappable(["No wrap: ", T.N['<b>example</b>']], 120*mm)).\
            vAdd(Wrappable(["Tag wrap: ", T.b['example']], 120*mm))
            
    ww1.drawOn(c, 20*mm, 30*mm + ww.height*mm)

if __name__=='__main__':
    # testing page
    from localreportlab import MyCanvas
    import tempfile
    ff = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    ff.close()

    c = MyCanvas(ff.name)
    _test_page(c)
    c.save()
    print (ff.name)