import pandas as pd
import numpy as np


# relative path to the original master compendium data file
df = pd.read_excel('BioDeconProcessed_Original.xlsx', sheet_name = 'ProcessedData')

# relative path to the surfaces master excel file 
# has the rep surface for each record in order and the corresponding representative surface
# as well as the surface type lookup categories
surfacesMaster = pd.read_excel('SurfacesMaster.xlsx', sheet_name = 'Sheet2')

# pulling in the representative surfaces from the surface master and adding the column to the main data set
df['RepSurface'] = surfacesMaster.RepSurface

# creating a smaller data frame with only relevant columns so we can further clean and convert this subset of data
cd = pd.DataFrame()

cd['Reference'] = df.Ref
cd['AppMethod'] = df.AppMeth
cd['Surface'] = df.RepSurface
cd['Loading'] = df.LoadingNum
cd['LoadingUn'] = df.LoadingUn
cd['LPosRec'] = df.LPosRec
cd['Area'] = df.CoupArea
cd['AreaUn'] = df.CoupAreaUn
cd['ConcDose'] = df.ConcDoseNum
cd['ConcDoseUn'] = df.ConcDoseUn
cd['OriginalConcDose'] = df.ConcDoseNum
cd['OriginalConcDoseUn'] = df.ConcDoseUn
cd['DeconAgent'] = surfacesMaster.GeneralDeconAgent
cd['ClO2'] = df['ClO2(ppm)']
cd['MB'] = df['MB(mg/L)']
cd['H2O2'] = df['H2O2(ppm)']
cd['VolApp'] = df.VolApp
cd['VolAppUn'] = df.VolAppUn

# temp is always given in celsius
cd['Temp'] = df.TempNum

# relative humidity is always given in %
cd['RH'] = df.RHNum

# conttimenummin is always given in minutes
cd['ContTime'] = df.ContTimeNumMin
cd['EffMeas'] = df.EffMeas
cd['Eff'] = df.Eff
cd['EffVar'] = df.EffVar
cd['EffVarStat'] = df.EffVarStat

cd['Positives'] = df.Positives
cd['N'] = df.N

# Nt is the number of spores that are recovered from the test coupon after treatment (this will need to be calculated)
cd['Nt'] = np.nan

# number of reapplications
cd['ReApp'] = df.Reapp

cd['Rinsate'] = df.Rinsate
cd['RinsateUn'] = df.RinsateUn

# indoor surface categories
cd['IndoorInterior'] = surfacesMaster.IndoorInterior
cd['IndoorExterior'] = surfacesMaster.IndoorExterior
cd['IndoorCarpet'] = surfacesMaster.IndoorCarpet
cd['IndoorNonCarpet'] = surfacesMaster.IndoorNonCarpet
cd['IndoorCeilings'] = surfacesMaster.IndoorCeilings
cd['HVAC'] = surfacesMaster.HVAC
cd['IndoorMisc'] = surfacesMaster.IndoorMisc

# outdoor surface categories
cd['OutdoorExterior'] = surfacesMaster.OutdoorExterior
cd['Roofing'] = surfacesMaster.Roofing
cd['Pavement'] = surfacesMaster.Pavement
cd['Water'] = surfacesMaster.Water
cd['Soil'] = surfacesMaster.Soil
cd['OutdoorMisc'] = surfacesMaster.OutdoorMisc

# underground surface categories
cd['UndergroundInterior'] = surfacesMaster.UndergroundInterior
cd['UndergroundCarpet'] = surfacesMaster.UndergroundCarpet
cd['UndergroundNonCarpet'] = surfacesMaster.UndergroundNonCarpet
cd['UndergroundCeilings'] = surfacesMaster.UndergroundCeilings
cd['UndergroundMisc'] = surfacesMaster.UndergroundMisc

# concatenation of surface types within each scenario
cd['Indoor'] = surfacesMaster.IndoorCategories
cd['Outdoor'] = surfacesMaster.OutdoorCategories
cd['Underground'] = surfacesMaster.UndergroundCategories

