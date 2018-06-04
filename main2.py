import tkinter
import glob

# for imbedding matplotlib plot
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pylab import *

import meth2

calibrea = "./calibration spectra/*"
coefficient = "./coefficients/"

class App:
    def __init__(self, master, calibrea, files = []):

        master.configure(background = "white", padx = 10, pady = 10)
        global max_val
        max_val = 6

        # Initialise frames ----------------------------------------------------

        energy_dict = {
                "Ba-133 30 keV" : "30.625",
                "Ba-133 35 keV" : "35.818",
                "Eu-152 40 keV" : "40.118",
                "Eu-152 45 keV" : "45.414",
                "Ba-133 80 keV" : "80.9971",
                "Eu-152 122 keV" : "121.7817",
                "Eu-152 344 keV" : "344.2785",
                "Eu-152 411 keV" : "411.1163",
                "Eu-152 443 keV" : "443.965",
                "Cs-137 662 keV" : "661.657",
                "Eu-152 779 keV" : "778.9040",
                "Eu-152 964 keV" : "964.079",
                "Eu-152 1085 keV" : "1085.869",
                "Eu-152 1112 keV" : "1112.074",
                "Eu-152 1408 keV" : "1408.006"
            }

        # max values here
        max_1 = tkinter.Entry(master, fg = "purple", justify = "center")
        max_1.insert(tkinter.END, "")
        max_1.grid(row = 7, column = 7)

        max_2 = tkinter.Entry(master, fg = "purple", justify = "center")
        max_2.insert(tkinter.END, "")
        max_2.grid(row = 8, column = 7)

        max_3 = tkinter.Entry(master, fg = "purple", justify = "center")
        max_3.insert(tkinter.END, "")
        max_3.grid(row = 9, column = 7)

        max_4 = tkinter.Entry(master, fg = "purple", justify = "center")
        max_4.insert(tkinter.END, "")
        max_4.grid(row = 10, column = 7)

        max_5 = tkinter.Entry(master, fg = "purple", justify = "center")
        max_5.insert(tkinter.END, "")
        max_5.grid(row = 11, column = 7)

        energy_1 = tkinter.StringVar()
        energy_1.set('                        ') # this determines the width of frame_4
        option1 = tkinter.OptionMenu(master, energy_1, *energy_dict.keys())
        option1.grid(row = 7, column = 8)

        energy_2 = tkinter.StringVar()
        energy_2.set('                        ')
        option2 = tkinter.OptionMenu(master, energy_2, *energy_dict.keys())
        option2.grid(row = 8, column = 8)

        energy_3 = tkinter.StringVar()
        energy_3.set('                        ')
        option3 = tkinter.OptionMenu(master, energy_3, *energy_dict.keys())
        option3.grid(row = 9, column = 8)

        energy_4 = tkinter.StringVar()
        energy_4.set('                        ')
        option4 = tkinter.OptionMenu(master, energy_4, *energy_dict.keys())
        option4.grid(row = 10, column = 8)

        energy_5 = tkinter.StringVar()
        energy_5.set('                        ')
        option5 = tkinter.OptionMenu(master, energy_5, *energy_dict.keys())
        option5.grid(row = 11, column = 8)

        self.calculateButton = tkinter.Button(master, text = 'add to file',
                                 command = lambda: meth2.add_to_file(self,
                                                                     max_1,
                                                                     max_2,
                                                                     max_3,
                                                                     max_4,
                                                                     max_5,
                                                                     energy_1,
                                                                     energy_2,
                                                                     energy_3,
                                                                     energy_4,
                                                                     energy_5,
                                                                     energy_dict,
                                                                     coefficient)) # resfresh if files are added or removed
        self.calculateButton.grid(row = 12, column = 7, columnspan = 2)

        # ----------------------------------------------------------------------

        # Middle plot panel ----------------------------------------------------

        f = Figure(figsize = (5, 5), dpi = 120) # initial spectra
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[0,0,0,0,0,0,0,0], '#6B1AD3')
        a.text(2.5,0.01,"click a file to open the spectrum")
        a.axis('off')
        canvas = FigureCanvasTkAgg(f, master) # add figure to canvas
        canvas.get_tk_widget().grid(row = 0, column = 3, rowspan = 34) # add canvas to app

        # ----------------------------------------------------------------------

        # left-most panel ------------------------------------------------------

        self.refreshButton = tkinter.Button(master,
                                            text = 'refresh',
                                            command = lambda: meth2.refreshList(self, calibrea)) # resfresh if files are added or removed
        self.refreshButton.grid(row = 0, column = 0)

        self.listbox = tkinter.Listbox(master, height = 34)
        self.listbox.grid(row = 1, column = 0, rowspan = 34)

        scrollbar = tkinter.Scrollbar(command = self.listbox.yview, orient = tkinter.VERTICAL)
        scrollbar.grid(row = 1, column = 1, rowspan = 34, sticky = 'ns')
        self.listbox.configure(yscrollcommand = scrollbar.set)

        self.listbox.bind("<Double-Button-1>",
                          lambda event: meth2.plot_update(event,
                                                          self,
                                                          canvas,
                                                          a,
                                                          f,
                                                          max_1,
                                                          max_2,
                                                          max_3,
                                                          max_4,
                                                          max_5,
                                                          energy_1,
                                                          energy_2,
                                                          energy_3,
                                                          energy_4,
                                                          energy_5))
        self.placeButtons(files)

        # ----------------------------------------------------------------------

   # adds buttons to listbox in alphabetical then numerical order
    def placeButtons(self, fileNames):
        mwd_files = [s for s in fileNames if 'mwd' in s]
        bld_files = [s for s in fileNames if 'bld' in s]
        mwd_scat = [s for s in mwd_files if 'scat' in s]
        mwd_abs = [s for s in mwd_files if 'abs' in s]
        bld_scat = [s for s in bld_files if 'scat' in s]
        bld_abs = [s for s in bld_files if 'abs' in s]
        mwd_scat.sort(key = lambda x: int(x.rsplit('.')[2])) # rearranges files
        mwd_abs.sort(key = lambda x: int(x.rsplit('.')[2]))
        bld_scat.sort(key = lambda x: int(x.rsplit('.')[2]))
        bld_abs.sort(key = lambda x: int(x.rsplit('.')[2]))
        names = mwd_scat + mwd_abs + bld_scat + bld_abs
        for item in names:
            self.listbox.insert(tkinter.END,item.split('/')[2])

root = tkinter.Tk() # initialise new window
root.wm_title("Calibrater - Caffrey Version")

files = glob.glob(calibrea)
app = App(root, calibrea, files) # pass window to class

root.mainloop() #open window
def onClose():
    print('closed')
    root.destroy()
root.protocol("WM_DELETE_WINDOW", onClose)
root.destroy() # optional; close window
root.mainloop()
