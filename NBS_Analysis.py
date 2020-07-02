# Python program to create
# a file explorer in Tkinter

# import all components from the tkinter library, the libraries to process images (PIL), generate plots (seaborn,
# matplotlib), and data analysis libraries (numpy, pandas, scipy)

import os
from tkinter import *
from typing import List, Any

from PIL import ImageTk, Image
# import filedialog module
from tkinter import filedialog
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import scipy.special.cython_special  # needed for conversion to executable using pyinstaller
from scipy import stats
from sys import exit

# Global variables used in the tkinter generation
file_name = ""
plots = []
df = 0
counter = 0
img = 0
img2 = 0


# Function for opening the file explorer window

def get_columns(dataframe):
    """
    Extracts the Column names from a data frame
    :param dataframe: The data frame used in analysis, data must be formatted as per the instructions in the readme
    :return: the column names of a data frame
    """
    col_names: List[Any] = []
    for col in dataframe.columns:
        col_names.append(col)
    return col_names


def clean_col(dataframe, col_name):
    """
    Removes missing values from a data frame, sorts them in ascending order, and prints them. Used in development and
    debugging
    :param dataframe: The data frame used in analysis, data must be formatted as per the instructions in the readme
    :param col_name: the corresponding column names from the function get_columns
    :return: None
    """
    temp_data = dataframe[col_name].dropna().to_numpy()
    sorted_data = np.sort(temp_data)
    length_data = len(sorted_data)
    for i in range(length_data):
        print(sorted_data[i])


def process_col(dataframe):
    """
    Processes the data frame and provides statistical information about the population including the values of
    population ranges and their corresponding z_scores
    :param dataframe: The data frame used in analysis, data must be formatted as per the instructions in the readme
    :return: The population range values in dictionary format, the column names, and a clean data frame of the original
            input data
    """
    pop_data = {}
    clean_data = {}
    col_names = get_columns(dataframe)
    for name in col_names:
        if name != "Patient_ID":
            temp_data = dataframe[name].dropna().to_numpy()
            sorted_data = np.sort(temp_data)
            length_data = len(sorted_data)
            Q1 = int(length_data * 0.25)
            Q2 = int(length_data * 0.5)
            Q3 = int(length_data * 0.75)
            ninty = int(length_data * 0.90)
            nintythree = int(length_data * 0.93)
            nintyfive = int(length_data * 0.95)
            nintyseven = int(length_data * 0.97)
            nintynine = int(length_data * 0.99)
            nintyninefive = int(length_data * 0.995)
            mean = np.mean(sorted_data)
            median = np.median(sorted_data)
            sd = np.std(sorted_data)
            z_val = z_28score(mean,sd)
            min_value = np.min(sorted_data)
            max_value = np.max(sorted_data)
            pop_data[name] = {"Q1": sorted_data[Q1], "Q2": sorted_data[Q2], "Q3": sorted_data[Q3],
                              "90": sorted_data[ninty],
                              "93": sorted_data[nintythree], "95": sorted_data[nintyfive],
                              "97": sorted_data[nintyseven],
                              "99": sorted_data[nintynine], "Mean": mean, "Median": median, "Min": min_value,
                              "Max": max_value,
                              "99.5": sorted_data[nintyninefive], "z_score": z_val, "sd": sd}

            clean_data[name] = temp_data

    return pop_data, col_names, clean_data


def z_28score(mu, sd):
    """
    Calculates the variable value to achieve a z-score of 2.8
    :param mu: the mean of the data
    :param sd: the standard deviation of the data
    :return: the z-score rounded to 3 decimal points
    """
    return round(((2.8 * sd) + mu), 3)


