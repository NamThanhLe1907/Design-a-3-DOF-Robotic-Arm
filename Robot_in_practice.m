%% Forward Kinematic
clear all
clc
%syms L0 L1 L2 L3 theta1 theta2 theta3 d1 d2 d4 r11 r12 r13 x r21 r22 r23 y r31 r32 r33 z
%FK = [r11 r12 r13 x; r21 r22 r23 y; r31 r32 r33 z; 0 0 0 1];
%% Degree
d1 = 95;L1 = 113.72; L2 = 162.61;  L3 = 122.29; theta1 = 78.588253480073050; theta2 = -59.293643928415165; theta3 = 91.297809945653820; d2 = 175; d4 =50; 
T01 = CT_JcraigDEG(0,0,d1,theta1);
%T12 = CT_JcraigDEG(90,L1,d2,theta2);
T12 = CT_JcraigDEG(90,L1,d2,theta2);
T23 = CT_JcraigDEG(0,L2,0,theta3);
T34 = CT_JcraigDEG(0,L3,d4,0);
T04 = T01*T12*T23*T34;
P = T04(:,4);
%%
%% Radians, equation only
%d1 = 95;L1 = 113.72; L2 = 162.61;  L3 = 122.29; theta1 = 30; theta2 = 45; theta3 = 10; d2 = 175; d4 =50; 
T01 = CT_JcraigRAD(0,0,d1,theta1);
T12 = CT_JcraigRAD(sym(pi/2),L1,d2,theta2);
%T12 = CT_JcraigDEG(90,L1,d2,theta2);
T23 = CT_JcraigRAD(0,L2,0,theta3);
T34 = CT_JcraigRAD(0,L3,d4,0);
T04 = T01*T12*T23*T34;
P = T04(:,4);
%% Inverse Kinematics JC
Px = T04(1,4);Py= T04(2,4); Pz =T04(3,4);

%%
alpha =0;
alpha1 = asind(-Py/sqrt((Px^2 +Py^2)));
alpha2 = acosd(Px/sqrt((Px^2+Py^2)));
if (Px >0) 
   alpha = alpha1; 
else
   alpha = alpha2;
end
theta11 = asind((d2+d4)/(sqrt(Px^2+Py^2))) - alpha;
K2 = Pz-d1 ;
K1 = Px*cosd(theta11) + Py*sind(theta11) - L1;
c3 = ((K1^2 + K2^2-L3^2-L2^2)/(2*L2*L3));
s3 = sqrt(1-(c3^2));
theta333 = acosd(c3);
%theta33 = atan2d(s3,c3);
theta34 = asind(s3);
s2 = ((K2*(L2+L3*cosd(theta333)))-(K1*L3*sind(theta333)))/((L3*sind(theta333))^2+(L2+L3*cosd(theta333))^2);
c22 = (K1+(L3*s2*sind(theta333)))/(L2+(L3*cosd(theta333)));  

theta22 = atan2d(s2,c2);

