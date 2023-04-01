import numpy as np
import matplotlib . pyplot as plt
import pandas as pd
import datetime
from dateutil . relativedelta import relativedelta
from astropy . coordinates import SkyCoord , Angle , Distance
import astropy . units as u
import itertools # for looping through colors when plotting all points
import os
from subprocess import Popen , PIPE # used to call Find_Orb
import re # regular expressions , used to search for mean residuals in Find_orb output files
from time import sleep
import matplotlib . cm as cm
import time
from astropy . time import Time
from datetime import timedelta
import math
from matplotlib . backends . backend_pdf import PdfPages

def linking ( saveObs , combinations , correctTracklets , falsePositives , lines, data , speed , maxResidual , original , originalAddNoise , angleLim ,nullResid = True , MOIDLim = False ) :
  timeA = ( data . loc [ data ['time'] == 0])
  for i in np . arange (len ( timeA ) ) : # loop through all time A images
    findOrbTxt = open ( os . path . expanduser (" ~/. find_orb /fo. txt ") ,"w")
    indexes = []
    trackletFound = False
    FOV = timeA ['frame']. iloc [ i ]
    coord1 = SkyCoord ( ra = timeA ['RA']. iloc [ i ] , dec = timeA ['Dec']. iloc [i] ,unit =( u . hourangle , u . deg ) , distance =70* u. kpc )
    date = timeA ['date']. iloc [ i ]
    maxTime = max( original . loc [ original ['frame'] == FOV ]['time'])
    findOrbTxt . write ( lines [ timeA ['line']. iloc [ i ]])
    indexes . append ( timeA ['line']. iloc [ i ])
    findOrbTxt . close ()
    trackletFound , indexes , timenum = findTracklet ( indexes ,trackletFound , 1 , lines , FOV , data , coord1 , speed , date , maxTime ,maxResidual , originalAddNoise , angleLim , nullResid , MOIDLim )
    if trackletFound :
      rightTracklet = True
      combinations = combinations + 1
      for line in open ( os . path . expanduser ('~/. find_orb /fo. txt ') ) :
        match = re . search ('FAKE', line )
        if match :
          rightTracklet = False
      if rightTracklet :
        correctTracklets = correctTracklets + 1
      if not rightTracklet :
        falsePositives = falsePositives + 1
      if saveObs :
        open (" outputs / OrbitalElements . txt ", "a+") . writelines ([ l for l in open ( os . path . expanduser (" ~/. find_orb /fo. txt ") ) . readlines () ])
        for line in open ( os . path . expanduser (" ~/. find_orb / elements .txt ") ):
          li = line . strip ()
          if not li . startswith ("#") :
              open (" outputs / OrbitalElements . txt ", "a").writelines ( line . rstrip () )
              open (" outputs / OrbitalElements . txt ", "a").writelines ("\n")
        open (" outputs / OrbitalElements . txt ", "a") . writelines ("\n\n")
      open (" outputs / tracklets . txt ", "a") . writelines ([ l for l in open( os . path . expanduser ("~/. find_orb /fo. txt ") ) . readlines () ])
      os . remove ( os . path . expanduser (" ~/. find_orb /fo. txt ") )
      for ii in ( indexes ) :
        data = data [ data . line != ii ]
        originalAddNoise = originalAddNoise [ originalAddNoise . line!= ii ]
  return data , originalAddNoise , combinations , correctTracklets ,falsePositives


