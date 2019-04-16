import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats.mstats as statistics
import scipy.stats as sp
import os
import Tkinter as tk
import csv
#import vrep
#import vrepConst
import subprocess
 

from subprocess import Popen


def MatrixCreate(rows, columns):
    my_matrix = [[0 for x in xrange(columns)] for x in xrange(rows)]
    return my_matrix

def getColumn(matrix, i):
    return [row[i] for row in matrix]


def meanColumn(matrix, i):
    col = [row[i] for row in matrix]
    return np.mean(col)

#def histGeneration(matrix, i):
#    col = [row[i] for row in matrix]
#    return col

def percentileColumn(matrix, i, p):
    col = [row[i] for row in matrix]
    return np.percentile(col, p)

def medianColumn(matrix, i):
    col = [row[i] for row in matrix]
    return np.median(col)

class EvoBotApplication(tk.Frame):
    runNum = 0
    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self,
                          master,
                          width=600,
                          height=400)
        self.master.title('EVOBOT')  
        self.pack_propagate(0)
        self.pack()
        
        #parameter frame
        self.parameter_frame = tk.Frame(self)

        self.graph_frame = tk.Frame(self, background='red')

      #  top = Toplevel();

        # option
        self.mode_var = tk.StringVar()
        self.mode = tk.OptionMenu(self,
                                      self.mode_var,
                                      'plant evolution',
                                      'other')
        self.mode_var.set('plant evolution')
 
        # The evolve button
        self.evolve_button = tk.Button(self,
                                   text='Evolve!',
                                   command=self.run_vrep)
        # amount runs
        self.amountRuns_label = tk.Label(self.parameter_frame,
                                          text='amount runs')
        self.amountRuns_var = tk.IntVar()
        self.amountRuns_entry = tk.Entry(self.parameter_frame,
                                          textvariable=self.amountRuns_var)
        self.amountRuns_var.set(8)
        # frame for changeable values
        self.generations_label = tk.Label(self.parameter_frame,
                                          text='generations')
        self.generations_var = tk.IntVar()
        self.generations_entry = tk.Entry(self.parameter_frame,
                                          textvariable=self.generations_var)
        self.generations_var.set(1000)
        #popsize
        self.populationSize_label = tk.Label(self.parameter_frame, 
                                             text='population size')
        self.populationSize_var = tk.IntVar()
        self.populationSize_entry = tk.Entry(self.parameter_frame,
                                             textvariable=self.populationSize_var)
        self.populationSize_var.set(100)
        #mutRate
        self.mutationRate_label = tk.Label(self.parameter_frame,
                                           text='mutation rate')
        self.mutationRate_var = tk.DoubleVar()
        self.mutationRate_entry = tk.Entry(self.parameter_frame,
                                           textvariable= self.mutationRate_var)
        self.mutationRate_var.set(0.05);
        self.crossover_label = tk.Label(self.parameter_frame,
                                           text='crossover')
        self.crossover_var = tk.BooleanVar()
        self.crossover_check = tk.Checkbutton(self.parameter_frame,
                                           variable= self.crossover_var)
        self.crossover_var.set(1);
        self.crossoverRate_label = tk.Label(self.parameter_frame,
                                           text='crossover rate')
        self.crossoverRate_var = tk.DoubleVar()
        self.crossoverRate_entry = tk.Entry(self.parameter_frame,
                                           textvariable= self.crossoverRate_var)
        self.crossoverRate_var.set(0.02);
       
        self.amountIncrements_label = tk.Label(self.parameter_frame,
                                               text='amount increments')
        self.amountIncrements_var = tk.IntVar()
        self.amountIncrements_entry = tk.Entry(self.parameter_frame,
                                               textvariable=self.amountIncrements_var)
        self.amountIncrements_var.set(5);

        self.customInd_label = tk.Label(self.parameter_frame,
                                               text='customIndNum')
        self.customInd_var = tk.IntVar()
        self.customInd_entry = tk.Entry(self.parameter_frame,
                                               textvariable=self.customInd_var)
        self.customInd_var.set(0);
        
        self.run_label = tk.Label(self.parameter_frame,
                                               text='run')
        self.run_var = tk.IntVar()
        self.run_entry = tk.Entry(self.parameter_frame,
                                               textvariable=self.run_var)
        self.run_var.set(0);

        self.load_button = tk.Button(self.parameter_frame,
                                   text='Load Individual!',
                                   command=self.loadBest)   
        
        
             
        

        # some custom modes
        self.differentMode_var = tk.StringVar()
        self.evolutionMode = tk.OptionMenu(self.parameter_frame,
                                      self.differentMode_var,
                                      'EVOLUTION',
                                      'COEVOLUTION',
                                      'OBSTACLEEVOLUTION',
                                      'GROWEVOLUTION',
                                      'ROTATE',
                                      'HORMONE',
                                      'RECALLCUSTOM',
                                      'RECALLBEST',
                                      'RECALLPOP', 
                                      'RECALLROTATOR')
        self.differentMode_var.set('EVOLUTION')
        self.evolutionMode_label = tk.Label(self.parameter_frame,
                                            text='evolution mode:')

        #debug button
        self.debug_button = tk.Button(self,
                                   text='Print Settings',
                                   command=self.read_settingsData)
        #debug button
        self.analyseData_button = tk.Button(self.graph_frame,
                                   text='Analyse Data',
                                   command=self.read_generationFile)
        self.compareData_button = tk.Button(self.graph_frame,
                                   text='Compare Data',
                                   command=self.read_files)
        self.printImportant_button = tk.Button(self.graph_frame,
                                   text='printImportant',
                                   command=self.printImportant)   
        self.printTwo_button = tk.Button(self.graph_frame,
                                   text='printTwo',
                                   command=self.printTwo)   

       
        # Put the controls on the form
        self.mode.pack(fill=tk.X, side=tk.TOP)
        # parameters 
        self.debug_button.pack(fill= tk.X, side = tk.TOP)
        self.analyseData_button.pack(side = tk.TOP)
        self.compareData_button.pack(side = tk.BOTTOM)
        self.printImportant_button.pack(side =tk.BOTTOM)
        self.printTwo_button.pack(side =tk.BOTTOM)
        self.graph_frame.pack(fill=tk.BOTH, side = tk.RIGHT)
        self.parameter_frame.pack(fill=tk.BOTH, side= tk.TOP)
        self.evolutionMode_label.grid(row = 0, column = 0, sticky='E')
        self.evolutionMode.grid(row = 0, column = 1, rowspan=2, columnspan = 1, sticky='EW')
        self.amountRuns_label.grid(row = 2, column = 3)
        self.amountRuns_entry.grid(row = 2, column = 4)
        self.generations_label.grid(row = 2, column = 0, sticky='E')
        self.generations_entry.grid(row = 2, column = 1)
        self.populationSize_label.grid(row = 3, column = 0, sticky='E')
        self.populationSize_entry.grid(row = 3, column = 1, sticky = 'E')
        self.mutationRate_label.grid(row = 4, column = 0, sticky='E')
        self.mutationRate_entry.grid(row = 4, column = 1,sticky='EW')
        self.crossover_label.grid(row = 5, column = 0,sticky='E')
        self.crossover_check.grid(row = 5, column = 1)
        self.crossoverRate_label.grid(row = 6, column = 0,sticky='E')
        self.crossoverRate_entry.grid(row = 6, column = 1)
        self.amountIncrements_label.grid(row = 7, column = 0, sticky='E')
        self.amountIncrements_entry.grid(row = 7, column = 1)
        self.customInd_label.grid(row = 8, column = 0)
        self.customInd_entry.grid(row = 8, column = 1)
        self.run_label.grid(row = 9, column = 0)
        self.run_entry.grid(row = 9, column = 1)
        self.load_button.grid(row = 10, column = 0, columnspan = 2)


        self.evolve_button.pack(fill=tk.X, side=tk.BOTTOM)

