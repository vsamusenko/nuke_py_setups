import nuke

def sampleMnMx(src, chan='depth.Z'):

    minCl = nuke.nodes.MinColor(channels=chan, target=0, inputs=[src])
    inv = nuke.nodes.Invert(channels=chan, inputs=[src])
    maxCl = nuke.nodes.MinColor(channels=chan, target=0, inputs=[inv])

    curF = nuke.frame()
    nuke.execute(minCl, curF, curF)
    minD = -minCl['pixeldelta'].value()

    nuke.execute(maxCl, curF, curF)
    maxD = maxCl['pixeldelta'].value() + 1

    for n in (minCl, maxCl, inv):
        nuke.delete(n)
    return minD, maxD