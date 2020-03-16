# -*- coding: utf-8 -*-

from reportlab.pdfgen.canvas import Canvas as _Canvas
from reportlab.platypus import Paragraph, Frame
from .pagedata import page_ylen, A4
from .filters import Filter, Tag, T


class MyFrame(Frame):
    def __init__(self, xx, yy, xlen, ylen, unit=1, *args, **kwargs):
        Frame.__init__(self, unit*xx, unit* (page_ylen-yy-ylen), unit*xlen, unit*ylen, *args, **kwargs)


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
        
    def drawOn(self, canvas, x, y, _sW=0, unit=1):
        Paragraph.drawOn(self, canvas, x*unit, page_ylen-unit*y, _sW)


class MyCanvas(_Canvas):
    def __init__(self, filename, pagesize=A4, *args, **kwargs):
        _Canvas.__init__(self, filename, pagesize, *args, **kwargs)

    def line(self, x1,y1, x2,y2, unit=1):
        _Canvas.line(self, unit*x1, page_ylen-unit*y1, unit*x2, page_ylen-unit*y2)

    def rect(self, xx, yy, xlen, ylen, unit=1, **kwargs):
        # stroke=0, fill=1)
        # print xx/mm,yy/mm
        _Canvas.rect(self, xx*unit, page_ylen-(yy)*unit, xlen*unit, -ylen*unit, **kwargs)

    def lines(self, linelist, unit=1):
        newlinelist = []
        for (x1,y1,x2,y2) in linelist:
            newlinelist.append( (unit*x1, page_ylen-unit*y1, unit*x2, page_ylen-unit*y2) )
        _Canvas.lines(self, newlinelist)
