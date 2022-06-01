from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3
import json
import numpy as np
import math



tableIWF = open('iwf.json')
data = json.load(tableIWF)

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)


# Connecting to the Database where all information will be stored
connector = sqlite3.connect('ConstructionSteel.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS CONSTRUCTION_STEEL (STEEL_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, PROYEK_NAME TEXT, RATIO FLOAT, ZX FLOAT, H FLOAT, B FLOAT, RATIO_LENTUR TEXT, RATIO_GESER TEXT, RATIO_STABILITAS_TEKUK TEXT, STABILITAS_PENAMPANG_FLENGE TEXT,STABILITAS_PENAMPANG_WEB TEXT )"
)

# Creating the functions
def reset_fields():
    global proyek_name,panjang,modulus_elastisitas,kekuatan_min_baja,kekuatan_max_baja,ketinggian_gedung,beban_terbagi_rata,beban_terpusat,radius,koefisien_b,koefisien_geser,faktor_distribusi_vertikal

    for i in ['proyek_name', 'panjang', 'modulus_elastisitas', 'kekuatan_min_baja', 'kekuatan_max_baja','ketinggian_gedung','beban_terbagi_rata','beban_terpusat','radius','koefisien_b','koefisien_geser','faktor_distribusi_vertikal']:
        exec(f"{i}.set('')")

def reset_form():
    connector.execute('DELETE FROM CONSTRUCTION_STEEL')
    connector.commit()
    display_records()


def display_records():
    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM CONSTRUCTION_STEEL')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)

