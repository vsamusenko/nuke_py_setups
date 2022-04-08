import nuke

node = nuke.selectedNode()
for n in nuke.selectedNodes():
    n.setSelected(False)

node.setSelected(True)
nuke.nodeCopy("%clipboard%")
node.setSelected(False)

copiedNodes = nuke.nodePaste("%clipboard%")
copiedNodes.setSelected(False)
nuke.show(copiedNodes)

for i in range(node.inputs()):
    copiedNodes.setInput(i, node.input(i))

nodeEditor_offset = 45
copiedNodes['xpos'].setValue(node.xpos() + nodeEditor_offset)
copiedNodes['ypos'].setValue(node.ypos() + nodeEditor_offset)
