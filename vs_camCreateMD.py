import nuke

def createMetaDatCam(node):

    md = node.metadata()
    reqData = ['exr/nuke/camera/%s' % i for i in ('focal', 'haperture', 'vaperture', 'matrix')]
    if not set(reqData).issubset(md):
        print('Not enough data provided in metadata')
        return

    firstFrame = node.firstFrame()
    lastFrame = node.lastFrame()
    ret = nuke.getFramesAndViews('Create Camera', '%s-%s' %(firstFrame, lastFrame))
    frameRange = nuke.FrameRange(ret[0])

    NewCam = nuke.createNode('CameraFromMD')
    NewCam['useMatrix'].setValue(True)

    for k in ('focal', 'haperture', 'vaperture', 'matrix'):
        NewCam[k].setAnimated()

    progTask = nuke.ProgressTask( 'Baking camera settings in %s' % node.name())

    for currentTask, frame in enumerate(frameRange):
        if progTask.isCancelled():
            break
        progTask.setMessage('Processing frame %s' % frame)

        for k in ('focal', 'haperture', 'vaperture'):
            val = float(node.metadata( 'exr/nuke/camera/%s' % k, frame))
            NewCam[k].setValueAt(float(val), frame)

        matrixList = eval(node.metadata('exr/nuke/camera/matrix'))
        for i, v in enumerate(matrixList):
            NewCam['matrix'].setValueAt(v, frame, i)

        progTask.setProgress(int(float(currentTask) / frameRange.frames() * 100))
