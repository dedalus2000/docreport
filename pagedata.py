# -*- coding: utf-8 -*-

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm  #  mm = 2.834645669291339
from reportlab.lib.pagesizes import A4


page_xlen, page_ylen = A4

styles = getSampleStyleSheet()
styleN = styles['Normal']
styleH = styles['Heading1']

