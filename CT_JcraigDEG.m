function [t] = CT_JcraigDEG(alpha, a, d, theta)
t = [cosd(theta)             -sind(theta)              0              a;
     cosd(alpha)*sind(theta) cosd(alpha)*cosd(theta) -sind(alpha) -sind(alpha)*d;
     sind(alpha)*sind(theta) sind(alpha)*cosd(theta) cosd(alpha)  cosd(alpha)*d
                0               0                   0               1];
end