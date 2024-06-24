from ctypes import sizeof #gọi các hàm từ các thư viện khác không thuộc về python
from tkinter import * # thư viện GUI tiêu chuẩn cho Python
import tkinter
from tkinter import font
from typing import Mapping, Sized #thư viện mảng kich thuoc
import numpy as np #thư viện toán học

from serial.serialutil import Timeout #thu vien serial, timeout: limit the max time for calling a function
import FKIK #thu vien dong hoc
import serial # cong serial
import time # thoi gian

import threading

def action(): #ham chuyen doi 2 giao dien

    top.destroy() # tat man hinh dau
    GiaoDien.deiconify() #hien thi man hinh giao dien

GiaoDien = Tk() #tao man hinh giao dien
top=Toplevel()  # màn hình hiện thị đầu tiên
top.title("GIAO DIỆN ROBOT 3 DOF") #tên
top.geometry('1070x605') #kích  thước 
MC = PhotoImage(file="D:\\Study\\Robotic\\Robot 2024\\Robotic in Pratice S2-2023\\codene\\hehe.png")  #hinh C:\\Users\\84382\\Pictures\\
Label(top,image=MC).place(x=0,y=0)  # vi tri
#MC=PhotoImage(file="VSP.png") # hình
Label(top,image=MC).grid() # vị trí
Button(top,text="GO CONTROL INTERFACE",font='Times 15 bold', bg='#6666ff',fg='white',command=lambda:action()).place(x=400,y=500) # nút nhấn fg mau vien bg mau nen

GiaoDien.withdraw() # de chi hien thi 1 giao dien TOP ban dau
ser = serial.Serial('COM6',9600)

x_axis = 15
y_axis = 30
y_lable_IK = 250
value1 = 0
value2 = 0 
value3 = 0
x=0
L1 = 113.72
L2 = 162.61
L3 = 122.29

background_color = '#FFEBCD' # mã TLP RGB xem ở https://htlit.maytinhhtl.com/lam-web/bang-ma-mau-css-html-code-thet-ke-design.html

GiaoDien.geometry('570x600')
GiaoDien.title("CONTROL INTERFACE")
GiaoDien.configure(bg=background_color)

#------------------------------- VIẾT HÀM CON ------------------------------------
def slider_theta1_value(x):
    value1 = slider_theta1.get()
    txb_slider_theta1.delete(0,END) # Xóa dữ liệu trước đó
    txb_slider_theta1.insert(0,value1) # hiển thị dữ liệu mới
    return value1

def slider_theta2_value(x):
    txb_slider_theta2.delete(0,END)
    value2 = slider_theta2.get()
    txb_slider_theta2.insert(0,value2)
    return value2

def slider_theta3_value(x):
    txb_slider_theta3.delete(0,END)
    value3 = slider_theta3.get()
    txb_slider_theta3.insert(0,value3)  
    return value3

def FK(x):
    txb_Px_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Py_FK.delete(0,END) # Xóa dữ liệu trước đó
    txb_Pz_FK.delete(0,END) # Xóa dữ liệu trước đó
    value1 = slider_theta1_value(x)
    value2 = slider_theta2_value(x)
    value3 = slider_theta3_value(x)
    Px = FKIK.Forward_Kinematic(value1,value2,value3)[0]
    Py = FKIK.Forward_Kinematic(value1,value2,value3)[1]
    Pz = FKIK.Forward_Kinematic(value1,value2,value3)[2]
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới vao PX PY PZ
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới
    #mang = str(value1)+'A'+str(value2)+'B'+str(value3)+'C'
    #ser.write(mang.encode())
    #time.sleep(0.01)

def IK():
    txb_theta1_IK.delete(0, END)
    txb_theta2_IK.delete(0, END)
    txb_theta3_IK.delete(0, END)
    Px = float(txb_Px_IK.get())
    Py = float(txb_Py_IK.get())
    Pz = float(txb_Pz_IK.get())
    theta1 = FKIK.Inverse_Kinematic(Px, Py, Pz)[0]
    theta2 = FKIK.Inverse_Kinematic(Px, Py, Pz)[1]
    theta3 = FKIK.Inverse_Kinematic(Px, Py, Pz)[2]
    txb_theta1_IK.insert(0, "{:.1f}".format(theta1))
    txb_theta2_IK.insert(0, "{:.1f}".format(theta2))
    txb_theta3_IK.insert(0, "{:.1f}".format(theta3))
    command = "IKM1({:.1f})M2({:.1f})M3({:.1f})\n".format(theta1, theta2, theta3)
    print(command)
    ser.write(command.encode())
    time.sleep(0.01)  #để thêm độ trễ trong quá trình thực thi chương trình. 
    #txb_Px_IK.delete(0,END)
    #txb_Py_IK.delete(0,END)
    #txb_Pz_IK.delete(0,END)
    #txb_Theta.delete(0,END)

