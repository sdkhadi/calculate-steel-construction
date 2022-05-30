import datetime
from logging import PlaceHolder
from operator import mod
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from turtle import color
from tkcalendar import DateEntry  # pip install tkcalendar
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('ConstructionSteel.db')
cursor = connector.cursor()

connector.execute(
"CREATE TABLE IF NOT EXISTS CONSTRUCTION_STEEL (STEEL_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, PROYEK_NAME TEXT, RATIO FLOAT, ZX FLOAT, H FLOAT, B FLOAT, RATIO_LENTUR TEXT, RATIO GESER TEXT, RATIO_STABILITAS_TEKUK TEXT, STABILITAS_PENAMPANG TEXT)"
)

# Creating the functions
def reset_fields():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar', 'stream_strvar']:
        exec(f"{i}.set('')")
    dob.set_date(datetime.datetime.now().date())


def reset_form():
    global tree
    tree.delete(*tree.get_children())

    reset_fields()


def display_records():
    tree.delete(*tree.get_children())

    curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
    data = curr.fetchall()

    for records in data:
        tree.insert('', END, values=records)


def add_record():
    global proyek_name,panjang,modulus_elastisitas,kekuatan_min_baja,kekuatan_max_baja,ketinggian_gedung,beban_terbagi_rata,beban_terpusat,radius,koefisien_b,koefisien_geser,faktor_distribusi_vertikal
    global Zx,H,B,ratio,ratio_lentur,ratio_geser,ratio_stabilitas_tekuk,stabilitas_penampang

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
            connector.execute(
            'INSERT INTO CONSTRUCTION_STEEL (PROYEK_NAME,RATIO,ZX,H,B,RATIO_LENTUR,RATIO GESER,RATIO_STABILITAS_TEKUK,STABILITAS_PENAMPANG) VALUES (?,?,?,?,?,?,?,?,?)', (varProyekName,ratio, Zx, H, B, ratio_lentur, ratio_geser,ratio_stabilitas_tekuk,stabilitas_penampang)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {varProyekName} was successfully added")
            reset_fields()
            display_records()
        except:
            mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
    if not tree.selection():
        mb.showerror('Error!', 'Please select an item from the database')
    else:
        current_item = tree.focus()
        values = tree.item(current_item)
        selection = values["values"]

        tree.delete(current_item)

        connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
        connector.commit()

        mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')

        display_records()


def view_record():
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    current_item = tree.focus()
    values = tree.item(current_item)
    selection = values["values"]

    date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))

    name_strvar.set(selection[1]); email_strvar.set(selection[2])
    contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
    dob.set_date(date); stream_strvar.set(selection[6])


# Initializing the GUI window
main = Tk()
main.title('My Project')
main.geometry('1280x1280')
main.resizable(True, True)



# Creating the background and foreground color variables
lf_bg = 'Gray35' # bg color for the left_frame
cf_bg = 'Gray35' # bg color for the center_frame
primaryBg = "Gray35"
white ="#ffffff"

# Creating the StringVar or IntVar variables
name_strvar = StringVar()
email_strvar = IntVar()
contact_strvar = IntVar()
gender_strvar = IntVar()
fu = IntVar()
stream_strvar = IntVar()

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
stabilitas_penampang = StringVar()



# Placing the components in the main window
Label(main, text="Perhitungan Konstruksi Baja", font=headlabelfont, bg=primaryBg,fg=white).pack(side=TOP, fill=X)

left_frame = Frame(main, bg=primaryBg)
left_frame.place(x=0, y=25, relheight=1, relwidth=0.20)

center_frame = Frame(main, bg=primaryBg)
danger_frame = Frame(main, bg=primaryBg)

center_frame.place(relx=0.18, y=25, relheight=1, relwidth=0.20)

right_frame = Frame(main, bg=primaryBg)
right_frame.place(relx=0.35, y=25, relheight=1, relwidth=0.9)

# Placing components in the left frame
Label(left_frame, text="Nama Proyek", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.01)
Entry(left_frame, width=25, textvariable=proyek_name, font=entryfont).place(x=20, rely=0.05)

Label(left_frame, text="Panjang(L)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.1)
Entry(left_frame, width=25, textvariable=panjang, font=entryfont).place(x=20, rely=0.15)

Label(left_frame, text="Modulus Elastisitas(E)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.20)
Entry(left_frame, width=25, textvariable=modulus_elastisitas, font=entryfont).place(x=20, rely=0.25)

Label(left_frame, text="Kekuatan Minimum baja(FY)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.30)
OptionMenu(left_frame, kekuatan_min_baja, 410, 290, 250 ,240 , 210).place(x=20, rely=0.35, relwidth=0.65)

Label(left_frame, text="Kekuatan Maksimum baja(FU) ", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.40)
OptionMenu(left_frame, kekuatan_max_baja, 550, 500,410,370, 340).place(x=20, rely=0.45, relwidth=0.65)

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
Button(center_frame, text='Delete Record', font=labelfont, fg="#c62828", command=remove_record, width=16).place(relx=0.07, rely=0.75)
Button(left_frame, text='View Record', font=labelfont, command=view_record, width=16).place(relx=0.07, rely=0.75)
Button(left_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=16).place(relx=0.07, rely=0.80)
Button(center_frame, text='Delete database', font=labelfont,fg="#c62828", command=reset_form, width=16).place(relx=0.07, rely=0.80)

# Placing components in the right frame
Label(right_frame, text='Riwayat Hasil Analisa', font=headlabelfont, bg='Grey35', fg=white).pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('project_name', "ratio", "Zx", "H", "B", "r_lentur", "r_geser","r_stabilitas_tekuk","r_stabilitas_penampang"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('project_name', text='Nama Proyek', anchor=CENTER)
tree.heading('ratio', text='Ratio', anchor=CENTER)
tree.heading('Zx', text='Zx', anchor=CENTER)
tree.heading('H', text='H', anchor=CENTER)
tree.heading('B', text='B', anchor=CENTER)
tree.heading('r_lentur', text='Ratio Lentur', anchor=CENTER)
tree.heading('r_geser', text='Ratio Geser', anchor=CENTER)
tree.heading('r_stabilitas_tekuk', text='Ratio Stabilitas Tekuk', anchor=CENTER)
tree.heading('r_stabilitas_penampang', text='Stabilitas Penampang ', anchor=CENTER)



tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=100, stretch=NO)
tree.column('#2', width=60, stretch=NO)
tree.column('#3', width=60, stretch=NO)
tree.column('#4', width=60, stretch=NO)
tree.column('#5', width=60, stretch=NO)
tree.column('#6', width=100, stretch=NO)
tree.column('#7', width=100, stretch=NO)
tree.column('#8', width=150, stretch=NO)
tree.column('#9', width=150, stretch=NO)





tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
