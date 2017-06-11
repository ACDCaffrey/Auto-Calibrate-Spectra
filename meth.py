import glob
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.pyplot as plt
from matplotlib.widgets  import RectangleSelector
from pylab import *
import numpy as np

### refresh list if files are added or removed
def refreshList(self, calibrea):
    self.listbox.delete(0,END)
    files = glob.glob(calibrea)
    self.placeButtons(files)
    return self.listbox

# adds plot to canvas, sets event action on canvas, determines x-location of highest point
def plot_update(event, self, canvas, a, ff, max_1, max_2, max_3, max_4, max_5, energy_1, energy_2, energy_3, energy_4, energy_5):
    global ydata, max_val, current_val, point, selection
    p = "pie"
    max_1.delete(0, 'end') # clear the current values
    max_2.delete(0, 'end')
    max_3.delete(0, 'end')
    max_4.delete(0, 'end')
    max_5.delete(0, 'end')
    energy_1.set('                        ')
    energy_2.set('                        ')
    energy_3.set('                        ')
    energy_4.set('                        ')
    energy_5.set('                        ')
    max_val = 0 # open a new plot, set to zero
    widget = event.widget
    selection = widget.get(ACTIVE)
    with open("./calibration spectra/" + selection,'r') as f: # read in the data
        read_data = f.read()
        f.close()
    plt.clf()
    a.clear()
    a = ff.add_subplot(111)
    ydata = read_data.split()
    ydata = list(map(int, ydata))
    if "scat" in selection:
        if "24" not in selection:
            del ydata[2000:]
    if "abs" in selection:
        if "mwd" in selection:
            del ydata[4000:] # for absorber you need to increase height with energy
        if "bld" in selection:
            del ydata[2500:] # for absorber you need to increase height with energy
        b =  range(len(ydata))
        ydata = [x * 2*(1+y) for x, y in zip(ydata,b)] # zoom function is a bit off so I am mutating the data here
    xdata = range(len(ydata))
    a.plot(xdata,ydata,"#6B1AD3")
    point, = a.plot([],[], marker="o", color="black")
    toggle_selector.RS = RectangleSelector(a, lambda eclick, erelease: on_select(eclick, erelease, max_1, max_2, max_3, max_4, max_5, point),  drawtype='box',
            rectprops = dict(facecolor='#C49CF7', edgecolor = 'black', alpha=0.2, fill=True))
    connect('key_press_event', toggle_selector)
    canvas.draw() # keeps canvas open

def on_select(eclick, erelease, max_1, max_2, max_3, max_4, max_5, a):
    x_vals_min = eclick.xdata
    x_vals_max = erelease.xdata
    if x_vals_min < 1:
        x_vals_min = 0
    highest_val = max(ydata[int(x_vals_min):int(x_vals_max)])
    max_val = ydata[int(x_vals_min):int(x_vals_max)].index(highest_val) + int(x_vals_min)# alter me
    point.set_data([max_val, highest_val])
    if (max_1.get() != "" and max_2.get() != "" and max_3.get() != "" and max_4.get() != "" and max_5.get() == ""):
        max_5.insert(END, max_val)
    if (max_1.get() != "" and max_2.get() != "" and max_3.get() != "" and max_4.get() == ""):
        max_4.insert(END, max_val)
    if (max_1.get() != "" and max_2.get() != "" and max_3.get() == ""):
        max_3.insert(END, max_val)
    if (max_1.get() != "" and max_2.get() == ""):
        max_2.insert(END, max_val)
    if max_1.get() == "":
        max_1.insert(END, max_val)

def toggle_selector(event):
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        toggle_selector.RS.set_active(True)

def add_to_file(self, max_1, max_2, max_3, max_4, max_5, energy_1, energy_2, energy_3, energy_4, energy_5, energy_dict, coefficient):
    centroids = [max_1.get(), max_2.get(), max_3.get(), max_4.get(), max_5.get()]
    energies = [energy_1.get(), energy_2.get(), energy_3.get(), energy_4.get(), energy_5.get()]

    centroids = [float(x) for x in centroids if x != '']
    energies = energies[0:len(centroids)]
    energy_vals = [float(energy_dict.get(x)) for x in energies]

    coefficients = np.polyfit(centroids, energy_vals, 2)


    if 'scatter' in selection:
        if 'mwd' in selection:
            with open(coefficient + 'scatterCoefficients_mwd.txt','a+') as f:
                f.write('%s  ( %s\t%s\t%s )\n'%(selection.split('.')[1],coefficients[2],coefficients[1],coefficients[0]))
                f.seek(0)
                length = sum(1 for _ in f)
                f.seek(0)
                order = [0]*length
                for line in range(0,length):
                    lines = f.readline()
                    order[line] = lines
                f.seek(0)
                f.truncate()
                order.sort(key = lambda x: int(x.rsplit(' ',3)[0]))
                for value in range(0,len(order)):
                    f.write(order[value])
                f.close()

    if 'absorber' in selection:
        if 'mwd' in selection:
            with open(coefficient + 'absorberCoefficients_mwd.txt','a+') as f:
                f.write('%s  ( %s\t%s\t%s )\n'%(selection.split('.')[1],coefficients[2],coefficients[1],coefficients[0]))
                f.seek(0)
                length = sum(1 for _ in f)
                f.seek(0)
                order = [0]*length
                for line in range(0,length):
                    lines = f.readline()
                    order[line] = lines
                f.seek(0)
                f.truncate()
                order.sort(key = lambda x: int(x.rsplit(' ',3)[0]))
                for value in range(0,len(order)):
                    f.write(order[value])
                f.close()

    if 'scatter' in selection:
        if 'bld' in selection:
            with open(coefficient + 'scatterCoefficients_bld.txt','a+') as f:
                f.write('%s  ( %s\t%s\t%s )\n'%(selection.split('.')[1],coefficients[2],coefficients[1],coefficients[0]))
                f.seek(0)
                length = sum(1 for _ in f)
                f.seek(0)
                order = [0]*length
                for line in range(0,length):
                    lines = f.readline()
                    order[line] = lines
                f.seek(0)
                f.truncate()
                order.sort(key = lambda x: int(x.rsplit(' ',3)[0]))
                for value in range(0,len(order)):
                    f.write(order[value])
                f.close()

    if 'absorber' in selection:
        if 'bld' in selection:
            with open(coefficient + 'absorberCoefficients_bld.txt','a+') as f:
                f.write('%s  ( %s\t%s\t%s )\n'%(selection.split('.')[1],coefficients[2],coefficients[1],coefficients[0]))
                f.seek(0)
                length = sum(1 for _ in f)
                f.seek(0)
                order = [0]*length
                for line in range(0,length):
                    lines = f.readline()
                    order[line] = lines
                f.seek(0)
                f.truncate()
                order.sort(key = lambda x: int(x.rsplit(' ',3)[0]))
                for value in range(0,len(order)):
                    f.write(order[value])
                f.close()
