# -*- coding: utf-8 -*-

from .wrapobjs import WrappableInterface, HorizzontalWrappable, Wrappable, VerticalWrappable
from .localreportlab import MyCanvas
from .pagedata import mm


class RowsUtil(VerticalWrappable):
    # a VertivalWrap. filled with Horiz.Wrap.
    #
    max_height = 0
    cols_widths = None
    escape = None

    def __init__(self, cols_widths, max_height=None, escape=None, *args, **kwargs):
        self.max_height = max_height
        self.cols_widths = cols_widths
        self.escape = escape
        super(RowsUtil, self).__init__(*args, **kwargs)

    def vAdd(self, row):
        assert isinstance(row, WrappableInterface)
        if self.max_height and row.height>self.max_height:
            print ("Warning: che faccio? riga maggiore dello spazio pagina %s>%s"%(row.height/mm, self.max_height/mm))
        super(RowsUtil, self).vAdd(row)

    def _cloneEmpty(self):
        rr = RowsUtil(self.cols_widths, max_height=self.max_height)
        rr.width = self.width  # inutile
        return rr

    def addRowValues(self, fields, cols_widths=None, escape=None):
        cols_widths = cols_widths or self.cols_widths
        
        assert isinstance(cols_widths, (tuple,list))
        assert isinstance(fields, (tuple,list))
        assert len(cols_widths)==len(fields)

        hh = HorizzontalWrappable()
        for field, width in zip(fields, cols_widths):
            ww = Wrappable(field, width, escape=escape or self.escape)
            hh.add(ww)
        self.add(hh)
            
    def splitByHeight(self, requested_height):
        assert requested_height>0
        if not self.wrappables:
            return None, None
        
        rr_before = self._cloneEmpty()
        rr_after = self._cloneEmpty()

        hsum = 0
        for row in self.wrappables:
            hsum += row.height
            if hsum<=requested_height:
                rr_before.add(row)
            else:
                rr_after.add(row)
        return rr_before, rr_after

        # def drawOn(self, canvas, x, y):
        #     cury = y
        #     for row in self.wrappables:
        #         row.drawOn(canvas, x, cury)
        #         cury += row.height
        #     canvas.lines([[x,y, self.width,y], [x,cury, self.width,cury]])


class MyPage(object):
    y_padding = 2*mm
    x_padding = 2*mm

    rows_start_x = 10*mm
    rows_end_x = None
    rows_start_y = 50*mm
    rows_end_y = 210*mm

    _is_first_row = True
    curpage = None
    rows_obj = None
    escape = None  # escape filter instance

    def __init__(self, filename_or_canvas, cols_widths=None, escape=None, *args, **kwargs):
        try:
            filename_or_canvas + ''
            self.canvas = MyCanvas(filename_or_canvas, *args, **kwargs)
        except:
            self.canvas = filename_or_canvas
        self.escape = escape
        self.curpage = 0
        self.cur_y = self.rows_start_y
        self._is_first_row = True

        self.cols_widths = cols_widths
        self.rows_obj = RowsUtil(cols_widths, max_height=self.rows_end_y-self.rows_start_y, escape=escape)

        self.canvas.setLineWidth(0.2)

    def save(self):
        self.generate()
        self.canvas.save()

    def new_page(self):
        self.canvas.showPage()
        self.curpage +=1
        self.cur_y = self.rows_start_y  # FIX serve?
        self._is_first_row = True

    def on_init_page(self, rows):
        # può attingere a self.curpage e self.data
        #print ("Pagina %s : rimangono %s"%(self.curpage, rows.height ))
        
        self._line_hor(self.rows_start_y)
        self._line_hor(self.rows_end_y)

    def _line_hor(self, yy):
        endx = self.rows_end_x
        if not endx:
            if not self.rows_obj:
                raise Exception('eh')
            endx = self.rows_obj.width

        self.canvas.line(self.rows_start_x, yy, endx, yy)

    def generate(self, rows_obj=None):
        rows_height = self.rows_end_y - self.rows_start_y

        if not rows_obj:
            self.on_init_page(self.rows_obj)
            rows_obj = self.rows_obj

        if rows_height<rows_obj.height:
            # ci sono più righe di quelle visualizzabili
            before, after = rows_obj.splitByHeight(rows_height)
            before.drawOn(self.canvas, self.rows_start_x, self.rows_start_y)

            self.new_page()
            self.on_init_page(after)
            self.generate(after)
        else:
            rows_obj.drawOn(self.canvas, self.rows_start_x, self.rows_start_y)

    def addRowValues(self, fields, cols_widths=None, escape=None):
        self.rows_obj.addRowValues(fields, cols_widths, escape=escape)
    
    def addRowWrappable(self, wrappable):
        self.rows_obj.add(wrappable)
