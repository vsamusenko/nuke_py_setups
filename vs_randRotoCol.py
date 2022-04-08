
import nuke
import random
import colorsys

def randRotoCol():
    node = nuke.thisNode()
    curveKnob = node['curves']
    rootLayer = curveKnob.rootLayer

    for shape in rootLayer:
        nodeAttributes = shape.getAttributes()
        if nodeAttributes.getValue(1, 'ro') == 0 and nodeAttributes.getValue(1, 'go') == 0 and nodeAttributes.getValue(1, 'bo') == 0:
            convert = colorsys.hsv_to_rgb(random.random(), 1, 1)
            nodeAttributes.set('ro', convert[0])
            nodeAttributes.set('go', convert[1])
            nodeAttributes.set('bo', convert[2])
            nodeAttributes.set('ao', 1)
            break

nuke.addKnobChanged(randRotoCol, nodeClass='Roto')