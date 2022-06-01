import math 

L = float(input("L: "))
E = float(input("E: "))
Bj = float(input("Bj: "))
Fu = float(input("Fu: "))
Fy = float(input("Fy: "))
h = float(input("h: "))
qu = float(input("qu: "))
pu = float(input("pu: "))
Ra = float(input("Ra=Rb: "))
Øb = float(input("Øb: "))
Øv = float(input("Øv: "))
Øc = float(input("Øc: "))
Cv = float(input("Cv: "))

Vmax = Ra
Mmax = (1/4*pu*L)+(1/8*qu*L**2)
Zxperlu = Mmax / (Fy*Øb)

H = float(input("H: "))
B = float(input("B: "))
Tf = float(input("Tf: "))
Tw = float(input("Tw: "))
A = float(input("A: "))
Iy = float(input("Iy: "))
Ry = float(input("Ry: "))
Sx = float(input("Lebar: "))

print("CEK RASIO KAPASITAS LENTUR")
Sx = (B*Tf)*(H*Tf)+Tw*(1/2*H-Tf)*(1/2*H-Tf)
Mu = Mmax
Mn = Zx*Fy
Rasio1 = Mmax/(Øb*Mn)
if Rasio1 < 1:
    OK
elif Rasio1 > 1:
    TidakOK

print("CEK RASIO KAPASITAS GESER") 
Vu = Vmax
Vn = 0,6*Fy*Cv*(H-2*Tf)*Tw
Rasio2 = Vu/(Øv*Vn)
if Rasio2 < 1:
    OK
elif Rasio2 > 1:
    TidakOK

print("Cek Stabilitas penampang") 
print("flenge") 
λpf = 0,38*sqrt(E/Fy)
λf = Bf/(2*Tf)
if λf < λpf:
    Kompak
elif λf > λpf:
    TidakKompak
print("web") 
λpw = 3,78*sqrt(E/Fy)
λw = (H-2*Tf)/Tw
if λw < λpw:
    Kompak
elif λw > λpw:
    TidakKompak

print("Cek Stabilitas Tekuk/Torsi")
ry = 784
c = 1
Lb = 5000
Lp = 1.76*ry*sqrt(E/Fy)
Ho = H-Tf
Cw = (Iy*Ho**2)/4
rts^2 == (sqrt(Iy*Cw))/Zx
rts = sqrt(sqrt^2)
j = (2*B*Tf**3+Ho*tw**3)/3
A = (j*c)/(Zx*Ho)
B = sqrt((A)**2+6.79*((0.7*Fy)/E)**2)
C = sqrt(A+B)
Lr = 1.95*rts*(E/(0.75*Fy))*C
ØMn = 0.9*Mn
ØMn > Mmax (ok) 
if ØMn > Mmax:
    OK
elif ØMn < Mmax:
    TidakOK
