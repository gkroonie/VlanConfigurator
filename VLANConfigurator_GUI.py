#Using Python and the Netmiko library to run commands on Cisco IOS devices.



import netmiko
from tkinter import *
import sys
import time
from tkinter.messagebox import showinfo


#Called by the login button, this function validates that the user posseses the correct credentials.
def Login():  
    global user
    global pwd
    global enable
    user = username.get()
    pwd = password.get()
    enable = enableSecret.get()    

    connection = netmiko.ConnectHandler(ip="10.50.1.124", device_type="cisco_ios", username=user, password=pwd, secret=enable, fast_cli = False)
    connection.enable()
    
    testLogin = connection.send_command("sh env temp")
    
    connection.disconnect()

    if testLogin[:18] != "SYSTEM TEMPERATURE":
        showinfo("Error", "Bad login credentials. Please try again or give up and go home.")
        #cancelLogin()
    else:
        goodLogin_lbl = Label(top, text = "logging in...", font = ('Helvetica', 18)).pack()
        time.sleep(0.3)
    
    #Destroys login window and makes root visible.
    root.deiconify()
    top.grab_release()
    top.destroy()


#Allows the user to cancel out of the programme.
def cancelLogin():
    time.sleep(1)
    top.destroy()
    root.destroy()
    sys.exit()
    
    
#Build the "vlan access" string and submits the VLAN changes to the switch. 
def submission():
    switchportAllList = [SP2, SP4, SP6, SP8, SP10, SP12, SP14, SP16, SP18, SP20, SP22, SP24, SP26, SP28, SP30, SP32, SP34, SP36, SP38, SP40]
    
    switchportSelectionList = []
    for i in switchportAllList:
        #print (i.get()) #debug
        if i.get() != "0":
            switchportSelectionList.append(i.get())
    
    intSelectString1 = "int range "    
    intSelectString2 = ', '.join(str(x) for x in switchportSelectionList)
    intSelectString = intSelectString1 + intSelectString2
    print(intSelectString) #debug
    vlanSelectString = "switchport access vlan " + vlanID.get()
    print(vlanSelectString) #debug
  
    if vlanID.get() == "No Selection" and intSelectString == "int range ":
        showinfo("Error", "Please make sure you have selected both a VLAN ID and at least one switchport.")

    elif intSelectString == "int range ":
        showinfo("Error", "Please make sure you have selected at least one switchport.")

    elif vlanID.get() == "No Selection":
        showinfo("Error", "Please make sure you have selected a VLAN ID.")

    else:
        connection = netmiko.ConnectHandler(ip="10.50.1.124", device_type="cisco_ios", username=user, password=pwd, secret=enable, fast_cli = False, global_delay_factor = 10)
        connection.enable()
       
        #Command constructed from the checkbox variables.
        connection.send_config_set(config_commands = [intSelectString, vlanSelectString], exit_config_mode = True)
       
        connection.disconnect() 
    
    vlanID.set("No Selection")
    deselectAll()


    #Call getVLANs() to update display.
    getVLANs()


#Retrieves the current VLAN configuration from the switch.    
def getVLANs():
    displayVLANs.delete("1.0", "end")
    
    connection = netmiko.ConnectHandler(ip="10.50.1.124", device_type="cisco_ios", username=user, password=pwd, secret=enable)
    connection.enable()
    
    vlanConfig = connection.send_command("sh vlan brief")
 
    connection.disconnect()   
    
    #print (vlanConfig)
    
    displayVLANs.insert(INSERT, vlanConfig)
    

def selectAll():
    box1.select()
    box2.select()
    box3.select()
    box4.select()
    box5.select()
    box6.select()
    box7.select()
    box8.select()
    box9.select()
    box10.select()
    box11.select()
    box12.select()
    box13.select()
    box14.select()
    box15.select()
    box16.select()
    box17.select()
    box18.select()
    box19.select()
    box20.select()


def deselectAll():
    box1.deselect()
    box2.deselect()
    box3.deselect()
    box4.deselect()
    box5.deselect()
    box6.deselect()
    box7.deselect()
    box8.deselect()
    box9.deselect()
    box10.deselect()
    box11.deselect()
    box12.deselect()
    box13.deselect()
    box14.deselect()
    box15.deselect()
    box16.deselect()
    box17.deselect()
    box18.deselect()
    box19.deselect()
    box20.deselect()
    
    
