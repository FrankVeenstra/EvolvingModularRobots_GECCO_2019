# -*- coding: utf-8 -*-
import numpy as np
#import math
import matplotlib.pyplot as plt
import random
import time; 
import sys;
import os.path 
import os; 


def VectorCreate(length):
    vector1 = []
    for i in range(length):
        vector1.append(0)
    for i in range(0, length, 2):
        vector1[i] = 1
    return vector1

def Fitness(v1,v2):
    d = 0
    for i in range(10):
        c = ((v1[i]-v2[i])**2)
        d = d + c
#        print ":::", v1[i] ,",", v2[i], ' and ', d
    a = d/10
    b = 1- a
    return b
    
def Fitness2(neuronValues):
    diff=0.0
    for i in range(1,9): 
        for j in range(0,9):
            diff=diff + abs(neuronValues[i][j]-neuronValues[i][j+1])
            diff=diff + abs(neuronValues[i+1][j]-neuronValues[i][j]) 
    diff=diff/(2*8*9)
    return diff
    
    """
def Fitness2(neuronValues):
    diff = 0
    for (i,j) in neuronValues(range(9), repeat=2):
        diff += abs(neuronValues[i,j] - neuronValues[i,j+1])
        diff += abs(neuronValues[i,j] - neuronValues[i+1,j])
    return diff/(2*9*9)
"""
def MatrixCreate(rows, columns):
    my_matrix = [[0 for x in xrange(columns)] for x in xrange(rows)]
    return my_matrix

def MatrixRandomize(v):
    for i in range(len(v)):
       # my_matrix[i].append(0)
        for j in range(len(v[i])):
            v[i][j] = random.uniform(-1.0, 1.0)
    return v
    
def MatrixPerturb(p, prob):
    offspring = MatrixCreate(len(p),len(p[0]))
    for i in range(len(p)):
        for j in range(len(p[i])):
            offspring[i][j] = p[i][j]
            if prob > random.random():
                offspring[i][j] = random.uniform(-1.0, 1.0)
                #if a > offspring[i][j]:
                #    offspring[i][j] = a
    return offspring


#def Fitness(v):
#    total = 0
#    count = 0
#    for i in range(len(v)):
#        for j in range(len(v[i])):
#            count += 1
#            total += v[i][j]
#    total = total / count
#    return total
    
def initializeNeuronValues(parent):
    neuronValues = MatrixCreate(10,10)
    for i in range(len(neuronValues)):
        neuronValues[0][i] = 0.5
    return neuronValues

def initializeNewNeuronValues(parent):
    for i in range(len(neuronValues)):
        neuronValues[0][i] = 0.5
        for j in range(9):
            if j > 0:
                neuronValues[j][i] = neuronValues[j][i]


def Update(neuronValues, synapses, i):
    for m in range(len(synapses)):
        temp = neuronValues[i][m]
        for n in range(len(synapses)):
            temp += neuronValues[i][n] * (synapses[m][n])
            if temp > 1:
               # print "i = ", i
               temp = 1           
            elif temp < 0:
                temp = 0
            neuronValues[i+1][m] = temp
        #print neuronValues[0][0]
    return neuronValues

"""
def Update(neuronValues, synapses, i):
    for m in range(len(synapses)):
        neuronValues[i+1][m] = neuronValues[i][m]
        for n in range(len(synapses)):
            neuronValues[i+1][m] += neuronValues[i][m] * (synapses[m][m])
            if neuronValues[i+1][m] > 1:
               # print "i = ", i
                neuronValues[i+1][m] = 1           
            elif neuronValues[i+1][m] < 0:
                neuronValues[i+1][m] = 0
        #print neuronValues[0][0]
    return neuronValues


def Update(neuronValues, synapses, i):
    if i != 0:
        for j in range(len(neuronValues[0])):
            temp = 0
            for k in range(len(neuronValues[0])):
                temp += synapses[j][k]*neuronValues[i-1][k]
            if temp<0:
                temp=0
            if temp>1:
                temp=1
            neuronValues[i][j] = temp
    return neuronValues
"""
def Fitness3_Get(synapses):

 #   weightsFileName = "weights.dat" 
 #   fitFileName = "fits.dat"
 #   print synapses
    file = open("C:\Users\Frank\Desktop\Bullet\weights.dat", "w")
    file.write("synapses ,")
    for m in range(sensoryNeurons):
        for n in range(motorNeurons):
            file.write(str(synapses[m][n]))
            file.write(", ")
    file.write("\n")
    file.write
    file.close()
    path = "C:\Users\Frank\Desktop\App_RagdollDemo_vs2010_debug.exe"
    os.system(path);


def Fitness3():
 #  path = "C:\\Users\\Frank\\Desktop\\Bullet/weights.dat"
 #  os.system(path) 
    while not os.path.exists("C:\Users\Frank\Desktop\\Bullet/fitness.dat") :
        time.sleep(0.5); 
    os.remove("C:\Users\Frank\Desktop\\Bullet/fitness.dat")
    os.remove("C:\Users\Frank\Desktop\\Bullet/weights.dat")

    

  #  Simulate_Robot()
#
 #   Wait_For_Fitness_File(fitFileName)
#
 #   fitness = Fitness_Collect_From_File(fitFileName)
#
 #   Delete_File(weightsFileName)
#
 #   Delete_File(fitFileName)
#
 #   return( fitness )


sensoryNeurons = 4;
motorNeurons = 11;
numGenerations = 1000;
#fits = Update(numSensors.
fits = MatrixCreate(1, numGenerations)

parent = MatrixCreate(sensoryNeurons,motorNeurons) 
parent = MatrixRandomize(parent)
#print "parent: " , parent
Fitness3_Get(parent) 

