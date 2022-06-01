
# CEK RASIO KAPASITAS LENTUR
Sx = (B*Tf)*(H*Tf)+Tw*(1/2*H-Tf)*(1/2*H-Tf)
Mu = Mmax
Mn = Zx*Fy
Rasio = Mmax/(Øb*Mn)
Rasio < 1 (Ok)

# CEK RASIO KAPASITAS GESER 
Vu = Vmax
Vn = 0,6*Fy*Cv*(H-2*Tf)*Tw
Rasio = Vu/(Øv*Vn)
Rasio < 1 (ok)

# Cek Rasio Kapasitas Geser 
# Flenge :
λp = 0,38*sqrt(E/Fy)
λ = Bf/(2*Tf)
λ < λp  (kompak)
# Web:
λp = 3,78*sqrt(E/Fy)
λ = (H-2*Tf)/Tw
λ < λp  (kompak)

# Cek Stabilitas Tekuk/Torsi
ry = 784
c = 1
Lb = 5000
Lp = 1,76*ry*sqrt(E/Fy)
Ho = H-Tf
Cw = (Iy*Ho**2)/4
# rts^2 = (sqrt(Iy*Cw))/Zx
rts = sqrt(sqrt^2)
j = (2*B*Tf**3+Ho*tw**3)/3
A = (j*c)/(Zx*Ho)
B = sqrt((A)**2+6,79*((0,7*Fy)/E)**2)
C = sqrt(A+B)
Lr = 1,95*rts*(E/(0,75*Fy))*C
ØMn = 0,9*Mn
ØMn > Mmax (ok) 