def plotTracklets () :
  """
  Plots all found tracklets in 4x4 subplots .
  """
  widths = [
  14 , # name
  18 , # date
  12 , #RA
  12 , #Dec

  ]
  data = pd . read_fwf ('outputs / tracklets . txt ', widths = widths , header = None )
  pp = PdfPages ('outputs / trackletsPlot . pdf ')
  data . columns = [" name ", " date ", "RA", " Dec "]
  xlim =( None , None )
  ylim =( None , None )
  figsNum = np . ceil (len( data ) /3/4)
  for figs in np . arange ( figsNum ) :
    fig = plt . figure ( figsize =(15 ,15) )
    ax1 = fig . add_subplot (221)
    ax1 . set_xlabel ('RA ( degrees )')
    ax1 . set_ylabel ('Dec ( degrees )')
    ax1 . axis ('equal ')
    ax1 . grid ( True )
    set = data [int ( figs *4) : int ( figs *4+3) ]
    ra = Angle (set ['RA '] , unit =( u . hourangle ) )
    ra = ra . wrap_at (180* u . degree )
    dec = Angle (set ['Dec '] , unit =( u . deg ) )
    for i in np . arange (len ( ra ) ) :
      ax1 . scatter ( ra . degree [ i ] , dec . degree [ i ] , label =" observation %i"%( i ) )
    ax1 . set_title ('Tracklet %i'%( figs *4+1) )
    ax1 . legend ()
    if (len ( data ) /3) -( figs *4+1) > 0:
      ax2 = fig . add_subplot (222)
      ax2 . set_xlabel ('RA ( degrees )')
      ax2 . set_ylabel ('Dec ( degrees )')
      ax2 . grid ( True )
      ax2 . axis ('equal ')
      set = data [ int ( figs *4+3) : int ( figs *4+6) ]
      ra = Angle (set ['RA'] , unit =( u . hourangle ) )
      ra = ra . wrap_at (180* u . degree )

      dec = Angle ( set ['Dec'] , unit =( u . deg ) )
      for i in np . arange ( len ( ra ) ) :
        ax2 . scatter ( ra . degree [ i ] , dec . degree [ i ] , label ="observation %i"%( i ) )
      ax2 . legend ()
      ax2 . set_xlim ( xlim )
      ax2 . set_ylim ( ylim )
      ax2 . set_title ('Tracklet %i'%( figs *4+2) )
    if (len ( data ) /3) -( figs *4+2) > 0:
      ax3 = fig . add_subplot (223)
      ax3 . set_xlabel ('RA ( degrees )')
      ax3 . set_ylabel ('Dec ( degrees )')
      ax3 . grid ( True )
      ax3 . axis ('equal ')
      set = data [ int ( figs *4+6) : int ( figs *4+9) ]
      ra = Angle (set ['RA '] , unit =( u . hourangle ) )
      ra = ra . wrap_at (180* u . degree )
      dec = Angle ( set ['Dec '] , unit =( u . deg ) )
      for i in np . arange ( len ( ra ) ) :
        ax3 . scatter ( ra . degree [ i ] , dec . degree [ i ] , label ="observation %i"%( i ) )
      ax3 . legend ()
      ax3 . set_xlim ( xlim )
      ax3 . set_ylim ( ylim )
      ax3 . set_title ('Tracklet %i'%( figs *4+3) )
    if (len ( data ) /3) -( figs *4+3) > 0:
      ax4 = fig . add_subplot (224)
      ax4 . set_xlabel ('RA ( degrees )')
      ax4 . set_ylabel ('Dec ( degrees )')
      ax4 . grid ( True )
      ax4 . axis ('equal')
      set = data [ int ( figs *4+9) : int ( figs *4+12) ]

      ra = Angle (set ['RA '] , unit =( u . hourangle ) )
      ra = ra . wrap_at (180* u . degree )
      dec = Angle ( set ['Dec '] , unit =( u . deg ) )
      for i in np . arange ( len ( ra ) ) :
        ax4 . scatter ( ra . degree [ i ] , dec . degree [ i ] , label ="observation %i"%( i ) )
      ax4 . legend ()
      ax4 . set_xlim ( xlim )
      ax4 . set_ylim ( ylim )
      ax4 . set_title ('Tracklet %i'%( figs *4+4) )
    plt . savefig ( pp , format ='pdf ')
    plt . clf ()
  pp . close ()


