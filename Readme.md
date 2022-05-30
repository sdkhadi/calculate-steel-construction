# Calculate Steel Construction 

FU : 550, 500,410,370, 340
FY : 410, 290, 250 ,240 , 210

L = panjang
E = Modulus Elastisitas
FU = Kekuatan maksimum baja
FY = Kekuatan minimum baja
H = Ketinggian Gedung
qu = Beban Terbagi rata
pu = Beban terpusat
Ra = Radius
Øb = koefisien b
Øv = koefisien geser
cv = faktor distribusi vertikal


Rumus

Vmax = Ra
Mmax = (1/4 * pu * L ) + (1/8 * qu * L**)
Zxperlu = Mmax / (FY * Øb )

Zx = klasifikasi dari nilai Zxperlu

Cek Zx dari Table Profil Baja IWF

Zx = 26700
Sx = (B*Tf)(H-Tf)+Tw(1/28*H-Tf)*(1/2*H-Tf)

Mn =  Zx * FY
Ratio = Mmax / Øb * Mn


nilai klasifikasi didapatkan dari Ratio

## Output

project |Ratio|Zx | H | B | Ratio Lentur | Ratio Geser | Ratio Stabilitas tekuk | Stabilitas Penampang 

Baja Podomoro |  26700 | 100 |  75 |  OK | OK | OK | Tidak OK
 


