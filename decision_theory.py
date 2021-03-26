from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox


root = Tk()                                              # Kreira glavni prozor sa nazivom root
root.title("Izbor u uslovima neizvesnosti")                            # Naslov glavnog prozora
root.geometry('747x527+200+10')                          # Dimenzija glavnog prozora
root.configure(background='mediumturquoise')             # Boja pozadine

global entries,matrix,text_var
text_var=[]
global c_rang_max,c_rang_min,c_rang_hur,c_rang_sav,c_rang_lap
c_rang_max,c_rang_min,c_rang_hur,c_rang_sav,c_rang_lap=0,0,0,0,0

global uspesno
uspesno=0


class DMMButton(Button):
    def __init__(self, master,**kw):
        Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = 'aquamarine'

    def on_leave(self, e):
        self['background'] = self.defaultBackground



def open_file_temp():
    try:
        f=open("help.txt", "r")
        text.delete(0.0, END)
        podatak_2=f.read()
        text.tag_config('b', font=('Arial', 10, 'bold', 'italic'))
        text.insert(INSERT, podatak_2, 'b')
        f.close()
    except FileNotFoundError:
        text.delete(0.0, END)
        text.insert(0.0, "Ne postoji datoteka pod tim imenom.")
    except (IndexError,ValueError):
        podatak = "Loši podaci."
        messagebox.showinfo('Obavestenje',podatak)



def file_mat():
    global rows,cols,alpha
    
    if E1.get()=='':
        rows=0
    else:
        rows= int(E1.get())
    
    if E2.get()=='':
        cols=0
    else:
        cols = int(E2.get())
    if Enalfa.get()=='':
        alpha=-1
    else:
        alpha = float(Enalfa.get())
        
    if rows<1 or cols<1 or alpha <0 or alpha>1 :
        reset()
        messagebox.showinfo('Obavestenje','Dimenzije moraju biti brojevi veci od 0, indeks optimizma mora biti broj izmedju 0 i 1.')
  
    else:
        global uspesno
        uspesno=0
        entries=[]
        global main_frame
        main_frame.destroy()
        main_frame= Frame(tab1)
        main_frame.grid()
        
        l2 = Label(main_frame, text="Unesi vrednosti:",bg='cadet blue', font=('arial', 10, 'bold'))
        l2.grid()


        x2 = 0
        y2 = 0
        m=0
        global file_name
        f=open(file_name,'r')
        data=f.readlines()[1:]
        
        for i,line in enumerate(data):
            if i ==0:
                for j in range(cols):
                    Label(main_frame,text='S{}'.format(j+1)).grid(row=4,column=1+j)

            text_var.append([])
            entries.append([])
            frow=line.split(',')
            Label(main_frame,text='A{}'.format(i+1)).grid(row=5+x2)

            for j in range(len(frow)):
                if(frow[j]!="\t?" and frow[j]!="\tCode" and frow[j] !="\n"):
                    
                    text_var[i].append(StringVar())
                    entries[i].append(Entry(main_frame, textvariable=text_var[i][j],width=3))
                    entries[i][j].grid(row=5 + x2, column=1 + y2)
                    entries[i][j].insert(INSERT,int(frow[j]))
               
                y2 += 1
                m=max(y2,m)           

            y2=0
            x2+=1
        f.close()

        button= DMMButton(main_frame,text="Potvrdi", bg='cadet blue', width=15, command=methods)
        button.grid(row =x2+6,column=m+1)
        resetbutton = DMMButton(main_frame,text="Ponovi", bg='cadet blue', width=15, command=reset)
        resetbutton.grid(row=x2+6,column=m+2)


def ucitaj():
    try:
        global file_name
        file_name = fd.askopenfilename()
        f=open(file_name, "r")
        E1.delete(0, END)
        E2.delete(0,END)
        Enalfa.delete(0,END)
        dim=f.readline()

        frow = dim.split(',')
        if (frow[0]!="\t?" and frow[0]!="\tCode" and frow[1]!="\t?" and frow[1]!="\tCode"  and frow[2]!="\t?" and frow[2]!="\tCode"):
            E1.insert(INSERT, int(frow[0]))
            E2.insert(INSERT, int(frow[1]))
            Enalfa.insert(INSERT,float(frow[2]))
        f.close()

    except FileNotFoundError:

        podatak = "Niste izabrali datoteku za učitavanje podataka."
        messagebox.showinfo('Obavestenje',podatak)

    except (IndexError,ValueError):
        podatak = "Loši podaci."
        messagebox.showinfo('Obavestenje',podatak)


    else:
        file_mat()

    



