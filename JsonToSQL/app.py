import json
import os.path
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog as fd
from tkinter import messagebox


# gen script
def gen_script(param_directory, param_table_name):
    newFileName = param_table_name + ".sql"
    list_query = []
    with open(param_directory) as json_file:
        data = json.load(json_file)  # import to list of object
        count_row = len(data)
        for row in range(0, count_row):
            column_name = str(list(data[row].keys())).replace("'", "").replace('[', '').replace(']', '')
            data_value = str(list(data[row].values())).replace("None", "NULL").replace('[', '').replace(']', '')
            query_string = f"INSERT INTO public.{param_table_name}({column_name}) VALUES ({data_value});\n"
            list_query.append(query_string)
    
    # write file
    f = open(newFileName, "w")
    for _list in list_query:
        f.write(_list)
    f.close()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # global variable
        global dir, table_name
        dir = StringVar()
        table_name = StringVar()
        # set up title
        self.title("Hihi's app")
        self.geometry('500x60')
        self.resizable(0, 0)
        self.setup_title()
        # configure the grid
        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=5)
        
        self.button_open_file()
        self.button_gen_script()
    
    # setup title
    def setup_title(self):
        self.label = ttk.Label(self, width = 20, text='Input table name:', font=("Arial")).grid(column=0, row=0) 
        self.input_txt = ttk.Entry(self, width=40, textvariable=table_name).grid(column=1, row=0)
        table_name.set(self.input_txt)
    
    # setup file explorer dialog
    def file_explorer_popup(self):
        self.open_file = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=(('Json file', '*.json'), ('All file', '*.*')), typevariable=dir)
        dir.set(self.open_file)
    
    # execution script
    def button_gen_script(self):
        self.button_gen = ttk.Button(self, text="Generate script", command=self.final_execution).grid(column=3, row=1)
    
    # button open file explorer dialog
    def button_open_file(self):
        self.open_file_button = ttk.Button(self, text="Choose file", command=self.file_explorer_popup).grid(column=3,row=0)
    
    # run function with param
    def final_execution(self):
        if len(dir.get()) == 0 or len(table_name.get()) == 0 or table_name.get().lower() == "none":
            messagebox.showerror(title="Error", message="Empty directory or table name")
        # check exist and overwrite
        is_exist = os.path.exists(f"{table_name.get()}.sql")

        if is_exist == True:
            is_overwrite = messagebox.askyesno(title="Overwrite file?", message="File is already exist, want to overwrite it?")
            if is_overwrite == False:
                messagebox.showwarning(title="Cancel overwrite", message="Exit program!")
                self.destroy()
            else:
                gen_script(dir.get(), table_name.get())
                messagebox.showinfo(title="Success", message="Generate success")
                self.destroy()
        else:
            gen_script(dir.get(), table_name.get())
            messagebox.showinfo(title="Success", message="Generate success")
            self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
