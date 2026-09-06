import viz
import vizshape
import vizcam
import vizdlg
import vizinfo
import viztask
import vizinput
viz.go(viz.FULLSCREEN)
'''
custom_theme = viz.Theme()
custom_theme.back = [205/255.0, 20/255.0, 20/255.0, 0.8]

viz.setTheme(custom_theme)
'''

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

'''
NicknameLabel = panel.addItem(viz.addText('Enter first player\'s nickname: '),align=vizdlg.ALIGN_CENTER)
NicknameLabel2 = panel.addItem(viz.addText('Enter second player\'s nickname: '),align=vizdlg.ALIGN_CENTER)
inputBox = vizdlg.InputDialog(value='Nickname',length=1.0,validate=None)
inputBox2 = vizdlg.InputDialog(value='Nickname',length=1.0,validate=None)

panel.addItem(inputBox, fontSize=16, padding=16)
panel.addItem(inputBox2, fontSize=16, padding=16)
'''
'''
inputBox.drawOrder(2)
inputBox2.drawOrder(3)


playOptionsDlg.visible(True)
NicknameLabel.visible(False)
NicknameLabel2.visible(False)
inputBox.visible(False)
'''
'''
playOptionsDlg.onAccept(changeScreen())

def changeScreen():
	if  playOptionsDlg.accepted == True:
		playOptionsDlg.visible(False)
		NicknameLabel.visible(True)
		inputBox.visible(True)
	else:

'''		


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
                    break
            else:
                return viz.quit()

viztask.schedule(handleGameSetup())


def validateInput(inputBox):
    if 0 < len(inputBox.value) <= 10:
        return True
    else:
        inputBox.error = 'Nickname must be 1 to 10 characters long'
        return False


#def showEnv(bool):
	
'''
def checkNicknames():
	while True:
		yield inputBox2.show() and inputBox3.show()
		
'''	
	

			
	
#vizinput.message('The nicknames doesn\'t meet the requirments')






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


'''

if __name__ == "__main__":
	viz.go()