#Creates the root (main) and login windows.
root = Tk()
top = Toplevel()
rightFrame = Frame(root)
rightFrame.pack(side = RIGHT, fill = BOTH, expand = True)

#Hides the root window and builds the login window 'above' it.
root.withdraw()
top.grab_set()
top.geometry("300x250")
top.title("Please Login")
top.lift(root)

#Creates the login page.
username_lbl = Label(top, text = "Username:", font = ('Helvetica', 10)).pack(pady = (5,0))
global username
username = StringVar()
username = Entry(top, textvariable = username)
username.pack()
password_lbl = Label(top, text = "Password:", font=('Helvetica', 10)).pack(pady = (5,0))
global password
password = StringVar()
password = Entry(top, show="*", textvariable = password)
password.pack()
enableSecret_lbl = Label(top, text = "Enable Secret:", font=('Helvetica', 10)).pack(pady = (5,0))
global enableSecret
enableSecret = StringVar()
enableSecret = Entry(top, show="*", textvariable = enableSecret)
enableSecret.pack()

login = Button(top, text = "Login", command = lambda:Login()).pack(padx = 10, pady = 10)
cancel = Button(top, text = "Cancel", command = lambda:cancelLogin()).pack(padx = 10)

loginNotice_lbl = Label(top, text = "Invalid credentials will simply do nothing...", font=('Helvetica', 8)).pack(side=BOTTOM, anchor=SE)



#Builds a root window that will dynamically resize itself around its component widgets.
root.title('VLAN Configurator - Open Bench')
root.geometry("1150x850")
#root.geometry("")
author_lbl = Label(rightFrame, text = "Written by George Kroon - December 2020", font=('Helvetica', 8)).pack(side=BOTTOM, anchor=SE, padx = 20, pady = (0, 5))

improvements_lbl = Label(rightFrame, text = "Desired Improvements:\n- Increase the delay_time so that the session doesn't time out with big changes.\n- Make the pop-up dialogue box for invalid credentials work (not function critical).\n- Show interface status window to see if switchports are up/down.\n- Display the VLAN config in a more human-readable way.", font=('Helvetica', 8), justify=LEFT, anchor="w").pack(side=BOTTOM, anchor=SW, padx = 20, pady = (0, 5))

SwitchPorts_lbl = Label(root, text = "Select Switchport/s:", font=('Helvetica', 10)).pack(anchor = W, padx = (20, 20), pady = (20,10))

#Button to call the selectAll() function and select all boxes.
selectAllBoxes = Button(root, text = "Select All", command = selectAll).pack(anchor = W, padx = (20, 10), pady = 5)

#Button to call the deselectAll() function and deselect all boxes.
deselectAllBoxes = Button(root, text = "Deselect All", command = deselectAll).pack(anchor = W, padx = (20, 10), pady = 5)

#Creates the switchport checkboxes.
SP2 = StringVar()
box1 = Checkbutton(root, text = "Switchport 2", variable = SP2, onvalue = "Gi4/0/2", offvalue = None)
box1.deselect()
box1.pack(anchor = W, padx = (20, 20))

SP4 = StringVar()
box2 = Checkbutton(root, text = "Switchport 4", variable = SP4, onvalue = "Gi4/0/4", offvalue = None)
box2.deselect()
box2.pack(anchor = W, padx = (20, 20))

SP6 = StringVar()
box3 = Checkbutton(root, text = "Switchport 6", variable = SP6, onvalue = "Gi4/0/6", offvalue = None)
box3.deselect()
box3.pack(anchor = W, padx = (20, 20))

SP8 = StringVar()
box4 = Checkbutton(root, text = "Switchport 8", variable = SP8, onvalue = "Gi4/0/8", offvalue = None)
box4.deselect()
box4.pack(anchor = W, padx = (20, 20))

SP10 = StringVar()
box5 = Checkbutton(root, text = "Switchport 10", variable = SP10, onvalue = "Gi4/0/10", offvalue = None)
box5.deselect()
box5.pack(anchor = W, padx = (20, 20))

SP12 = StringVar()
box6 = Checkbutton(root, text = "Switchport 12", variable = SP12, onvalue = "Gi4/0/12", offvalue = None)
box6.deselect()
box6.pack(anchor = W, padx = (20, 20))

