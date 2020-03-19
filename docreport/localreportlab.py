# -*- coding: utf-8 -*-

from reportlab.pdfgen.canvas import Canvas as _Canvas
from reportlab.platypus import Paragraph, Frame
from .pagedata import page_ylen, A4
from .filters import Filter, Tag, T


class MyFrame(Frame):
    def __init__(self, xx, yy, xlen, ylen, *args, **kwargs):
        Frame.__init__(self, xx, page_ylen-yy-ylen, xlen, ylen, *args, **kwargs)


class MyParagraph(Paragraph):
    def __init__(self, text, style, escape=None, **kwargs):
        if not escape:
            escape = Filter()
        
        if isinstance(text, (tuple, list)):
            text = T[text]
        
        if isinstance(text, Tag):
            text = text.toXml(escape)
        else:
            text = escape(text)
        Paragraph.__init__(self, text, style, **kwargs)
        
    def drawOn(self, canvas, x, y, _sW=0):
        Paragraph.drawOn(self, canvas, x, page_ylen-y, _sW)


class MyCanvas(_Canvas):
    def __init__(self, filename, pagesize=A4, *args, **kwargs):
        _Canvas.__init__(self, filename, pagesize, *args, **kwargs)

    def line(self, x1,y1, x2,y2):
        _Canvas.line(self, x1, page_ylen-y1, x2, page_ylen-y2)

    def roundRect(self, x, y, width, height, radius, stroke=1, fill=0):
        _Canvas.roundRect(self, x, page_ylen-y-height, width, height, radius, stroke, fill)

    def rect(self, xx, yy, xlen, ylen, **kwargs):
        # stroke=0, fill=1)
        # print xx/mm,yy/mm
        _Canvas.rect(self, xx, page_ylen-(yy), xlen, -ylen, **kwargs)

    def lines(self, linelist):
        newlinelist = []
        for (x1,y1,x2,y2) in linelist:
            newlinelist.append( (x1, page_ylen-y1, x2, page_ylen-y2) )
        _Canvas.lines(self, newlinelist)