def find_orb ( maxResidual , nullResid = True , MOIDLim = False ) :
  """
  Feeds observations in MPC format that are located ~/. find_orb /fo. txt
  to
  the non - interactive version of find orb , fo. find_orb stores orbital
  elements in ~/. find_orb / elements .txt , which this function will read
  to
  find the mean residual to the orbital fit . If the mean residual is
  less
  than maxResidual ( specified in ") and all observations in
  ~/. find_orb /fo.txt was used to generate the orbital fit , then the
  function will return True . In other cases (e.g. find_orb doesn ’t run ;
  mean residual greater than maxResidual ; not all observations in
  ~/. find_orb /fo.txt used ), the function will return False .
  """
  if os . path . exists ( os . path . expanduser (" ~/. find_orb / elements . txt ") ):
    os . remove ( os . path . expanduser (" ~/. find_orb / elements . txt ") )
  sp = Popen ([ 'cd ~/. find_orb \n~/ find_orb / find_orb /fo fo. txt -c'] , shell= True )
  totSleep = 0
  # wait for find_orb to create elements . txt . If it takes longer than 20 seconds
  # then find_orb probably can ’t find an orbit .
  while not os . path . exists ( os . path . expanduser (" ~/. find_orb / elements . txt ") ) :
    sleep (0.2)
    totSleep = totSleep + 0.2
    if totSleep > 20:
      break
  if os . path . exists ( os . path . expanduser (" ~/. find_orb / elements . txt ") ):
    if os . path . getsize ( os . path . expanduser (" ~/. find_orb / elements . txt "))== 0:
      sleep (0.2)
    numObs = sum (1 for line in open ( os . path . expanduser (" ~/. find_orb /fo. txt") ) )
  # save all inputs to find_orb
    open (" outputs / AllPotentialTracklets . txt ", "a+") . writelines ([ l for l in open ( os . path . expanduser (" ~/. find_orb /fo. txt ") ) . readlines () ])
    for line in open ( os . path . expanduser (" ~/. find_orb / elements . txt ") ) :
      li = line . strip ()
      if not li . startswith ("#") :
        open (" outputs / AllPotentialTracklets . txt ", "a") . writelines (line . rstrip () )
        open (" outputs / AllPotentialTracklets . txt ", "a") . writelines ( "\n")
    open (" outputs / AllPotentialTracklets . txt ", "a") . writelines ("\n\n")
    resCheck = False
    for line in open ( os . path . expanduser ('~/. find_orb / elements . txt ') ) :
      match = re . search ('mean residual (\d+) ".(\ d+) ', line )
      match2 = re . search ('MOID : (\d+) .(\ d+) ', line )
      if match :
        res = int ( match . group (1) ) + float (( '0. '+ match . group (2) ) )
        if nullResid :
          if ( res < maxResidual ) & ( res > 0) : # maxResidual in "
            resCheck = True
          else :
            resCheck = False
        else :
          if ( res < maxResidual ) : # maxResidual in "
            resCheck = True
          else :
            resCheck = False
      if ( match2 ) :
        if MOIDLim :
          MOID = int ( match2 . group (1) ) + float (( '0. '+ match2 . group(2) ) )
          if MOID > MOIDLim :
            break
    if resCheck :
      return True
    else :
      return False
  else :
    return False


