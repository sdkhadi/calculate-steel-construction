from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3
import json
import math
import numpy as np

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
"CREATE TABLE IF NOT EXISTS CONSTRUCTION_STEEL (STEEL_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, PROYEK_NAME TEXT, ZX DOUBLE, H DOUBLE, B DOUBLE, RATIO_LENTUR TEXT, RATIO_GESER TEXT, STABILITAS_PENAMPANG_FLENGE TEXT,STABILITAS_PENAMPANG_WEB TEXT, RATIO_STABILITAS_TEKUK TEXT )"
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

def getMmax():
    global beban_terpusat,panjang, beban_terbagi_rata
    pu = float(beban_terpusat.get())
    L = float(panjang.get())
    qu = float(beban_terbagi_rata.get())
    Mmax =  (0.25*pu*L)+(0.125*qu*pow(L,2))
    return Mmax

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def getZx():
    global kekuatan_min_baja,koefisien_b
    Fy = float(kekuatan_min_baja.get())
    Øb = float(koefisien_b.get())
    Mmax = getMmax()

    Zxperlu = Mmax / (Fy * Øb )
    print("ZxpERLU = "+ str(Zxperlu))

    array = []
    for i in data['IWF']:
        res = i['Zx']
        array.append(res)
        
    getFixZx = find_nearest(array,Zxperlu)
    return getFixZx

def getAllDataIWFByZx():

    getFixZx = getZx()
    print("ZxFromTable = " + str(getFixZx))

    array = []
    for i in data['IWF']:
        res = i['Zx']
        array.append(res)
        if res == getFixZx :
            jsonObject = {
            "H":i['H'],
            "B":i['B'],
            "Tf":i['Tf'],
            "Tw":i['Tw'],
            "A":i['A'],
            "R":i['r'],
            "Ix":i['Ix'],
            "Iy":i['Iy'],
            "Zy":i['Zy'],
            "Zx":i['Zx']
        }       
    return jsonObject


def analyzeRatioKapasitasLentur():
    global kekuatan_min_baja,koefisien_b
    Øb = float(koefisien_b.get())
    Fy= float(kekuatan_min_baja.get())
    jsonLoads = getAllDataIWFByZx()
    # jsonLoads = json.load(getDataIWF)
    print("Get IWF = " + str(jsonLoads))
    Sx = (jsonLoads["B"] * jsonLoads["Tf"]) * (jsonLoads["H"] * jsonLoads["Tf"]) + jsonLoads["Tw"] * (0.5 * jsonLoads["H"] - jsonLoads["Tf"]) * (0.5 * jsonLoads["H"] - jsonLoads["Tf"])
    # Mmax = getMmax(beban_terpusat,panjang,beban_terbagi_rata)
    Mmax = getMmax()
    Mn = Sx * Fy
    Rasio = Mmax / (Øb * Mn)

    if Rasio < 1:
        print("Result Kapasitas Lentur OK")
        return "OK"
    elif Rasio > 1:
        print("Result Kapasitas Lentur Tidak OK")
        return "Tidak OK" 

def analyzeRatioKapasitasGeser():
    global radius,koefisien_b,kekuatan_min_baja, faktor_distribusi_vertikal
    r = float(radius.get())
    Fy = float(kekuatan_min_baja.get())
    Cv = float(faktor_distribusi_vertikal.get())
    Øb = float(koefisien_b.get())
    jsonLoads = getAllDataIWFByZx()

    Vu = r
    Vn = 0.6 * Fy * Cv * (jsonLoads["H"] - 2 * jsonLoads["Tf"]) * jsonLoads["Tw"]
    Rasio = Vu/(Øb * Vn)
    if Rasio < 1:
        print("Result Kapasitas Geser OK")
        return "OK"
    elif Rasio > 1:
        print("Result Kapasitas Geser Tidak OK")
        return "Tidak OK"

def analyzeRatioStabilitasPenampangFlenge():
    global modulus_elastisitas,kekuatan_min_baja
    e = float(modulus_elastisitas.get())
    Fy = float(kekuatan_min_baja.get())
    jsonLoads = getAllDataIWFByZx()
    λpf = 0.38*math.sqrt(e/Fy)
    λf = jsonLoads["B"]/(2*jsonLoads["Tf"])
    if λf < λpf:
        print("Flenge Kompak")
        return "Kompak"
    elif λf > λpf:
        print("Flenge tidak Kompak")
        return "Tidak Kompak"

def analyzeRatioStabilitasPenampangWeb():
    global modulus_elastisitas,kekuatan_min_baja
    e = float(modulus_elastisitas.get())
    Fy = float(kekuatan_min_baja.get())
    jsonLoads = getAllDataIWFByZx()
    λpw = 3.78 * math.sqrt(e/Fy)
    λw = (jsonLoads["H"]-2 * jsonLoads["Tf"]) / jsonLoads["Tw"]
    if λw < λpw:
        print("Web Kompak")
        return "Kompak"
    elif λw > λpw:
        print("Web Tidak Kompak")
        return "Tidak Kompak"

