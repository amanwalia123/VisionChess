omega = -pi:pi/1000:pi;
z = 1./sqrt(1.9025-1.9*cos(omega));
plot(omega,z);
mean(z)