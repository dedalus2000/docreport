# -*- coding: utf-8 -*-

from docreport.wrapobjs import WrappableInterface, HorizzontalWrappable, Wrappable, VerticalWrappable
from docreport.borders import hborders, vborders, table_borders
from docreport.thepage import MyPage, RowsUtil
from docreport.pagedata import mm
from utils import pdfFileCanvas


def _test_page(c):    
    rr = RowsUtil(cols_widths=[40*mm,20*mm,40*mm])
    rr.addRowValues(['col1', 'col2', 'col3'])
    rr.addRowValues(['col4 è molto grossa ma molto molto', 'col5', 'col6'])
    rr.addRowValues(['col7', 'col8', 'col9'])
    rr.drawOn(c, 10*mm, 30*mm)

    a,b = rr.splitByHeight(rr.wrappables[0].height+1)
    a.drawOn(c, 10*mm, 70*mm)
    b.drawOn(c, 10*mm, 100*mm)

    c.showPage() ##################  With borders
    rr = RowsUtil(cols_widths=[40*mm,20*mm,40*mm], border_cb=vborders)
    rr.addRowValues(['col1', 'col2', 'col3'])
    rr.addRowValues(['col4 è molto grossa ma molto molto', 'col5', 'col6'])
    rr.addRowValues(['col7', 'col8', 'col9'])
    rr.drawOn(c, 10*mm, 30*mm)

    rr = RowsUtil(cols_widths=[40*mm,20*mm,40*mm], border_cb=table_borders)
    rr.addRowValues(['col1', 'col2', 'col3'])
    rr.addRowValues(['col4 è molto grossa ma molto molto', 'col5', 'col6'])
    rr.addRowValues(['col7', 'col8', 'col9'])
    rr.drawOn(c, 10*mm, 80*mm)

    c.showPage() #####################################################
    mp = MyPage(c, cols_widths=[40*mm,20*mm,40*mm])
    for ii in range(59):
        mp.addRowValues(['col{}'.format(ii), 'col2', 'col3'])

        mp.addRowValues(['col{}\n  <ah>'.format(ii), 'col5', 'col6'])
    mp.generate()


if __name__=='__main__':
    # testing page
    with pdfFileCanvas() as c:
        _test_page(c)
    