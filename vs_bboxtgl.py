import nuke

def bbox_toggle():
    for node in nuke.selectedNodes():
        if node.knob('bbox'):
            if node['bbox'].value() == "union":
                node['bbox'].setValue('B')
            else:
                node['bbox'].setValue('union')

nuke.menu('Nuke').addMenu('sj_tools').addCommand('Bbox toggle', lambda: bbox_toggle(), 'ctrl+B')