clear all;
close all;
clc; 
x(1) = 0; y(1) = 0; phi (1) = 0;
dt = 0.1; t(1) = 0;
for i = 2 : 1149
    t(i) = t(i-1)+dt;
    vr(i) = 0.2; or(i) = 0;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i));
    y(i) = y(i-1) + vr(i)*sin(phi(i));
end
for i = 1145:1254
    t(i) = t(i-1)+dt;
    or(i) = -pi/22; vr(i) = 1.4 * pi/22;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i));
    y(i) = y(i-1) + vr(i)*sin(phi(i));
end
for i = 1255:1839
    t(i) = t(i-1)+dt;
    vr(i) = 0.2; or(i) = 0;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i));
    y(i) = y(i-1) + vr(i)*sin(phi(i));
end
for i = 1840:1949
    t(i) = t(i-1)+dt;
    or(i) = pi/22; vr(i) = 1.4 * pi/22;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i));
    y(i) = y(i-1) + vr(i)*sin(phi(i));
end
for i = 1950:2629
    t(i) = t(i-1)+dt;
    vr(i) = 0.2; or(i) = 0;
    phi(i) = phi(i-1) + or(i)*dt;
    x(i) = x(i-1) + vr(i)*cos(phi(i));
    y(i) = y(i-1) + vr(i)*sin(phi(i));
end
figure 
plot(x,y);
axis equal;
figure
subplot(2,1,1)
plot(t,vr);
subplot(2,1,2)
plot(t,or)