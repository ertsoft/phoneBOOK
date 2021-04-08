                                ### CREATE A PHONE BOOK IN PYTHON WITH TKINTER ###


from tkinter import *
import sqlite3
from tkinter import ttk, messagebox


#Initialize the root
root = Tk()
root.resizable(0, 0)  #disable Maximze button
root.title("Phone Book")
#root.geometry("360x600")
root.minsize(360, 800)
root.iconbitmap('D:/Projects_python/Phone Book/phone.png')
root.configure(background="gray")


def show():
    #create a databases or connect to one
    data1 = sqlite3.connect('book_phone.db')
    #create cursor
    c = data1.cursor()

    #select all data from table

    c.execute("SELECT * FROM Register")
    registers = c.fetchall()    # fetchall() take all data from table and return it into a list
    print_record = ""
    for register in registers:
        print_record += str(register) + '\n'

    mylabel = Label(root, text=print_record)
    mylabel.grid(row=1, column=0, columnspan=2)
    data1.commit()

    data1.close()

    def hide_func():
        mylabel.destroy()
        hide_button.destroy()

    hide_button = ttk.Button(root, text="Hide contacts", command=hide_func)
    hide_button.grid(row=2, column=0, columnspan=2, ipady=5, ipadx=125, pady=1.5)


def add():
    adder = Tk()
    adder.title("Add a new contact")
    adder.geometry("300x400")

    def save_func():
        # create a databases or connect to one
        data1 = sqlite3.connect('book_phone.db')
        # create cursor
        c = data1.cursor()

        record_phone_add = phone_box.get()  # Save phone number.

        if len(record_phone_add) > 11 or len(record_phone_add) < 11:
            messagebox.showinfo("INFO", "Phone number must have 10 characters!")  ## Phone number must have 10 characters, not more, not less !
        else:
            # select all data from table
            c.execute("INSERT INTO Register VALUES (:f_name_box, :l_name_box, :mail_box, :phone_box)",
                     {
                         'f_name_box': f_name_box.get(),     ### Here i created a dictionary , ':f_name_box' is just a key , it could be any name/variable
                         'l_name_box': l_name_box.get(),
                         'mail_box': mail_box.get(),
                         'phone_box': phone_box.get()
                     }
                     )

            data1.commit()

            data1.close()

        #Clear the boxes
        f_name_box.delete(0, END)
        l_name_box.delete(0, END)
        mail_box.delete(0, END)
        phone_box.delete(0, END)

    def cancel_func():
        # Clear the boxes
        f_name_box.delete(0, END)
        l_name_box.delete(0, END)
        mail_box.delete(0, END)
        phone_box.delete(0, END)

#Create Labels
    f_name = Label(adder, text="First Name")
    f_name.grid(row=0, column=0)
    l_name = Label(adder, text="Last Name")
    l_name.grid(row=1, column=0)
    mail = Label(adder, text="E-mail")
    mail.grid(row=2, column=0)
    phone = Label(adder, text="Phone")
    phone.grid(row=3, column=0)

#Create Text Box
    f_name_box = Entry(adder, width=35)
    f_name_box.grid(row=0, column=1)
    l_name_box = Entry(adder, width=35)
    l_name_box.grid(row=1, column=1)
    mail_box = Entry(adder, width=35)
    mail_box.grid(row=2, column=1)
    phone_box = Entry(adder, width=35)
    phone_box.grid(row=3, column=1)


    #save button AND cancel button
    save_btn = Button(adder, text="Save", command=save_func)
    save_btn.grid(row=4, column=1, pady=5, ipadx=15)

    cancel_btn = Button(adder, text="Cancel", command=cancel_func)
    cancel_btn.grid(row=4, column=0, pady=5)

    adder.mainloop()


def delete():
    deleter = Tk()
    deleter.title("Delete a contact")
    deleter.geometry("250x200")

    def cancel_func():
        # Clear the boxes
        phone_box.delete(0, END)

    def delete_func():
        data1 = sqlite3.connect('book_phone.db')

        #create cursor
        c = data1.cursor()

        #delete reccord
        c.execute("DELETE FROM Register WHERE oid= "+phone_box.get())

        #commit changes
        data1.commit()

        #close connection
        data1.close()
        # Clear the boxes
        phone_box.delete(0, END)

    phone = Label(deleter, text="Phone")
    phone.grid(row=0, column=0, pady=6)

    phone_box = Entry(deleter, width=29)
    phone_box.grid(row=0, column=1)

    #Create delete_button AND cancel_button
    delete_button = Button(deleter, text="DELETE", bg="green", command=delete_func)
    delete_button.grid(row=1, column=0, ipadx=20)

    cancel_button = Button(deleter, text="Cancel", command=cancel_func)
    cancel_button.grid(row=1, column=1, ipadx=19)

    deleter.mainloop()