# Korisnicka f-ja za zatvaranje i sacuvavanje sadrzaja datoteke 
def sacuvaj(j):
    try:
        file_name1 = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),("HTML files", "*.html;*.htm"),
                                                ("All files", "*.*") ))
        f=open(file_name1, "w")
        if j !=5:
            for i in range(rows):
   
                line= 'A{} '.format(i+1) + str(rang_all[i][j])+'\n'
                f.writelines(line)
        else:
            for i in range(rows):
                
                line= 'A{} '.format(i+1) + str(rang_all[i])+'\n'
                f.writelines(line)
        f.close()
        messagebox.showinfo("Obaveštenje","Podaci su sačuvani.")
    except FileNotFoundError:
        messagebox.showinfo("Obaveštenje","Niste sačuvali podatke.")



def start():
    global E1,E2,Enalfa
    global main_frame
    main_frame.destroy()
    main_frame = Frame(tab1)
    main_frame.grid()
    
    L1 = Label(main_frame, text="Red:")
    L1.grid(row=0,column=0)
    L2 = Label(main_frame, text="Kolona:")
    L2.grid(row=1,column=0)

    E1 = Entry(main_frame, bg='cadet blue')
    E1.grid(row=0,column=1)
    E2 = Entry(main_frame, bg='cadet blue')
    E2.grid(row=1,column=1)

    Label(main_frame, text="Unesi indeks optimizma:").grid()
    Enalfa=Entry(main_frame, bg='cadet blue')
    Enalfa.grid(row=2,column=1)

    button = DMMButton(main_frame, text="Potvrdi", command = mat_dim)
    button.grid(row=2,column=3)
    button2= DMMButton(main_frame, text='Ucitaj', command = ucitaj)
    button2.grid(row=0,column=3)


def reset():
    mat_frame.destroy()    
    text_var.clear()
    global c_rang_max,c_rang_min,c_rang_hur,c_rang_sav,c_rang_lap
    c_rang_max,c_rang_min,c_rang_hur,c_rang_sav,c_rang_lap=0,0,0,0,0
    global rang_all
    rang_all=[[0 for j in range(5)]for i in range(rows)]
    
    tbmax.configure(state='normal')
    tbmax.delete(1.0,END)
    tbmax.configure(state='disabled')

    tbmin.configure(state='normal')
    tbmin.delete(1.0,END)
    tbmin.configure(state='disabled')

    tbhur.configure(state='normal')
    tbhur.delete(1.0,END)
    tbhur.configure(state='disabled')

    tbsav.configure(state='normal')
    tbsav.delete(1.0,END)
    tbsav.configure(state='disabled')

    tblap.configure(state='normal')
    tblap.delete(1.0,END)
    tblap.configure(state='disabled')

    savemax.configure(state='disabled')
    savemin.configure(state='disabled')
    savehur.configure(state='disabled')
    savesav.configure(state='disabled')
    savelap.configure(state='disabled')

    bsave.configure(state='disabled')


    start()


