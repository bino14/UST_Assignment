from tkinter import *
import sqlite3
from tkinter import ttk, messagebox

top = Tk()
top.geometry('1600x1200')
top.configure(background="grey")
top.title("Student Application")


class student:
    def __init__(self):
        try:
            self.con = sqlite3.connect("studentdatadb.db")
            self.curs = self.con.cursor()
            self.curs.execute(
                "create table if not exists student (sid integer primary key AUTOINCREMENT,name text,mobile int,"
                "age int, "
                "college text)")
            self.con.commit()

        except:
            messagebox.showinfo("Sql3 package Not available")

    def select(self):
        self.curs.execute("select * from student")
        rows = self.curs.fetchall()
        return rows

    def insert(self, name, mobile, age, college):
        self.curs.execute("insert into student values(NULL,?,?,?,?)", (name, mobile, age, college))
        self.con.commit()
        self.select()

    def delete(self, sid):
        self.curs.execute("delete from student where sid=?", (sid,))
        self.con.commit()
        self.select()

    def update(self, sid, name, mobile, age, college):
        self.curs.execute("update student SET name=?,mobile=?,age=?,college=? where sid=?",
                          (name, mobile, age, college, sid))
        self.con.commit()
        self.select()


studentobj = student()  # object for the class student


# Button click Functions
def clean_text():
    name.delete(0, END)
    age.delete(0, END)
    mobile.delete(0, END)
    college.delete(0, END)


def selectrow(event):
    global row_tupple
    try:

        data = lbox.curselection()[0]
        row_tupple = lbox.get(data)
        clean_text()
        name.insert(END, row_tupple[1])
        age.insert(END, row_tupple[2])
        mobile.insert(END, row_tupple[3])
        college.insert(END, row_tupple[4])


    except:
        messagebox.showinfo("Alert", "Please Select A Row")


def insert():
    var = check()
    if var:
        studentobj.insert(name.get(), mobile.get(), age.get(), college.get())
        lbox.delete(0, END)
        # lbox.insert(END, (name.get(), mobile.get(), age.get(), college.get()))
        messagebox.showinfo("Successful", "Data Inserted!")
        clean_text()
    else:
        messagebox.showinfo("Alert", "Please Fill the fields")


def view():
    lbox.delete(0, END)
    op = studentobj.select()
    if op:
        for row in studentobj.select():
            lbox.insert(END, row)
    clean_text()


def delete():
    var = check()
    if var:
        studentobj.delete(row_tupple[0])
        messagebox.showinfo("Alert", "Student Removed!")
        lbox.delete(0, END)
        clean_text()
    else:
        messagebox.showinfo("Alert", "Please Select a field")


def modify():
    studentobj.update(row_tupple[0], name.get(), mobile.get(), age.get(), college.get())
    messagebox.showinfo("Alert", "Student Data Updated!")
    lbox.delete(0, END)
    clean_text()


def check():
    if name.get() == '' or age.get() == '' or college.get() == '' or mobile.get() == '':
        return 0
    else:
        return 1


def close():
    top.destroy()


topheading = Label(top, text="STUDENT DATA MANAGEMENT", width=30, height=2, font=("Helvetica", 20), fg="white",
                   bg="grey", relief=RIDGE)
topheading.pack()
addlabel = Label(top, text="ENTER STUDENT DETAILS", fg="white", width=20, bg="grey", relief=RIDGE).place(x=180, y=115)
viewlabel = Label(top, text="DATA VIEW", width=20, fg="white", bg="grey", relief=RIDGE).place(x=830, y=115)
label1 = Label(top, text="Name", width=10).place(x=100, y=200)
label2 = Label(top, text="Age", width=10).place(x=100, y=250)
label3 = Label(top, text="Mobile", width=10).place(x=100, y=300)
label4 = Label(top, text="College", width=10).place(x=100, y=350)

name = Entry(top, width=30)
# name.pack()
name.place(x='200', y='200')
age = Entry(top, width=30)
# age .pack()
age.place(x='200', y='250')
mobile = Entry(top, width=30)
# mobile.pack()
mobile.place(x='200', y='300')
college = Entry(top, width=30)
# college.pack()
college.place(x='200', y='350')

lbox = Listbox(top, height=20, width=85)
lbox.place(x='650', y='180')
lbox.bind('<<ListboxSelect>>', selectrow)
# Controls
Button(text="ADD", command=insert).place(x='250', y='400')
Button(text="VIEW", command=view).place(x='700', y='600')
Button(text="DELETE", command=delete).place(x='750', y='600')
Button(text="MODIFY", command=modify).place(x='810', y='600')
Button(text="CLEAR FIELD", command=clean_text).place(x='875', y='600')
Button(text="EXIT", command=close,bg='red').place(x='1300', y='100')
top.mainloop()
