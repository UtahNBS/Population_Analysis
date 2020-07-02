# Statistical_Analysis
Statistical Analysis Script that helps visualize important statistical data to determine cutoffs in newbron screening. Command line to execute the code is (for my biologist friends): python NBS_Analysis.py


Developer: Bryce Asay (aka paleomanic) Laboratory: Utah Newborn Screening Date: 7/2/2020

General user interface (GUI) to help visualize a population sample of multiple cohorts to help determine the cutoff used in analysis. The software output will display each individual cohorts density plot, the population value at Q1, Q2, Q3, 90%, 93%, 95%, 97%, 99%, 99.5% and the value to achieve a z-score of 2.8.

Instructions: Data must be setup in a specific manner as displayed below and saved as a .csv (comma separated values) file. The first column entry must be exactly written as: Patient_ID. There cannot be empty columns between data entries. If there are missing values you may leave them blank but NA is best practice. Also, for column headers keep the name simple and avoid spaces. For example: 'RNA Solution 1 & 2' shold be changed to 'RNA_SOL1_2'. Do not include any numbers not part of the cohorts (e.g. notes, formulas) or else they will be incorporated into the analysis and output incorrect results.

After the file is run click on Browser in the upper left side and select you .csv file. To navigate between cohorts press the next and previous buttons located underneath the plots. When you are finished exit using the exit button located on the bottom right. Values and images are saved automatically at the time of generation in the directory that the software is being run.
