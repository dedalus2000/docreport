# -*- coding: utf-8 -*-

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm  #  mm = 2.834645669291339
from reportlab.lib.pagesizes import A4
from .filters import Filter


#page_xlen, page_ylen = A4

styles = getSampleStyleSheet()
# Title, OrderedList Normal Italic Heading6.. Heading1  Definition  Code Bullet  BodyText
styleN = styles['Normal']
styleH = styles['Heading1']



# default_context = dict(
#     page_width = A4[0],
#     page_height = A4[1],
#     #unit=mm,
#     filter_cls=Filter,
#     locale='en_DK',
#     canvas=None,
# )