import unittest
import json
import os
import csv
class TestSensistivity(unittest.TestCase):
    def test_days(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        Infra = open(master_path+"\\TestSens\\Days\\Harvey1.csv", "r")
        read_file = csv.reader(Infra)
        names=[]
        names=[0 for i in range(10)]
        numbers=[]
        numbers=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names[i]=s[1]
            numbers[j]=s[2]
            j=j+1
            i=i+1
        
        Sensitivity = open(master_path+"\\TestSens\\Days\\\Days Backup_0.csv", "r")
        read_file = csv.reader(Sensitivity)
        names2=[]
        names2=[0 for i in range(10)]
        numbers2=[]
        numbers2=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names2[i]=s[1]
            numbers2[j]=s[2]
            j=j+1
            i=i+1
        check=True
        for i in names:  
            for z in names2:
                if i==z and i !="Sectors":
                   ind=names.index(i)
                   ind2=names2.index(z)
                   if float(numbers[ind])==float(numbers2[ind2]):
                       continue
                   else:
                       print("Both Scenarios are not the same check days of recovery. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        Infra.close()
        Sensitivity.close()
    def test_Eff(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        Infra = open(master_path+"\\TestSens\\Efficiency\\harv.csv", "r")
        read_file = csv.reader(Infra)
        names=[]
        names=[0 for i in range(10)]
        numbers=[]
        numbers=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names[i]=s[1]
            numbers[j]=s[2]
            j=j+1
            i=i+1
        
        Sensitivity = open(master_path+"\\TestSens\\Efficiency\\Efficiency of Backups_0.csv", "r")
        read_file = csv.reader(Sensitivity)
        names2=[]
        names2=[0 for i in range(10)]
        numbers2=[]
        numbers2=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names2[i]=s[1]
            numbers2[j]=s[2]
            j=j+1
            i=i+1
        check=True
        for i in names:  
            for z in names2:
                if i==z and i !="Sectors":
                   ind=names.index(i)
                   ind2=names2.index(z)
                   if float(numbers[ind])==float(numbers2[ind2]):
                       continue
                   else:
                       print("Both Scenarios are not the same check Efficiency. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        Infra.close()
        Sensitivity.close()
    def test_InitialEfficiency(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        Infra = open(master_path+"\\TestSens\\InitialEfficiency\\harvInitial.csv", "r")
        read_file = csv.reader(Infra)
        names=[]
        names=[0 for i in range(10)]
        numbers=[]
        numbers=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names[i]=s[1]
            numbers[j]=s[2]
            j=j+1
            i=i+1
        
        Sensitivity = open(master_path+"\\TestSens\\InitialEfficiency\\Initial Efficiency_50.csv", "r")
        read_file = csv.reader(Sensitivity)
        names2=[]
        names2=[0 for i in range(10)]
        numbers2=[]
        numbers2=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names2[i]=s[1]
            numbers2[j]=s[2]
            j=j+1
            i=i+1
        check=True
        for i in names:  
            for z in names2:
                if i==z and i !="Sectors":
                   ind=names.index(i)
                   ind2=names2.index(z)
                   if float(numbers[ind])==float(numbers2[ind2]):
                       continue
                   else:
                       print("Both Scenarios are not the same Initial Efficiency. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        Infra.close()
        Sensitivity.close()
    def test_RepairFactor(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        Infra = open(master_path+"\\TestSens\\RepairFactor\\Harvey1.csv", "r")
        read_file = csv.reader(Infra)
        names=[]
        names=[0 for i in range(10)]
        numbers=[]
        numbers=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names[i]=s[1]
            numbers[j]=s[2]
            j=j+1
            i=i+1
        
        Sensitivity = open(master_path+"\\TestSens\\RepairFactor\\Repair Factors_10.csv", "r")
        read_file = csv.reader(Sensitivity)
        names2=[]
        names2=[0 for i in range(10)]
        numbers2=[]
        numbers2=[0 for i in range(10)]
        i=0
        j=0
        for s in read_file:
            names2[i]=s[1]
            numbers2[j]=s[2]
            j=j+1
            i=i+1
        check=True
        for i in names:  
            for z in names2:
                if i==z and i !="Sectors":
                   ind=names.index(i)
                   ind2=names2.index(z)
                   if float(numbers[ind])==float(numbers2[ind2]):
                       continue
                   else:
                       print("Both Scenarios are not the same Initial Efficiency. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        Infra.close()
        Sensitivity.close()
if __name__ =='__main__':
    unittest.main()