def mat_dim():
    global rows,cols,alpha
    
    if E1.get()=='':
        rows=0
    else:
        rows= int(E1.get())
    
    if E2.get()=='':
        cols=0
    else:
        cols = int(E2.get())
        
    if Enalfa.get()=='':
        alpha=-1
    else:
        alpha = float(Enalfa.get())
        
    if rows<1 or cols<1 or alpha <0 or alpha>1 :
        reset()
        messagebox.showinfo('Obavestenje','Dimenzije moraju biti brojevi veci od 0')
    else:
        global uspesno
        uspesno=0
        entries=[]
        global main_frame
        main_frame.destroy()
        main_frame= Frame(tab1)
        main_frame.grid()
        
        l2 = Label(main_frame, text="Unesi vrednosti:",bg='cadet blue', font=('arial', 10, 'bold'))
        l2.grid()

        x2 = 0
        y2 = 0
        m=0
        
        for i in range(rows):
            # append an empty list to your two arrays
            # so you can append to those later
            if i==0:
                for j in range(cols):
                    Label(main_frame,text='S{}'.format(j+1)).grid(row=4,column=1+j)
            text_var.append([])
            entries.append([])
            Label(main_frame,text='A{}'.format(i+1)).grid(row=5+x2)
            for j in range(cols):
                # append your StringVar and Entry
                text_var[i].append(StringVar())
                entries[i].append(Entry(main_frame, textvariable=text_var[i][j],width=3))
                entries[i][j].grid(row=5 + x2, column= 1+y2)
               
                y2 += 1
                m=max(y2,m)           

            y2=0
            x2+=1

        button= DMMButton(main_frame,text="Potvrdi", bg='cadet blue', width=15, command=methods)
        button.grid(row =x2+6,column=m+1)
        resetbutton = DMMButton(main_frame,text="Ponovi", bg='cadet blue', width=15, command=reset)
        resetbutton.grid(row=x2+6,column=m+2)


def mat_view(fun_tab,matrix):
    global rows,cols
    global mat_frame
    mat_frame.destroy()
    entries=[]
    mat_frame= Frame(fun_tab)
    mat_frame.grid()    
    x2 = 0
    y2 = 0
    m=0
    
    for i in range(rows):
        if i==0:
            for j in range(cols):
                Label(mat_frame,text='S{}'.format(j+1)).grid(row=4,column=2+j)
        # append an empty list to your two arrays
        # so you can append to those later
        Label(mat_frame,text='A{}'.format(i+1)).grid(row=5+x2)
        entries.append([])
        for j in range(cols):
            # append your StringVar and Entry
            entries[i].append(Entry(mat_frame,width=3))
            entries[i][j].grid(row=5 + x2, column=2 + y2)
            entries[i][j].insert(INSERT,str(matrix[i][j]))
            y2 += 1

        y2=0
        x2+=1


def rang_met(rang_list):

    global rows,cols
    x2 = 0
    y2 = 0
    r_list = []
    Label(mat_frame,text='Rang').grid(row=4,column=cols+2+y2)
    
    for i in range(rows):
        r_list.append([])

        for j in range(1):
            r_list[i].append(Entry(mat_frame,width=3))
            r_list[i][j].grid(row=5+x2, column=cols+y2+2)
            r_list[i][j].insert(INSERT,str(rang_list[i]))
            y2 += 1

        y2=0
        x2+=1

def rang_tot(rang_max,m):
    for j in range(rows):
        rang_all[j][m]+=rang_max[j]
        


def maximax():
    if uspesno==0:
        messagebox.showinfo('Obavestenje', 'Potvrdi unos podataka.')
    else:
        matrix = get_matrix()
        maxrix=[]
        c=0
        minind=[]
        mat_view(tab2,matrix)
        rang_max={}
        rang=rows
        c_max=0
        global c_rang_max
                                
        for i in range(rows):
            matrix[i].sort()

        maxval=matrix[0][-1]

        
        while True:
            c+=1
            maxrix=[]
            for i in range(rows):
                maxrix.append(matrix[i][-1])
                if matrix[i][-1] > maxval:
                    maxval=matrix[i][-1]
                              
            
            for i in range(rows):
                if i not in minind and maxrix[i]!=maxval:
                    minind.append(i)
                    
            a = rows- len(minind)
            m=0
            minmaxr= sorted(maxrix)
            while len(minind)>len(rang_max):
                for index in minind:
                    if index not in rang_max and maxrix[index]==minmaxr[m]:
                        rang_max[index]= rang
                        c_max+=1
                
                rang = rang-c_max
                c_max=0
                m+=1
                
            tbmax.configure(state='normal')
            savemax.configure(state='normal')
            tbmax.delete(1.0,END)
            if a> 1 and c<cols:
                              
                for i in range(rows):
                    matrix[i].pop()
                              
                maxval=float('-inf')
                    
            elif a ==1:
                rowlist= [i for i in range(rows)]
                maxind = list(set(rowlist)-set(minind))
                best=maxind[0]+1
                for index in maxind:
                    rang_max[index]= 1

                tbmax.insert(1.0,"Najbolja akcija po maximax metodi je {}".format(best))
                tbmax.configure(state='disabled')
                rang_met(rang_max)
                c_rang_max+=1
                if c_rang_max <2:
                    m=0
                    rang_tot(rang_max,m)

                matrix.clear()
                break

            else:
                rowlist= [i for i in range(rows)]
                maxind = list(set(rowlist)-set(minind))
                tbmax.insert(1.0,"Najbolje akcije po maximax metodi su ")
                for i,index in enumerate(maxind):
                    rang_max[index]= 1
                    best= maxind[i]+1
                    tbmax.insert(END,'{} '.format(best))

                tbmax.configure(state='disabled')
                rang_met(rang_max)
                c_rang_max+=1
                if c_rang_max <2:
                    m=0
                    rang_tot(rang_max,m)
                matrix.clear()
                break
         
 
