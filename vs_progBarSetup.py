import time
import nuke

tsk1 = nuke.ProgressTask("Frame")
tsk2 = nuke.ProgressTask("Iteration")

frameRange = 50
iter = 50

for f in range(frameRange):
    if tsk1.isCancelled():
        break
    percentage_init = int(100 * (float(f) / (frameRange - 1)))
    tsk1.setProgress(percentage_init)
    tsk1.setMessage("Frame %s of %d" % (f, frameRange))
    time.sleep(0.5)
    for i in range(iter):
        if tsk2.isCancelled():
            break
        percentageSec = int(100 * (float(i) / (iter - 1)))
        tsk2.setProgress(percentageSec)
        tsk2.setMessage("Iterations %s of %d" % (i, iter))
        time.sleep(0.1)

del tsk1, tsk2