def Reset_Slider():
    txb_slider_theta1.delete(0,END)
    txb_slider_theta2.delete(0,END)
    txb_slider_theta3.delete(0,END) 
    txb_slider_theta1.insert(0,value1)
    txb_slider_theta2.insert(0,value2)
    txb_slider_theta3.insert(0,value3)    
    slider_theta1.set('0') #đặt lại vị trí thanh slider tương ứng với giá trị lấy từ textbox
    slider_theta2.set('0')
    slider_theta3.set('0')

def Reset_lable_Slider():
    Reset_Slider()
    Px = FKIK.Forward_Kinematic(0,0,0)[0]
    Py = FKIK.Forward_Kinematic(0,0,0)[1]
    Pz = FKIK.Forward_Kinematic(0,0,0)[2] 

    txb_Px_FK.delete(0,END) # hiển thị dữ liệu mới
    txb_Py_FK.delete(0,END) # hiển thị dữ liệu mới
    txb_Pz_FK.delete(0,END) # hiển thị dữ liệu mới 
    txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
    txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
    txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới    

def ReSet_btn():
    new_thread = threading.Thread(target=Reset_lable_Slider) # Thread là các hàm hay thủ tục chạy độc lập đối với chương trình chính
    new_thread.start()
    mang = f'RS'
    print(mang,type(mang))
    ser.write(mang.encode())
    time.sleep(0.01)


def send_command(value1, value2, value3):
    txb_Px_FK.delete(0, END)  # Xóa dữ liệu trước đó
    txb_Py_FK.delete(0, END)  # Xóa dữ liệu trước đó
    txb_Pz_FK.delete(0, END)  # Xóa dữ liệu trước đó
    Px, Py, Pz = FKIK.Forward_Kinematic(value1, value2, value3)
    txb_Px_FK.insert(0, "{:.1f}".format(Px))  # Hiển thị dữ liệu mới
    txb_Py_FK.insert(0, "{:.1f}".format(Py))  # Hiển thị dữ liệu mới
    txb_Pz_FK.insert(0, "{:.1f}".format(Pz))  # Hiển thị dữ liệu mới
    command = "FKM1({:.1f})M2({:.1f})M3({:.1f})\n".format(value1, value2, value3)
    print(command, type(command))
    ser.write(command.encode())
    time.sleep(0.01)

def theta1_set_btn():
    slider_theta1.set(txb_slider_theta1.get())
    value1 = float(slider_theta1_value(x))
    value2 = float(slider_theta2_value(x))
    value3 = float(slider_theta3_value(x))
    send_command(value1, value2, value3)

def theta2_set_btn():
    slider_theta2.set(txb_slider_theta2.get())
    value1 = float(slider_theta1_value(x))
    value2 = float(slider_theta2_value(x))
    value3 = float(slider_theta3_value(x))
    send_command(value1, value2, value3)

def theta3_set_btn():
    slider_theta3.set(txb_slider_theta3.get())
    value1 = float(slider_theta1_value(x))
    value2 = float(slider_theta2_value(x))
    value3 = float(slider_theta3_value(x))
    send_command(value1, value2, value3)

def Start():
    command = 'S'
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)

def Stop():
    command = 'E'
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def Dropp():
    command = 'T'
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)    
def Suck():
    command = 'H'
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)    
def one():
    command = "IKM1(24.5)M2(-39.0)M3(-17.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def two():
    command = "IKM1(18.5)M2(-40.0)M3(-19.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def three():
    command = "IKM1(13.0)M2(-40.5)M3(-19.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)     