def graph_df(dataframe):
    """
    Creates graphs from the original input data
    :param dataframe: the original data frame used in analysis
    :return: the plot names and the pop data in dictionary form
    """
    plot_names = []
    pop_df, col_names, clean_df = process_col(dataframe)
    for name in col_names:
        if name != "Patient_ID":
            plot = sb.distplot(clean_df[name], hist=True, kde=True)
            plt.axvline(z_28score(np.mean(clean_df[name]), np.std(clean_df[name])), color='black', lw=3,
                        label='Z-score 2.8')
            plt.axvline(pop_df[name]["Q2"], color='pink', linestyle='dashed', label='Q2')
            plt.axvline(pop_df[name]["Q3"], color='yellow', linestyle='dashed', label='Q3')
            plt.axvline(pop_df[name]["90"], color='brown', linestyle='dashed', label='90')
            plt.axvline(pop_df[name]["93"], color='purple', linestyle='dashed', label='93')
            plt.axvline(pop_df[name]["95"], color='blue', linestyle='dashed', label='95')
            plt.axvline(pop_df[name]["97"], color='green', linestyle='dashed', label='97')
            plt.axvline(pop_df[name]["99"], color='red', linestyle='dashed', label='99')
            plt.axvline(pop_df[name]["99.5"], color='orange', linestyle='dashed', label='99.5')
            plt.legend(loc=0, prop={'size': 6})
            # plt.gca().legend(('Z-score 2.8','Q2 (50)',"Q3 (75)",'90','93','95','97',"99","99.5"))
            plt.title(name + " Distribution")
            plt.ylabel('Density')
            plt.xlabel('Variable Value')
            save_name = name + "plot.png"
            pathSave_name = os.path.join(os.getcwd(), save_name)
            print(pathSave_name)
            plot_names.append(save_name)
            plt.savefig(pathSave_name)
            plt.close()
    return plot_names, pop_df


def lab_stats(dataframe, name):
    """
    Generates statistics on uploaded data frame, generates graphical plots, and saves the data
    :param dataframe:The data frame used in analysis, data must be formatted as per the instructions in the readme
    :param name: Name of the new file
    :return:
    """
    df = pd.read_csv(dataframe)
    plot_names, pop_df = graph_df(df)
    panda_dataframe = pd.DataFrame.from_dict(pop_df)
    panda_dataframe.to_csv(name.replace('.csv', "Analyzed.csv"))
    return name.replace('.csv', "Analyzed.csv"), plot_names, pop_df


def z_score(x, mu, sd):
    """
    Generates a z-score for each value
    :param x: the variable value used to generate the z-score
    :param mu: the mean of the input data
    :param sd: the standard deviation of the input data
    :return: a z-score
    """
    return round(((x - mu) / sd), 4)


def browse_files():
    """
    Opens the file explorer menu, processes the data using the lab_stats function, resets the global variables
    (e.g. counter) and displays plots on the tkinter canvas
    :param: None
    :return: None
    """
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("CSV files",
                                                      "*.csv*"),
                                                     ("all files",
                                                      "*.*")))
    global file_name
    file_name = filename

    # Change label contents
    label_file_explorer.configure(text="Opened:   " + os.path.basename(filename))

    # Process information within the selected file
    __, plot_names, file_df = lab_stats(file_name, os.path.basename(filename))
    global plots
    plots = plot_names
    global df
    df = file_df
    global img
    img = ImageTk.PhotoImage(Image.open(plots[0]))
    # canvas = Canvas(window, width=600, height=500)
    # canvas.place(x=5, y=45)
    canvas.create_image(0, 0, anchor=NW, image=img)
    update_label(counter, df)


def next_image():
    """
    Uploads the next plot to be displayed on the tkinter GUI and updates global variables
    :param: None
    :return: None
    """
    global counter
    global plots
    global df
    global img
    if counter < len(plots) - 1:
        counter += 1
        canvas.delete('all')
        img = ImageTk.PhotoImage(Image.open(plots[counter]))
        canvas.create_image(0, 0, anchor=NW, image=img)
        update_label(counter, df)


def previous_image():
    """
    Uploads the previous plot displayed on the tkinter GUI and updates global variables
    :param: None
    :return: None
    """
    global counter
    global plots
    global img
    global df
    if counter > 0:
        counter -= 1
        canvas.delete('all')
        img = ImageTk.PhotoImage(Image.open(plots[counter]))
        canvas.create_image(0, 0, anchor=NW, image=img)
        update_label(counter, df)


