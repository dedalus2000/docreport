# -*- coding: utf-8 -*-

from docreport.localreportlab import MyParagraph
from docreport.pagedata import styleN, mm
from docreport.filters import Filter
from docreport.wrapobjs import Wrappable, HorizzontalWrappable, VerticalWrappable
from docreport.localreportlab import MyCanvas
from docreport.filters import T
from utils import pdfFileCanvas


def _test_page(c):
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
    
    ww = Wrappable("Test Markup System", 130*mm)
    ww.drawOn(c, 10*mm, 30*mm)

    ww1 = Wrappable(["This ", "is ", "a" , "list"], 120*mm).\
            vAdd(Wrappable(["To be wrapped (default escaping): ", '<b>example</b>'], 120*mm)).\
            vAdd(Wrappable(["No wrap: ", T.N['<b>example</b>']], 120*mm)).\
            vAdd(Wrappable(["Tag wrap: ", T.b['example']], 120*mm))
            
    ww1.drawOn(c, 20*mm, 30*mm + ww.height*mm)


if __name__=='__main__':
    # testing page
    with pdfFileCanvas() as c:
        _test_page(c)
    