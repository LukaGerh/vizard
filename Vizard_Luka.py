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


viz.mouse.setOverride(	 
    state = viz.ON	 
)




panel = vizdlg.Panel(layout=vizdlg.LAYOUT_VERT_CENTER, align=vizdlg.ALIGN_CENTER, background=True, border=True, theme=None, drawOrder=1)
panel.setMinSize([1000, 600])
viz.link(viz.MainWindow.CenterCenter, panel)

panel.Texture = None
panel.color([205/255.0, 20/255.0, 20/255.0, 0.8])

prompt = "Choose one of the following modes: "
options = ['Single player','Two players']
playOptionsDlg = vizdlg.AskDialog(prompt, options=options, title = "Choose mode")
panel.addItem(playOptionsDlg, visible=True)

singlePlayer = False
multiPlayer = False

firstWindowView = None
secondWindowView = None    

pointCount = 0
pointCount2 = 0
pointCount3 = 0
balls = []
cylinders = []
cubes = []
gameTime = 30  
gameActive = False





def handleGameSetup():

    global nickname1, nickname2#, nickname3

    
    yield playOptionsDlg.show()
    
    if not playOptionsDlg.accepted:
        return viz.quit()

    selectedOption = playOptionsDlg.selection

    
    if selectedOption == 0:
        inputBox = vizdlg.InputDialog(prompt='Enter your nickname: ', value='Player', length=1.0, validate=validateInput)
        panel.addItem(inputBox, fontSize=16, padding=16, align=vizdlg.ALIGN_CENTER)
        
        yield inputBox.show()
        if inputBox.accepted:
            nickname1 = inputBox.value
            inputBox.visible(False)
            showOneWindow(nickname1)
        else:
            viz.quit()
            return

    
    else:
        panel.setCellLayout(vizdlg.LAYOUT_HORZ_CENTER)
        
        
        inputBox2 = vizdlg.InputDialog(prompt='Enter first player\'s nickname: ', value='Player 1', length=1.0, validate=validateInput)
        panel.addItem(inputBox2, fontSize=16, padding=16)
        
        yield inputBox2.show()
        if inputBox2.accepted:
            nickname1 = inputBox2.value
            inputBox2.visible(False)
        else:
            return viz.quit()
        
        
        inputBox3 = vizdlg.InputDialog(prompt='Enter second player\'s nickname: ', value='Player 2', length=1.0, validate=validateInput)
        panel.addItem(inputBox3, fontSize=16, padding=16)
        

        while True:
            yield inputBox3.show()
            
            if inputBox3.accepted:
                if inputBox3.value == nickname1:
                    inputBox3.error = "Nicknames can't be the same!"
                else:
                    nickname2 = inputBox3.value
                    inputBox3.visible(False)
                    showTwoWindows(nickname1, nickname2)
                    return
            else:
                viz.quit()

viztask.schedule(handleGameSetup())


def validateInput(inputBox):
    if 0 < len(inputBox.value) <= 10:
        return True
    else:
        inputBox.error = 'Nickname must be 1 to 10 characters long'
        return False