def check(record_phone):              # Check if there is phone already stored in agenda  #
    data = sqlite3.connect('book_phone.db')
    c = data.cursor()
    c.execute("SELECT * FROM Register")

    v_records = c.fetchall()

    ok = 0
    for rec in v_records:
        if record_phone == str(rec[3]):
            ok = 1
            break
        else:
            ok = 0

    data.close()

    return ok


def edit():

    record_phone = select_phone_box.get()  ### HERE we are getting the value from the text_box , and save it into qa variable. ###

    def save():
        data = sqlite3.connect('book_phone.db')
        curs = data.cursor()
        curs.execute("""UPDATE Register SET
                First_Name= :first,
                Last_Name= :last,
                E_mail= :mail,
                Phone= :phone
                            
                WHERE oid= :oid""",
                {
                    'first': f_name_box_editor.get(),
                    'last': l_name_box_editor.get(),
                    'mail': mail_box_editor.get(),
                    'phone': phone_box_editor.get(),
                    'oid': record_phone
                })
        curs.execute("SELECT * FROM Register Where oid =" + record_phone)
        v_records = curs.fetchall()
        data.commit()

        data.close()


        #Destroy the window after change
        editer.destroy()

    verify_existent_phone = check(record_phone)

    if len(record_phone) < 4:
        messagebox.showinfo("INFO", "Please insert phone number.")
    elif verify_existent_phone == 0:
        messagebox.showerror("ERROR", "This phone number does not exist! Please add!")
    elif len(record_phone) > 11:
        messagebox.showinfo("INFO", "Phone number must have 10 characters!")
    else:
        editer = Tk()
        editer.title("Edit existent contact")
        editer.geometry("300x400")

        # create a databases or connect to one
        data1 = sqlite3.connect('book_phone.db')
        # create cursor
        c = data1.cursor()
        c.execute("SELECT * FROM Register Where oid =" + record_phone)
        records = c.fetchall()

        # Create Labels
        f_name_editor = Label(editer, text="First Name")
        f_name_editor.grid(row=0, column=0)
        l_name_editor = Label(editer, text="Last Name")
        l_name_editor.grid(row=1, column=0)
        mail_editor = Label(editer, text="E-mail")
        mail_editor.grid(row=2, column=0)
        phone_editor = Label(editer, text="Phone")
        phone_editor.grid(row=3, column=0)


        # Create Text Box
        f_name_box_editor = Entry(editer, width=35)
        f_name_box_editor.grid(row=0, column=1)
        l_name_box_editor = Entry(editer, width=35)
        l_name_box_editor.grid(row=1, column=1)
        mail_box_editor = Entry(editer, width=35)
        mail_box_editor.grid(row=2, column=1)
        phone_box_editor = Entry(editer, width=35)
        phone_box_editor.grid(row=3, column=1)

        # save button AND cancel button
        save_btn = Button(editer, text="Save", command=save)
        save_btn.grid(row=4, column=1, pady=5, ipadx=99)

        for record in records:
            f_name_box_editor.insert(0, record[0])
            l_name_box_editor.insert(0, record[1])
            mail_box_editor.insert(0, record[2])
            phone_box_editor.insert(0, record[3])

        data1.commit()
        data1.close()

        editer.mainloop()


 # Create show_list button
show_button = Button(root, text="Show List", command=show, pady=6, padx=147, bd=4)
show_button.grid(row=0, column=0, columnspan=2)


#Create add_button AND delete_button
add_btn = Button(root, text="Add", command=add, bd=4, padx=11, pady=2)
add_btn.grid(row=3, column=1, ipadx=58)

del_btn = Button(root, text="Delete", command=delete, bd=4, padx=11, pady=2)
del_btn.grid(row=3, column=0, ipadx=58)

select_phone = Label(root, text="Phone Number(RO)", bg="yellow", width=25)
select_phone.grid(row=4, column=0)

select_phone_box = Entry(root, width=29, bg="yellow")
select_phone_box.insert(END, '4')
select_phone_box.grid(row=4, column=1, pady=1.9)

edit_button = ttk.Button(root, text="Edit a contact", command=edit)
edit_button.grid(row=5, column=0, columnspan=2, ipadx=130, ipady=10, pady=2.5)


#Run the root
root.mainloop()