def add_record():
    global proyek_name,panjang,modulus_elastisitas,kekuatan_min_baja,kekuatan_max_baja,ketinggian_gedung,beban_terbagi_rata,beban_terpusat,radius,koefisien_b,koefisien_geser,faktor_distribusi_vertikal
    global Zx,H,B,ratio,ratio_lentur,ratio_geser,ratio_stabilitas_tekuk,stabilitas_penampang_flenge,stabilitas_penampang_web

    varProyekName = proyek_name.get()
    varPanjang = panjang.get()
    varModulusElastisitas = modulus_elastisitas.get()
    varKekuatanMinBaja = kekuatan_min_baja.get()
    varKekuatanMaxBaja = kekuatan_max_baja.get()
    varKetinggianGedung = ketinggian_gedung.get()
    varBebanTerbagiRata = beban_terbagi_rata.get()
    varBebanTerpusat = beban_terpusat.get()
    varRadius = radius.get()
    varKoefisienB = koefisien_b.get()
    varKoefisienGeser = koefisien_geser.get()
    varDistribusiVertikal = faktor_distribusi_vertikal.get()

    if not varProyekName or not varPanjang or not varModulusElastisitas or not varKekuatanMinBaja or not varKekuatanMaxBaja or not varKetinggianGedung or not varBebanTerbagiRata or not varBebanTerpusat or not varRadius or not varKoefisienB or not varKoefisienGeser or not varDistribusiVertikal:
        mb.showerror('Error!', "Semua Field Wajib Diisi")
    else:
        try:
            # connector.execute(
            # 'INSERT INTO CONSTRUCTION_STEEL(PROYEK_NAME,RATIO,ZX,H,B,RATIO_LENTUR,RATIO_GESER,RATIO_STABILITAS_TEKUK,STABILITAS_PENAMPANG_FLENGE,STABILITAS_PENAMPANG_WEB) VALUES (?,?,?,?,?,?,?,?,?,?)', (varProyekName,ratio, Zx, H, B, ratio_lentur, ratio_geser,ratio_stabilitas_tekuk,stabilitas_penampang_flenge,stabilitas_penampang_web)
            # )
            connector.execute(
            'INSERT INTO CONSTRUCTION_STEEL(PROYEK_NAME,RATIO,ZX,H,B,RATIO_LENTUR,RATIO_GESER,RATIO_STABILITAS_TEKUK,STABILITAS_PENAMPANG_FLENGE,STABILITAS_PENAMPANG_WEB) VALUES (?,?,?,?,?,?,?,?,?,?)', ("Proyek A",291, 2729, 20, 10, "OK", "OK","TIDAK OK","OK")
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {varProyekName} was successfully added")
            reset_fields()
            display_records()
        except:
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Silahkan klik pada salah satu list untuk menghapus')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)

        connector.execute('DELETE FROM CONSTRUCTION_STEEL WHERE STEEL_ID=%d' % selection[0])
        connector.commit()

        mb.showinfo('Done', 'Berhasil Menghapus Data')

        display_records()

def getMmax(pu,L,qu):
    Mmax =  (0.25*pu*L)+(0.125*qu*pow(L,2))
    return Mmax

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def getZx(FY,Øb):
    
    # Mmax = getMmax(beban_terpusat,panjang,beban_terbagi_rata)
    Mmax = getMmax(200,100,25)

    Zxperlu = Mmax / (FY * Øb )
    array = []
    for i in data['IWF']:
        res = i['Zx']
        array.append(res)
        
    getFixZx = find_nearest(array,Zxperlu)
    return getFixZx

def getAllDataIWFByZx():

    getFixZx = getZx(200,100)
    print(getFixZx)
    jsonObject = {}
    for i in data['IWF']:
        if getFixZx == i['Zx']:
            H = i['H']
            B = i['B']
            Tf = i['Tf']
            Tw = i['Tw']
            A = i['A']
            Iy = i['Iy']
            Ry = i['Zy']
            # set data to json
            print(H) 

# def analyzeRatioKapasitasLentur():
#     Sx = (B*Tf)*(H*Tf)+Tw*(1/2*H-Tf)*(1/2*H-Tf)
#     Mu = Mmax
#     Mn = Zx*Fy
#     Rasio1 = Mmax/(Øb*Mn)
#     if Rasio1 < 1:
#         return "OK"
#     elif Rasio1 > 1:
#         return "Tidak OK" 

def analyzeRatioKapasitasGeser():
    return "Hasil perhitungan Ratio Geser"

def analyzeRatioStabilitasPenampangFlenge():
    return "Hasil perhitungan Stabilitas Penampang Flenge"

def analyzeRatioStabilitasPenampangWeb():
    return "Hasil perhitungan Stabilitas Penampang Flenge"

def analyzeRatioStabilitasTekuk():
    return "Hasil perhitungan Stabilitas Penampang Flenge"



# Initializing the GUI window
main = Tk()
main.title('My Python Project')
main.geometry('1920x1280')
# main.resizable(False, True)

# Creating the background and foreground color variables
lf_bg = 'Gray35' # bg color for the left_frame
cf_bg = 'Gray35' # bg color for the center_frame
primaryBg = "Gray35"
white ="#ffffff"

# Creating the StringVar or IntVar variables
proyek_name = StringVar()
panjang = DoubleVar()
modulus_elastisitas = DoubleVar()
kekuatan_min_baja = DoubleVar()
kekuatan_max_baja = DoubleVar()
ketinggian_gedung = DoubleVar()
beban_terbagi_rata = DoubleVar()
beban_terpusat = DoubleVar()
radius =DoubleVar()
koefisien_b =DoubleVar()
koefisien_geser = DoubleVar()
faktor_distribusi_vertikal = DoubleVar()

Zx = DoubleVar()
ratio = DoubleVar()
H = DoubleVar()
B = DoubleVar()
ratio_lentur = StringVar()
ratio_geser = StringVar()
ratio_stabilitas_tekuk = StringVar()
stabilitas_penampang_flenge = StringVar()
stabilitas_penampang_web = StringVar()




# Placing the components in the main window
Label(main, text="Perhitungan Konstruksi Baja", font=headlabelfont, bg=primaryBg,fg=white).pack(side=TOP, fill=X)

left_frame = Frame(main, bg=primaryBg)
left_frame.place(x=0, y=25, relheight=1, relwidth=0.20)

center_frame = Frame(main, bg=primaryBg)

center_frame.place(relx=0.18, y=25, relheight=1, relwidth=0.25)

right_frame = Frame(main, bg=primaryBg)
right_frame.place(relx=0.35, y=25, relheight=1, relwidth=0.75)

# Placing components in the left frame
Label(left_frame, text="Nama Proyek", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.01)
Entry(left_frame, width=25, textvariable=proyek_name, font=entryfont).place(x=20, rely=0.05)

Label(left_frame, text="Panjang(L)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.1)
Entry(left_frame, width=25, textvariable=panjang, font=entryfont).place(x=20, rely=0.15)

Label(left_frame, text="Modulus Elastisitas(E)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.20)
Entry(left_frame, width=25, textvariable=modulus_elastisitas, font=entryfont).place(x=20, rely=0.25)

Label(left_frame, text="Kekuatan Minimum baja(FY)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.30)
OptionMenu(left_frame, kekuatan_min_baja, 410, 290, 250 ,240 , 210).place(x=20, rely=0.35, relwidth=0.60)

Label(left_frame, text="Kekuatan Maksimum baja(FU) ", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.40)
OptionMenu(left_frame, kekuatan_max_baja, 550, 500,410,370, 340).place(x=20, rely=0.45, relwidth=0.60)

Label(left_frame, text="Ketinggian Gedung(H)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.50)
Entry(left_frame, width=25, textvariable=ketinggian_gedung, font=entryfont).place(x=20, rely=0.55)

Label(center_frame, text="Beban Terbagi Rata(qu)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.01)
Entry(center_frame, width=25, textvariable=beban_terbagi_rata, font=entryfont).place(x=20, rely=0.05)

Label(center_frame, text="Beban Terpusat(pu)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.1)
Entry(center_frame, width=25, textvariable=beban_terpusat, font=entryfont).place(x=20, rely=0.15)

Label(center_frame, text="Radius(Ra)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.20)
Entry(center_frame, width=25, textvariable=radius, font=entryfont).place(x=20, rely=0.25)

Label(center_frame, text="Koefisien b(Øb)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.30)
Entry(center_frame, width=25, textvariable=koefisien_b, font=entryfont).place(x=20, rely=0.35)

Label(center_frame, text="Koefisien Geser(Øv)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.40)
Entry(center_frame, width=25, textvariable=koefisien_geser, font=entryfont).place(x=20, rely=0.45)

Label(center_frame, text="Faktor Distribusi Vertikal(cv)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.50)
Entry(center_frame, width=25, textvariable=faktor_distribusi_vertikal, font=entryfont).place(x=20, rely=0.55)




Button(left_frame, text='Submit and Analyze', font=labelfont, command=add_record, width=16).place(relx=0.07, rely=0.65)

# Placing components in the center frame
Button(left_frame, text='Delete Record', font=labelfont, fg="#c62828", command=remove_record, width=16).place(relx=0.07, rely=0.75)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=16).place(relx=0.05, rely=0.65)
Button(center_frame, text='Delete All Data', font=labelfont,fg="#c62828", command=getAllDataIWFByZx, width=16).place(relx=0.05, rely=0.75)

# Placing components in the right frame
Label(right_frame, text='Riwayat Hasil Analisa', font=headlabelfont, bg='Grey35', fg=white).pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('STEEL_ID','project_name', "ratio", "Zx", "H", "B", "r_lentur", "r_geser","r_stabilitas_tekuk","r_stabilitas_penampang_flenge","r_stabilitas_penampang_web"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('STEEL_ID', text='ID', anchor=CENTER)

tree.heading('project_name', text='Nama Proyek', anchor=CENTER)
tree.heading('ratio', text='Ratio', anchor=CENTER)
tree.heading('Zx', text='Zx', anchor=CENTER)
tree.heading('H', text='H', anchor=CENTER)
tree.heading('B', text='B', anchor=CENTER)
tree.heading('r_lentur', text='Ratio Lentur', anchor=CENTER)
tree.heading('r_geser', text='Ratio Geser', anchor=CENTER)
tree.heading('r_stabilitas_tekuk', text='Ratio Stabilitas Tekuk', anchor=CENTER)
tree.heading('r_stabilitas_penampang_flenge', text='Stabilitas Penampang Flenge', anchor=CENTER)
tree.heading('r_stabilitas_penampang_web', text='Stabilitas Penampang Web', anchor=CENTER)




tree.column('#0', width=0, stretch=NO,anchor=CENTER)
tree.column('#1', width=20, stretch=NO,anchor=CENTER)
tree.column('#2', width=120, stretch=NO,anchor=CENTER)
tree.column('#3', width=50, stretch=NO,anchor=CENTER)
tree.column('#4', width=50, stretch=NO,anchor=CENTER)
tree.column('#5', width=40, stretch=NO,anchor=CENTER)
tree.column('#6', width=50, stretch=NO,anchor=CENTER)
tree.column('#7', width=75, stretch=NO,anchor=CENTER)
tree.column('#8', width=80, stretch=NO,anchor=CENTER)
tree.column('#9', width=130, stretch=NO,anchor=CENTER)
tree.column('#10', width=160, stretch=NO,anchor=CENTER)
tree.column('#11', width=160, stretch=NO,anchor=CENTER)


tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