def showOneWindow(nickname):
    panel.remove()
    
    global singlePlayer, pointCount, gameTime, gameActive, timerEvent
    gameActive = True
        
    
    viz.MainView.collision(viz.ON)
    
    monitor = viz.window.getMonitorList()
    monitorTop = monitor[0].size[1]
    monitorWidth = monitor[0].size[0]
    textY = monitorTop - 30
    textX = monitorWidth - 30
    
    
    
    singlePlayer = True
    
    viz.MainView.setPosition([0, 0.5, 0], mode=viz.REL_PARENT)
    
    playerLabel = viz.addText(	 
        value = 'Spēlētājs: ' + nickname,	 
        parent = viz.ORTHO, 
        scene = viz.MainWindow	 
    )
    playerLabel.color(0, 0, 0)
    playerLabel.fontSize(
        size = 30
    )
    
    playerLabel.alignment(viz.ALIGN_LEFT_TOP)
    playerLabel.setPosition(30,textY)
    
    
    pointsCollected = viz.addText(
        value = 'Punkti: ' + str(pointCount),	 
        parent = viz.ORTHO, 
        scene = viz.MainWindow	 
    )
    pointsCollected.color(0, 0, 0)
    pointsCollected.alignment(viz.ALIGN_RIGHT_TOP)
    pointsCollected.setPosition(textX,textY)
    pointsCollected.fontSize(
            size = 30
    )
    def collectedPoints():
    
        
        pointsCollected.message('Punkti: ' + str(pointCount))
        
    vizact.ontimer(0, collectedPoints)
    
    timerText = viz.addText(value = 'Laiks: ' + str(gameTime),	 
        parent = viz.ORTHO, 
        scene = viz.MainWindow	 
    )
    timerText.setPosition((textX+30)/2, (textY - 30))
    timerText.alignment(viz.ALIGN_LEFT_TOP)
    timerText.fontSize(
            size = 30
    )
    timerText.color(0, 0, 0)
 
    
    def updateTimer():
        global gameTime, gameActive, timerEvent
    
        if gameActive and gameTime > 0:
            gameTime -= 1
            timerText.message("Laiks: " + str(gameTime))
        
        if gameTime == 0:
            
            timerEvent.remove()
            
            viztask.schedule(endGame())
            
        
    
    
    timerEvent = vizact.ontimer(1.0, updateTimer)
        
    
    def endGame():
        global pointCount, gameActive
        gameActive = False
        
        message='Tavs rezultāts ir: ' + str(pointCount)
        
        viz.MainView.collision(viz.OFF)
        viz.MainView.setPosition([0, 1000, 0])
        
        panel = vizdlg.Panel(layout=vizdlg.LAYOUT_VERT_CENTER, align=vizdlg.ALIGN_CENTER, background=True, border=True, theme=None, drawOrder=1)
        panel.setMinSize([1000, 600])
        viz.link(viz.MainWindow.CenterCenter, panel)
        panel.color([205/255.0, 20/255.0, 20/255.0, 0.8])
        
        dialog = vizdlg.MessageDialog(message=message, title='Punkti', accept='Labi', cancel='Arī labi')
        dialog.setScreenAlignment(viz.ALIGN_CENTER)
        panel.addItem(dialog)
        while True:
            yield dialog.show()

            if dialog.accepted:
                viz.quit()
            else:
                viz.quit()

            yield viztask.waitTime(1)
    
    TURN_SPEED = 60
    
    def update_main_view():
        global gameActive
        
        
        if not gameActive:
            return
        if viz.key.isDown('d'):
            viz.MainView.setEuler([TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown('a'):
            viz.MainView.setEuler([-TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown(viz.KEY_RIGHT):
            viz.MainView.setEuler([TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown(viz.KEY_LEFT):
            viz.MainView.setEuler([-TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
    
       
    vizact.whilekeydown('w', viz.MainView.move, [0, 0, 0.1])
    vizact.whilekeydown('s', viz.MainView.move, [0, 0, -0.1])

           
    vizact.whilekeydown(viz.KEY_UP, viz.MainView.move, [0, 0, 0.1])
    vizact.whilekeydown(viz.KEY_DOWN, viz.MainView.move, [0, 0, -0.1])
    
    vizact.ontimer(0, update_main_view)
    createObjects()


def showTwoWindows(nickname1, nickname2):
    panel.remove()
    
    
    
    monitor = viz.window.getMonitorList()
    monitorTop = monitor[0].size[1]
    monitorWidth = monitor[0].size[0] / 2
    textY = monitorTop - 30
    textX = monitorWidth - 30
    
    
    
    
    global multiPlayer, pointCount2, pointCount3, gameActive, gameTime, timerEvent, firstWindow, secondWindow
    gameActive = True
    multiPlayer = True
    gameTime = 30
       	
    global firstWindowView, secondWindowView
   
    
    firstWindowView = viz.addView()
    firstWindowView.setPosition([0, 0.5, 0], mode=viz.REL_PARENT)
    firstWindow = viz.addWindow()
    firstWindow.setSize([0.5, 1])
    firstWindow.setPosition( 0,1 )
    firstWindow.setView(firstWindowView)
    
    
    secondWindowView = viz.addView()
    secondWindowView.setPosition([0, 0.5, 0], mode=viz.REL_PARENT)
    secondWindowView.setEuler(180, 0, 0)
    secondWindow = viz.addWindow()
    secondWindow.setSize([0.5, 1])
    secondWindow.setPosition( 0.5, 1 )
    secondWindow.setView(secondWindowView)
    
    firstWindowView.collision(viz.ON)
    secondWindowView.collision(viz.ON)
    
    playerLabel = viz.addText(	 
        value = 'Spēlētājs: ' + nickname1,	 
        parent = viz.ORTHO, 
        scene = firstWindow	 
    )
    
    playerLabel.fontSize(
        size = 30
    )
    playerLabel.alignment(viz.ALIGN_LEFT_TOP)
    playerLabel.setPosition(30,textY)
    playerLabel.color(0, 0, 0)
    
    playerLabel2 = viz.addText(	 
        value = 'Spēlētājs: ' + nickname2,	 
        parent = viz.ORTHO, 
        scene = secondWindow	 
    )
    
    playerLabel2.fontSize(
        size = 30
    )
    playerLabel2.alignment(viz.ALIGN_LEFT_TOP)
    playerLabel2.setPosition(30,textY)
    playerLabel2.color(0, 0, 0)
    
    
    timerText1 = viz.addText(value='Laiks: ' + str(gameTime), parent=viz.ORTHO, scene=firstWindow)
    timerText1.setPosition((textX + 30) / 2, (textY - 30))
    timerText1.alignment(viz.ALIGN_LEFT_TOP)
    timerText1.fontSize(size=30)
    timerText1.color(0, 0, 0)

    timerText2 = viz.addText(value='Laiks: ' + str(gameTime), parent=viz.ORTHO, scene=secondWindow)
    timerText2.setPosition((textX + 30) / 2, (textY - 30))
    timerText2.alignment(viz.ALIGN_LEFT_TOP)
    timerText2.fontSize(size=30)
    timerText2.color(0, 0, 0)
    
    
    def updateTimerMulti():
        global gameTime, gameActive, timerEvent
        if gameActive and gameTime > 0:
            gameTime -= 1
            timerText1.message("Laiks: " + str(gameTime))
            timerText2.message("Laiks: " + str(gameTime))

        if gameTime == 0:
            timerEvent.remove()
            viztask.schedule(endGameMulti())
    
    timerEvent = vizact.ontimer(1.0, updateTimerMulti)
    
    def endGameMulti():
        global pointCount2, pointCount3, gameActive
        gameActive = False
        
        firstWindowView.collision(viz.OFF)
        secondWindowView.collision(viz.OFF)
        
        if pointCount2 > pointCount3:
            winnerMessage = nickname1 + ' uzvarēja ar ' + str(pointCount2) + ' punktiem!'
        elif pointCount3 > pointCount2:
            winnerMessage = nickname2 + ' uzvarēja ar ' + str(pointCount3) + ' punktiem!'
        else:
            winnerMessage = 'Neizšķirts! Abiem ir ' + str(pointCount2) + ' punkti.'

        
        firstWindowView.setPosition([0, 1000, 0])
        secondWindowView.setPosition([0, 1000, 0])

        
        resultText1 = viz.addText(winnerMessage, parent=viz.ORTHO, scene=firstWindow)
        resultText1.fontSize(25)
        resultText1.alignment(viz.ALIGN_CENTER)
        resultText1.setPosition(textX / 2, textY / 2)

        
        resultText2 = viz.addText(winnerMessage, parent=viz.ORTHO, scene=secondWindow)
        resultText2.fontSize(25)
        resultText2.alignment(viz.ALIGN_CENTER)
        resultText2.setPosition(textX / 2, textY / 2)

        
        dialog = vizdlg.MessageDialog(message='Spēle beigusies!', title='Rezultāts', accept='Iziet')
        yield dialog.show()
        viz.quit()
                    
            
    
    pointsCollected = viz.addText(
        value = 'Punkti: ' + str(pointCount2),	 
        parent = viz.ORTHO, 
        scene = firstWindow	 
    )
    pointsCollected.color(0, 0, 0)
    pointsCollected.alignment(viz.ALIGN_RIGHT_TOP)
    pointsCollected.setPosition(textX,textY)
    pointsCollected.fontSize(
            size = 30
    )
    pointsCollected2 = viz.addText(
        value = 'Punkti: ' + str(pointCount3),	 
        parent = viz.ORTHO, 
        scene = secondWindow 
    )
    pointsCollected2.color(0, 0, 0)
    pointsCollected2.alignment(viz.ALIGN_RIGHT_TOP)
    pointsCollected2.setPosition(textX,textY)
    pointsCollected2.fontSize(
            size = 30
    )
    def collectedPoints():
    
        
        pointsCollected.message('Punkti: ' + str(pointCount2))
        pointsCollected2.message('Punkti: ' + str(pointCount3))
        
    vizact.ontimer(0, collectedPoints)
    
    
    
    
    TURN_SPEED = 60
    
    def update_first_view():
        if viz.key.isDown('d'):
            firstWindowView.setEuler([TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown('a'):
            firstWindowView.setEuler([-TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        
    
    def update_second_view():
        if viz.key.isDown(viz.KEY_RIGHT):
            secondWindowView.setEuler([TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)
        elif viz.key.isDown(viz.KEY_LEFT):
            secondWindowView.setEuler([-TURN_SPEED * viz.elapsed(), 0, 0], viz.BODY_ORI, viz.REL_PARENT)

    vizact.ontimer(0, update_first_view)
    vizact.ontimer(0, update_second_view)
    
    
    
    
    vizact.whilekeydown('w', firstWindowView.move, [0, 0, 0.1])
    vizact.whilekeydown('s', firstWindowView.move, [0, 0, -0.1])

   
    vizact.whilekeydown(viz.KEY_UP, secondWindowView.move, [0, 0, 0.1])
    vizact.whilekeydown(viz.KEY_DOWN, secondWindowView.move, [0, 0, -0.1])
  
    
    createObjects()


def createObjects():
    light = vizfx.addDirectionalLight(color=viz.BLUE, euler=(0,90,0))
    
    floor = vizshape.addPlane(size=(25.0, 25.0))
    floor.disable(viz.COLLISION)
    floor.setPosition( 0, 0, 0 )
    floor.color(145, 145, 145)
    #floor.setEuler(180, 0, 0)
    ceiling = vizshape.addPlane(size=(25.0, 25.0))
    ceiling.setPosition(0, 6.0, 0)
    ceiling.setEuler(	 
        [0,0,180],	 
        mode = viz.ABS_GLOBAL
    )
    ceiling.color([255, 255, 255],
        node = '',
        op = viz.OP_DEFAULT
    )
    
    
    sidePlane1 = vizshape.addPlane(	 
        size = [25.0,6.0],	 
        axis = vizshape.AXIS_Z,	 
        cullFace = False  
    )
    sidePlane1.collideMesh()
    
    
    sidePlane1.setPosition(	 
        [0,3.0,-12.5],	 
        mode = viz.REL_PARENT
    )
    sidePlane1.color(	 
        [0, 255, 0],
        node = '',
        op = viz.OP_DEFAULT
    )
    
    
    sidePlane2 = vizshape.addPlane(	 
        size = [25.0,6.0],	 
        axis = vizshape.AXIS_X,	 
        cullFace = False  
    )
    sidePlane2.collideMesh()
    sidePlane2.setPosition(	 
        [-12.5,3.0,0],	 
        mode = viz.ABS_GLOBAL
    )
    sidePlane2.color(	 
        [128, 0, 128],
    )
    
    
    sidePlane3 = vizshape.addPlane(	 
        size = [25.0,6.0],	 
        axis = vizshape.AXIS_Z,	 
        cullFace = False  
    )
    sidePlane3.collideMesh()
    sidePlane3.setPosition(	 
        [0,3.0,12.5],	 
        mode = viz.ABS_GLOBAL
    )
    sidePlane3.setEuler(	 
        [0,180,0],	 
        mode = viz.ABS_GLOBAL
    )
    sidePlane3.color(	 
        [255, 165, 0],
    )
    
    
    sidePlane4 = vizshape.addPlane(
        size = [25.0,6.0],	 
        axis = vizshape.AXIS_X,	 
        cullFace = False  
    )
    sidePlane4.collideMesh()
    sidePlane4.setPosition(	 
        [12.5,3.0,0],	 
        mode = viz.ABS_GLOBAL
    )
    sidePlane4.setEuler(	 
        [180,0,0],	 
        mode = viz.ABS_GLOBAL
    )
    sidePlane4.color(	 
        [255, 0, 0],
    )
    

    #light = vizfx.addDirectionalLight(color=viz.WHITE, euler=(0,90,0))
    #light.setPosition(0, 3, 0)
        
    global balls, cylinders, cubes
    
    def randomPosElements():
            
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
                ball.color(0, 0, 0)
                balls.append(ball)
                ball.disable(viz.COLLISION)
        for i in range(2):
                xCoordinate = random.randint(-12, 12)  
                zCoordinate = random.randint(-12, 12) 
                cylinder = vizshape.addCylinder(	 
                height = 1.0,	 
                radius = 0.5,	 
                topRadius = None,	 
                bottomRadius = None, 
                axis = vizshape.AXIS_Y,	 
                slices = 20,	 
                bottom = True,	 
                top = True, 
                )
                cylinder.setPosition(xCoordinate, 0.4, zCoordinate)
                cylinder.setScale(0.5,0.5,0.5)
                cylinder.color(0, 0, 0)
                cylinders.append(cylinder)
                cylinder.disable(viz.COLLISION)
        for i in range(1):
                xCoordinate = random.randint(-12, 12)
                zCoordinate = random.randint(-12, 12)
                cube = vizshape.addCube(	 
                size = 1	 
                )
                cube.setPosition(xCoordinate, 0.5, zCoordinate)
                cube.setScale(0.5,0.5,0.5)
                cube.color(0, 0, 0)
                cubes.append(cube)
                cube.disable(viz.COLLISION)
    
               
    randomPosElements()

       
        
def checkDistance():
    global singlePlayer, multiPlayer, firstWindowView, secondWindowView, pointCount, pointCount2, pointCount3, balls, cylinders, cubes, gameActive
    
    if not gameActive:
        return
    
    if singlePlayer == True: 
        mainViewPos = viz.MainView.getPosition()
        
        for ball in balls[:]:
            ballPos = ball.getPosition()
            distanceMain = vizmat.Distance(mainViewPos, ballPos)
            if distanceMain <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                pointCount += 1
                ball.remove()      
                balls.remove(ball)
                additionalElement("ball")  

       
        for cylinder in cylinders[:]:
            cylinderPos = cylinder.getPosition()
            distanceMain = vizmat.Distance(mainViewPos, cylinderPos)
            if distanceMain <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                pointCount += 2
                cylinder.remove()      
                cylinders.remove(cylinder)
                additionalElement("cylinder")  

        
        for cube in cubes[:]:
            cubePos = cube.getPosition()
            distanceMain = vizmat.Distance(mainViewPos, cubePos)
            if distanceMain <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                pointCount += 3
                cube.remove()      
                cubes.remove(cube)
                additionalElement("cube")
                
        
    elif multiPlayer == True:
        
        currentFirstViewPos = firstWindowView.getPosition()
        currentSecondViewPos = secondWindowView.getPosition()
        
            
        for ball in balls[:]:
            ballPos = ball.getPosition()
            
            distanceFirst = vizmat.Distance(currentFirstViewPos, ballPos)
            distanceSecond = vizmat.Distance(currentSecondViewPos, ballPos)
            
                
            if distanceFirst <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                ball.remove()      
                balls.remove(ball)
                pointCount2+= 1
                additionalElement("ball")
            elif distanceSecond <= 1.0: 
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                ball.remove()      
                balls.remove(ball)
                pointCount3+= 1
                additionalElement("ball")
        for cylinder in cylinders[:]:
            cylinderPos = cylinder.getPosition()
            
            distanceFirst = vizmat.Distance(currentFirstViewPos, cylinderPos)
            distanceSecond = vizmat.Distance(currentSecondViewPos, cylinderPos)
            
                
            if distanceFirst <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                cylinder.remove()      
                cylinders.remove(cylinder)
                pointCount2+= 2
                additionalElement(cylinder)
            elif distanceSecond <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                cylinder.remove()      
                cylinders.remove(cylinder)
                pointCount3+= 2
                additionalElement(cylinder)
        for cube in cubes[:]:
            cubePos = cube.getPosition()
            
            distanceFirst = vizmat.Distance(currentFirstViewPos, cubePos)
            distanceSecond = vizmat.Distance(currentSecondViewPos, cubePos)
            
                
            if distanceFirst <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                cube.remove()      
                cubes.remove(cube)
                pointCount2+= 3
                additionalElement("cube")
            elif distanceSecond <= 1.0:
                sound = viz.addAudio('collectsound.mp3') 
                sound.play()
                cube.remove()      
                cubes.remove(cube)
                pointCount3+= 3
                additionalElement("cube")
    else:
        return
                
            

            
vizact.ontimer(0, checkDistance)
    
   
        
def additionalElement(elementType):
    global balls, cylinders, cubes
    xCoordinate = random.randint(-12, 12)
    zCoordinate = random.randint(-12, 12)
    if elementType == "ball":
    
        ball = vizshape.addSphere(	 
        radius = 1.0,	 
        slices = 20, 
        stacks = 20,	 
        axis = vizshape.AXIS_Y	 
        )
        ball.setPosition(xCoordinate, 0.5, zCoordinate)
        ball.setScale(0.5,0.5,0.5)
        ball.color(0, 0, 0)
        balls.append(ball)
        ball.disable(viz.COLLISION)
    elif elementType == "cylinder":
        
        cylinder = vizshape.addCylinder(	 
        height = 1.0,	 
        radius = 0.5,	 
        topRadius = None,	 
        bottomRadius = None, 
        axis = vizshape.AXIS_Y,	 
        slices = 20,	 
        bottom = True,	 
        top = True, 
        )
        cylinder.setPosition(xCoordinate, 0.5, zCoordinate)
        cylinder.setScale(0.5,0.5,0.5)
        cylinder.color(0, 0, 0)
        cylinders.append(cylinder)
        cylinder.disable(viz.COLLISION)
    elif elementType == "cube":
        
        cube = vizshape.addCube(	 
        size = 1	 
        )
        cube.setPosition(xCoordinate, 0.5, zCoordinate)
        cube.setScale(0.5,0.5,0.5)
        cube.color(0, 0, 0)
        cubes.append(cube)
        cube.disable(viz.COLLISION)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