def maximin():
    if uspesno==0:
        messagebox.showinfo('Obavestenje', 'Potvrdi unos podataka.')
    else:
        matrix = get_matrix()
        maxrix=[]

        c=0
        minind=[]
        mat_view(tab3,matrix)
        rang_max={}
        rang=rows
        c_max=0        
        global c_rang_min

        for i in range(rows):
            matrix[i].sort()

        maxval=matrix[0][0]

        
        while True:
            c+=1
            minrix=[]
            for i in range(rows):
                minrix.append(matrix[i][0])
                if i not in rang_max and matrix[i][0] > maxval:
                    maxval=matrix[i][0]

            for i in range(rows):
                if i not in minind and minrix[i]!=maxval:
                    minind.append(i)

            a = rows- len(minind)

            m=0
            minmaxr= sorted(minrix)
            while len(minind)>len(rang_max):
                for index in minind:
                    if index not in rang_max and minrix[index]==minmaxr[m]:
                        rang_max[index]= rang
                        c_max+=1
                
                rang = rang-c_max
                c_max=0
                m+=1

                
            tbmin.configure(state='normal')
            tbmin.delete(1.0,END)
            savemin.configure(state='normal')

            if a> 1 and c<cols:
                              
                for i in range(rows):
                    matrix[i].pop(0)                      

                maxval=float('-inf')


            elif a <=1:
                
                rowlist= [i for i in range(rows)]
                maxind = list(set(rowlist)-set(minind))
                tbmin.insert(1.0,"Najbolja akcija po maximin metodi je {}".format(maxind[0]+1))
                tbmin.configure(state='disabled')
                rang_max[maxind[0]]=1
                rang_met(rang_max)
                c_rang_min+=1
                if c_rang_min <2:
                    m=1
                    rang_tot(rang_max,m)
                matrix.clear()
                break

            else:
                rowlist= [i for i in range(rows)]
                maxind = list(set(rowlist)-set(minind))
                tbmin.insert(1.0,"Najbolje akcije po maximin metodi su ")
                for i,index in enumerate(maxind):
                    rang_max[index]= 1
                    best= maxind[i]+1
                    tbmin.insert(END,'{} '.format(best))
                    
                tbmin.configure(state='disabled')
                rang_met(rang_max)
                c_rang_min+=1
                if c_rang_min <2:
                    m=1
                    rang_tot(rang_max,m)
                    
                matrix.clear()
                break

