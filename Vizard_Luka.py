import viz
import vizshape
import vizcam
import vizdlg
import vizinfo
import viztask
import vizinput
import vizfx
import random
import vizmat
viz.go(viz.FULLSCREEN)




#Paneļa izveide
panel = vizdlg.Panel(layout=vizdlg.LAYOUT_VERT_CENTER, align=vizdlg.ALIGN_CENTER, background=True, border=True, theme=None, drawOrder=1)
panel.setMinSize([1000, 600])
viz.link(viz.MainWindow.CenterCenter, panel)

panel.Texture = None
panel.color([205/255.0, 20/255.0, 20/255.0, 0.8])

prompt = "Choose one of the following modes: "
options = ['Single player','Two players']
playOptionsDlg = vizdlg.AskDialog(prompt, options=options, title = "Choose mode")
panel.addItem(playOptionsDlg, visible=True)



def handleGameSetup():

    global nickname1, nickname2

    # Izvēlās spēles režīmu
    yield playOptionsDlg.show()
    
    if not playOptionsDlg.accepted:
        return viz.quit()

    selectedOption = playOptionsDlg.selection

    # Viena spēlētāja režīms
    if selectedOption == 0:
        inputBox = vizdlg.InputDialog(prompt='Enter your nickname: ', value='Nickname', length=1.0, validate=validateInput)
        panel.addItem(inputBox, fontSize=16, padding=16, align=vizdlg.ALIGN_CENTER)
        
        yield inputBox.show()
        if inputBox.accepted:
            nickname1 = inputBox.value
            inputBox.visible(False)
            showOneWindow()
        else:
            viz.quit()
            return

    # Divu spēlētāju režīms
    else:
        panel.setCellLayout(vizdlg.LAYOUT_HORZ_CENTER)
        
        # Pirmais spēlētājs
        inputBox2 = vizdlg.InputDialog(prompt='Enter first player\'s nickname: ', value='Nickname 1', length=1.0, validate=validateInput)
        panel.addItem(inputBox2, fontSize=16, padding=16)
        
        yield inputBox2.show()
        if inputBox2.accepted:
            nickname1 = inputBox2.value
            inputBox2.visible(False)
        else:
            return viz.quit()
        
        # Izveidojam otro logu vienu reizi pirms cikla
        inputBox3 = vizdlg.InputDialog(prompt='Enter second player\'s nickname: ', value='Nickname 2', length=1.0, validate=validateInput)
        panel.addItem(inputBox3, fontSize=16, padding=16)
        
        # cikls, kas turpinās kamēr būs atšķirīgi vārdi
        while True:
            yield inputBox3.show()
            
            if inputBox3.accepted:
                if inputBox3.value == nickname1:
                    inputBox3.error = "Nicknames can't be the same!"
                else:
                    nickname2 = inputBox3.value
                    inputBox3.visible(False)
                    return showTwoWindows()
            else:
                return viz.quit()

viztask.schedule(handleGameSetup())


def validateInput(inputBox):
    if 0 < len(inputBox.value) <= 10:
        return True
    else:
        inputBox.error = 'Nickname must be 1 to 10 characters long'
        return False






def showOneWindow():
    panel.remove()