# clean up inconsistent naming within string columns
cd.loc[(cd.AppMethod == 'liquid (ambiguous)'),'AppMethod'] = 'liquid ambiguous'
cd.loc[(cd.EffMeas == 'Qual Pos'), 'EffMeas'] = 'QualPos'
cd.loc[(cd.EffMeas == 'Qualneg'), 'EffMeas'] = 'QualNeg'
cd.loc[(cd.EffMeas == 'LRsurf'), 'EffMeas'] = 'LRSurf'
cd.loc[(cd.EffMeas == 'Lsurv'), 'EffMeas'] = 'LSurv'
cd.loc[(cd.AreaUn == 'inch^2'), 'AreaUn'] = 'in^2'
cd.loc[(cd.LoadingUn == 'spores/L'), 'LoadingUn'] = 'CFU/L'

# clean numerical columns of various strings that cannot be converted into values
strings = ['unlisted', 'undefined', 'not reported', 'Not reported', 'Not Reported', 'not applicable',
           'Not Applicable', 'ambiguous', 'Ambiguous', 'authors censor', 'inconclusive', 'NA', 'nd', 'No Value', 'not significant', 'NT', 'NR', 'as needed to keep wetted', 'Not significant', 'until wetted', 
		   'trigger pulls of sprayer', '0.5 LR', 'no rinsate', 'discarded', 'combined', 
		   'discarded (but spores filtered out)']

for i in strings:
    cd.loc[cd.Loading == i, 'Loading'] = np.nan
    cd.loc[cd.Area == i, 'Area'] = np.nan
    cd.loc[cd.Eff == i, 'Eff'] = np.nan
    cd.loc[cd.LPosRec == i, 'LPosRec'] = np.nan
    cd.loc[cd.Temp == i, 'Temp'] = np.nan
    cd.loc[cd.RH == i, 'RH'] = np.nan
    cd.loc[cd.ReApp == i, 'ReApp'] = np.nan
    cd.loc[cd.VolApp == i, 'VolApp'] = np.nan
    cd.loc[cd.VolAppUn == i, 'VolAppUn'] = np.nan
    cd.loc[cd.ConcDose == i, 'ConcDose'] = np.nan
    cd.loc[cd.ConcDoseUn == i, 'ConcDoseUn'] = np.nan
    cd.loc[cd.Rinsate == i, 'Rinsate'] = np.nan
    cd.loc[cd.N == i, 'N'] = np.nan

# a few more ambiguous strings need to be resolved
# as per the compendium, '>' and '<' are simply removed from values
cd.loc[cd.Eff == '>7', 'Eff'] = 7
cd.loc[cd.Eff == '>6', 'Eff'] = 6
cd.loc[cd.N == '>3', 'N'] = 3
cd.loc[cd.N == '>1', 'N'] = 1
cd.loc[cd.N == '>2', 'N'] = 2
cd.loc[cd.N == '>5', 'N'] = 5
cd.loc[cd.N == '> 1', 'N'] = 1

# as per the compendium and in order to remain conservative, ranges should be converted to the minimum value
cd.loc[cd.Eff == '50-75', 'Eff'] = 50
cd.loc[cd.Area == '100-361', 'Area'] = 100
cd.loc[cd.N == '2 or 4', 'N'] = 2
cd.loc[cd.N == '"2-4"', 'N'] = 2

# converting numerical columns to floats
cd['Loading'] = cd.Loading.astype(float)
cd['Area'] = cd.Area.astype(float)
cd['Eff'] = cd.Eff.astype(float)
cd['LPosRec'] = cd.LPosRec.astype(float)
cd['Temp'] = cd.Temp.astype(float)
cd['RH'] = cd.RH.astype(float)
cd['ReApp'] = cd.ReApp.astype(float)
cd['VolApp'] = cd.VolApp.astype(float)
cd['ConcDose'] = cd.ConcDose.astype(float)
cd['ClO2'] = cd.ClO2.astype(float)
cd['MB'] = cd.MB.astype(float)
cd['H2O2'] = cd.H2O2.astype(float)
cd['Positives'] = cd.Positives.astype(float)
cd['N'] = cd.N.astype(float)

