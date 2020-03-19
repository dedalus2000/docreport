# -*- coding: utf-8 -*-

from docreport.wrapobjs import Wrappable as WW, HorizzontalWrappable as HW, VerticalWrappable as VW
from docreport.localreportlab import MyParagraph
from docreport.pagedata import styleN, mm
from docreport.filters import Filter
from docreport.filters import T
from docreport import borders
from utils import pdfFileCanvas
from docreport.borders import hborders, vborders


def _test_page(c):
    class TmpFilter(Filter):
        def text(self, txt):
            txt = super(TmpFilter, self).text(txt)
            txt ="* "+txt
            return txt

    def l(c, x1,y1, obj):
        thikness = 3
        
        x2 = x1 + obj.width
        y2 = y1 + obj.height
        c.line( x1-thikness,y1, x1,y1) # - 
        c.line( x1,y1-thikness, x1,y1) # |

        c.line( x2,y1, x2+thikness,y1)  # -
        c.line( x2,y1, x2,y1-thikness)  # |

        c.line( x1-thikness,y2, x1, y2) # -
        c.line( x1,y2, x1,y2+thikness)  # |

        c.line( x2,y2, x2+thikness,y2)
        c.line( x2,y2, x2, y2+thikness)
        
    #################### PAGE 1
    xx=10; min_height=None; 
    
    yy=20; ll=50; 
    WW("[{}:{},{}] Wrappable Test 1".format(xx,yy,ll), ll*mm,
            min_height=min_height, border_cb=l).drawOn(c, xx*mm, yy*mm)

    yy=30; ll=80
    WW("[{}:{},{}] 1 riga breve".format(xx,yy,ll), ll*mm,
            min_height=min_height, border_cb=l).drawOn(c, xx*mm, yy*mm)

    yy=50; ll=50
    WW("[{}:{},{}] 1 riga spezzata a metà".format(xx,yy,ll), ll*mm,
            min_height=min_height, border_cb=l).drawOn(c, xx*mm, yy*mm)

    yy=70; ll=40; min_height=50; 
    WW("[{}:{},{}] No <br/>escape <br/>    min 40".format(xx,yy,ll), ll*mm,
            min_height=min_height, border_cb=l).drawOn(c, xx*mm, yy*mm)

    xx=140
    yy=70; ll=40; min_height=50; 
    WW("[{}:{},{}] Escape\n    min 40".format(xx,yy,ll), ll*mm,
            min_height=min_height, border_cb=l, escape=TmpFilter()).drawOn(c, xx*mm, yy*mm)


    ## composition
    
    w1 = WW("W1", 30*mm, border_cb=l)
    w2 = WW("W2", 40*mm, border_cb=l)
    w3 = WW("W3", 50*mm, border_cb=l)
    
    h1 = HW()
    h1.add(w1)
    h1.add(w2)
    h1.add(w3)
    h1.drawOn(c, 30*mm, 120*mm)

    h2 = HW()\
        .add(w1)\
        .add(w2)\
        .add(w3)
    h2.drawOn(c, 30*mm, 150*mm)

    v1 = VW()\
        .add(h1)\
        .add(WW("Single field", 65*mm))\
        .add(h2)
    v1.drawOn(c, 30*mm, 200*mm)

    c.showPage()  ######################################
    
    ww = WW("Test Markup System", 130*mm)
    ww.drawOn(c, 10*mm, 30*mm)

    ww1 = VW()\
        .add(WW(["This ", "is ", "a " , "list"], 120*mm))\
        .add(WW(["To be wrapped (default escaping): ", '<b>example</b>'], 120*mm))\
        .add(WW(["No wrap: ", T.N['<b>example</b>']], 120*mm))\
        .add(WW(["Tag wrap: ", T.b['example']], 120*mm))
            
    ww1.drawOn(c, 20*mm, 30*mm + ww.height*mm)

    c.showPage()  ######################################
    WW("Borders", 130*mm, border_cb=borders.borderbox).drawOn(c, 20*mm, 20*mm )

    HW(border_cb=hborders)\
        .add(WW("Col1", 15*mm))\
        .add(WW("Col2", 15*mm))\
        .add(WW("Col3", 15*mm))\
        .drawOn(c, 20*mm, 40*mm)

    VW(border_cb=vborders)\
        .add(WW("row1", 15*mm))\
        .add(WW("row2", 15*mm))\
        .add(WW("row3", 15*mm))\
        .drawOn(c, 20*mm, 60*mm)

    c.showPage()  ######################################
    WW("Relative position (to the last draw point)", 200*mm).drawOn(c, 20*mm, 20*mm )
    
    w1 = WW("Center", 15*mm)
    w2 = WW("Right", 15*mm)
    w3 = WW("Bottom", 15*mm)
    w1.drawOn(c, 30*mm, 40*mm)
    w2.drawOn(w1, x=w1.width)
    w3.drawOn(w2, y=w2.height)

    w1 = WW("Center", 15*mm)
    w2 = WW("Right", 15*mm)
    w3 = WW("Bottom", 15*mm)
    w2.drawOn(w1, x=w1.width)
    w3.drawOn(w2, y=w2.height)
    w1.drawOn(c, 30*mm, 70*mm)

if __name__=='__main__':
    # testing page
    with pdfFileCanvas() as c:
        _test_page(c)
    