import nuke
import subprocess

def submitToDeadline():
    panelConstr = nuke.Panel( 'Submit to Deadline' )

    panelConstr.addSingleLineInput( 'first', nuke.root().firstFrame() )
    panelConstr.addSingleLineInput( 'last', nuke.root().lastFrame() )

    panelConstr.addEnumerationPulldown( 'threads', '1 2 4 8' )
    panelConstr.addSingleLineInput( 'batch size', '10' )
    panelConstr.addBooleanCheckBox( 'local render', 0 )

    if panelConstr.show():
        args = dict( first = panelConstr.value('first'),
            last = panelConstr.value('last'),
            threads = panelConstr.value('threads'),
            batchSize = panelConstr.value('batch size'),
            local = panelConstr.value('local'),
            executable = 'C:/Program Files/Nuke13.1v1/Nuke13.1.exe')

        application = 'deadlinecommand.exe'


        cmdString = application + '-executable %(executable)s -range %(first)s-%(last)s -threads %(threads)s -batch %(batchSize)s' % args

        subprocess.Popen( cmdString.split() )

nuke.menu( 'Nuke' ).addCommand( 'Send to Deadline', submitToDeadline )