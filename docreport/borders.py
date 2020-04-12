
def borderbox(canvas, x,y, obj):
    canvas.rect(x,y, obj.width,obj.height)

def getRborderbox(radius):
    def rborderbox(canvas, x,y, obj):
        canvas.roundRect(x,y, obj.width,obj.height, radius)
    return rborderbox

def hborders(canvas, x,y, hobj):
    canvas.line(x,y, x,y+hobj.height)

    if hobj.paths:
        for path in hobj.paths[:-1]:
            canvas.line(x+path.x+path.width,y, x+path.x+path.width,y+hobj.height)
    canvas.line(x+hobj.width,y, x+hobj.width,y+hobj.height)

def vborders(canvas, x,y, vobj):
    canvas.line(x,y, x+vobj.width,y)
    #canvas.line(x,y+vobj.height, x+vobj.width,y+vobj.height)

    if vobj.paths:
        for path in vobj.paths:
            canvas.line(x,y+path.y+path.height, x+vobj.width,y+path.y+path.height)


def table_borders(canvas, x,y, vobj):
    canvas.line(x,y, x+vobj.width,y)
    #canvas.line(x,y+vobj.height, x+vobj.width,y+vobj.height)
    cury = y
    if vobj.paths:
        for path in vobj.paths:
            hborders(canvas, x,cury, path.wrappable)
            canvas.line(x,y+path.y+path.height, x+vobj.width,y+path.y+path.height)
            cury += path.height

class Generic(object):
    def __init__(self, canvas, x,y, obj):
        pass