def update_label(counter, dataframe):
    """
    Updates the label's displayed on the tkinter GUI to match the data displayed in the plot
    :param counter: The global variable used to check which dataset is being displayed
    :param dataframe: The data frame used in analysis, data must be formatted as per the instructions in the readme
    :return: None
    """
    # print(dataframe.keys())
    work_df = dataframe[list(dataframe.keys())[counter]]
    work_df_Q1 = work_df['Q1']
    work_df_Q2 = work_df['Q2']
    work_df_Q3 = work_df['Q3']
    work_df_90 = work_df['90']
    work_df_93 = work_df['93']
    work_df_95 = work_df['95']
    work_df_97 = work_df['97']
    work_df_99 = work_df['99']
    work_df_99five = work_df['99.5']
    work_df_mean = work_df['Mean']
    work_df_median = work_df['Median']
    work_df_min = work_df['Min']
    work_df_max = work_df['Max']
    work_df_sd = work_df['sd']

    z_Q1 = z_score(work_df_Q1, work_df_mean, work_df_sd)
    z_Q2 = z_score(work_df_Q2, work_df_mean, work_df_sd)
    z_Q3 = z_score(work_df_Q3, work_df_mean, work_df_sd)
    z_90 = z_score(work_df_90, work_df_mean, work_df_sd)
    z_93 = z_score(work_df_93, work_df_mean, work_df_sd)
    z_95 = z_score(work_df_95, work_df_mean, work_df_sd)
    z_97 = z_score(work_df_97, work_df_mean, work_df_sd)
    z_99 = z_score(work_df_99, work_df_mean, work_df_sd)
    z_99five = z_score(work_df_99five, work_df_mean, work_df_sd)

    z_2eight = z_28score(work_df_mean, work_df_sd)
    label_z_2eight.configure(text="Z-score(2.8):   " + str(z_2eight))

    label_z_Q1.configure(text=str(z_Q1))
    label_z_Q2.configure(text=str(z_Q2))
    label_z_Q3.configure(text=str(z_Q3))
    label_z_90.configure(text=str(z_90))
    label_z_93.configure(text=str(z_93))
    label_z_95.configure(text=str(z_95))
    label_z_97.configure(text=str(z_97))
    label_z_99.configure(text=str(z_99))
    label_z_99five.configure(text=str(z_99five))

    label_Q1.configure(text="Q1:  " + str(work_df_Q1))
    label_Q2.configure(text="Q2:  " + str(work_df_Q2))
    label_Q3.configure(text="Q3:  " + str(work_df_Q3))
    label_90.configure(text="90:  " + str(work_df_90))
    label_93.configure(text="93:  " + str(work_df_93))
    label_95.configure(text="95:  " + str(work_df_95))
    label_97.configure(text="97:  " + str(work_df_97))
    label_Mean.configure(text="Mean:  " + str(round(work_df_mean, 2)))
    label_Median.configure(text="Median:  " + str(round(work_df_median, 2)))
    label_Min.configure(text="Min:  " + str(work_df_min))
    label_Max.configure(text="Max:  " + str(work_df_max))
    label_99.configure(text="99:  " + str(work_df_99))
    label_99five.configure(text="99.5:  " + str(work_df_99five))
    label_SD.configure(text="SD: " + str(round(work_df_sd, 4)))
    # label_Z.configure(text="Z: " + str(work_df_Z))


# Create the root window
window = Tk()
canvas = Canvas(window, width=615, height=520)

# Set window title
window.title('Utah NBS Experimental Analysis')

# Set window size
window.geometry("850x600")

# Set window background color
window.config(background="white")

# Create a File Explorer label
label_file_explorer = Label(window,
                            text="Selected File",
                            width=77, height=2,
                            fg="blue")

label_StatVar = Label(window,
                      text="Statistical Values",
                      width=15, height=1,
                      font=('Helvetica 18', 8, 'bold'),
                      borderwidth=1,
                      relief='solid')

label_z_2eight = Label(window,
                       text="Z-score(2.8):  ...",
                       width=20, height=2,
                       font=('Helvetica 18', 12, 'bold'),
                       borderwidth=4,
                       bg='white', fg='black',
                       relief='solid')

label_z_Q1 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='white', fg='black',
                   relief='sunken')

label_z_Q2 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='pink', fg='black',
                   relief='sunken')

label_z_Q3 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='yellow', fg='black',
                   relief='sunken')

