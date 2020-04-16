# -*- coding: utf-8 -*-

from reportlab.pdfgen.canvas import Canvas as _Canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.platypus.flowables import KeepInFrame

#from .pagedata import default_context  # page_ylen, A4
from .filters import Filter, Tag, T


# class MyFrame(Frame):
#     ctx = None
#     def __init__(self, xx, yy, xlen, ylen, page_height, *args, **kwargs):
#         Frame.__init__(self, xx, page_height-yy-ylen, xlen, ylen, *args, **kwargs)


# to be done
class MyKeepInFrame(KeepInFrame):
    ctx = None
    def __init__(self, ctx, *args, **kwargs):
        self.ctx = ctx
        self.canv = None  # bug?
        KeepInFrame.__init__(self, *args, **kwargs)

    def drawAt(self, x, y):
        KeepInFrame.drawOn(self, self.ctx.canvas, x, self.ctx.page_height-y)


class MyParagraph(Paragraph):
    ctx = None
    def __init__(self, text, style, ctx, escape=None, **kwargs):
        self.ctx = ctx

        if not escape:
            escape = self.ctx.escape #Filter()

        if isinstance(text, (tuple, list)):
            text = T[text]

        if isinstance(text, Tag):
            text = text.toXml(escape)
        else:
            text = escape(text)
        Paragraph.__init__(self, text, style, **kwargs)

    def drawAt(self, x, y, _sW=0):
        Paragraph.drawOn(self, self.ctx.canvas, x, self.ctx.page_height-y, _sW)


class MyCanvas(_Canvas):
    ctx = None
    def __init__(self, filename, ctx, *args, **kwargs):
        self.ctx = ctx
        _Canvas.__init__(self, filename, (self.ctx.page_width, self.ctx.page_height), *args, **kwargs)

    def line(self, x1,y1, x2,y2):
        _Canvas.line(self, x1, self.ctx.page_height-y1, x2, self.ctx.page_height-y2)

    def roundRect(self, x, y, width, height, radius, stroke=1, fill=0):
        _Canvas.roundRect(self, x, self.ctx.page_height-y-height, width, height, radius, stroke, fill)

    def rect(self, xx, yy, xlen, ylen, **kwargs):
        # stroke=0, fill=1)
        # print xx/mm,yy/mm
        _Canvas.rect(self, xx, self.ctx.page_height-(yy), xlen, -ylen, **kwargs)

    def lines(self, linelist):
        newlinelist = []
        for (x1,y1,x2,y2) in linelist:
            newlinelist.append( (x1, self.ctx.page_height-y1, x2, self.ctx.page_height-y2) )
        _Canvas.lines(self, newlinelist)