fitnessFile = open("C:\Users\Frank\Desktop\Bullet/fitness.dat", "r")
fitnessValue = float(fitnessFile.read(10))
fitnessValueParent = fitnessValue
fitnessFile.close()

child = parent
#print "parent" , fitnessValue

Fitness3()

for i in range(numGenerations):
    #print " "
    child = MatrixPerturb(parent, 0.05)
    #print "child ", child
    Fitness3_Get(child)
    fitnessFile = open("C:\Users\Frank\Desktop\Bullet/fitness.dat", "r")
    fitnessValue = float(fitnessFile.read(10))
    fitnessFile.close()
    
    Fitness3()

    print "generation: ", i, ", fitness parent:", fitnessValueParent, ", fitness child:", fitnessValue 
    
    if fitnessValue > fitnessValueParent:
        fitnessValueParent = fitnessValue
        parent = child


#print "child" , fitnessValue

"""for i in range(numGenerations):
    #print parent
    fitnessFile = open("C:\Users\Frank\Desktop\Bullet/fitness.dat", "r")
    fitnessValue = fitnessFile.read(10)
    fitnessFile.close()
    
    fits[0][i] = float(fitnessValue)
#    parentFitness = fitnessValue;
    Fitness3()
    child = MatrixPerturb(parent,0.05)
    Fitness3_Get(child)
#   print child
    print i, fitnessValue
   """ 



#neuronValues = initializeNeuronValues(parent)
##print neuronValues[1] 

##for i in range(9):
# #   neuronValues = Update(neuronValues, parent, i)
#    #print i +1
#    #print neuronValues[i+1]
#    
##Genes = MatrixCreate(10,10)
##print neuronValues#
#
#"""Genes = neuronValues
#for i in range(10):
#    for j in range(10):
#        Genes[i][j] = neuronValues[j][i]
#"""
#"""
#plt.imshow(neuronValues, cmap=plt.cm.gray, aspect='auto',interpolation='nearest')
#plt.show()
#plt.xlabel("update iteration")
#plt.ylabel("neuron") 
#"""###

#actualNeuronValues = neuronValues[9]
#desiredNeuronValues = VectorCreate(10)
##print 'desval: ', desiredNeuronValues
##print 'distance = ', MeanDistance(actualNeuronValues, desiredNeuronValues)
#fitnessVector = []
#parentFitness = 0
#for i in range(9):
#    neuronValues = Update(neuronValues, parent, i)
#    #print "neuronValues = ", neuronValues[i]
#    #meandis = Fitness(neuronValues[i], desiredNeuronValues)
#    #  print "meandis ", i ," = ", meandis
#    actualNeuronValues = neuronValues[9]
#    desiredNeuronValues = VectorCreate(10)
#    #parentFitness = Fitness(actualNeuronValues, desiredNeuronValues)
#    parentFitness = Fitness2(neuronValues)


#initialNeuronValues = neuronValues
#
#fig = plt.figure(figsize=(18,6))
#ax1 = fig.add_subplot(1,3,1)
#init_neurons = np.copy(neuronValues)
#ax1.imshow(init_neurons, cmap=plt.cm.gray, aspect='auto',interpolation='nearest')
#
#
#for currentGeneration in range(0,1000):
#    #print neuronValues[1] 
#    """if currentGeneration == 0: 
#        for i in range(9):
#            neuronValues = Update(neuronValues, parent, i)
#            #print "neuronValues = ", neuronValues[i]
#            meandis = Fitness2(neuronValues[i], desiredNeuronValues)
#            #  print "meandis ", i ," = ", meandis
#        actualNeuronValues = neuronValues[9]
#        desiredNeuronValues = VectorCreate(10)
#        parentFitness = MeanDistance(actualNeuronValues, desiredNeuronValues)
#        #print "parfit = " , parentFitness """
    
##    print currentGeneration, parentFitness 
#    child = MatrixPerturb(parent,0.05) 
#    for i in range(9):
#            neuronValues = Update(neuronValues, child, i)
#            #print "neuronValues = ", neuronValues[i]
#            #meandis = Fitness(neuronValues[i], desiredNeuronValues)
#            #  print "meandis ", i ," = ", meandis
#            
#    actualNeuronValues = neuronValues[9]
#    
#    #childFitness = Fitness(actualNeuronValues, desiredNeuronValues)
#    childFitness = Fitness2(neuronValues)
#    
#    if childFitness != parentFitness:
#        print parentFitness, ' and ', childFitness
#    if ( childFitness > parentFitness ):
#        parent = child 
#        parentFitness = childFitness
#        #print 'something'
#    fitnessVector.append(parentFitness)#
#
#print "fitnessVector = " , fitnessVector
#


#ax2 = fig.add_subplot(1,3,2)
#init_neurons = np.copy(neuronValues)
#ax2.imshow(init_neurons, cmap=plt.cm.gray, aspect='auto',interpolation='nearest')
#Show fitnessVector        

#ax3 = fig.add_subplot(1,3,3)
#ax3.plot(fitnessVector)

#ax1.set_xlabel('neuron')
#ax1.set_ylabel('Update Iteration')

#ax2.set_xlabel('neuron')
#ax2.set_ylabel('Update Iteration')

#ax3.set_xlabel('generation')
#ax3.set_ylabel('fitness')


##plt.plot(fitnessVector)      
#plt.show()
##plt.xlabel("update iteration")
##plt.ylabel("neuron")                 
                        
                                        
## show the neuronValues        
##plt.imshow(neuronValues, cmap=plt.cm.gray, aspect='auto',interpolation='nearest')
##plt.show()
##plt.xlabel("update iteration")
##plt.ylabel("neuron") 