def hurwicz():
    if uspesno==0:
        messagebox.showinfo('Obavestenje', 'Potvrdi unos podataka.')
    else:
        global alpha
        matrix = get_matrix()
        revalpha= 1-alpha
        hurmatr=[]
        maxval=float('-inf')
        minind=[]    
        mat_view(tab4,matrix)
        rang_max={}
        rang=rows
        c_max=0
        global c_rang_hur

        for i in range(rows):
            matrix[i].sort()

        for i in range(rows):
            val=matrix[i][0] * revalpha + matrix[i][-1] * alpha
            hurmatr.append(val)
            if val >maxval:
                maxval=val

        for i in range(rows):
            if hurmatr[i]!=maxval:
                minind.append(i)
                
        a = rows- len(minind)
        m=0
        minmaxr= sorted(hurmatr)
        while len(minind)>len(rang_max):
            for index in minind:
                if index not in rang_max and hurmatr[index]==minmaxr[m]:
                    rang_max[index]= rang
                    c_max+=1
                
            rang = rang-c_max
            c_max=0
            m+=1

        tbhur.configure(state='normal')
        tbhur.delete(1.0,END)
        savehur.configure(state='normal')
           
        if a ==1:
            rowlist= [i for i in range(rows)]
            maxind = list(set(rowlist)-set(minind))
            best=maxind[0]+1
            for index in maxind:
                rang_max[index]= 1
            tbhur.insert(1.0,"Najbolja akcija po Hurvicovoj metodi je {}".format(best))
            tbhur.configure(state='disabled')
            c_rang_hur+=1
            
            if c_rang_hur <2:
                m=2
                rang_tot(rang_max,m)
            rang_met(rang_max)
            matrix.clear()

        else:
            rowlist= [i for i in range(rows)]
            maxind = list(set(rowlist)-set(minind))
            tbhur.insert(1.0,"Najbolje akcije po Hurvicovoj metodi su ")
            for i,index in enumerate(maxind):
                rang_max[index]= 1
                best= maxind[i]+1
                tbhur.insert(END,'{} '.format(best))               

            tbhur.configure(state='disabled')
            c_rang_hur+=1
            if c_rang_hur <2:
                m=2
                rang_tot(rang_max,m)

            rang_met(rang_max)
            matrix.clear()


def savage():
    if uspesno==0:
        messagebox.showinfo('Obavestenje', 'Potvrdi unos podataka.')
    else:
        matrix = get_matrix()
        matrix1= matrix
        c=0
        minind=[]
        helplist = []
        mat_view(tab5,matrix)
        rang_max={}
        rang=rows
        c_max=0
        global c_rang_sav



        for col in range(cols):
            maxval= matrix1[0][col]
            for row in range(1,rows):
                maxval = max(maxval,matrix1[row][col])
            helplist.append(maxval)

        for col in range(cols):
            for row in range(rows):
                matrix[row][col]=helplist[col]-matrix1[row][col]
        for i in range(rows):
            matrix[i].sort()

        savesav.configure(state='normal')

        while True:
            minval=float('inf')
            c+=1
            maxrix=[]
            
            for i in range(rows):
                maxrix.append(matrix[i][-1])
                if matrix[i][-1] < minval:
                    minval=matrix[i][-1]

            
            for i in range(rows):
                if i not in minind and maxrix[i]!=minval:
                    minind.append(i)
                    
            a = rows- len(minind)

            m=0
            minmaxr= sorted(maxrix,reverse=True)
            while len(minind)>len(rang_max):
                for index in minind:
                    if index not in rang_max and maxrix[index]==minmaxr[m]:
                        rang_max[index]= rang
                        c_max+=1
                
                rang = rang-c_max
                c_max=0
                m+=1

            
            tbsav.configure(state='normal')
            tbsav.delete(1.0,END)

            if a>1 and c<cols:
                for i in range(rows):
                    matrix[i].pop()
                              
                maxval=float('-inf')
           
            elif a ==1:
                rowlist= [i for i in range(rows)]
                maxind = list(set(rowlist)-set(minind))
                for index in maxind:
                    rang_max[index]= 1
                best=maxind[0]+1
                tbsav.insert(1.0,"Najbolja akcija po Sevidžovoj metodi je {}".format(best))
                tbsav.configure(state='disabled')
                rang_met(rang_max)
                c_rang_sav+=1
                if c_rang_sav <2:
                    m=3
                    rang_tot(rang_max,m)
                matrix.clear()
                break

            else:
                rowlist= [i for i in range(rows)]
                maxind = list(set(rowlist)-set(minind))
                tbsav.insert(1.0,"Najbolje akcije po Sevidžovoj metodi su ")
                for i,index in enumerate(maxind):
                    rang_max[index]= 1
                    best= maxind[i]+1
                    tbsav.insert(END,'{} '.format(best))                

                rang_met(rang_max)
                c_rang_sav+=1
                if c_rang_sav <2:
                    m=3
                    rang_tot(rang_max,m)
                tbsav.configure(state='disabled')
                matrix.clear()
                break