def analyzeRatioStabilitasTekuk():
    global kekuatan_min_baja
    Fy = float(kekuatan_min_baja.get())

    jsonLoads = getAllDataIWFByZx()
        # jsonLoads = json.load(getDataIWF)
    print("Get IWF = " + str(jsonLoads))
    Sx = (jsonLoads["B"] * jsonLoads["Tf"]) * (jsonLoads["H"] * jsonLoads["Tf"]) + jsonLoads["Tw"] * (0.5 * jsonLoads["H"] - jsonLoads["Tf"]) * (0.5 * jsonLoads["H"] - jsonLoads["Tf"])
    # Mmax = getMmax(beban_terpusat,panjang,beban_terbagi_rata)
    Mmax = getMmax()
    # Sx*Fy
    Mn = Sx * Fy
    ØMn = 0.9 * Mn
    if ØMn > Mmax:
        print("Result Tekuk OK")
        return "OK"
    elif ØMn < Mmax:
        print("Result Tekuk Tidak OK")
        return "Tidak OK"

def add_record():
    global proyek_name,panjang,modulus_elastisitas,kekuatan_min_baja,kekuatan_max_baja,ketinggian_gedung,beban_terbagi_rata,beban_terpusat,radius,koefisien_b,koefisien_geser,faktor_distribusi_vertikal

    varProyekName = proyek_name.get()
    varPanjang = panjang.get()
    varModulusElastisitas = float(modulus_elastisitas.get())
    varKekuatanMinBaja = float(kekuatan_min_baja.get())
    varKekuatanMaxBaja = float(kekuatan_max_baja.get())
    varKetinggianGedung = float(ketinggian_gedung.get())
    varBebanTerbagiRata = float(beban_terbagi_rata.get())
    varBebanTerpusat = float(beban_terpusat.get())
    varRadius = float(radius.get())
    varKoefisienB = float(koefisien_b.get())
    varKoefisienGeser = float(koefisien_geser.get())
    varDistribusiVertikal = float(faktor_distribusi_vertikal.get())

    if not varProyekName or not varPanjang or not varModulusElastisitas or not varKekuatanMinBaja or not varKekuatanMaxBaja or not varKetinggianGedung or not varBebanTerbagiRata or not varBebanTerpusat or not varRadius or not varKoefisienB or not varKoefisienGeser or not varDistribusiVertikal:
        mb.showerror('Error!', "Semua Field Wajib Diisi")
    else:
        try:
            jsonLoads = getAllDataIWFByZx()
            kapasitasLentur = analyzeRatioKapasitasLentur()
            print("AAAAA = " + kapasitasLentur)
            kapasitasGeser = analyzeRatioKapasitasGeser()
            print("BBBBB = " + kapasitasGeser)
            stabilitasPenampangFlenge = analyzeRatioStabilitasPenampangFlenge()
            print("CCCC= "+stabilitasPenampangFlenge)
            stabilitasPenampangWeb = analyzeRatioStabilitasPenampangWeb()
            print("DDDDD = " +stabilitasPenampangWeb)

            stabilitasTekuk = analyzeRatioStabilitasTekuk()

            print("EEEEE = " + stabilitasTekuk)
            connector.execute(
            'INSERT INTO CONSTRUCTION_STEEL(PROYEK_NAME,ZX,H,B,RATIO_LENTUR,RATIO_GESER,STABILITAS_PENAMPANG_FLENGE,STABILITAS_PENAMPANG_WEB,RATIO_STABILITAS_TEKUK) VALUES (?,?,?,?,?,?,?,?,?)', (varProyekName, jsonLoads['Zx'], jsonLoads["H"], jsonLoads["H"], kapasitasLentur, kapasitasGeser,stabilitasPenampangFlenge,stabilitasPenampangWeb,stabilitasTekuk)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {varProyekName} was successfully added")
            reset_fields()
            display_records()
        except:
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')

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
panjang = IntVar()
modulus_elastisitas = IntVar()
kekuatan_min_baja = IntVar()
kekuatan_max_baja = IntVar()
ketinggian_gedung = IntVar()
beban_terbagi_rata = IntVar()
beban_terpusat = IntVar()
radius =IntVar()
koefisien_b =IntVar()
koefisien_geser = IntVar()
faktor_distribusi_vertikal = IntVar()



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
Button(center_frame, text='Delete All Data', font=labelfont,fg="#c62828", command=reset_form, width=16).place(relx=0.05, rely=0.75)

# Placing components in the right frame
Label(right_frame, text='Riwayat Hasil Analisa', font=headlabelfont, bg='Grey35', fg=white).pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('STEEL_ID','project_name', "Zx", "H", "B", "r_lentur", "r_geser","r_stabilitas_tekuk","r_stabilitas_penampang_flenge","r_stabilitas_penampang_web"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('STEEL_ID', text='ID', anchor=CENTER)

tree.heading('project_name', text='Nama Proyek', anchor=CENTER)
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
tree.column('#3', width=70, stretch=NO,anchor=CENTER)
tree.column('#4', width=60, stretch=NO,anchor=CENTER)
tree.column('#5', width=60, stretch=NO,anchor=CENTER)
tree.column('#6', width=75, stretch=NO,anchor=CENTER)
tree.column('#7', width=80, stretch=NO,anchor=CENTER)
tree.column('#8', width=130, stretch=NO,anchor=CENTER)
tree.column('#9', width=160, stretch=NO,anchor=CENTER)
tree.column('#10', width=160, stretch=NO,anchor=CENTER)


tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
