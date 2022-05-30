import datetime
from logging import PlaceHolder
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
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, DOB TEXT, STREAM TEXT)"
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
    global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar

    name = name_strvar.get()
    email = email_strvar.get()
    contact = contact_strvar.get()
    gender = gender_strvar.get()
    DOB = dob.get_date()
    stream = stream_strvar.get()

    if not name or not email or not contact or not gender or not DOB or not stream:
        mb.showerror('Error!', "Please fill all the missing fields!!")
    else:
        try:
            connector.execute(
            'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (?,?,?,?,?,?)', (name, email, contact, gender, DOB, stream)
            )
            connector.commit()
            mb.showinfo('Record added', f"Record of {name} was successfully added")
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
main.geometry('1280x720')
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

# Placing the components in the main window
Label(main, text="Perhitungan Konstruksi Baja", font=headlabelfont, bg=primaryBg,fg=white).pack(side=TOP, fill=X)

left_frame = Frame(main, bg=primaryBg)
left_frame.place(x=0, y=25, relheight=1, relwidth=0.20)

center_frame = Frame(main, bg=primaryBg)
danger_frame = Frame(main, bg=primaryBg)

center_frame.place(relx=0.18, y=25, relheight=1, relwidth=0.20)

right_frame = Frame(main, bg=primaryBg)
right_frame.place(relx=0.35, y=25, relheight=1, relwidth=0.7)

# Placing components in the left frame
Label(left_frame, text="Nama Proyek", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.01)
Entry(left_frame, width=25, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.05)

Label(left_frame, text="Panjang(L)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.1)
Entry(left_frame, width=25, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.15)

Label(left_frame, text="Modulus Elastisitas(E)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.20)
Entry(left_frame, width=25, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.25)

Label(left_frame, text="Kekuatan minimum baja(FY)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.30)
Entry(left_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.35)

Label(left_frame, text="Kekuatan maksimum baja(FU) ", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.40)
OptionMenu(left_frame, gender_strvar, 410, 290, 250 ,240 , 210).place(x=20, rely=0.45, relwidth=0.65)

Label(left_frame, text="Ketinggian Gedung(H)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.50)
OptionMenu(left_frame, fu, 550, 500,410,370, 340).place(x=20, rely=0.55, relwidth=0.65)

Label(center_frame, text="Beban Terbagi Rata(qu)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.01)
Entry(center_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.05)

Label(center_frame, text="Beban terpusat(pu)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.1)
Entry(center_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.15)

Label(center_frame, text="Radius(Ra)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.20)
Entry(center_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.25)

Label(center_frame, text="koefisien b(Øb)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.30)
Entry(center_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.35)

Label(center_frame, text="koefisien Geser(Øv)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.40)
Entry(center_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.45)

Label(center_frame, text="faktor distribusi vertikal(cv)", font=labelfont, bg=lf_bg,fg=white).place(relx=0.07, rely=0.50)
Entry(center_frame, width=25, textvariable=stream_strvar, font=entryfont).place(x=20, rely=0.55)




Button(left_frame, text='Submit and Analyze', font=labelfont, command=add_record, width=16).place(relx=0.07, rely=0.65)

# Placing components in the center frame
Button(center_frame, text='Delete Record', font=labelfont, fg="#c62828", command=remove_record, width=16).place(relx=0.07, rely=0.75)
Button(left_frame, text='View Record', font=labelfont, command=view_record, width=16).place(relx=0.07, rely=0.75)
Button(left_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=16).place(relx=0.07, rely=0.80)
Button(center_frame, text='Delete database', font=labelfont,fg="#c62828", command=reset_form, width=16).place(relx=0.07, rely=0.80)

# Placing components in the right frame
Label(right_frame, text='Riwayat Hasil Analisa', font=headlabelfont, bg='Grey35', fg=white).pack(side=TOP, fill=X)

tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                    columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Date of Birth", "Stream"))

X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)

X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)

tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

tree.heading('Student ID', text='Nama Proyek', anchor=CENTER)
tree.heading('Name', text='Ratio', anchor=CENTER)
tree.heading('Email Address', text='H', anchor=CENTER)
tree.heading('Contact Number', text='B', anchor=CENTER)
tree.heading('Gender', text='Ratio Lentur', anchor=CENTER)
tree.heading('Date of Birth', text='Ratio Geser', anchor=CENTER)
tree.heading('Stream', text='Stream', anchor=CENTER)

tree.column('#0', width=0, stretch=YES)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=80, stretch=NO)
tree.column('#7', width=150, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)

display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
