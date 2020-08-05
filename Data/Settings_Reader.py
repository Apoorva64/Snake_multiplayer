# Fonctions pour lire les settings files
def Read_Settings_Server():
	Settings_File = open("Settings.txt", "r")
	Header=[]
	for loop in range(2):
		Header.append(Settings_File.readline())
	Data={}
	# print(Header)
	# x=str(Settings_File.readline())
	# print(x.split(' = ')
	Data['Game_Update_Fps']=int(Settings_File.readline().split('Game_Update_Fps  	= ')[1].strip('\n'))
	Data['Server_Update_Fps']=int(Settings_File.readline().split('Server_Update_Fps	= ')[1].strip('\n'))
	Data['Background_Color']=Settings_File.readline().split('Background_Color 	= ')[1].strip('\n').split(' ')
	for i,color in enumerate (Data['Background_Color']):
		Data['Background_Color'][i]=int(color.split(':')[1])
	Data['Enable_Draw']=Settings_File.readline().split('Enable_Draw        	= ')[1].strip('\n')
	if Data['Enable_Draw']=='True':
		Data['Enable_Draw']=True
	else:
		Data['Enable_Draw']=False
	return Data
#print(Read_Settings_Server())
def Read_Settings_Client():
	Settings_File = open("Settings_client.txt", "r")
	Header=[]
	for loop in range(2):
		Header.append(Settings_File.readline())
	Data={}
	# print(Header)
	# x=str(Settings_File.readline())
	# print(x.split(' = ')
	Data['Client_Update_Fps']=int(Settings_File.readline().split('Client_Update_Fps  	= ')[1].strip('\n'))
	#Data['Server_Update_Fps']=int(Settings_File.readline().split('Server_Update_Fps	= ')[1].strip('\n'))
	Data['Background_Color']=Settings_File.readline().split('Background_Color 	= ')[1].strip('\n').split(' ')
	for i,color in enumerate (Data['Background_Color']):
		Data['Background_Color'][i]=int(color.split(':')[1])
	Data['Draw_Grid']=Settings_File.readline().split('Draw_grid               = ')[1].strip('\n')
	if Data['Draw_Grid']=='True':
		Data['Draw_Grid']=True
	else:
		Data['Draw_Grid']=False
	return Data
def Write_Settings_Server(Game_Update_Fps,Server_Update_Fps,Background_Color,Enable_Draw):
	Settings_File = open("Settings.txt", "w")
	Settings_File.write("This is the File to edit the settings of the server\n")
	Settings_File.write("\n")
	Settings_File.write("Game_Update_Fps  	= "+str(Game_Update_Fps)+"\n")
	Settings_File.write("Server_Update_Fps	= "+str(Server_Update_Fps)+"\n")
	Settings_File.write("Background_Color 	= R:"+str(Background_Color[0])+" G:"+str(Background_Color[1])+" B:"+str(Background_Color[2])+"\n")
	Settings_File.write("Enable_Draw        	= "+str(Enable_Draw)+"\n")
	Settings_File.close()
def Write_Settings_Client(Client_Update_Fps,Background_Color,Draw_Grid):
	Settings_File = open("Settings_client.txt", "w")
	Settings_File.write("#settings_client\n")
	Settings_File.write("\n")
	Settings_File.write("Client_Update_Fps  	= "+str(Client_Update_Fps)+"\n")
	Settings_File.write("Background_Color 	= R:"+str(Background_Color[0])+" G:"+str(Background_Color[1])+" B:"+str(Background_Color[2])+"\n")
	Settings_File.write("Draw_grid               = "+str(Draw_Grid)+"\n")
	Settings_File.close()

# #######################CLIENT SETTINGS
# #reading
# settings_client=Read_Settings_Client()

# Client_Update_Fps=settings_client['Client_Update_Fps']
# Background_Color=settings_client['Background_Color']
# Draw_Grid=settings_client['Draw_Grid']
# #Changing values
# Client_Update_Fps=50
# Background_Color=[100,100,100]
# Draw_Grid=False
# #Writing
# Write_Settings_Client(Client_Update_Fps,Background_Color,Draw_Grid)


# #######################SERVER SETTINGS
# # Reading
# settings_server=Read_Settings_Server()

# Game_Update_Fps  	= settings_server['Game_Update_Fps']
# Server_Update_Fps	= settings_server['Server_Update_Fps']
# Background_Color 	= settings_server['Background_Color']
# Enable_Draw        	= settings_server['Enable_Draw']

# #Changing Values
# Game_Update_Fps  	= 25
# Server_Update_Fps	= 50
# Background_Color 	= [0,100,15]
# Enable_Draw        	= False
# #writing
# Write_Settings_Server(Game_Update_Fps,Server_Update_Fps,Background_Color,Enable_Draw)