# fix ambiguous naming of application methods
cd.loc[(cd.AppMethod == 'liquid'), 'AppMethod'] = 'liquid ambiguous'
cd.loc[(cd.AppMethod == 'liquid ambiguous'), 'AppMethod'] = 'liquid spray'
cd.loc[(cd.AppMethod == 'fumigation/liquid'), 'AppMethod'] = 'liquid spray'
cd.loc[(cd.AppMethod == 'liquid dropper'), 'AppMethod'] = 'liquid spray'
cd.loc[(cd.AppMethod == 'immersion'), 'AppMethod'] = 'liquid immersion'
cd.loc[(cd.AppMethod == 'foam ambiguous'), 'AppMethod'] = 'foam spray'

# remove records that don't list a treatment application method as they cannot be classified
appMethToDrop = [np.nan]
cd = cd[cd.AppMethod.apply(lambda x: x not in appMethToDrop)].copy()

# remove all qualpos/qualneg records
effToDrop = ['QualPos', 'QualNeg']
cd = cd[cd.EffMeas.apply(lambda x: x not in effToDrop)].copy()

# dropping all records that provide loading in CFU but give no area as these cannot be converted to CFU/area
indexCfuNoArea = cd[(cd['LoadingUn'] == 'CFU') & (np.isnan(cd['Area']))].index
cd.drop(indexCfuNoArea, inplace=True)

# changing the label of LRSurf to LR since we found out that there really isn't a distinction between
# the two based on EPA methodology
cd.loc[(cd.EffMeas == 'LRSurf'), 'EffMeas'] = 'LR'

# dividing all survfrac values greater than 1 by 100 as they are likely given in percentages but should be decimals
cd.loc[(cd.EffMeas == 'SurvFrac') & (cd.Eff > 1), 'Eff'] = cd['Eff'] / 100

# converting various efficacies to Nt
cd.loc[(cd.EffMeas == 'LSurv'), 'Nt'] = 10 ** cd['Eff']
cd.loc[(cd.EffMeas == '%Surv'), 'Nt'] = (cd['Eff'] / 100) * cd['Loading']
cd.loc[(cd.EffMeas == '%Kill'), 'Nt'] = (-1 * cd['Loading']) * (cd['Eff'] / 100)
cd.loc[(cd.EffMeas == 'LR'), 'Nt'] = 10 ** (cd['LPosRec'] - cd['Eff'])
cd.loc[(cd.EffMeas == 'SurvFrac'), 'Nt'] = cd['Loading'] * cd['Eff']

# converting all of the areas/volumes (and in some cases mass) in CoupArea
# to either cm^2 or cm^3 (or g for mass) so we have a standard
cd.loc[(cd.AreaUn == 'mL'),'AreaUn'] = 'cm^3'

cd.loc[(cd.AreaUn == 'L'),'Area'] = cd['Area'] * 1000
cd.loc[(cd.AreaUn == 'L'),'AreaUn'] = 'cm^3'

cd.loc[(cd.AreaUn == 'gallon'),'Area'] = cd['Area'] * 3785.41
cd.loc[(cd.AreaUn == 'gallon'),'AreaUn'] = 'cm^3'

cd.loc[(cd.AreaUn == 'm^3'),'Area'] = cd['Area'] * 1000000
cd.loc[(cd.AreaUn == 'm^3'),'AreaUn'] = 'cm^3'

cd.loc[(cd.AreaUn == 'uL'),'Area'] = cd['Area'] * 0.001
cd.loc[(cd.AreaUn == 'uL'),'AreaUn'] = 'cm^3'

cd.loc[(cd.AreaUn == 'm^2'),'Area'] = cd['Area'] * 10000
cd.loc[(cd.AreaUn == 'm^2'),'AreaUn'] = 'cm^2'

cd.loc[(cd.AreaUn == 'mm^2'),'Area'] = cd['Area'] * 0.01
cd.loc[(cd.AreaUn == 'mm^2'),'AreaUn'] = 'cm^2'

cd.loc[(cd.AreaUn == 'ft^2'),'Area'] = cd['Area'] * 929.03
cd.loc[(cd.AreaUn == 'ft^2'),'AreaUn'] = 'cm^2'