def findTracklet ( indexes , trackletFound , timenum , lines , FOV , df , coord1 ,speed , date , maxTime , maxResidual , originalAddNoise , angleLim ,nullResid = True , MOIDLim = False ) :

  """
  Function recursively identifies nearby observations in the next frame .
  Saves each observation it links to fo. txt for use with find_orb .
  """
  FOVB = df . loc [ df ['time '] == timenum ]
  FOVB = FOVB . loc [ FOVB ['frame '] == FOV ]
  for i in np . arange (len ( FOVB ) ) :
    if ( trackletFound ) :
      return trackletFound , indexes , timenum
      break
    coord2 = SkyCoord ( ra = FOVB ['RA' ]. iloc [ i ] , dec = FOVB ['Dec' ]. iloc [ i ],
    unit =( u . hourangle , u . deg ) , distance =70* u. kpc )
    timeDelta = FOVB ['date']. iloc [i ] - date
    maxDist = ( timeDelta / np . timedelta64 (1 , 's') ) *( speed )
    maxDist = Distance ( maxDist , u . kpc )
    sep = coord1 . separation_3d ( coord2 )
    # print (sep , ’ separation ’)
    if ( maxDist > sep ) & ( timenum != maxTime ) :
      # ####
      # enters this if statement if observations A and B are
      # enough in distance from each other , AND there are
      # additional exposures to loop through
      # ####
      # setup variables for recursive loop , by turning the
      # current observation B into observation A
      date = FOVB ['date' ]. iloc [ i ]
      coord1 = coord2
      timenum = timenum + 1
      findOrbTxt = open ( os . path . expanduser (" ~/. find_orb /fo. txt ") ,"a")
      findOrbTxt . write ( lines [ FOVB ['line' ]. iloc [ i ]])
      findOrbTxt . close ()

      indexes . append ( FOVB ['line' ]. iloc [ i ])
      # print ( ’ next : ’ , FOVB [ ’ name ’]. iloc [i])
      findOrbTxt = findOrbTxt . close ()
      trackletFound , indexes , timenum = findTracklet ( indexes ,
      trackletFound , timenum , lines , FOV , df , coord1 , speed , date , maxTime ,
      maxResidual , originalAddNoise , angleLim , nullResid , MOIDLim )

    elif ( maxDist < sep ) :
      # ####
      # if B is too far away from A, delete B
      # ####
      df = df [ df . line != FOVB ['line ']. iloc [ i ]]

    elif ( maxDist >= sep ) & ( timenum == maxTime ) :
        # ####
        # if A and B are close enough AND there are no more
        # exposures to loop through
        # ####
        findOrbTxt = open ( os . path . expanduser (" ~/. find_orb /fo. txt ") ,"a")
        findOrbTxt . write ( lines [ FOVB ['line' ]. iloc [ i ]])
        findOrbTxt . close ()
        indexes . append ( FOVB ['line ']. iloc [ i ])
        # print ( ’ final : ’ , FOVB [ ’ name ’]. iloc [i])
        angle = findAngle ( angleLim )
        if angle >= ( angleLim * u . radian ) :
          # ####
          # if linked tracklet makes an angle greater than
          # angleLim
          # ####
          print (" angle =", angle )
          trackletFound = find_orb ( maxResidual , nullResid , MOIDLim )

        if not trackletFound :
          # ####
          # if linked tracklet is rejected ( either by find_orb
          # or by angle ), delete last observation , and re - enter
          # recursive function
          # ####
          indexes = indexes [: -1]
          readFile = open ( os . path . expanduser (" ~/. find_orb /fo. txt ") )
          fileLines = readFile . readlines ()
          readFile . close ()
          findOrbTxt = open ( os . path . expanduser (" ~/. find_orb /fo. txt "),"w")
          findOrbTxt . writelines ([ item for item in fileLines [: -1]])
          findOrbTxt . close ()
          df = df [ df . line != FOVB ['line' ]. iloc [ i ]]

        if trackletFound :
          return trackletFound , indexes , timenum


  if ( not trackletFound ) & ( timenum >= 2) :
    # ####
    # if no tracklets are found using , go back one exposure
    # as long as not working with first or second exposure .
    timenum = timenum - 1
    df = df [ df . line != indexes [ -1]]
    B = originalAddNoise . loc [ originalAddNoise ['time' ] == timenum +1]
    df = df . append ( B )
    df = df . sort_values ( by ='date' )
    date = df [ df . line == indexes [ timenum -1]]. iloc [0]. date
    if len ( indexes [: -1]) != 0:
      indexes = indexes [: -1]

    readFile = open ( os . path . expanduser (" ~/. find_orb /fo. txt ") )
    fileLines = readFile . readlines ()
    readFile . close ()
    findOrbTxt = open ( os . path . expanduser (" ~/. find_orb /fo. txt ") ,"w")
    findOrbTxt . writelines ([ item for item in fileLines [: -1]])
    findOrbTxt . close ()
    coord1 = SkyCoord ( ra = df [ df . line == indexes [ -1]]. iloc [0]. RA , dec= df [ df . line == indexes [ -1]]. iloc [0]. Dec , unit =( u . hourangle , u . deg ) ,
    distance =70* u . kpc )
    trackletFound , indexes , timenum = findTracklet ( indexes ,
    trackletFound , timenum , lines , FOV , df , coord1 , speed , date , maxTime ,
    maxResidual , originalAddNoise , angleLim , nullResid , MOIDLim )


  return trackletFound , indexes , timenum

