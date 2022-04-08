import nukescripts
import nuke
import re
import os
from glob import glob

os.environ['SHOW'] = 'fooShow'
os.environ['SEQ'] = 'fooSeq'
os.environ['SHOT'] = 'fooShot'


def rootDir():
    return 'C:/projects/'


def nukeDir():
    nkDir = os.path.join(rootDir(), os.getenv('SHOW'), os.getenv('SEQ'), os.getenv('SHOT'), 'nuke')
    if not os.path.isdir(nkDir):
        raise ValueError('Nuke directory does not exist!')
    return nkDir


def easySave():
    nkDir = nukeDir()
    description = nuke.getInput('script description', 'bashComp').replace(' ', '')

    fileSaved = False
    version = 1
    while not fileSaved:
        nkName = '%s_%s_%s_%s_v%02d.nk' % (os.getenv('SHOW'), os.getenv('SEQ'), os.getenv('SHOT'), description, version)
        nkPath = os.path.join(nkDir, nkName)
        if os.path.isfile(nkPath):
            version += 1
            continue
        nuke.scriptSaveAs(nkPath)
        fileSaved = True
    return nkPath


def checkScriptName():
    if not re.search(r'[vV]\d+', nuke.root().name()):
        raise NameError('Please include a version number and save script again.')


def getNukeScripts():
    nukeDir = os.path.join(rootDir(), os.getenv('SHOW'), os.getenv('SEQ'), os.getenv('SHOT'), 'nuke')
    nkFiles = glob(os.path.join(nukeDir, '*.nk'))
    return nkFiles


def getVersions():
    types = ['plates', 'cg', 'comp', 'roto']
    versionDict = {}
    shotDir = os.path.join(rootDir(), os.getenv('SHOW'), os.getenv('SEQ'), os.getenv('SHOT'))
    for t in types:
        versionDict[t] = []
        typeDir = os.path.join(shotDir, t)
        for d in os.listdir(typeDir):
            path = os.path.join(typeDir, d)
            if os.path.isdir(path):
                versionDict[t].append(
                    getFileSeq(path))

    return versionDict


def createVersionKnobs():
    node = nuke.thisNode()
    tabKnob = nuke.Tab_Knob('DB', 'DB')
    typeKnob = nuke.Enumeration_Knob('versionType', 'type', ['plates', 'cg', 'roto'])
    updateKnob = nuke.PyScript_Knob('update', 'update')
    updateKnob.setValue('assetManager.updateVersionKnob()')
    versionKnob = nuke.Enumeration_Knob('_version', 'version', [])
    loadKnob = nuke.PyScript_Knob('load', 'load')
    loadScript = '''
node = nuke.thisNode()
path, range = node['_version'].value().split()
first, last = range.split('-')
node['file'].setValue( path )
node['first'].setValue( int(first) )
node['last'].setValue( int(last) )'''

    loadKnob.setValue(loadScript)

    for k in (tabKnob, typeKnob, updateKnob, versionKnob, loadKnob):
        node.addKnob(k)
    updateVersionKnob()


def updateVersionKnob():
    node = nuke.thisNode()
    knob = nuke.thisKnob()

    if not knob or knob.name() in ['versionType', 'showPanel']:
        versionDict = getVersions()
        node['_version'].setValues(versionDict[node['versionType'].value()])
        node['_version'].setValue(0)


def createOutDirs():
    trgDir = os.path.dirname(nuke.filename(nuke.thisNode()))
    if not os.path.isdir(trgDir):
        os.makedirs(trgDir)


def getFileSeq(dirPath):
    dirName = os.path.basename(dirPath)
    files = glob(os.path.join(dirPath, '%s.*.*' % dirName))
    firstString = re.findall(r'\d+', files[0])[-1]
    padding = len(firstString)
    paddingString = '%02s' % padding
    first = int(firstString)
    last = int(re.findall(r'\d+', files[-1])[-1])
    ext = os.path.splitext(files[0])[-1]
    fileName = '%s.%%%sd%s %s-%s' % (dirName, str(padding).zfill(2), ext, first, last)
    return os.path.join(dirPath, fileName)


class NkPanel(nukescripts.PythonPanel):
    def __init__(self, nkScripts):
        nukescripts.PythonPanel.__init__(self, 'Open Nuke Script')
        self.checkboxes = []
        self.nkScripts = nkScripts
        self.selectedScript = ''

        for i, n in enumerate(self.nkScripts):
            k = nuke.Boolean_Knob('nk_%s' % i, os.path.basename(n))
            self.addKnob(k)
            k.setFlag(nuke.STARTLINE)
            self.checkboxes.append(k)

    def knobChanged(self, knob):
        if knob in self.checkboxes:
            for cb in self.checkboxes:
                if knob == cb:
                    index = int(knob.name().split('_')[-1])
                    self.selectedScript = self.nkScripts[index]
                    continue
                cb.setValue(False)