cd.loc[(cd.AreaUn == 'in^2'),'Area'] = cd['Area'] * 6.4516
cd.loc[(cd.AreaUn == 'in^2'),'AreaUn'] = 'cm^2'

cd.loc[(cd.AreaUn == 'kg'),'Area'] = cd['Area'] * 1000
cd.loc[(cd.AreaUn == 'kg'),'AreaUn'] = 'g'

# converting all of the VolApps to mL as a standard
cd.loc[(cd.VolAppUn == 'uL'),'VolApp'] = cd['VolApp'] * 0.001
cd.loc[(cd.VolAppUn == 'uL'),'VolAppUn'] = 'mL'

cd.loc[(cd.VolAppUn == 'L'),'VolApp'] = cd['VolApp'] * 1000
cd.loc[(cd.VolAppUn == 'L'),'VolAppUn'] = 'mL'

cd.loc[(cd.VolAppUn == 'L/m^2'),'VolApp'] = cd['VolApp'] * 1000
cd.loc[(cd.VolAppUn == 'L/m^2'),'VolAppUn'] = 'mL/m^2'

# dividing the VolApp by the area of the coupon for those with units of mL or g
cd.loc[(cd.VolAppUn == 'mL') & (pd.isnull(cd.Area) == False),'VolApp'] = cd['VolApp'] / cd['Area']
cd.loc[(cd.VolAppUn == 'g') & (pd.isnull(cd.Area) == False),'VolApp'] = cd['VolApp'] / cd['Area']
cd.loc[(cd.VolAppUn == 'mL') & (pd.isnull(cd.Area) == False),'VolAppUn'] = cd['VolAppUn'] + '/' + cd['AreaUn']
cd.loc[(cd.VolAppUn == 'g') & (pd.isnull(cd.Area) == False),'VolAppUn'] = cd['VolAppUn'] + '/' + cd['AreaUn']

# converting the m^2 and m^3 in VolAppUn to cm^2 and cm^3 in line with the conversions done on coupon area
cd.loc[(cd.VolAppUn == 'mL/m^2'),'VolApp'] = cd['VolApp'] * 0.01
cd.loc[(cd.VolAppUn == 'mL/m^2'),'VolAppUn'] = 'mL/cm^2'

cd.loc[(cd.VolAppUn == 'mL/m^3'),'VolApp'] = cd['VolApp'] * 0.01
cd.loc[(cd.VolAppUn == 'mL/m^3'),'VolAppUn'] = 'mL/cm^3'

# converting all of the loadings to CFU/cm^2 or CFU/cm^3
# we also need to convert the PosRec and Nt at the same time since they (should) have the same units as the Loading
cd.loc[(cd.LoadingUn == 'CFU/L'),'Loading'] = cd['Loading'] / 1000
cd.loc[(cd.LoadingUn == 'CFU/L'),'LPosRec'] = np.log10((10 ** cd['LPosRec']) / 1000)
cd.loc[(cd.LoadingUn == 'CFU/L'),'Nt'] = cd['Nt'] / 1000
cd.loc[(cd.LoadingUn == 'CFU/L'),'LoadingUn'] = 'CFU/cm^3'

cd.loc[(cd.LoadingUn == 'CFU/100cm^2'),'Loading'] = cd['Loading'] / 100
cd.loc[(cd.LoadingUn == 'CFU/L'),'LPosRec'] = np.log10((10 ** cd['LPosRec']) / 100)
cd.loc[(cd.LoadingUn == 'CFU/100cm^2'),'Nt'] = cd['Nt'] / 100
cd.loc[(cd.LoadingUn == 'CFU/100cm^2'),'LoadingUn'] = 'CFU/cm^2'

cd.loc[(cd.LoadingUn == 'CFU/mL'),'LoadingUn'] = 'CFU/cm^3'
cd.loc[(cd.LoadingUn == 'CFU/mL'),'LoadingUn'] = 'CFU/cm^3'

