from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from DB import Database


db = Database()
win = Tk()
win.title("EXPENSE TRACKER")
win.geometry("1918x1080+0+0")


bg_image = Image.open("03.jpg")
bg_image = bg_image.resize((1918, 1080))  
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(win, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

win.state("zoomed")


category = StringVar()
amount = StringVar()
date = StringVar()
description = StringVar()
selected_row = None  


Entries_Frame = Frame(win)
Entries_Frame.pack(side=TOP)
title = Label(Entries_Frame, text="EXPENSE TRACKER", font=("Tahoma", 35, "bold"), bg="#4cd0ff")
title.grid(row=0, columnspan=2)


lblCategory = Label(text="Category :", font=("Tahoma", 18, "bold"), bg="#4cd0ff")
lblCategory.place(x=100, y=150)
txtCategory = Entry(textvariable=category, font=("Tahoma", 18, "bold"), bg="white")
txtCategory.place(x=250, y=150)

lblAmount = Label(text="Amount :", font=("Tahoma", 18, "bold"), bg="#4cd0ff")
lblAmount.place(x=760, y=150)
txtAmount = Entry(textvariable=amount, font=("Tahoma", 18, "bold"), bg="white")
txtAmount.place(x=950, y=150)

lblDate = Label(text="Date :", font=("Tahoma", 18, "bold"), bg="#4cd0ff")
lblDate.place(x=100, y=210)
txtDate = Entry(textvariable=date, font=("Tahoma", 18, "bold"), bg="white")
txtDate.place(x=250, y=210)

lblDescription = Label(text="Description :", font=("Tahoma", 18, "bold"), bg="#4cd0ff")
lblDescription.place(x=100, y=270)
txtDescription = Text(font=("Tahoma", 18, "bold"), width=67, height=5)
txtDescription.place(x=250, y=320)


def getdata(event, tv):
    global selected_row
    selectrow = tv.focus()
    data = tv.item(selectrow)
    selected_row = data["values"]
    category.set(selected_row[1])
    amount.set(selected_row[2])
    date.set(selected_row[3])
    txtDescription.delete(1.0, END)
    txtDescription.insert(END, selected_row[4])

def disp_all(tv):
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

def add_expense():
    if txtCategory.get() == "" or txtAmount.get() == "" or txtDate.get() == "" or txtDescription.get(1.0, END) == "":
        messagebox.showerror("Error in input", "Please fill the details")
        return
    db.insert(txtCategory.get(), txtAmount.get(), txtDate.get(), txtDescription.get(1.0, END))
    messagebox.showinfo("Success", "Insertion successful")
    clear()

def upd_expense():
    if txtCategory.get() == "" or txtAmount.get() == "" or txtDate.get() == "" or txtDescription.get(1.0, END) == "":
        messagebox.showerror("Error in input", "Please fill the details")
        return
    db.update(selected_row[0], txtCategory.get(), txtAmount.get(), txtDate.get(), txtDescription.get(1.0, END))
    messagebox.showinfo("Success", "Update successful")
    clear()

def del_expense():
    db.remove(selected_row[0])
    clear()
    messagebox.showinfo("Success", "Deletion Successful")

def clear():
    category.set("")
    amount.set("")
    date.set("")
    txtDescription.delete(1.0, END)

def show_total_amount():
    total = db.get_total_amount()
    messagebox.showinfo("Total Amount", f"Total amount of all expenses: {total}")

def show_category_amount():
    if txtCategory.get() == "":
        messagebox.showerror("Error", "Please enter a category")
        return
    total = db.get_category_amount(txtCategory.get())
    messagebox.showinfo("Category Amount", f"Total amount for category '{txtCategory.get()}': {total}")

def open_treeview_window():
    tv_win = Toplevel(win)
    tv_win.title("Expense Records")
    tv_win.geometry("800x400")

    tree_fr = Frame(tv_win)
    tree_fr.pack(fill=BOTH, expand=True)
    style = ttk.Style()
    style.configure("mystyle.Treeview", font=("Tahoma", 12))
    style.configure("mystyle.Treeview.Heading", font=("Tahoma", 12, "bold"))

    tv = ttk.Treeview(tree_fr, columns=(1, 2, 3, 4, 5), style="mystyle.Treeview")
    tv.heading("1", text="ID")
    tv.column("1", width=90)
    tv.heading("2", text="Category")
    tv.heading("3", text="Amount")
    tv.column("3", width=90)
    tv.heading("4", text="Date")
    tv.heading("5", text="Description")
    tv['show'] = 'headings'
    tv.bind("<ButtonRelease-1>", lambda event: getdata(event, tv))
    tv.pack(fill=BOTH, expand=True)

    disp_all(tv)


Btnadd = Button(command=add_expense, text="Add Expense", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btnadd.place(x=250, y=500)

Btnupd = Button(command=upd_expense, text="Update Expense", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btnupd.place(x=400, y=500)

Btndel = Button(command=del_expense, text="Delete Expense", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btndel.place(x=550, y=500)

Btnclr = Button(command=clear, text="Clear Fields", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btnclr.place(x=700, y=500)

Btntotal = Button(command=show_total_amount, text="Total Amount", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btntotal.place(x=850, y=500)

Btncat_total = Button(command=show_category_amount, text="Category Amount", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btncat_total.place(x=1000, y=500)

Btnview = Button(command=open_treeview_window, text="View Records", height=2, width=15, bd=0, bg="#4a9fd6", foreground="white")
Btnview.place(x=1150, y=500)

win.mainloop()


