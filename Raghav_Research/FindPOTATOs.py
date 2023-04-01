import numpy as np
import pandas as pd
import datetime
from astropy . coordinates import SkyCoord , Angle , Distance
import astropy . units as u
import os
import re # regular expressions , used to search for noise points in tracklets
import linking_library as ll
import add_library as al
import shutil
import math
print ('reading data ')
"""
change below based on input and desired outputs .
"""
import configparser
config = configparser . ConfigParser ()
config . read ('inputs / linking_parameters . ini ')

if config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ ' IPAC_table_file '] and config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ 'NEAT_file ']:
  print ('please only specify one file : either NEAT data or IPAC -formatted data ')
  quit ()
elif ( not config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ 'NEAT_file ']) and ( not config ['C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ 'NEAT_file ']) :
  print ('please specify one file for analysis ')
  quit ()
elif config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ ' IPAC_table_file ']:
  ipac = 1
elif config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ 'NEAT_file ']:
  ipac = 0

noise_lvl = float ( config ['SETTINGS '][ ' Noise_level '])
saveObs = float ( config ['SETTINGS '][ ' Save_observation '])
maxSep = float ( config ['SETTINGS '][ ' Maximum_separation '])



if ipac == 1:
  filename = config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ ' IPAC_table_file '] #'ptf10_2 '# 'onlyGood ' # ' ptf_10arcmin '
  starFile = config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ 'star_file ']
  filename , data = al . tblConvert ( filename , starFile )
if ipac == 0:
  filename = config [' C:/Users/ragha/OneDrive/college stuff/4th sem/AIML project '][ 'NEAT_file ']
  widths = [14 , # name
            18 , # date
            12 , #RA
            12 , #Dec
            ]
  raw = pd . read_fwf ('%s.txt ' %( filename ) , widths = widths , header = None )
  raw . columns = [" name ", " date ", "RA", " Dec "]
  data = pd . DataFrame ()
  data ['name ']= raw ['name ']
  data ['date ']= raw ['date ']. apply ( lambda x : datetime . datetime . strptime ( x[ -16: -6] , '%Y %m %d') + datetime . timedelta ( days = float ( x [ -6: len ( x ) ]) ) )
  data ['RA ']= raw ['RA ']

  data ['Dec ']= raw ['Dec ']
  data ['line ']= np . arange ( len ( data ) )
  data = data . sort_values ( by ='date ')
  print ('labelling data ')
  data = al . labelNEAT ( data )

inputTxt = open ('%s.txt ' %( filename ) )
lines = inputTxt . readlines ()
inputTxt . close ()

original = data . copy ( deep = True )


if ( noise_lvl ) > 0 & ( ipac == 0) :
  """
  Datafile is duplicated to create noise file .
  """
  shutil . copy ('%s.txt ' %( filename ) , '%s. txt ' %( filename +'_noise ') )
  filename = filename + '_noise '
  print ('adding noise ')
  data = al . addNoise ( data , noise_lvl , maxSep , filename , lines )

originalAddNoise = data . copy ( deep = True )
noiseObsNum = len ( data ) - len ( original )

if not os . path . exists (" outputs /") :
  os . mkdir (" outputs ")

if ipac ==0:
  ll . plot_coords ( data ,len ( lines ) )

inputTxt = open ('%s.txt ' %( filename ) )
lines = inputTxt . readlines ()

inputTxt . close ()

dates = data . date . unique ()

if os . path . exists (" outputs / tracklets . txt ") :
  os . remove (" outputs / tracklets . txt ")
if os . path . exists (" outputs / OrbitalElements . txt ") :
  os . remove (" outputs / OrbitalElements . txt ")
if os . path . exists (" outputs / AllPotentialTracklets . txt ") :
  os . remove (" outputs / AllPotentialTracklets . txt ")

print ('finding tracklets and running through find_orb ')
print ( data )


combinations = 0
correctTracklets = 0
falsePositives = 0


### first pass ###
print ('first pass ')

for x in np . arange (len ( config . sections () ) -2) :
  keyName = 'PARAMETERS ' + str ( x + 1)
  print ('pass #'+str ( x +1) )
  """
  parameters , can be changed with linking_parameters . ini
  """
  angleLim = float ( config [ keyName ][ ' Angle_limit '])
  speed = float ( config [ keyName ][ ' Angular_speed '])
  maxResidual = float ( config [ keyName ][ ' Maximum_residual '])

  MOIDLim = float ( config [ keyName ][ ' MOID_limit '])
  nullResid = True
  if ( x +1) ==2:
    nullResid = False
    MOIDLim = False
  data , originalAddNoise , combinations , correctTracklets , falsePositives= ll . linking ( saveObs , combinations , correctTracklets , falsePositives ,
                                                                                            lines , data , speed , maxResidual , original , originalAddNoise , angleLim ,
                                                                                            nullResid = nullResid , MOIDLim = MOIDLim )


if os . path . exists (" outputs / tracklets . txt ") :
  ll . plotTracklets ()
print (" unlinked observations ")
print ( data )
print ( noiseObsNum , 'noise observations added ')
print ( len ( original ) , 'real observations used ')
print ( combinations , 'total tracklets found ')
print ( correctTracklets , 'good tracklets found ')
print ( falsePositives , 'false positives found ')
