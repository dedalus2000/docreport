# -*- coding: utf-8 -*-

from .wrapobjs import WrappableInterface, Composition, Text
from .localreportlab import MyCanvas
from .pagedata import mm
from .filters import Filter


class RowsUtil(Composition):
    # a VerticalWrap. filled with Horiz.Wrap.
    #
    cols_widths = None
    cols_styles = None

    def __init__(self, ctx, *args, **kwargs):
        # in kwargs c'è -opzionale- border_cb
        self.ctx = ctx
        self.cols_widths = kwargs.pop('cols_widths', None)
        self.cols_styles = kwargs.pop('cols_styles', None)
        super(RowsUtil, self).__init__(ctx=self.ctx,*args, **kwargs)

    def _beforeAddingPath(self, path):
        if self.paths:
            path.idx = self.paths[-1].idx + 1
            path.height_sum = self.paths[-1].height_sum + path.height
        else:
            path.idx = 0
            path.height_sum = path.height

    # def vAdd(self, row):
    #     assert isinstance(row, WrappableInterface)
    #     if self.ctx.rows_frame_height and row.height>self.ctx.rows_frame_height:
    #         print ("Warning: che faccio? riga maggiore dello spazio pagina %s>%s"%(row.height, self.ctx.rows_frame_height))
    #     return super(RowsUtil, self).vAdd(row)

    def add(self, row):
        raise Exception('Dont use me')

    def hAdd(self, row):
        raise Exception('Dont use me')

    def _cloneEmpty(self):
        return RowsUtil(ctx=self.ctx, border_cb=self.border_cb)

    def addRowValues(self, fields, cols_widths=None, border_cb=None, cols_styles=None):
        if cols_widths is False:
            cols_widths = [None]*len(fields)

        cols_widths = cols_widths or self.cols_widths or self.ctx.cols_widths
        cols_styles = cols_styles or self.cols_styles or self.ctx.cols_styles
        if cols_styles is None:
            cols_styles = [self.ctx.style] * len(fields)
        assert isinstance(cols_widths, (tuple,list))
        assert isinstance(fields, (tuple,list))
        assert len(cols_widths)==len(fields)==len(cols_styles)

        hh = Composition(self.ctx, border_cb=border_cb)

        # calcola il width rimasto in "single"
        #  quando width richiesto è None
        nnone = 0
        xdim = self.width
        for dd in cols_widths:
            if dd is None:
                nnone += 1
            else:
                xdim -= dd
        single = xdim / nnone if nnone else 0

        for field, width, style in zip(fields, cols_widths, cols_styles):
            ww = Text(field, width if width is not None else single, style=style, ctx=self.ctx)
            hh.hAdd(ww)
        return self.vAdd(hh)

    def splitByHeight(self, requested_height):
        assert requested_height>0

        rr_before = self._cloneEmpty()
        rr_after = self._cloneEmpty()

        for path in self.paths:
            if path.height_sum<=requested_height:
                rr_before.vAdd(path.wrappable)
            else:
                rr_after.vAdd(path.wrappable)
        return rr_before, rr_after

        # def drawOn(self, canvas, x, y):
        #     cury = y
        #     for row in self.wrappables:
        #         row.drawOn(canvas, x, cury)
        #         cury += row.height
        #     canvas.lines([[x,y, self.width,y], [x,cury, self.width,cury]])


class MyPage(object):
    y_padding = 0*mm
    x_padding = 0*mm

    rows_start_x = 10*mm
    rows_end_x = None
    rows_start_y = 50*mm
    rows_end_y = 260*mm

    page_height = None
    page_width = None

    @property
    def curpage_x(self):
        return self.page_width-20*mm

    @property
    def curpage_y(self):
        return self.page_height-15*mm

    _is_first_row = True
    curpage = None
    rows_obj = None
    escape = None  # escape filter instance

    cols_widths = None
    cols_styles = None
    style = None

    @property
    def rows_frame_height(self):
        return self.rows_end_y - self.rows_start_y

    def drawCurPage(self):
        cp = self.curpage + 1
        self.Text(cp, 50*mm).drawAt(self.curpage_x, self.curpage_y)

    def __init__(self, filename_or_canvas, cols_widths=None, cols_styles=None, escape=None, rows=None, *args, **kwargs):
        try:
            filename_or_canvas + ''
            self.canvas = MyCanvas(filename_or_canvas, ctx=self, *args, **kwargs)
        except:
            self.canvas = filename_or_canvas

        self.escape = escape or self.escape or Filter()
        self.curpage = 0
        self.cur_y = self.rows_start_y
        self._is_first_row = True

        if cols_widths:
            self.cols_widths = cols_widths
        if cols_styles:
            self.cols_styles = cols_styles

        if rows is None:
            rows = {}

        self.initRows(rows=rows)

        self.canvas.setLineWidth(0.2)

    def initRows(self, rows=None):
        self.rows_obj = RowsUtil(ctx=self, **(rows or {}))

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
                raise Exception('Missing rows')
            endx = self.rows_obj.width

        self.canvas.line(self.rows_start_x, yy, endx, yy)

    def generate(self, rows_obj=None):
        rows_height = self.rows_end_y - self.rows_start_y

        if rows_obj is None:
            rows_obj = self.rows_obj
            self.on_init_page(rows_obj)

        assert isinstance(rows_obj, RowsUtil)

        before, after = rows_obj.splitByHeight(rows_height)
        before.drawAt(self.rows_start_x, self.rows_start_y)

        if after:
            self.new_page()
            self.on_init_page(after)
            self.generate(after)
        # else:
        #     self.rows_obj.drawAt(self.rows_start_x, self.rows_start_y, paths=rows_obj)

    def addRowValues(self, *args, **kwargs):
        self.rows_obj.addRowValues(*args, **kwargs)

    def addRow(self, text):
        self.rows_obj.vAdd(text)

    def RowsUtil(self, *args, **kwargs):
        return RowsUtil(self, *args, **kwargs)

    ###
    def Text(self, *args, **kwargs):
        kwargs['ctx'] = self
        return Text(*args, **kwargs)

    def Composition(self, *args, **kwargs):
        kwargs['ctx'] = self
        return Composition(*args, **kwargs)
