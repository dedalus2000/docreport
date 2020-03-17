
def borderbox(canvas, x,y, obj):
    canvas.rect(x,y, obj.width,obj.height)


def hborders(canvas, x,y, hobj):
    canvas.line(x,y, x,y+hobj.height)
    canvas.line(x+hobj.width,y, x+hobj.width,y+hobj.height)
    
    curx = x
    if hobj.wrappables:
        for ww in hobj.wrappables[:-1]:
            canvas.line(curx+ww.width,y, curx+ww.width,y+hobj.height)
            curx += ww.width

def vborders(canvas, x,y, vobj):
    canvas.line(x,y, x+vobj.width,y)
    #canvas.line(x,y+vobj.height, x+vobj.width,y+vobj.height)
    
    cury = y
    if vobj.wrappables:
        for ww in vobj.wrappables:
            canvas.line(x,cury+ww.height, x+vobj.width,cury+ww.height)
            cury += ww.height

def table_borders(canvas, x,y, vobj):
    canvas.line(x,y, x+vobj.width,y)
    #canvas.line(x,y+vobj.height, x+vobj.width,y+vobj.height)
    
    cury = y
    if vobj.wrappables:
        for hobj in vobj.wrappables:
            hborders(canvas, x,cury, hobj)
            canvas.line(x,cury+hobj.height, x+vobj.width,cury+hobj.height)
            cury += hobj.height

class Generic(object):
    def __init__(self, canvas, x,y, obj):
        pass