def four():
    command = "IKM1(6.5)M2(-40.5)M3(-21.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def five():
    command = "IKM1(0.0)M2(-38.5)M3(-28.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def six():
    command = "IKM1(-6.5)M2(-35.5)M3(-31.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def seven():
    command = "IKM1(-12.5)M2(-35)M3(-29)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def eight():
    command = "IKM1(-18.0)M2(-37)M3(-21)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def nine():
    command = "IKM1(26.0)M2(-35.0)M3(-35.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ten():
    command = "IKM1(20.3)M2(-32.9)M3(-48.4)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tone():
    command = "IKM1(14.0)M2(-32.5)M3(-54.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttwo():
    command = "IKM1(6.5)M2(-34.0)M3(-44.5)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tthree():
    command = "IKM1(0)M2(-31.5)M3(-54.5)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tfour():
    command = "IKM1(-6.5)M2(-32.0)M3(-51.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tfive():
    command = "IKM1(-13.0)M2(-31.7)M3(-45.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tsix():
    command = "IKM1(-20.5)M2(-35.0)M3(-35)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tseven():
    command = "IKM1(29.0)M2(-31.0)M3(-58.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def teight():
    command = "IKM1(22.0)M2(-29.5)M3(-65.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def tnine():
    command = "IKM1(14.0)M2(-29.5)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)     
def twenty():
    command = "IKM1(7.0)M2(-28.0)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def ttone():
    command = "IKM1(0.0)M2(-28.0)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tttwo():
    command = "IKM1(-7.5)M2(-28.0)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttthree():
    command = "IKM1(-16.0)M2(-29.0)M3(-65.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttfour():
    command = "IKM1(-22.0)M2(-28.0)M3(-60.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttfive():
    command = "IKM1(32.0)M2(-29.0)M3(-65.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttsix():
    command = "IKM1(25.0)M2(-29.0)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttseven():
    command = "IKM1(18.0)M2(-30.0)M3(-75.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def tteight():
    command = "IKM1(9.0)M2(-32.0)M3(-75.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def ttnine():
    command = "IKM1(0.0)M2(-32.5)M3(-78.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def thirty():
    command = "IKM1(-9.5)M2(-30.0)M3(-79.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def thone():
    command = "IKM1(-17.0)M2(-30.0)M3(-75.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def thtwo():
    command = "IKM1(-25.0)M2(-30.0)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)    
def ththree():
    command = "IKM1(37.0)M2(-32.0)M3(-75.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def thfour():
    command = "IKM1(29.0)M2(-34.5)M3(-80.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def thfive():
    command = "IKM1(25.0)M2(-30.0)M3(-70.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def theight():
    command = "IKM1(-9.5)M2(-33.0)M3(-81.4)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def thnine():
    command = "IKM1(-19.5)M2(-33.0)M3(-81.4)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def fourty():
    command = "IKM1(-29.5)M2(-32.0)M3(-76.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01) 
def fone():
    command = "IKM1(42.8)M2(-36.0)M3(-83.7)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def feight():
    command = "IKM1(-35.0)M2(-33.0)M3(-85.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)
def Drop():
    command = "IKM1(65)M2(-25.0)M3(-75.0)\n"
    print(command,type(command))
    ser.write(command.encode())
    time.sleep(0.01)             
                                                                                           
#--------------------------------------------------------------------------

