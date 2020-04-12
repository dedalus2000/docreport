# -*- coding: utf-8 -*-

from docreport.wrapobjs import WrappableInterface, Wrappable as WW, Composition
from docreport.borders import hborders, vborders, table_borders
from docreport.thepage import MyPage, RowsUtil
from docreport.pagedata import mm
from utils import pdfFileCanvas
from reportlab.lib.pagesizes import A4
import random


def _test_page(c):
    def newPage(title):
        c.showPage()
        WW(title, 200*mm, ctx=c.ctx).drawAt(20*mm, 10*mm)

    c.ctx.rows_frame_height = 200*mm
    c.ctx.cols_widths = [40*mm,20*mm,40*mm]

    rr = RowsUtil(ctx=c.ctx)
    rr.addRowValues(['col1', 'col2', 'col3'])
    rr.addRowValues(['col4 è molto grossa ma molto molto', 'col5', 'col6'])
    rr.addRowValues(['col7', 'col8', 'col9'])
    rr.drawAt(10*mm, 30*mm)

    a,b = rr.splitByHeight(rr.paths[0].height+1)
    a.drawAt( 10*mm, 140*mm)
    b.drawAt( 10*mm, 180*mm)

    newPage("Page 2: Borders") ##################  With borders
    c.ctx.cols_widths=[40*mm,20*mm,40*mm]
    c.ctx.border_cb=vborders

    rr = RowsUtil(ctx=c.ctx)
    rr.addRowValues(['col1', 'col2', 'col3'])
    rr.addRowValues(['col4 è molto grossa ma molto molto', 'col5', 'col6'])
    rr.addRowValues(['col7', 'col8', 'col9'])
    rr.drawAt( 10*mm, 30*mm)

    rr = RowsUtil(ctx=c.ctx, border_cb=table_borders)
    rr.addRowValues(['col1', 'col2', 'col3'])
    rr.addRowValues(['col4 è molto grossa ma molto molto', 'col5', 'col6'])
    rr.addRowValues(['col7', 'col8', 'col9'])
    rr.drawAt( 10*mm, 150*mm)

    newPage("Page 4: Page") #####################################################
    mp = MyPage(c, cols_widths=[40*mm,20*mm,40*mm], rows=dict(border_cb=table_borders))
    mp.page_height = A4[1]
    for ii in range(14):
#        mp.addRowValues(['col{}'.format(ii), 'col2', 'col3'])
        mp.addRowValues(['\n'.join(['col1']*random.randint(2,2)) , 'col2', 'col3 [%s]'%ii])
    mp.generate()

    newPage("Page 5: inherited page") #####################################################

    class Page(MyPage):
        page_width = A4[0]
        page_height = A4[1]

        def on_init_page(self, rows):
            rect_width = self.page_width-20*mm
            self.canvas.rect(10*mm,10*mm,rect_width,20*mm)
            self.Wrappable('Page %s'%self.curpage, 20*mm).drawAt(10*mm, 20*mm)

    mp = Page(c, cols_widths=[40*mm,20*mm,40*mm], rows=dict(border_cb=table_borders))
    for ii in range(16):
        mp.addRowValues(['\n'.join(['col1']*random.randint(1,3)) , 'col2', 'col3'])
    mp.generate()

if __name__=='__main__':
    # testing page
    with pdfFileCanvas() as c:
        _test_page(c)
