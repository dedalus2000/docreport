# -*- coding: utf-8 -*-


from docreport.wrapobjs import Wrappable as WW, Composition
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

    def newPage(title):
        c.showPage()
        WW(title, 200*mm, ctx=c.ctx).drawAt(20*mm, 10*mm)

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
    WW("Page 1", 200*mm, ctx=c.ctx).drawAt(20*mm, 10*mm )

    xx=10; min_height=None;

    yy=20; ll=50;
    WW("[{}:{},{}] Wrappable Test 1".format(xx,yy,ll), ll*mm, ctx=c.ctx,
            min_height=min_height, border_cb=l).drawAt(xx*mm, yy*mm)

    yy=30; ll=80
    WW("[{}:{},{}] 1 riga breve".format(xx,yy,ll), ll*mm, ctx=c.ctx,
            min_height=min_height, border_cb=l).drawAt(xx*mm, yy*mm)

    yy=50; ll=50
    WW("[{}:{},{}] 1 riga spezzata a metà".format(xx,yy,ll),
        ll*mm, ctx=c.ctx, min_height=min_height, border_cb=l).drawAt(xx*mm, yy*mm)

    yy=70; ll=40; min_height=50;
    WW("[{}:{},{}] No <br/>escape <br/>    min 40".format(xx,yy,ll), ll*mm, ctx=c.ctx,
            min_height=min_height, border_cb=l).drawAt(xx*mm, yy*mm)

    xx=140
    yy=70; ll=40; min_height=50;
    # tmpcontext = default_context.copy()
    # tmpcontext['filter_cls'] = TmpFilter
    # WW("[{}:{},{}] Escape\n    min 40".format(xx,yy,ll), ll*mm,
    #         min_height=min_height, border_cb=l, ctx=c.ctx).drawAt(xx*mm, yy*mm)


    ## composition

    w1 = WW("W1", 30*mm, border_cb=l, ctx=c.ctx)
    w2 = WW("W2", 40*mm, border_cb=l, ctx=c.ctx)
    w3 = WW("W3", 50*mm, border_cb=l, ctx=c.ctx)

    h1 = Composition(c.ctx)
    h1.hAdd(w1)
    h1.hAdd(w2)
    h1.hAdd(w3)
    h1.drawAt(30*mm, 120*mm)

    h2 = Composition(c.ctx)\
        .hAdd(w1)\
        .hAdd(w2)\
        .hAdd(w3)
    h2.drawAt(30*mm, 150*mm)

    v1 = Composition(c.ctx)\
        .vAdd(h1)\
        .vAdd(WW("Single field", 65*mm,ctx=c.ctx))\
        .vAdd(h2)
    v1.drawAt(30*mm, 200*mm)

    newPage("Page 2:Test Markup System") ###################################

    ww = WW('Test1', 30*mm, ctx=c.ctx)
    ww1 = Composition(c.ctx)\
        .vAdd(WW(["This ", "is ", "a " , "list"], 120*mm, ctx=c.ctx))\
        .vAdd(WW(["To be wrapped (default escaping): ", '<b>example</b>'], 120*mm, ctx=c.ctx))\
        .vAdd(WW(["No wrap: ", T.N['<b>example</b>']], 120*mm, ctx=c.ctx))\
        .vAdd(WW(["Tag wrap: ", T.b['example']], 120*mm, ctx=c.ctx))

    ww1.drawAt(20*mm, 30*mm + ww.height*mm)

    newPage("Page 3:Borders") ###################################

    Composition(c.ctx,border_cb=hborders)\
        .hAdd(WW("Col1", 15*mm, ctx=c.ctx))\
        .hAdd(WW("Col2", 15*mm, ctx=c.ctx))\
        .hAdd(WW("Col3", 15*mm, ctx=c.ctx))\
        .drawAt(20*mm, 40*mm)

    Composition(c.ctx,border_cb=vborders)\
        .vAdd(WW("row1", 15*mm, ctx=c.ctx))\
        .vAdd(WW("row2", 15*mm, ctx=c.ctx))\
        .vAdd(WW("row3", 15*mm, ctx=c.ctx))\
        .drawAt(20*mm, 60*mm)

    newPage("Page 4:Relative position")  ############################
    #c.showPage()  ######################################
    # WW("Relative position (to the last draw point)", 200*mm).drawAt(20*mm, 20*mm )


    w1 = WW("Text", 15*mm, min_height=30*mm, border_cb=borders.borderbox, ctx=c.ctx)
    w2 = WW("Bottom", 15*mm, ctx=c.ctx)
    cc = Composition(c.ctx) #border_cb=borders.borderbox)
    cc.hAdd(w1)
    cc.add(w2, 2*mm, cc.height-w2.height)
    cc.drawAt(20*mm, 40*mm)
    # w3 = WW("Bottom", 15*mm)
    # w1.drawAt(30*mm, 40*mm)
    # w2.drawOn(w1, x=w1.width)
    # w3.drawOn(w2, y=w2.height)

    # w1 = WW("Center", 15*mm)
    # w2 = WW("Right", 15*mm)
    # w3 = WW("Bottom", 15*mm)
    # w2.drawOn(w1, x=w1.width)
    # w3.drawOn(w2, y=w2.height)
    # w1.drawAt(30*mm, 70*mm)

    newPage("Page 5: Composition")  ############################
    cc = Composition(c.ctx)\
        .hAdd(WW("H1", 15*mm, ctx=c.ctx))\
        .hAdd(WW("H2", 20*mm, ctx=c.ctx))\
        .hAdd(WW("H3", 30*mm, ctx=c.ctx))
    cc.drawAt(20*mm, 40*mm)

    cc2 = Composition(c.ctx)\
        .hAdd(WW("R1", 15*mm, ctx=c.ctx))\
        .vAdd(cc)\
        .vAdd(WW("R3", 15*mm, ctx=c.ctx))
    cc2.drawAt(20*mm, 60*mm)

    newPage("Page 6:Composition")  ############################
    # root.layout().row().cell() => ww
    # root.layout().row().cell() => ww

if __name__=='__main__':
    # testing page
    with pdfFileCanvas() as c:
        _test_page(c)