# convert the loadings given in log(CFU) to just CFU
cd.loc[(cd.LoadingUn == 'log(CFU)'),'Loading'] = 10 ** cd['Loading']
cd.loc[(cd.LoadingUn == 'log(CFU)'),'LoadingUn'] = 'CFU'

# dividing all of the Loadings, PosRecs, and Nts by the area of the coupon for those with units of CFU 
cd.loc[(cd.LoadingUn == 'CFU') & (pd.isnull(cd.Area) == False),'Loading'] = cd['Loading'] / cd['Area']
cd.loc[(cd.LoadingUn == 'CFU') & (pd.isnull(cd.Area) == False),'LPosRec'] = np.log10((10 ** cd['LPosRec']) / cd['Area'])
cd.loc[(cd.LoadingUn == 'CFU') & (pd.isnull(cd.Area) == False),'Nt'] = cd['Nt'] / cd['Area']
cd.loc[(cd.LoadingUn == 'CFU') & (cd.AreaUn == 'cm^3') & (pd.isnull(cd.Area) == False),'LoadingUn'] = 'CFU/cm^3'
cd.loc[(cd.LoadingUn == 'CFU') & (cd.AreaUn == 'cm^2') & (pd.isnull(cd.Area) == False),'LoadingUn'] = 'CFU/cm^2'
cd.loc[(cd.LoadingUn == 'CFU') & (cd.AreaUn == 'g') & (pd.isnull(cd.Area) == False),'LoadingUn'] = 'CFU/g'

# remove units for empty doses
cd.loc[(np.isnan(cd['ConcDose'])),'ConcDoseUn'] = np.nan

# concdoseun conversions
cd.loc[(cd.ConcDoseUn == 'v%'),'ConcDoseUn'] = 'vol%'
cd.loc[(cd.ConcDoseUn == '%'),'ConcDoseUn'] = 'vol%'
cd.loc[(cd.ConcDoseUn == '% ambiguous'),'ConcDoseUn'] = 'vol%'
cd.loc[(cd.ConcDoseUn == '% (ambiguous)'),'ConcDoseUn'] = 'vol%'

cd.loc[(cd.ConcDoseUn == 'wt% (liquid applied)'),'ConcDoseUn'] = 'wt%'
cd.loc[(cd.ConcDoseUn == 'wt% in wetting liquid'),'ConcDoseUn'] = 'wt%'

cd.loc[(cd.ConcDoseUn == 'wt%'),'ConcDose'] = cd['ConcDose'] * 10000
cd.loc[(cd.ConcDoseUn == 'wt%'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == 'wt% NaOCl'),'ConcDose'] = cd['ConcDose'] * 10000
cd.loc[(cd.ConcDoseUn == 'wt% NaOCl'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == '% wt/vol (ambiguous)'),'ConcDose'] = cd['ConcDose'] * 10000
cd.loc[(cd.ConcDoseUn == '% wt/vol (ambiguous)'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == '% wt/vol'),'ConcDose'] = cd['ConcDose'] * 10000
cd.loc[(cd.ConcDoseUn == '% wt/vol'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == '% w/v'),'ConcDose'] = cd['ConcDose'] * 10000
cd.loc[(cd.ConcDoseUn == '% w/v'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == 'ppmv'),'ConcDoseUn'] = 'mg/L'
cd.loc[(cd.ConcDoseUn == 'ppm'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == 'ug/L FAC'),'ConcDoseUn'] = 'ug/L'
cd.loc[(cd.ConcDoseUn == 'ppm'),'ConcDoseUn'] = 'mg/L'
cd.loc[(cd.ConcDoseUn == 'maximum ppm'),'ConcDoseUn'] = 'mg/L'
cd.loc[(cd.ConcDoseUn == 'FAC ppm (FAC mg/L)'),'ConcDoseUn'] = 'mg/L'
cd.loc[(cd.ConcDoseUn == 'mg tablet/L'),'ConcDoseUn'] = 'mg/L'

cd.loc[(cd.ConcDoseUn == 'mg/L'),'ConcDose'] = cd['ConcDose'] / 1000000
cd.loc[(cd.ConcDoseUn == 'mg/L'),'ConcDoseUn'] = 'g/mL'

