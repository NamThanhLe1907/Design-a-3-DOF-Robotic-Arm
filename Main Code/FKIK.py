from math import *
def Forward_Kinematic(theta1,theta2,theta3):
    theta1 = (theta1/180)*3.14
    theta2 = (theta2/180)*3.14
    theta3 = (theta3/180)*3.14
    L1 = 113.72
    L2 = 162.61
    L3 = 122.29
    d1 = 95
    d2 = 175
    d4 = 50
    Px = L1*cos(theta1) + d2*sin(theta1) + d4*sin(theta1) - L3*(cos(theta1)*sin(theta2)*sin(theta3) - cos(theta1)*cos(theta2)*cos(theta3)) + L2*cos(theta1)*cos(theta2)
    Py = L1*sin(theta1) - L3*(sin(theta1)*sin(theta2)*sin(theta3) - cos(theta2)*cos(theta3)*sin(theta1)) - d2*cos(theta1) - d4*cos(theta1) + L2*cos(theta2)*sin(theta1)
    Pz = d1 + L3*sin(theta2 + theta3) + L2*sin(theta2)
    Px = round(Px,3)
    Py = round(Py,3)
    Pz = round(Pz,3)
    return Px,Py,Pz
def Inverse_Kinematic(Px,Py,Pz):
    L1 = 113.72
    L2 = 162.61
    L3 = 122.29
    d1 = 95
    d2 = 175
    d4 = 50
    alpha =0
    alpha1 = asin(-Py/sqrt((Px**2 +Py**2)))
    alpha2 = acos(Px/sqrt((Px**2+Py**2)))
    if float(Px)>0 and float(Py) > 0 :
        alpha = alpha1
    else:
        alpha = alpha2
    theta1 = asin((d2+d4)/(sqrt(Px**2+Py**2))) - alpha
    K2 = Pz-d1
    K1 = Px*cos(theta1) + Py*sin(theta1) - L1
    c3 = ((K1**2 + K2**2-L3**2-L2**2)/(2*L2*L3))
    s3 = sqrt(1-(c3**2))
    theta3 = -acos(c3)
    theta33 = atan2(s3,c3)
    s2 = ((K2*(L2+L3*cos(theta3)))-(K1*L3*sin(theta3)))/((L3*sin(theta3))**2+(L2+L3*cos(theta3))**2)
    c2 =((K1*(L2+L3*cos(theta3)))+(K2*L3*sin(theta3)))/((L3*sin(theta3))**2+(L2+L3*cos(theta3))**2)
    #c2 = (K2+(L3*s2*sin(theta33)))/(L2+(L3*cos(theta33)));  
    theta2 = atan2(s2,c2)
    theta1 = (theta1/3.14)*180
    theta2 = (theta2/3.14)*180
    theta3 = (theta3/3.14)*180
    return theta1,theta2,theta3

