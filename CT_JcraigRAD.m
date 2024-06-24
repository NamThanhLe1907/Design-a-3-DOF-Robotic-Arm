function [t] = CT_JcraigRAD(alpha, a, d, theta)
t = [cos(theta)             -sin(theta)              0              a;
     cos(alpha)*sin(theta) cos(alpha)*cos(theta) -sin(alpha) -sin(alpha)*d;
     sin(alpha)*sin(theta) sin(alpha)*cos(theta) cos(alpha)  cos(alpha)*d
                0               0                   0               1];
 
end


