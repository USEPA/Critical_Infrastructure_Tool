import unittest
import json
import os
import csv

class TestInfra(unittest.TestCase):

    def test_Parent(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        fifty_noREduction = open(master_path+"\\TestFiles\\ParentReduction\\fiftyNoRed.csv", "r")
        read_file = csv.reader(fifty_noREduction)
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
        
        fifty_Reduction = open(master_path+"\\TestFiles\\ParentReduction\\fiftRED.csv", "r")
        read_file = csv.reader(fifty_Reduction)
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
                   if float(numbers[ind])<float(numbers2[ind2]):
                       continue
                   else:
                       print("Reducing Parent Efficacy did not produce correct value,a value is larger. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        fifty_Reduction.close()
        fifty_noREduction.close()

        
    def test_fifty_eighty(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        fifty_noREduction = open(master_path+"\\TestFiles\\Percent\\fiftyNoRed.csv", "r")
        read_file = csv.reader(fifty_noREduction)
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
        Eighty_Reduction = open(master_path+"\\TestFiles\\Percent\\80NotReduced.csv", "r")
        read_file = csv.reader(Eighty_Reduction)
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
                   if float(numbers[ind])>float(numbers2[ind2]):
                       continue
                   else:
                       print("The test has failed 80% should be lower then 50%. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        fifty_noREduction.close()
        Eighty_Reduction.close()

        
    def test_RemediationFactor(self):
            master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
            RemFactor1 = open(master_path+"\\TestFiles\\Remediation\\Rem1.csv", "r")
            read_file = csv.reader(RemFactor1)
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
            RemFactor_point1 = open(master_path+"\\TestFiles\\Remediation\\lowRem.csv", "r")
            read_file = csv.reader(RemFactor_point1)
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
                       if float(numbers[ind])<=float(numbers2[ind2]):
                           
                           continue
                       else:
                           print(numbers[ind],numbers2[ind2])
                           print("The test has failed 80% should be lower then 50%. TEST FAIL")
                           self.assertFalse(True)
                    else:
                        continue

            self.assertTrue(check)
            RemFactor1.close()
            RemFactor_point1.close()
            
    def test_RepairFactor(self):
            master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
            LowRep = open(master_path+"\\TestFiles\\RepairFactor\\LOW.csv", "r")
            read_file = csv.reader(LowRep)
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
            HighRep = open(master_path+"\\TestFiles\\RepairFactor\\HIGH.csv", "r")
            read_file = csv.reader(HighRep)
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
                       if float(numbers[ind])>=float(numbers2[ind2]):
                           
                           continue
                       else:
                           print(numbers[ind],numbers2[ind2])
                           print("Repair Factor has shown unequal result. TEST FAIL")
                           self.assertFalse(True)
                    else:
                        continue

            self.assertTrue(check)
            LowRep.close()
            HighRep.close()
   


    def test_stoichFactor(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        StoichLow = open(master_path+"\\TestFiles\\StoichiometricFactor\\\STOICH1.csv", "r")
        read_file = csv.reader(StoichLow)
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
        StoichHigh = open(master_path+"\\TestFiles\\StoichiometricFactor\\STOICH400.csv", "r")
        read_file = csv.reader(StoichHigh)
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
                   if float(numbers[ind])>=float(numbers2[ind2]):
                       
                       continue
                   else:
                       print(numbers[ind],numbers2[ind2])
                       print("Stoichiometric factor has given an unequal result. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        StoichLow.close()
        StoichHigh.close()
    def test_backup(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        NOBack = open(master_path+"\\TestFiles\\backup\\NOBACKUP.csv", "r")
        read_file = csv.reader(NOBack)
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
        WithBack = open(master_path+"\\TestFiles\\backup\\WithBackup.csv", "r")
        read_file = csv.reader(WithBack)
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
                   if i=="Emergency Services":
                       if float(numbers[ind])>=float(numbers2[ind2]):
                            continue
                       else:
                           print(numbers[ind],numbers2[ind2])
                           print("Back Up is incorrect. TEST FAIL")
                           self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        NOBack.close()
        WithBack.close()
    def test_Outages(self):
        master_path = os.path.dirname(os.path.abspath('infrastructures_v4.py'))
        NoOut = open(master_path+"\\TestFiles\\AdditionalOut\\NOADDITIONALOUT.csv", "r")
        read_file = csv.reader(NoOut)
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
        WithOut = open(master_path+"\\TestFiles\\AdditionalOut\\WIthAdditional.csv", "r")
        read_file = csv.reader(WithOut)
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
                   if float(numbers[ind])<=float(numbers2[ind2]):
                       
                       continue
                   else:
                       print(numbers[ind],numbers2[ind2])
                       print("Error with Additional has given an unequal result. TEST FAIL")
                       self.assertFalse(True)
                else:
                    continue

        self.assertTrue(check)
        NoOut.close()
        WithOut.close()
    
                 
        
        
  
  
if __name__ =='__main__':
    unittest.main()