cd.loc[(cd.ConcDoseUn == 'g/m^3'),'ConcDose'] = cd['ConcDose'] / 1000000
cd.loc[(cd.ConcDoseUn == 'g/m^3'),'ConcDoseUn'] = 'g/mL'

cd.loc[(cd.ConcDoseUn == 'g/L'),'ConcDose'] = cd['ConcDose'] / 1000
cd.loc[(cd.ConcDoseUn == 'g/L'),'ConcDoseUn'] = 'g/mL'

cd.loc[(cd.ConcDoseUn == 'mg/mL'),'ConcDose'] = cd['ConcDose'] / 1000
cd.loc[(cd.ConcDoseUn == 'mg/mL'),'ConcDoseUn'] = 'g/mL'

cd.loc[(cd.ConcDoseUn == 'ug/mL'),'ConcDose'] = cd['ConcDose'] / 1000000
cd.loc[(cd.ConcDoseUn == 'ug/mL'),'ConcDoseUn'] = 'g/mL'

cd.loc[(cd.ConcDoseUn == 'ug/L'),'ConcDose'] = cd['ConcDose'] / 1000000000
cd.loc[(cd.ConcDoseUn == 'ug/L'),'ConcDoseUn'] = 'g/mL'

cd.loc[(cd.ConcDoseUn == 'J/m^2'),'ConcDose'] = cd['ConcDose'] / 100
cd.loc[(cd.ConcDoseUn == 'J/m^2'),'ConcDoseUn'] = 'J/cm^2'

cd.loc[(cd.ConcDoseUn == 'mJ/cm^2'),'ConcDose'] = cd['ConcDose'] / 1000
cd.loc[(cd.ConcDoseUn == 'mJ/cm^2'),'ConcDoseUn'] = 'J/cm^2'

cd.loc[(cd.ConcDoseUn == 'kJ'),'ConcDose'] = cd['ConcDose'] * 1000
cd.loc[(cd.ConcDoseUn == 'kJ'),'ConcDoseUn'] = 'J'

cd.loc[(cd.ConcDoseUn == 'uW/cm^2'),'ConcDose'] = cd['ConcDose'] / 1000000
cd.loc[(cd.ConcDoseUn == 'uW/cm^2'),'ConcDoseUn'] = 'W/cm^2'

cd.loc[(cd.ConcDoseUn == 'kW/cm^2'),'ConcDose'] = cd['ConcDose'] * 1000
cd.loc[(cd.ConcDoseUn == 'kW/cm^2'),'ConcDoseUn'] = 'W/cm^2'

cd.loc[(cd.ConcDoseUn == 'kW/m^2'),'ConcDose'] = cd['ConcDose'] / 10
cd.loc[(cd.ConcDoseUn == 'kW/m^2'),'ConcDoseUn'] = 'W/cm^2'

cd.loc[(cd.ConcDoseUn == 'mW/cm^2'),'ConcDose'] = cd['ConcDose'] / 1000
cd.loc[(cd.ConcDoseUn == 'mW/cm^2'),'ConcDoseUn'] = 'W/cm^2'

cd.loc[(cd.ConcDoseUn == 'W/m^2'),'ConcDose'] = cd['ConcDose'] / 10000
cd.loc[(cd.ConcDoseUn == 'W/m^2'),'ConcDoseUn'] = 'W/cm^2'

cd.loc[(cd.ConcDoseUn == 'mM'),'ConcDose'] = cd['ConcDose'] / 1000
cd.loc[(cd.ConcDoseUn == 'mM'),'ConcDoseUn'] = 'M'

# replace all negative contact times with 0
cd.loc[(cd.ContTime < 0),'ContTime'] = 0

# changing all null values to 0 under the assumption that if a value isn't given 
# the number of applications should be at least 1
cd.loc[(np.isnan(cd['ReApp'])),'ReApp'] = 0

# calculating the total number of applications
cd['TotalApp'] = cd['ReApp'] + 1

# export the cleaned dataset to an excel file
cd.to_excel("cleaned_data.xlsx", sheet_name='master')