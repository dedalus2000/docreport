
from __future__ import print_function
from docreport.localreportlab import MyCanvas
from contextlib import contextmanager
import subprocess
import tempfile
import sys
import os


@contextmanager
def pdfFileCanvas(fname=None, open=True):
    if fname is None:
        ff = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        ff.close()
        fname = ff.name
    else:
        if not fname.endswith('.pdf'):
            fname = "%s.pdf" % fname
    c = MyCanvas(fname)
    
    yield c
    
    c.save()

    print (fname)  # you can use okular `... |tail -n 1`
    
    #if sys.platform.startswith('freebsd'):
        # FreeBSD-specific code here...
    if sys.platform.startswith('linux'):
        subprocess.call(["xdg-open", fname])
    elif sys.platform == "darwin":
        subprocess.call(["open", fname])
    elif sys.platform in ('win32', 'cygwin'):
        os.startfile(fname)