## function to plot RA and Dec
def plot_coords ( df , noise_start = False , specframe = False , spectime = False ) :
  """
  Plots observations and noise . Not fully refined , especially with
  regards to color and scale .
  """
  if not specframe :
    specframe = df . frame . unique ()
  if not spectime :
    spectime = df . time . unique ()
  if not noise_start :
    noise_start = max ( df ['line '])

  fig = plt . figure ( figsize =(8 ,6) )
  ax1 = fig . add_subplot (211 , projection =" mollweide ")
  ax2 = fig . add_subplot (212)
  ax1 . set_xticklabels ([ '14h','16h','18h','20h','22h','0h','2h','4h','6h','8h','10h'])
  ax1 . grid ( True )
  # ax2. set_xticklabels ([ ’14h ’ , ’16h ’ , ’18h ’ , ’20h ’ , ’22h ’ , ’0h ’ , ’2h ’ , ’4h ’ , ’6h’ , ’8h ’ , ’10h ’])
  ax2 . set_xlabel ('RA ( degrees )')
  ax2 . set_ylabel ('Dec ( degrees )')
  # ax2. set_xlim ( -61.9 , -63.9)
  # ax2. set_ylim ( -33.4 , -35.4)
  ax2 . grid ( True )
  colors = itertools . cycle (( cm . rainbow ( np . linspace (0 , 1 , 11) )) )

  for frame in specframe :
    eachframe = df [ df ['frame ']== frame ]
    color = next ( colors )
    markers = itertools . cycle (( '+', '.', 'o', 'P') )
    for time in spectime :
      eachtime = eachframe [ eachframe ['time ']== time ]
      # find where noise
      noise = eachtime [ eachtime ['line '] >= noise_start ]
      ra = Angle ( noise ['RA '] , unit =( u . hourangle ))
      ra = ra . wrap_at (180* u . degree )
      dec = Angle ( noise ['Dec '], unit =( u . deg ) )
      ax1 . scatter ( ra . radian , dec . radian , s =20 , color = color , marker ='*', facecolors ='none ', alpha =0.5)
      ax2 . scatter ( ra . degree , dec . degree , s =20 , color = color , marker ='*', facecolors ='none ', alpha =0.5)
      # find where not noise :
      not_noise = eachtime [ eachtime ['line '] < noise_start ]
      ra = Angle ( not_noise ['RA '] , unit =( u . hourangle ) )
      ra = ra . wrap_at (180* u . degree )
      dec = Angle ( not_noise ['Dec '] , unit =( u . deg ) )
      ax1 . scatter ( ra . radian , dec . radian , s =10 , color = color , marker =next ( markers ) , facecolors ='none ', alpha =0.5)
      ax2 . scatter ( ra . degree , dec . degree , s =10 , color = color , marker =next ( markers ) , facecolors ='none ', alpha =0.5)


  plt . savefig ('outputs / coord_plot . pdf ')


def findAngle ( angleLim ) :
  """
  Finds angle of a tracklet ’s trajectory , assuming a flat
  plane of movement , using cosine rule . Obviously , only
  works with observations with three
  """
  col_specification = [(32 , 43) , (44 , 55) ]
  fo = pd . read_fwf ( os . path . expanduser (" ~/. find_orb /fo. txt ") , colspecs =col_specification , header = None )
  fo . columns = ["RA", " Dec "]
  if len ( fo ) == 3:

    print ("RAs :", fo ['RA ']. iloc [0] , fo ['RA ']. iloc [1] , fo ['RA ']. iloc [2])
    coordA = SkyCoord ( ra = fo ['RA ']. iloc [0] , dec = fo ['Dec ']. iloc [0] , unit =(u . hourangle , u . deg ) , distance =70* u . kpc )
    coordB = SkyCoord ( ra = fo ['RA ']. iloc [1] , dec = fo ['Dec ']. iloc [1] , unit =(u . hourangle , u . deg ) , distance =70* u . kpc )
    coordC = SkyCoord ( ra = fo ['RA ']. iloc [2] , dec = fo ['Dec ']. iloc [2] , unit =(u . hourangle , u . deg ) , distance =70* u . kpc )
    lenAB = coordA . separation_3d ( coordB )
    lenBC = coordB . separation_3d ( coordC )
    lenCA = coordC . separation_3d ( coordA )
    cosine_angle = (( lenAB ** 2) + ( lenBC ** 2) - ( lenCA ** 2) ) / (2 *lenAB * lenBC )
    angle = np . arccos ( cosine_angle )
  else :
    angle = angleLim * u . radian
  return angle