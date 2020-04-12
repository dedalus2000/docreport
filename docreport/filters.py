# encoding: utf-8

from babel.dates import format_date, format_time
#from babel.numbers import format_decimal
from markupsafe import escape as markup_escape
import datetime
import decimal
import sys


# TO BE IMPROVED
# def _get_price_filter(zero=2):
#     u"""Convert Decimal to a money formatted string.
#        No round is done, please provide it by your own
#     """
#     def prices(value):
#         if value is None or value== '':
#             return ''
#         # lo zero lo gestisce in modo più consono
#         return format_decimal(value, format='#,##0.' + ('0'*zero) + (("#"*10 ) if value else ''), locale=context['locale'])
#     return prices

# P = _get_price_filter(zero=2)

# def get_strip_filter(depth=2):
#     def strip_filter(value, ctx):
#         if value is None or value=='':
#             return ''
#         return format_decimal(value, format='0.' + "0"*depth + "##", locale=ctx['lang'])
#     return strip_filter


class EmptyFilter(object):
    def __call__(self, txt):
        return str(txt)


unary = ['br']  # l'unico "unario" che conosco

class Tag(object):
    children = None
    name = None
    attributes = None

    def __call__(self, **attributes):
        self.attributes = attributes
        self.children = []
        return self

    def __getitem__(self, children):
        if self.name in unary:
            raise Exception("Tag '{}' cannot have children".format(self.name))
        if not isinstance(children, (tuple, list)):
            children = [children]
        self.children = children
        return self

    def __getattr__(self, name):
        t = Tag()
        t.name = name
        return t

    def toXml(self, escape=None):
        tt = []
        attrs = ''
        if self.attributes:
            attrs = " %s " % ' '.join([ '''{}="{}"'''.format(k,v) for k,v in self.attributes.items() ])

        if self.name=='N':
            escape = None
        elif self.name in unary:
            tt.append('<{}{}/>'.format(self.name, attrs))
        elif self.name:
            tt.append("<{}{}>".format(self.name, attrs))

        for child in self.children or []:
            if isinstance(child, Tag):
                tt.append(child.toXml(escape=escape))
            elif escape:
                tt.append(escape(child))
            else:
                tt.append(child)  # qui mettere l'escape

        if self.name=='N':
            pass
        elif self.name and self.name not in unary:
            tt.append("</{}>".format(self.name))
        return ''.join(tt)

    def __str__(self):
        return self.toXml()
    __repr__ = __str__

T = Tag()


class Filter(object):
    def __init__(self, locale='en_DK'):
        self.locale = locale

    def __call__(self, txt):
        return self.default_filter(txt)

    def date(self, obj):
        return format_date(obj, format='long', locale=self.locale)

    def datetime(self, obj):
        # if obj.tzinfo:
        #     return u"[TO BE DONE]"
        # dt = format_time(obj, "hh:mm a", locale=thread_local.context.get('locale', 'en_DE'))
        txtdt = format_time(obj, "HH:mm a", locale=self.locale)
        txtdd = self.date(obj)
        return u'%s  %s' % (txtdd, txtdt)

    def decimal(self, txt):
        if txt is None:
            return ''
        int_txt = int(txt)
        if int_txt==txt:
            return str(int_txt)
        return str(txt).rstrip('0')

    def text(self, txt):
        ntxt = []
        def _addNBSP(t):
            if t and t[0]==' ':
                ntxt.append('&nbsp;')
                _addNBSP(t[1:])
            else:
                ntxt.append(t)
        for part in txt.split('\n'):
            part = markup_escape(part)
            _addNBSP(part)
            ntxt.append('<br/>')
        if ntxt:
            ntxt.pop() # l'ultimo br è fittizio
        return ''.join(ntxt)

    def default_filter(self, txt):
        # Filter
        if txt is None:
            return ''
        if isinstance(txt, datetime.datetime):
            return self.datetime(txt)
            #return txt.strftime('%X, %d %b %Y')
        if isinstance(txt, datetime.date):
            return self.date(txt)
            #return txt.strftime('%d %b %Y')
        if isinstance(txt, decimal.Decimal):
            # perche' i decimal arrivano anche 7 zeri dopo il punto, quindi li tratto a parte
            return self.decimal(txt)
        if sys.version_info[0]<3:
            # esegue l'escape
            # a sinistra aggiunge &nbsp; al posto degli spazi iniziali
            # sostituesce i \n con <br/>
            if isinstance(txt, (str, unicode)):   # py3 error
                return self.text(txt)
        elif isinstance(txt, str):
                return self.text(txt)
        print ("Warning %s not managed"%type(txt))
        return str(txt)