label_z_90 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='brown',
                   fg='white', relief='sunken')

label_z_93 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='purple', fg='black', relief='sunken')

label_z_95 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='blue', fg='black', relief='sunken')

label_z_97 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='green', fg='black', relief='sunken')

label_z_99 = Label(window,
                   text="...",
                   width=10, height=1,
                   borderwidth=2,
                   bg='red', fg='black', relief='sunken')

label_z_99five = Label(window,
                       text="...",
                       width=10, height=1,
                       borderwidth=2,
                       bg='orange', fg='black', relief='sunken')

label_Mean = Label(window,
                   text="...",
                   width=15, height=1,
                   borderwidth=2,
                   # relief='solid',
                   bg='white', fg='black', relief='sunken')

label_Median = Label(window,
                     text="...",
                     width=15, height=1,
                     borderwidth=2,
                     # relief='solid',
                     bg='white', fg='black', relief='sunken')

label_Min = Label(window,
                  text="...",
                  width=15, height=1,
                  borderwidth=2,
                  # relief='solid',
                  bg='white', fg='black', relief='sunken')

label_Max = Label(window,
                  text="...",
                  width=15, height=1,
                  borderwidth=2,
                  # relief='solid',
                  bg='white', fg='black', relief='sunken')

label_SD = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 # relief='solid',
                 bg='white', fg='black', relief='sunken')

label_zscore = Label(window,
                     text="Z-Score",
                     width=9, height=1,
                     font=('Helvetica 18', 8, 'bold'),
                     borderwidth=1,
                     relief='solid')

label_Q1 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='white', fg='black',
                 relief='sunken')

label_Q2 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='pink', fg='black',
                 relief='sunken')

label_Q3 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='yellow', fg='black',
                 relief='sunken')

label_90 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='brown',
                 fg='white', relief='sunken')

label_93 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='purple', fg='black', relief='sunken')

label_95 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='blue', fg='black', relief='sunken')

label_97 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='green', fg='black', relief='sunken')

label_99 = Label(window,
                 text="...",
                 width=15, height=1,
                 borderwidth=2,
                 bg='red', fg='black', relief='sunken')

label_99five = Label(window,
                     text="...",
                     width=15, height=1,
                     borderwidth=2,
                     bg='orange', fg='black', relief='sunken')

button_explore = Button(window,
                        text="Browse Files",
                        command=browse_files)

button_exit = Button(window,
                     text="Exit",
                     command=exit,
                     height=1, width=9)

button_next = Button(window,
                     text="Next",
                     command=next_image)

button_previous = Button(window,
                         text="Prev",
                         command=previous_image)

# Place method is chosen for placing the widgets at respective positions in a table like structure by
# specifying the x and y coordinates

label_file_explorer.place(x=80, y=1)

label_StatVar.place(x=633, y=75)
label_zscore.place(x=759, y=75)

label_z_Q1.place(x=755, y=100)
label_z_Q2.place(x=755, y=125)
label_z_Q3.place(x=755, y=150)
label_z_90.place(x=755, y=175)
label_z_93.place(x=755, y=200)
label_z_95.place(x=755, y=225)
label_z_97.place(x=755, y=250)
label_z_99.place(x=755, y=275)
label_z_99five.place(x=755, y=300)

label_Q1.place(x=632, y=100)
label_Q2.place(x=632, y=125)
label_Q3.place(x=632, y=150)
label_90.place(x=632, y=175)
label_93.place(x=632, y=200)
label_95.place(x=632, y=225)
label_97.place(x=632, y=250)
label_99.place(x=632, y=275)
label_99five.place(x=632, y=300)
label_Mean.place(x=632, y=325)
label_SD.place(x=632, y=350)
label_Median.place(x=632, y=375)
label_Min.place(x=632, y=400)
label_Max.place(x=632, y=425)

label_z_2eight.place(x=632, y=475)

button_explore.place(x=1, y=6)
canvas.place(x=5, y=45)
button_exit.place(x=768, y=570)
button_next.place(x=590, y=570)
button_previous.place(x=5, y=570)

# Let the window wait for any events, required for tkinter to display properly
window.mainloop()