#    def print_out(self):
#        print('%s, %s!' % (self.mode_var.get().title(),
#                           self.generations_var.get()))

    def loadBest(self):
        with open('interfaceFiles\\EvoSettings0.csv', 'wb') as csvfile:
            settingsWriter = csv.writer(csvfile, delimiter=',', 
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
            settingsWriter.writerow(('#mode',self.differentMode_var.get()))
            settingsWriter.writerow(('#generations', self.generations_var.get()))
            settingsWriter.writerow(('#populationSize', self.populationSize_var.get()))
            settingsWriter.writerow(('#mutationRate', self.mutationRate_var.get()))
            settingsWriter.writerow(('#amountRuns', self.amountRuns_var.get()))
            settingsWriter.writerow(('#amountIncrements', self.amountIncrements_var.get()))
            settingsWriter.writerow(('#customInd', self.customInd_var.get()))
            settingsWriter.writerow(('#run', self.run_var.get()))

        p = Popen(["start", "/WAIT", "plantScene0.ttt"], shell=True)
        instance = p;
       

    def run_vrep(self):
#        execfile('C:\Program Files (x86)\V-REP3\V-REP_PRO_EDU\vrep.exe')
#        FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
        temp_location=(r"C:\Program Files (x86)\V-REP3\V-REP_PRO_EDU\run0.bat")

     #   os.system('"' + temp_location + '"');
        subprocess.call(temp_location,shell=True)

        #vrep.simxStart
        #amountRuns = self.amountRuns_var.get()
        #print(str(amountRuns))
        #for i in range (0, amountRuns):
        #    print(str(i))
        #    with open('interfaceFiles\\EvoSettings'+str(i)+'.csv', 'wb') as csvfile:
        #        settingsWriter = csv.writer(csvfile, delimiter=',', 
        #                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #        settingsWriter.writerow(('#mode',self.differentMode_var.get()))
        #        settingsWriter.writerow(('#generations', self.generations_var.get()))
        #        settingsWriter.writerow(('#populationSize', self.populationSize_var.get()))
        #        settingsWriter.writerow(('#mutationRate', self.mutationRate_var.get()))
        #        settingsWriter.writerow(('#amountRuns', self.amountRuns_var.get()))
        #        settingsWriter.writerow(('#amountIncrements', self.amountIncrements_var.get()))
        #        settingsWriter.writerow(('#customInd', self.customInd_var.get()))
        #        settingsWriter.writerow(('#run', self.run_var.get()))


        ##path = "C:\\Program Files (x86)\\V-REP3\\V-REP_PRO_EDU\\run0.bat"
        ##print(path)
        #    p = Popen(["start", "/WAIT", "run"+str(i)+".bat"], shell=True)
        #    instance = p;
       # p = Popen("run0.bat", shell=True)
       # os.startfile('"'+path+'"')
       # os.system('"'+ path +'"')    
        
    def read_settingsData(self):
        with open('EvoSettings.csv', 'rb') as csvFile:
            settingsReader = csv.reader(csvFile, delimiter =',', quotechar='|')
            for row in settingsReader:
                print ', '.join(row)
    
    def read_volume(self):
        objects = []
        objectTypes = []
        for i in range (0, self.amountRuns_var.get()):
            with open('results\\SavedGenerations'+str(i)+'.csv', 'rb') as csvFile:
                settingsReader = csv.reader(csvFile, delimiter =',', quotechar='|')
                for j in range(0, 100):
                    with open('results\\SavedGenerations'+str(i)+'.csv', 'rb') as csvFile:
                        s
                avgFitCol = (self.populationSize_var.get() + 2)
                bestFitCol = (self.populationSize_var.get() + 6)
                generationData =[]
                bestFitData =[]
                for row in settingsReader:
                        content = float(row[avgFitCol])
                        generationData.append(float(content))
                        bestFitData.append(float(row[bestFitCol]))
                allData.append(generationData)

    def read_generationFile(self):
        #temp
        x = np.arange(0.0, 2, 0.01)
        y1 = np.sin(2*np.pi*x)
        y2 = 1.2*np.sin(4*np.pi*x)

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

        ax1.fill_between(x, 0, y1)
        ax1.set_ylabel('between y1 and 0')

        ax2.fill_between(x, y1, 1)
        ax2.set_ylabel('between y1 and 1')

        ax3.fill_between(x, y1, y2)
        ax3.set_ylabel('between y1 and y2')
        ax3.set_xlabel('x')
        plt.show()
        with open('interfaceFiles\\SavedGenerations0.csv', 'rb') as csvFile:
            settingsReader = csv.reader(csvFile, delimiter =',', quotechar='|')
            avgFitCol = (self.populationSize_var.get() + 2)
            bestFitCol = (self.populationSize_var.get() + 6)
            generationData =[]
            bestFitData =[]
            for row in settingsReader:
                    content = float(row[avgFitCol])
                    generationData.append(float(content))
                    bestFitData.append(float(row[bestFitCol]))
            #        print content
                    print float(content)
            fig = plt.figure(figsize = (12,6))
            ax1 = fig.add_subplot(1,2,1)
            ax1.set_xlabel('generation')
            ax1.set_ylabel('fitness')
            ax1.plot(generationData)
            ax2 = fig.add_subplot(1,2,1)
            ax2.plot(bestFitData)
            
            plt.show()
    
    def printTwo(self):
        plt.rcParams.update({'font.size': 22})
        amountGenerations = 250
        errorInterval = 20
        noError = True
        fig = plt.figure(figsize = (12,12))
        allData = []
        for i in range (0, self.amountRuns_var.get()):
    #        print('i = ', str(i))
            with open('results\\SavedGenerations'+str(i)+'.csv', 'rb') as csvFile:
                settingsReader = csv.reader(csvFile, delimiter =',', quotechar='|')
                avgFitCol = (self.populationSize_var.get() + 2)
                bestFitCol = (self.populationSize_var.get() + 6)
                generationData =[]
                bestFitData =[]
                for row in settingsReader:
                        content = float(row[avgFitCol])
                        generationData.append(float(content))
                        bestFitData.append(float(row[bestFitCol]))
                        #print float(content)
                allData.append(generationData)
               
    #    print allData
        arrayLength = np.shape(allData)
     #   print(arrayLength)
        #for i in allData:
       
        xMean = []
        xMedian = []
        xCount = []
        xPosErrDat = []
        xNegErrDat = []
        xPosErr = []
        xNegErr = []
        xPosHunDat = []
        xNegZeroDat = []
        xPosHun = []
        xNegZero = []
        xtest =[]
        std = []
        std2 = []
        for i in range(0, amountGenerations): # this needs to be within bounds
            y = meanColumn(allData, i)
            xMean.append(y)
            yM = medianColumn(allData, i)
            xMedian.append(yM)
        for i in range(0, amountGenerations): # this needs to be within bounds
            y = meanColumn(allData, i)
            xCount.append(i)
            std.append(np.std(y))
            std.append(np.std(y))
            e = percentileColumn(allData, i, 25)
            xNegErrDat.append(e)
            xNegErr.append(y - e)
            e = percentileColumn(allData, i, 75)
            xPosErrDat.append(e)
            xPosErr.append( e - y)
            e = percentileColumn(allData, i , 0)
            xNegZeroDat.append(e)
            xNegZero.append( y - e)
            e = percentileColumn(allData, i , 100)
            xPosHunDat.append(e)
            xPosHun.append( e - y)
           # e = percentileColumn(allData, i , 100)
           # xPosHunDat.append(e)
          #  xtest.append(e)
   #     print (y)
   #     print ("x = ")
   #     print (xMean)
   #     print ("neg = ")
    #    print (xNegErr)
    #    print ("pos = ")
    #    print (xPosErr)
        ax4 = fig.add_subplot(1, 1, 1)
#        y = np.mean(allData, axis = 1)
        ax4.plot(xMean, label = 'Static', linewidth = 4, linestyle = '-', marker= '^', color='#CC4F1B', markersize = 10.0, markevery=10)
     #   ax4.plot(xMedian, linewidth = 4, color='g')
   #     ax4.plot(xtest, linewidth = 8)
       # ax4.plot(xNegErrDat)
       # ax4.plot(xPosErrDat)
    #    ax5 = fig.add_subplot(3, 4, 11, sharex=ax4, sharey=ax4 )
 #       ax4.fill_between(xCount, xNegErrDat, xPosErrDat, 
 #                        alpha=0.4, edgecolor='#CC4F1B', facecolor='#FF9848',
 #                        linewidth=4, linestyle='dashdot', antialiased=True)
 #       ax4.fill_between(xCount, xNegZeroDat, xPosHunDat, 
 #                        alpha=0.2, edgecolor='#CC4F1B', facecolor='#FF9848',
 #                        linewidth=4, antialiased=True)
        if (noError == False):
            (_, errorBar ,_) = ax4.errorbar( xCount[::errorInterval], xMean[::errorInterval], yerr=[xNegErr[::errorInterval], xPosErr[::errorInterval]],ecolor='#FF9848', alpha = 0.6, elinewidth = 4, capsize = 10)
            for cap in errorBar:
                cap.set_markeredgewidth(2)
        
        (_, errorBar ,_) = ax4.errorbar( xCount[::errorInterval], xMean[::errorInterval], yerr=[xNegZero[::errorInterval], xPosHun[::errorInterval]],ecolor='#FF9848', alpha = 0.6, elinewidth = 2, capsize = 10)
        for cap in errorBar:
            cap.set_markeredgewidth(2)
        
        #ax4.plot(xPosErrDat,color='#FF9848', alpha = 0.4, linestyle = '', marker = 'v')
        #ax4.plot(xNegErrDat,color='#FF9848', alpha = 0.4, linestyle = '', marker = 'v')
        #ax4.plot(xPosHunDat,color='#FF9848', alpha = 0.4,linestyle = '', marker = 'v')
        #ax4.plot(xNegZeroDat,color='#FF9848', alpha = 0.4, linestyle = '', marker = 'v')
#        fill_between(xMean, xNegErr, xPosErr)
        #", alpha = 0.5, edgecolor = '#CC4F1B', facecolor = '#FF9848')
        ax4.set_xlabel('generation')
        ax4.set_ylabel('average fitness')



        # 2nd
        allData2 = []
        for i in range (0, self.amountRuns_var.get()):
            print('i = ', str(i))
            with open('results2\\SavedGenerations'+str(i)+'.csv', 'rb') as csvFile:
                settingsReader2 = csv.reader(csvFile, delimiter =',', quotechar='|')
                avgFitCol2 = (self.populationSize_var.get() + 2)
                bestFitCol2 = (self.populationSize_var.get() + 6)
                generationData2 =[]
                bestFitData2 =[]
                n = 0
                for row in settingsReader2:
                    if n % 2 == 0:
                      #  print ("n = " ,n)
                        content2 = float(row[avgFitCol2])
                        generationData2.append(float(content2))
                        bestFitData2.append(float(row[bestFitCol2]))
                        #print float(content)
                        allData2.append(generationData2)
               
                    n+=1
                
       # print allData2
        arrayLength = np.shape(allData2)
       # print(arrayLength)
        #for i in allData:
       
        xMean2 = []
        xMedian2 = []
        xCount2 = []
        xPosErrDat2 = []
        xNegErrDat2 = []
        xPosErr2 = []
        xNegErr2 = []
        xPosHunDat2 = []
        xNegZeroDat2 = []
        xPosHun2 = []
        xNegZero2 = []
        xtest2 =[]

        for i in range(0, amountGenerations): # this needs to be within bounds
            y = meanColumn(allData2, i)
            xMean2.append(y)
            yM = medianColumn(allData2, i)
            xMedian2.append(yM)
            xCount2.append(i)
            e = percentileColumn(allData2, i, 25)
            xNegErrDat2.append(e)
            xNegErr2.append(y - e)
            e = percentileColumn(allData2, i, 75)
            xPosErrDat2.append(e)
            xPosErr2.append( e - y)
            e = percentileColumn(allData2, i , 0)
            xNegZeroDat2.append(e)
            xNegZero2.append( y - e)
            e = percentileColumn(allData2, i , 100)
            xPosHunDat2.append(e)
            xPosHun2.append( e - y)
           # e = percentileColumn(allData, i , 100)
           # xPosHunDat2.append(e)
          #  xtest.append(e)
      #  print (y)
      #  print ("x = ")
      #  print (xMean2)
     #   print ("neg = ")
      #  print (xNegErr2)
     #   print ("pos = ")
      #  print (xPosErr2)
        ax4 = fig.add_subplot(1, 1, 1)
#        y = np.mean(allData, axis = 1)
#        ax4.plot(xMean2, linewidth = 4)
#        ax4.plot(xMedian2, linewidth = 4)
   #     ax4.plot(xtest, linewidth = 8)
       # ax4.plot(xNegErrDat)
       # ax4.plot(xPosErrDat)
    #    ax5 = fig.add_subplot(3, 4, 11, sharex=ax4, sharey=ax4 )
        ax4.plot(xMean2, label = 'Actuated',linewidth = 4,color='#1B2ACC', marker= 's', markersize = 10.0, markevery=10)
        
#        ax4.fill_between(xCount2, xNegErrDat2, xPosErrDat2, 
#                         alpha=0.4, edgecolor='#1B2ACC', facecolor='#089FFF',
#                         linewidth=4, linestyle='dashdot', antialiased=True)
#        ax4.fill_between(xCount2, xNegZeroDat2, xPosHunDat2, 
#                         alpha=0.2, edgecolor='#1B2ACC', facecolor='#089FFF',
#                         linewidth=4, antialiased=True)
#       
        if (noError == False): 
            (_, errorBar ,_) = ax4.errorbar( xCount2[::errorInterval], xMean2[::errorInterval], yerr=[xNegErr2[::errorInterval], xPosErr2[::errorInterval]],ecolor='#089FFF',alpha = 0.6, elinewidth=4, capsize = 10)
            for cap in errorBar:
                cap.set_markeredgewidth(2)
        (_, errorBar ,_) = ax4.errorbar( xCount2[::errorInterval], xMean2[::errorInterval], yerr=[xNegZero2[::errorInterval], xPosHun2[::errorInterval]],ecolor='#089FFF', alpha = 0.6, elinewidth = 2, capsize = 10)
        for cap in errorBar:
            cap.set_markeredgewidth(2)
        
        #ax4.plot(xPosErrDat2,color='#089FFF', alpha = 0.6, linestyle = '', marker = 's')
        #ax4.plot(xNegErrDat2,color='#089FFF', alpha = 0.6, linestyle = '', marker = 's')
        #ax4.plot(xPosHunDat2,color='#089FFF', alpha = 0.6, linestyle = '', marker = 's')
        #ax4.plot(xNegZeroDat2,color='#089FFF', alpha = 0.6, linestyle = '', marker = 's')
       # ax4.plot(xMedian2, linewidth = 4)

#        fill_between(xMean, xNegErr, xPosErr)
        #", alpha = 0.5, edgecolor = '#CC4F1B', facecolor = '#FF9848')


        #yerr = np.percentile(allData, 0)
       # y = np.mean(allData, axis=1, dtype= np.float64)
       # ax3.errorbar(percentile1, )
        
        for i in range(0, self.amountRuns_var.get()):
            x = allData[i][amountGenerations]
        

        mu, sigma = 100, 15

      #  x = self.amountRuns_var.get();
        
        x = zip(*allData)[80]
        print ("x = ",x)
#        print(statistics.normaltest(x))
#        print(statistics.normaltest(allData2[80]))
        print(sp.shapiro(x))
    #    axH = fig.add_subplot(1, 3, 2)
    #    axH.hist(x, 10, normed=1, facecolor='green', alpha=0.75)

        y = zip(*allData2)[80]
        print(sp.shapiro(y))
        
        mann = sp.mannwhitneyu(x, y, True)
        print('mann', mann)

        # the histogram of the data
        #n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
    #    axH = fig.add_subplot(1, 3, 3)
    #    axH.hist(x, 10, normed=1, facecolor='green', alpha=0.75)
        plt.legend(bbox_to_anchor=(0.05, 0.95), loc=2, borderaxespad=0.)
        plt.show()


    def printImportant(self):
        fig = plt.figure(figsize = (12,12))
        allData = []
        for i in range (0, self.amountRuns_var.get()):
            print('i = ', str(i))
            with open('results\\SavedGenerations'+str(i)+'.csv', 'rb') as csvFile:
                settingsReader = csv.reader(csvFile, delimiter =',', quotechar='|')
                avgFitCol = (self.populationSize_var.get() + 2)
                bestFitCol = (self.populationSize_var.get() + 6)
                generationData =[]
                bestFitData =[]
                for row in settingsReader:
                        content = float(row[avgFitCol])
                        generationData.append(float(content))
                        bestFitData.append(float(row[bestFitCol]))
                        #print float(content)
                allData.append(generationData)
               
        print allData
        arrayLength = np.shape(allData)
        print(arrayLength)
        #for i in allData:
       
        xMean = []
        xMedian = []
        xCount = []
        xPosErrDat = []
        xNegErrDat = []
        xPosErr = []
        xNegErr = []
        xPosHunDat = []
        xNegZeroDat = []
        xPosHun = []
        xNegZero = []
        xtest =[]
        for i in range(0, 20): # this needs to be within bounds
            y = meanColumn(allData, i)
            xMean.append(y)
            yM = medianColumn(allData, i)
            xMedian.append(y)
            xCount.append(i)
            e = percentileColumn(allData, i, 25)
            xNegErrDat.append(e)
            xNegErr.append(y - e)
            e = percentileColumn(allData, i, 75)
            xPosErrDat.append(e)
            xPosErr.append( e - y)
            e = percentileColumn(allData, i , 0)
            xNegZeroDat.append(e)
            xNegZero.append( y - e)
            e = percentileColumn(allData, i , 100)
            xPosHunDat.append(e)
            xPosHun.append( e - y)
            e = percentileColumn(allData, i , 100)
            xPosHunDat.append(e)
          #  xtest.append(e)
            

 
        print (y)
        print ("x = ")
        print (xMean)
        print ("neg = ")
        print (xNegErr)
        print ("pos = ")
        ax4 = fig.add_subplot(1, 1, 1)

        print (xPosErr)
   #     ax4 = fig.add_subplot(1, 1, 1)
#        y = np.mean(allData, axis = 1)
        ax4.plot(xMean, linewidth = 4)
        ax4.plot(xMedian, linewidth = 4)
   #     ax4.plot(xtest, linewidth = 8)
       # ax4.plot(xNegErrDat)
       # ax4.plot(xPosErrDat)
    #    ax5 = fig.add_subplot(3, 4, 11, sharex=ax4, sharey=ax4 )
        ax4.errorbar( xCount, xMean, yerr=[xNegErr, xPosErr], elinewidth=2)
        ax4.errorbar( xCount, xMean, yerr=[xNegZero, xPosHun])
#        fill_between(xMean, xNegErr, xPosErr)
        #", alpha = 0.5, edgecolor = '#CC4F1B', facecolor = '#FF9848')
        ax4.set_xlabel('generation')
        ax4.set_ylabel('average fitness')
        
        #yerr = np.percentile(allData, 0)
       # y = np.mean(allData, axis=1, dtype= np.float64)
       # ax3.errorbar(percentile1, )
        plt.show()

    def read_files(self):
        fig = plt.figure(figsize = (24,12))
        allData = []
        for i in range (0, self.amountRuns_var.get()):
            print('i = ', str(i))
            with open('results\\SavedGenerations'+str(i)+'.csv', 'rb') as csvFile:
                settingsReader = csv.reader(csvFile, delimiter =',', quotechar='|')
                avgFitCol = (self.populationSize_var.get() + 2)
                bestFitCol = (self.populationSize_var.get() + 6)
                generationData =[]
                bestFitData =[]
                for row in settingsReader:
                        content = float(row[avgFitCol])
                        generationData.append(float(content))
                        bestFitData.append(float(row[bestFitCol]))
                        #print float(content)
                allData.append(generationData)
                ax1 = fig.add_subplot(5,4,1 + i)
                ax1.set_xlabel('generation')
                ax1.set_ylabel('fitness')
                ax1.plot(generationData)
                ax2 = fig.add_subplot(5,4,1 + i)
                ax2.plot(bestFitData)
        print allData
        arrayLength = np.shape(allData)
        print(arrayLength)
        #for i in allData:
        ax3 = fig.add_subplot(5,4,19)
        for i in range(0, arrayLength[0]):
            ax3.plot(allData[i])
        #ax3.plot(allData[0])
        #ax3.plot(allData[1])
        #ax3.plot(allData[2])
        #ax3.plot(allData[3])
        #ax3.plot(allData[4])
        #ax3.plot(allData[5])
        #ax3.plot(allData[6])
        #ax3.plot(allData[7])
        ax3.set_xlabel('generation')
        ax3.set_ylabel('fitness')
        
        xMean = []
        xMedian = []
        xCount = []
        xPosErrDat = []
        xNegErrDat = []
        xPosErr = []
        xNegErr = []
        for i in range(0, 30): # this needs to be within bounds
            y = meanColumn(allData, i)
            xMean.append(y)
            y = medianColumn(allData, i)
            xMedian.append(y)
            xCount.append(i)
            e = percentileColumn(allData, i , 40)
            xNegErrDat.append(e)
            xNegErr.append( y - e)
            e = percentileColumn(allData, i , 60)
            xPosErrDat.append(e)
            xPosErr.append( e - y)
 
        print (y)
        print ("x = ")
        print (xMean)
        print ("neg = ")
        print (xNegErr)
        print ("pos = ")
        print (xPosErr)
        ax4 = fig.add_subplot(5, 4, 20)
#        y = np.mean(allData, axis = 1)
        ax4.plot(xMean)
        ax4.plot(xMedian)
       # ax4.plot(xNegErrDat)
       # ax4.plot(xPosErrDat)
    #    ax5 = fig.add_subplot(3, 4, 11, sharex=ax4, sharey=ax4 )
        ax4.errorbar( xCount, xMean, yerr=[xPosErr, xNegErr])
#        fill_between(xMean, xNegErr, xPosErr)
        #", alpha = 0.5, edgecolor = '#CC4F1B', facecolor = '#FF9848')
        ax4.set_xlabel('generation')
        ax4.set_ylabel('average fitness')
        
        #yerr = np.percentile(allData, 0)
       # y = np.mean(allData, axis=1, dtype= np.float64)
       # ax3.errorbar(percentile1, )
        plt.show()

                #print ', '.join(row)

    def run(self):
        ''' Run the app '''
        self.mainloop()
 
app = EvoBotApplication(tk.Tk())
app.run()

"""
class EvoBotApplication(tk.Frame): 
    def __init__(self, 
                 master = None, 
                 width = 500, 
                 height = 500):
        tk.Frame.__init__(self, master)
        self.master.title('EVOBOT')
        self.pack_propagate(0) # size specification takes effect
        self.pack() #flexible pack layout manager
        self.greeting_var = tk.StringVar()
        self.greeting = tk.OptionMenu(self, 
                                      self.greeting_var, 
                                      'hello',
                                      'goodbye')
        self.greeting_var.set('hello') 
        self.recipient_var = tk.StringVar()
        self.recipient = tk.Entry(self,
                                  textvariable=self.recipient_var)
        self.recipient_var.set('world')
 
        # The go button
        self.go_button = tk.Button(self,
                                   text='Go',
                                   command=self.print_out)
 
        # Put the controls on the form
        self.go_button.pack(fill=tk.X, side=tk.BOTTOM)
        self.greeting.pack(fill=tk.X, side=tk.TOP)
        self.recipient.pack(fill=tk.X, side=tk.TOP)
 
    def print_out(self):
        ''' Print a greeting constructed
            from the selections made by
            the user. '''
        print('%s, %s!' % (self.greeting_var.get().title(),
                           self.recipient_var.get()))
    def run(self):
        ''' Run the app '''
        self.mainloop()
 
app = EvoBotApplication(tk.Tk())
app.run()
"""

"""
        self.grid()
        self.createWidgets()
    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command = self.quit)
        self.quitButton.grid()
"""
#        return super(Application, self).__init__(master, cnf, **kw)

"""
root = Tk();
root.title("EVOBOT");
root.geometry("500x500");

app = Frame(root);
app.grid();

evolveButton = Button(app, text = "EVOLVOBUTTON");

evolveButton.grid();

root.mainloop();
"""