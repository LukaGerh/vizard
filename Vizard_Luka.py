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

#Paslēpj dialoga paneli, kad tiek nospiesta kāda no apstiprinošajām pogām
def hideDialog():
	while True:
		yield playOptionsDlg.show()

		if playOptionsDlg.accepted:
			global selectedOption
			selectedOption = playOptionsDlg.selection
			return showModeElements(selectedOption)
			
		else:
			return viz.quit()
	

viztask.schedule(hideDialog())		





#Parāda izvēletā režīma elementus
def showModeElements(selectedOption):
	if selectedOption == 0:
		
		inputBox = vizdlg.InputDialog(prompt='Enter your nickname: ', value='Nickname', length=1.0, validate=validateInput)
		panel.addItem(inputBox, fontSize=16, padding=16, align=vizdlg.ALIGN_CENTER)
		
		inputBox.visible(True)
	else:
		panel.setCellLayout(vizdlg.LAYOUT_HORZ_CENTER) 
		global inputBox2
		global inputBox3
		
		inputBox2 = vizdlg.InputDialog(prompt='Enter first player\'s nickname: ', value='Nickname', length=1.0, validate=validateInput)
		panel.addItem(inputBox2, fontSize=16, padding=16)
		inputBox3 = vizdlg.InputDialog(prompt='Enter second player\'s nickname: ', value='Nickname 2', length=1.0, validate=validateInput)
		panel.addItem(inputBox3, fontSize=16, padding=16)
		
		inputBox2.visible(True)
		inputBox3.visible(False)
		

def validateInput(inputBox):
	global inpBoxValue
	inpBoxValue = []
	
	if inputBox2.accepted or inputBox3.accepted:
		if len(inputBox.value) <= 10:
			inpBoxValue.append = inputBox.value
			if inpBoxValue[0] != inpBoxValue[1]:
				inputBox3.visible(True)
				return True
			else:
				inputBox.error = 'The nickname doesn\'t meet the requirments'
				return False
	else:
		inputBox.error = 'The nickname doesn\'t meet the requirments'
		return False

def inputCheck():
	yield inputBox2.show()
	nickname1 = inputBox2.value
	
	if inputBox2.accepted:
		inputBox2.visible(False)
	
	yield inputBox3.show()
	nickname2 = inputBox3.value
	
	if nickname1 != nickname2:
		inputBox3.visible(False)
	else:
		inputBox3.error= "Nicknames can\'t be the same"
viztask.schedule(inputCheck())

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