def laplace():
    if uspesno==0:
        messagebox.showinfo('Obavestenje', 'Potvrdi unos podataka.')
    else:
        matrix = get_matrix()
        Lalpha= 1/rows
        lapmatr=[]
        maxval=float('-inf')
        minind=[]
        mat_view(tab6,matrix)
        rang_max={}
        rang=rows
        c_max=0
        global c_rang_lap
        
        for i in range(rows):
            matrix[i].sort()

        for i in range(rows):
            val=0

            for j in range(cols):
                val+=matrix[i][j] * Lalpha
            lapmatr.append(val)
            if val > maxval:
                maxval=val

        for i in range(rows):
            if lapmatr[i]!=maxval:
                minind.append(i)

        a = rows- len(minind)

        m=0
        minmaxr= sorted(lapmatr)
        while len(minind)>len(rang_max):
            for index in minind:
                if index not in rang_max and lapmatr[index]==minmaxr[m]:
                    rang_max[index]= rang
                    c_max+=1
                
            rang = rang-c_max
            c_max=0
            m+=1

            
        tblap.configure(state='normal')
        tblap.delete(1.0,END)
        savelap.configure(state='normal')
        
        if a==1:
                
            rowlist= [i for i in range(rows)]
            maxind = list(set(rowlist)-set(minind))

            for index in maxind:
                rang_max[index]= 1

            best=maxind[0]+1
            tblap.insert(1.0,"Najbolja akcija po Laplasovoj metodi je {}".format(best))
            tblap.configure(state='disabled')
            rang_met(rang_max)
            c_rang_lap+=1
            if c_rang_lap <2:
                m=4
                rang_tot(rang_max,m)
            matrix.clear()

        elif a>1:
                
            rowlist= [i for i in range(rows)]
            maxind = list(set(rowlist)-set(minind))
            
            tblap.insert(1.0,"Najbolje akcije po Laplasovoj metodi su ")
            for i,index in enumerate(maxind):
                rang_max[index]= 1
                best= maxind[i]+1
                tblap.insert(END,'{} '.format(best))                

            tblap.configure(state='disabled')
            c_rang_lap+=1
            if c_rang_lap <2:
                m=4
                rang_tot(rang_max,m)
                
            rang_met(rang_max)
            matrix.clear()


def get_matrix():
    matrix=[]
    global text_var
    
    for i in range(rows):
        matrix.append([])
        for j in range(cols):
            matrix[i].append(int(text_var[i][j].get()))
    return matrix

        
def methods():   
    try:
        matrix=[]
        global text_var
        
        for i in range(rows):
            matrix.append([])
            for j in range(cols):
                matrix[i].append(int(text_var[i][j].get()))
    except (ValueError, IndexError):
        messagebox.showinfo('Obavestenje','Unete vrednosti moraju biti brojevi.')
        reset()

    else:
        
        messagebox.showinfo('Obavestenje','Uspesno uneti podaci. Izaberi metodu.')
        global rang_all
        rang_all=[[0 for j in range(5)]for i in range(rows)]
        global uspesno
        uspesno=1


def final():
    global rows,cols

    if uspesno==0:
        messagebox.showinfo('Obavestenje', 'Potvrdi unos podataka.')
    else:
        bsave.configure(state='normal')
        global mat_frame
        mat_frame.destroy()
        entries=[]
        mat_frame= Frame(tab7)
        mat_frame.grid()
        
        x2 = 0
        y2 = 0
        ei=0
        ej=0
        xmeth=0
        methods_list=['Maximax','Maximin','Hurwicz','Savage','Laplace']
        for i in range(rows):
            if i==0:
                for j in range(5):
                    if rang_all[i][j]!=0:
                        Label(mat_frame,text='{}'.format(methods_list[j])).grid(row=4,column=2+xmeth)
                        xmeth+=1
            # append an empty list to your two arrays
            # so you can append to those later
            Label(mat_frame,text='A{}'.format(i+1)).grid(row=5+x2)
            entries.append([])
            for j in range(5):
                # append your StringVar and Entry
                if rang_all[i][j]!=0:

                    entries[ei].append(Entry(mat_frame,width=3))
                    entries[ei][ej].grid(row=5 + x2, column=2 + y2)
                    entries[ei][ej].insert(INSERT,str(rang_all[i][j]))
                    y2 += 1
                    ej+=1
            ei+=1
            ej=0


            y2=0
            x2+=1

          