SP14 = StringVar()
box7 = Checkbutton(root, text = "Switchport 14", variable = SP14, onvalue = "Gi4/0/14", offvalue = None)
box7.deselect()
box7.pack(anchor = W, padx = (20, 20))

SP16 = StringVar()
box8 = Checkbutton(root, text = "Switchport 16", variable = SP16, onvalue = "Gi4/0/16", offvalue = None)
box8.deselect()
box8.pack(anchor = W, padx = (20, 20))

SP18 = StringVar()
box9 = Checkbutton(root, text = "Switchport 18", variable = SP18, onvalue = "Gi4/0/18", offvalue = None)
box9.deselect()
box9.pack(anchor = W, padx = (20, 20))

SP20 = StringVar()
box10 = Checkbutton(root, text = "Switchport 20", variable = SP20, onvalue = "Gi4/0/20", offvalue = None)
box10.deselect()
box10.pack(anchor = W, padx = (20, 20))

SP22 = StringVar()
box11 = Checkbutton(root, text = "Switchport 22", variable = SP22, onvalue = "Gi4/0/22", offvalue = None)
box11.deselect()
box11.pack(anchor = W, padx = (20, 20))

SP24 = StringVar()
box12 = Checkbutton(root, text = "Switchport 24", variable = SP24, onvalue = "Gi4/0/24", offvalue = None)
box12.deselect()
box12.pack(anchor = W, padx = (20, 20))

SP26 = StringVar()
box13 = Checkbutton(root, text = "Switchport 26", variable = SP26, onvalue = "Gi4/0/26", offvalue = None)
box13.deselect()
box13.pack(anchor = W, padx = (20, 20))

SP28 = StringVar()
box14 = Checkbutton(root, text = "Switchport 28", variable = SP28, onvalue = "Gi4/0/28", offvalue = None)
box14.deselect()
box14.pack(anchor = W, padx = (20, 20))

SP30 = StringVar()
box15 = Checkbutton(root, text = "Switchport 30", variable = SP30, onvalue = "Gi4/0/30", offvalue = None)
box15.deselect()
box15.pack(anchor = W, padx = (20, 20))

SP32 = StringVar()
box16 = Checkbutton(root, text = "Switchport 32", variable = SP32, onvalue = "Gi4/0/32", offvalue = None)
box16.deselect()
box16.pack(anchor = W, padx = (20, 20))

SP34 = StringVar()
box17 = Checkbutton(root, text = "Switchport 34", variable = SP34, onvalue = "Gi4/0/34", offvalue = None)
box17.deselect()
box17.pack(anchor = W, padx = (20, 20))

SP36 = StringVar()
box18 = Checkbutton(root, text = "Switchport 36", variable = SP36, onvalue = "Gi4/0/36", offvalue = None)
box18.deselect()
box18.pack(anchor = W, padx = (20, 20))

SP38 = StringVar()
box19 = Checkbutton(root, text = "Switchport 38", variable = SP38, onvalue = "Gi4/0/38", offvalue = None)
box19.deselect()
box19.pack(anchor = W, padx = (20, 20))

SP40 = StringVar()
box20 = Checkbutton(root, text = "Switchport 40", variable = SP40, onvalue = "Gi4/0/40", offvalue = None)
box20.deselect()
box20.pack(anchor = W, padx = (20, 20))

#VLAN ID selection dropdown.
vlanID_lbl = Label(root, text = "Select VLAN ID:", font=('Helvetica', 10)).pack(anchor = W, padx = (20, 20), pady = (10, 0))
global vlanID
vlanID = StringVar()
vlanID.set("No Selection")
dropDown = OptionMenu(root, vlanID, "No Selection", "1", "10", "20", "30", "50", "51", "52", "53", "54", "55", "60", "70", "90", "100", "120", "220", "410", "420", "550", "600", "710", "730", "740")
dropDown.pack(anchor = W, padx = (20, 10), pady = 10)

#Button to call the submission() function and submit changes.
submit = Button(root, text = "Submit Changes", command = submission).pack(anchor = W, padx = (20, 10), pady = 5)

reloadVLAN = Button(rightFrame, text = "Press to Load Current VLAN Config", command = getVLANs).pack(anchor = SE, padx = 20, pady = (20, 10))


displayVLANs = Text(rightFrame, fg = "white", bg = "black")
displayVLANs.pack(fill = BOTH, expand = True, padx = (0, 20), pady = (0, 10))


#Main event loop.
root.mainloop()