def showTwoWindows():
    
    panel.remove()
       	
    global firstWindowView, secondWindowView
    firstWindowView = viz.addView()
    firstWindowView.setPosition([0, 0.5, -18], mode=viz.REL_PARENT)
    firstWindow = viz.addWindow()
    firstWindow.setSize([0.5, 1])
    firstWindow.setPosition( 0,1 )
    firstWindow.setView(firstWindowView)
    
    
    secondWindowView = viz.addView()
    secondWindowView.setPosition([0, 0.5, -18], mode=viz.REL_PARENT)
    secondWindow = viz.addWindow()
    secondWindow.setSize([0.5, 1])
    secondWindow.setPosition( 0.5, 1 )
    secondWindow.setView(secondWindowView)
    
    
    
    
    TURN_SPEED = 60
    
    def update_view():
        if viz.key.isDown('d'):
            firstWindowView.setEuler([TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown('a'):
            firstWindowView.setEuler([-TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown(viz.KEY_RIGHT):
            secondWindowView.setEuler([TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown(viz.KEY_LEFT):
            secondWindowView.setEuler([-TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)


    vizact.ontimer(0, update_view)
    
    
    
    
    vizact.whilekeydown('w', firstWindowView.move, [0, 0, 0.1])
    vizact.whilekeydown('s', firstWindowView.move, [0, 0, -0.1])

   
    vizact.whilekeydown(viz.KEY_UP, secondWindowView.move, [0, 0, 0.1])
    vizact.whilekeydown(viz.KEY_DOWN, secondWindowView.move, [0, 0, -0.1])
  

    createObjects()
    
    
    
    
    
    
    
firstWindowView = None
secondWindowView = None    
balls = []



def createObjects():
    plane = vizshape.addPlane(size=(25.0, 25.0))
    plane.setPosition( 0, 0, 0 )
    light = vizfx.addDirectionalLight(color=viz.BLUE, euler=(0,90,0))
    

    
    global balls
    balls = []

    def randomPosElements():
    
        #firstViewXZ = firstViewPos[0]
        
        for i in range(4):
            xCoordinate = random.randint(-12, 12)
            zCoordinate = random.randint(-12, 12)
            ball = vizshape.addSphere(	 
            radius = 1.0,	 
            slices = 20, 
            stacks = 20,	 
            axis = vizshape.AXIS_Y	 
            )
            ball.setPosition(xCoordinate, 0.5, zCoordinate)
            ball.setScale(0.5,0.5,0.5)
            balls.append(ball)
            '''
            ballPosition = ball.getPosition()
            ballsPos.append(ballPosition)
            '''
    randomPosElements()
        
        
def checkDistance():
    global firstWindowView,secondWindowView, balls
    if firstWindowView == None or secondWindowView == None:
        return
        
    currentFirstViewPos = firstWindowView.getPosition()
    currentSecondViewPos = secondWindowView.getPosition()
        
    for ball in balls[:]:
        ballPos = ball.getPosition()
        distanceFirst = vizmat.Distance(currentFirstViewPos, ballPos)
        distanceSecond = vizmat.Distance(currentSecondViewPos, ballPos)
            
        if distanceFirst <= 1.0:
            ball.remove()      
            balls.remove(ball)
        elif distanceSecond <= 1.0:    
            ball.remove()      
            balls.remove(ball)
            
            
            '''
        for ballPos in ballsPos[:]:
            distance = vizmat.Distance(firstViewPos, ballPos)
            if distance <= 1.0:
                balls[ballPos].remove()
                
            else:
                print('all good')
            
            '''
            
vizact.ontimer(0, checkDistance)
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

'''

for ball in balls[:]:
            ballPos = ball.getPosition()
            ballsPos.append(ballPos)



    viz.add('tut_ground.wrl')
    viz.window.setPosition([400,200])
    
    
    
    window = viz.addWindow()
    
    window.setPosition([400, 500])
    
    view2 = viz.addView()
    
    myScene = viz.addScene()

    #Make new scene active
    
    '''
        
    
'''
 
viz.clearcolor(viz.SKYBLUE)

dir_light = viz.addDirectionalLight()
dir_light.direction(0, -1, 0)
dir_light.intensity(10)

floor = vizshape.addPlane(size=(20, 20), axis=vizshape.AXIS_Y, 
cullFace=False)
floor.setPosition(0, 0, 0)
floor.color(viz.GRAY)

navigator = vizcam.addWalkNavigate()
viz.cam.setHandler(navigator)
viz.MainView.setPosition(0, 1.8, 10)
viz.MainView.setEuler(0, 0, 0)

ball = vizshape.addSphere(radius=0.5)
ball.setPosition(2, 0.5, 2)
ball.color(viz.RED)

cube = vizshape.addCube(size=1)
cube.setPosition(-2, 0.5, -2)
cube.color(viz.BLUE)



cylinder = vizshape.addCylinder(height=1, radius=0.5)
cylinder.setPosition(0, 0.5, -5)
cylinder.color(viz.GREEN)


head_light = viz.MainView.getHeadLight()
head_light.intensity(0.5)

viz.window.setFullscreenRectangle( [0,0,650,300] )
startWindow = viz.addWindow()

chooseName = viz.addText('Ievadi vārdu ludzu')




if __name__ == "__main__":
        viz.go()

'''