#**********************************************************************************************
#***  GLVNI DEO PROGRAMA ***
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1,fill='both')
global main_frame
    
    # === Kreiramo prozore(tabove) i dodeljuemo im imena
tab1 = Frame(tab_control,bg='cadet blue')
tab_control.add(tab1, text='Unos podataka')

tab2 = Frame(tab_control,bg='cadet blue')
tab_control.add(tab2, text='Maximax')
bmax= DMMButton(tab2,text='Izracunaj',command= maximax)
bmax.grid()
savemax=DMMButton(tab2,text='Sacuvaj podatke',command= lambda: sacuvaj(0),state = 'disabled')
savemax.grid(row=0,column=1)
global tbmax
tbmax= Text(tab2,height=1,width=50)
tbmax.grid(pady=10,row=1)


tab3 = Frame(tab_control,bg='cadet blue')
tab_control.add(tab3, text='Maximin')
bmin= DMMButton(tab3,text='Izracunaj',command =maximin)
bmin.grid()
savemin=DMMButton(tab3,text='Sacuvaj podatke',command= lambda: sacuvaj(1),state = 'disabled')
savemin.grid(row=0,column=1)
global tbmin
tbmin= Text(tab3,height=1,width=50)
tbmin.grid(pady=10,row=1)

tab4 = Frame(tab_control,bg='cadet blue')
tab_control.add(tab4, text='Hurwicz')
bhur= DMMButton(tab4,text='Izracunaj',command= hurwicz)
bhur.grid()
savehur=DMMButton(tab4,text='Sacuvaj podatke',command= lambda: sacuvaj(2),state = 'disabled')
savehur.grid(row=0,column=1)
global tbhur
tbhur = Text(tab4,height=1,width=50)
tbhur.grid(pady=10,row=1)

tab5 = Frame(tab_control,bg='cadet blue')
tab_control.add(tab5, text='Savage')
bsav= DMMButton(tab5,text='Izracunaj',command= savage)
bsav.grid()
savesav=DMMButton(tab5,text='Sacuvaj podatke',command= lambda: sacuvaj(3),state = 'disabled')
savesav.grid(row=0,column=1)
global tbsav
tbsav = Text(tab5,height=1,width=50)
tbsav.grid(pady=10,row=1)

tab6 = Frame(tab_control,bg='cadet blue')
tab_control.add(tab6, text='Laplace')
blap= DMMButton(tab6,text='Izracunaj',command=laplace)
blap.grid()
savelap=DMMButton(tab6,text='Sacuvaj podatke',command= lambda: sacuvaj(4),state = 'disabled')
savelap.grid(row=0,column=1)
global tblap
tblap = Text(tab6,height=1,width=50)
tblap.grid(pady=10,row=1)

tab7= Frame(tab_control, bg='cadet blue')
tab_control.add(tab7,text='Rangiranje')
brang=DMMButton(tab7,text='Prikazi rang',command= final)
brang.grid()
bsave=DMMButton(tab7,text='Sacuvaj podatke',command= lambda: sacuvaj(5),state='disabled')
bsave.grid(row=0,column=1)

tab8=Frame(tab_control,bg='cadet blue')
tab_control.add(tab8,text='Pomoc')
text=Text(tab8, width=80, height=30, wrap=WORD, bg='#FFFFE0')
text.grid()


main_frame = Frame(tab1)
main_frame.grid()
global mat_frame
mat_frame= Frame()
open_file_temp()
start()


# === Pokretanje GUI prozora
root.mainloop()