lbl_tieude = Label(GiaoDien,text="   CONTROL INTERFACE",font=("Arial",17,font.BOLD),bg=background_color)
lbl_FK = Label(GiaoDien,text="FORWARD KINEMATIC",fg="blue",font=("Arial",14,font.BOLD),bg=background_color)
lbl_IK = Label(GiaoDien,text="INVERSE KINEMATIC",fg="blue",font=("Arial",14,font.BOLD),bg=background_color)
lbl_theta1_FK = Label(GiaoDien,text="Theta1",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta2_FK = Label(GiaoDien,text="Theta2",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta3_FK = Label(GiaoDien,text="Theta3",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta1_IK = Label(GiaoDien,text="Theta1",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta2_IK = Label(GiaoDien,text="Theta2",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_theta3_IK = Label(GiaoDien,text="Theta3",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Px_IK = Label(GiaoDien,text="Px",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Py_IK = Label(GiaoDien,text="Py",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Pz_IK = Label(GiaoDien,text="Pz",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Px_FK = Label(GiaoDien,text="Px",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Py_FK = Label(GiaoDien,text="Py",fg="black",font=("Arial",12,font.BOLD),bg=background_color)
lbl_Pz_FK = Label(GiaoDien,text="Pz",fg="black",font=("Arial",12,font.BOLD),bg=background_color)


txb_slider_theta1 = Entry(GiaoDien,width=6,font=("Arial",12,font.BOLD)) #tao o hien thi goc ben canh slider
txb_slider_theta1.insert(0,value1)

txb_slider_theta2 = Entry(GiaoDien,width=6,font=("Arial",12,font.BOLD))
txb_slider_theta2.insert(0,value2)

txb_slider_theta3 = Entry(GiaoDien,width=6,font=("Arial",12,font.BOLD))
txb_slider_theta3.insert(0,value3)

txb_Px_IK = Entry(GiaoDien,width=10,font=("Arial",12,font.BOLD)) # tao o hien thi Px Invert
txb_Py_IK = Entry(GiaoDien,width=10,font=("Arial",12,font.BOLD))
txb_Pz_IK = Entry(GiaoDien,width=10,font=("Arial",12,font.BOLD))
txb_Px_FK = Entry(GiaoDien,width=7,font=("Arial",12,font.BOLD))
txb_Py_FK = Entry(GiaoDien,width=7,font=("Arial",12,font.BOLD))
txb_Pz_FK = Entry(GiaoDien,width=7,font=("Arial",12,font.BOLD))
txb_theta1_IK = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD)) #tao o hien thi goc invert
txb_theta2_IK = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD))
txb_theta3_IK = Entry(GiaoDien,width=9,font=("Arial",12,font.BOLD))

slider_theta1 = Scale(GiaoDien,from_=-150, to_= 150,orient=HORIZONTAL,width=15,resolution=0.5,length=350,command=FK) # gioi han thanh slider
slider_theta1.set(value1)
slider_theta2 = Scale(GiaoDien,from_=-90, to_= 90,orient=HORIZONTAL,width=15,resolution=0.5,length=350,command=FK)
slider_theta2.set(value2)
slider_theta3 = Scale(GiaoDien,from_=-150, to_= 150,orient=HORIZONTAL,width=15,resolution=0.5,length=350,command=FK)
slider_theta3.set(value3)

btn_Start = Button(GiaoDien,text="Start",font=("Arial",12,font.BOLD),width=10,height=2,bg='#FF1493',command=Start)
btn_Stop = Button(GiaoDien,text="Stop",font=("Arial",12,font.BOLD),width=10,height=2,bg='#FF0000',command=Stop)
btn_Solve = Button(GiaoDien,text="Solve",font=("Arial",12,font.BOLD),width=10,height=2,bg='#98FB98',command=IK)
btn_ReSet = Button(GiaoDien,text="Reset",font=("Arial",12,font.BOLD),width=10,height=2,bg='#98FB98',command=ReSet_btn)
btn_Set_Theta1 = Button(GiaoDien,text="Set Theta1",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=theta1_set_btn)
btn_Set_Theta2 = Button(GiaoDien,text="Set Theta2",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=theta2_set_btn)
btn_Set_Theta3 = Button(GiaoDien,text="Set Theta3",font=("Arial",10,font.BOLD),width=8,height=2,bg='#98FB98',command=theta3_set_btn)
btn_one = Button(GiaoDien,text="1",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=one)
btn_two = Button(GiaoDien,text="2",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=two)
btn_three = Button(GiaoDien,text="3",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=three)
btn_four = Button(GiaoDien,text="4",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=four)
btn_five = Button(GiaoDien,text="5",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=five)
btn_six = Button(GiaoDien,text="6",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=six)
btn_seven = Button(GiaoDien,text="7",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=seven)
btn_eight = Button(GiaoDien,text="8",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=eight)
btn_nine = Button(GiaoDien,text="9",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=nine)
btn_ten = Button(GiaoDien,text="10",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=ten)
btn_tone = Button(GiaoDien,text="11",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=tone)
btn_ttwo = Button(GiaoDien,text="12",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=ttwo)
btn_tthree = Button(GiaoDien,text="13",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=tthree)
btn_tfour = Button(GiaoDien,text="14",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=tfour)
btn_tfive = Button(GiaoDien,text="15",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=tfive)
btn_tsix = Button(GiaoDien,text="16",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=tsix)
btn_tseven = Button(GiaoDien,text="17",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=tseven)
btn_teight = Button(GiaoDien,text="18",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=teight)
btn_tnine = Button(GiaoDien,text="19",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=tnine)
btn_twenty = Button(GiaoDien,text="20",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=twenty)
btn_ttone = Button(GiaoDien,text="21",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=ttone)
btn_tttwo = Button(GiaoDien,text="22",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=tttwo)
btn_ttthree = Button(GiaoDien,text="23",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=ttthree)
btn_ttfour = Button(GiaoDien,text="24",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=ttfour)
btn_ttfive = Button(GiaoDien,text="25",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=ttfive)
btn_ttsix = Button(GiaoDien,text="26",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=ttsix)
btn_ttseven = Button(GiaoDien,text="27",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=ttseven)
btn_tteight = Button(GiaoDien,text="28",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=tteight)
btn_ttnine = Button(GiaoDien,text="29",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=ttnine)
btn_thirty = Button(GiaoDien,text="30",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=thirty)
btn_thone = Button(GiaoDien,text="31",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=thone)
btn_thtwo = Button(GiaoDien,text="32",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=thtwo)
btn_ththree = Button(GiaoDien,text="33",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=ththree)
btn_thfour = Button(GiaoDien,text="34",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=thfour)
btn_thfive = Button(GiaoDien,text="35",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=thfive)
btn_theight = Button(GiaoDien,text="38",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=theight)
btn_thnine = Button(GiaoDien,text="39",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=thnine)
btn_fourty = Button(GiaoDien,text="40",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=fourty)
btn_fone = Button(GiaoDien,text="41",font=("Arial",10,font.BOLD),width=8,height=2,bg='#c0c0c0',command=fone)
btn_feight = Button(GiaoDien,text="48",font=("Arial",10,font.BOLD),width=8,height=2,bg='#ffffff',command=feight)
btn_Drop = Button(GiaoDien,text="Drop",font=("Arial",12,font.BOLD),width=10,height=2,bg='#FF1493',command=Drop)
btn_Suck = Button(GiaoDien,text="Suck",font=("Arial",12,font.BOLD),width=10,height=2,bg='#FF1493',command=Suck)
btn_Dropp = Button(GiaoDien,text="Dropp",font=("Arial",12,font.BOLD),width=10,height=2,bg='#FF1493',command=Dropp)

lbl_tieude.place(x=150,y=0)
lbl_FK.place(x=x_axis,y=y_axis)
lbl_IK.place(x=x_axis,y=y_axis+y_lable_IK)
lbl_theta1_FK.place(x=x_axis,y=y_axis+40)
lbl_theta2_FK.place(x=15,y=y_axis+85)
lbl_theta3_FK.place(x=15,y=y_axis+130)
lbl_theta1_IK.place(x=200,y=y_axis+y_lable_IK+53)
lbl_theta2_IK.place(x=200,y=y_axis+y_lable_IK+103)
lbl_theta3_IK.place(x=200,y=y_axis+y_lable_IK+153)
lbl_Px_FK.place(x=x_axis+40,y=y_axis+170)
lbl_Py_FK.place(x=x_axis+140,y=y_axis+170)
lbl_Pz_FK.place(x=x_axis+240,y=y_axis+170)
lbl_Px_IK.place(x=x_axis+20,y=y_axis+y_lable_IK+50)
lbl_Py_IK.place(x=x_axis+20,y=y_axis+y_lable_IK+100)
lbl_Pz_IK.place(x=x_axis+20,y=y_axis+y_lable_IK+150)

slider_theta1.place(x=x_axis+60,y=y_axis+30)
slider_theta2.place(x=x_axis+60,y=y_axis+75)
slider_theta3.place(x=x_axis+60,y=y_axis+120)

txb_slider_theta1.place(x=x_axis+420,y=y_axis+40)
txb_slider_theta2.place(x=x_axis+420,y=y_axis+80)
txb_slider_theta3.place(x=x_axis+420,y=y_axis+130)
txb_Px_FK.place(x=x_axis+20,y=y_axis+203)
txb_Py_FK.place(x=x_axis+120,y=y_axis+203)
txb_Pz_FK.place(x=x_axis+220,y=y_axis+203)
txb_Px_IK.place(x=x_axis+50,y=y_axis+y_lable_IK+53)
txb_Py_IK.place(x=x_axis+50,y=y_axis+y_lable_IK+103)
txb_Pz_IK.place(x=x_axis+50,y=y_axis+y_lable_IK+153)
txb_theta1_IK.place(x=270,y=y_axis+y_lable_IK+53)
txb_theta2_IK.place(x=270,y=y_axis+y_lable_IK+103)
txb_theta3_IK.place(x=270,y=y_axis+y_lable_IK+153)

btn_Start.place(x=x_axis+60,y=y_axis+y_lable_IK+250)
btn_Stop.place(x=x_axis+370,y=y_axis+y_lable_IK+250)
btn_Solve.place(x=x_axis+370,y=y_axis+y_lable_IK+85)
btn_ReSet.place(x=x_axis+370,y=y_axis+190)
btn_Set_Theta1.place(x=x_axis+480,y=y_axis+26)
btn_Set_Theta2.place(x=x_axis+480,y=y_axis+74)
btn_Set_Theta3.place(x=x_axis+480,y=y_axis+122)
btn_one.place(x = x_axis+630,y=y_axis+26)
btn_two.place(x = x_axis+700,y=y_axis+26)
btn_three.place(x = x_axis+770,y=y_axis+26)
btn_four.place(x = x_axis+840,y=y_axis+26)
btn_five.place(x = x_axis+910,y=y_axis+26)
btn_six.place(x = x_axis+980,y=y_axis+26)
btn_seven.place(x = x_axis+1050,y=y_axis+26)
btn_eight.place(x = x_axis+1120,y=y_axis+26)
btn_nine.place(x = x_axis+630,y=y_axis+74)
btn_ten.place(x = x_axis+700,y=y_axis+74)
btn_tone.place(x = x_axis+770,y=y_axis+74)
btn_ttwo.place(x = x_axis+840,y=y_axis+74)
btn_tthree.place(x = x_axis+910,y=y_axis+74)
btn_tfour.place(x = x_axis+980,y=y_axis+74)
btn_tfive.place(x = x_axis+1050,y=y_axis+74)
btn_tsix.place(x = x_axis+1120,y=y_axis+74)
btn_tseven.place(x = x_axis+630,y=y_axis+122)
btn_teight.place(x = x_axis+700,y=y_axis+122)
btn_tnine.place(x = x_axis+770,y=y_axis+122)
btn_twenty.place(x = x_axis+840,y=y_axis+122)
btn_ttone.place(x = x_axis+910,y=y_axis+122)
btn_tttwo.place(x = x_axis+980,y=y_axis+122)
btn_ttthree.place(x = x_axis+1050,y=y_axis+122)
btn_ttfour.place(x = x_axis+1120,y=y_axis+122)
btn_ttfive.place(x = x_axis+630,y=y_axis+170)
btn_ttsix.place(x = x_axis+700,y=y_axis+170)
btn_ttseven.place(x = x_axis+770,y=y_axis+170)
btn_tteight.place(x = x_axis+840,y=y_axis+170)
btn_ttnine.place(x = x_axis+910,y=y_axis+170)
btn_thirty.place(x = x_axis+980,y=y_axis+170)
btn_thone.place(x = x_axis+1050,y=y_axis+170)
btn_thtwo.place(x = x_axis+1120,y=y_axis+170)
btn_ththree.place(x = x_axis+630,y=y_axis+218)
btn_thfour.place(x = x_axis+700,y=y_axis+218)
btn_thfive.place(x = x_axis+770,y=y_axis+218)
btn_theight.place(x = x_axis+980,y=y_axis+218)
btn_thnine.place(x = x_axis+1050,y=y_axis+218)
btn_fourty.place(x = x_axis+1120,y=y_axis+218)
btn_fone.place(x = x_axis+630,y=y_axis+266)
btn_feight.place(x = x_axis+1120,y=y_axis+266)
btn_Drop.place(x = x_axis+630,y=y_axis+500)
btn_Suck.place(x = x_axis+980,y=y_axis+500)
btn_Dropp.place(x = x_axis+1120,y=y_axis+500)
#------------------------------------ TRẠNG THÁI BAN ĐẦU --------------------------------------
Px = FKIK.Forward_Kinematic(0,0,0)[0]
Py = FKIK.Forward_Kinematic(0,0,0)[1]
Pz = FKIK.Forward_Kinematic(0,0,0)[2]
txb_Px_FK.insert(0,Px) # hiển thị dữ liệu mới
txb_Py_FK.insert(0,Py) # hiển thị dữ liệu mới
txb_Pz_FK.insert(0,Pz) # hiển thị dữ liệu mới


GiaoDien.mainloop() # vong lap
