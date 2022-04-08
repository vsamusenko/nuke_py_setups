import nuke

def brshCol():
   for i in nuke.allNodes('RotoPaint'):
      if i.knob('toolbar_paint_color'):
         print(i['toolbar_paint_color'].value())
         if i['toolbar_paint_color'].value() == [1, 0, 0, 1]:
            i['toolbar_paint_color'].setValue([0, 1, 0, 1])
         elif i['toolbar_paint_color'].value() == [0, 1, 0, 1]:
            i['toolbar_paint_color'].setValue([0, 0, 1, 1])
         else:
            i['toolbar_paint_color'].setValue([1, 0, 0, 1])

nuke.menu('Nuke').addMenu('sj_tools').addCommand('Cycle Brush Color', "paintColor()", 'Shift+0')