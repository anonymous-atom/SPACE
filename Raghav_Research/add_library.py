import numpy as np
import pandas as pd
import datetime
from dateutil . relativedelta import relativedelta
from astropy . coordinates import SkyCoord , Angle , Distance
import astropy . units as u
from tqdm import tqdm , trange # used to make progress bars for star removal
import itertools # needed for progress bars
import os
import time
from astropy . time import Time
from datetime import timedelta
from astropy . io import ascii
import pickle
import random

def labelNEAT ( new ) :
  """
  Function labels NEAT data containing confirmed asteroids based on date
  and time of observation . Creates new columns in the input DataFrame :
  'image ', 'frame ' and 'time  '.
  
  
  'image ': Specifies a best guess of which NEAT image an observation
  comes from . Images are ordinally ranked according to chronology .
  'frame ': Specifies a best guess of which field of view an observation
  comes from .
  'time  ': Specifies a best guess of which image of a particular field of
  view an observation comes from . I.e. if a particular field of view has
  been scanned by NEAT 3 times , 'time  ' specifies if an observation comes
  from the 1st , 2nd or 3rd time .
  Might be easier to think of 'frame ' and 'time  ' as space and time
  representations . 'frame ' specifies where in the sky an observation is
  from ; 'time  ' represents that an observation comes from the nth time
  NEAT has surveyed that part of the sky .
  
  Not fully refined because of abnormalities in NEAT data , so labelling
  is off in non - specific instances .
  
  """
  deAsterisk = str. maketrans ({"*": r""})
  image =[]
  imagenum = 0
  for idx in np . arange (len ( new ) ) :
    if idx == 0:
      imagenum = 0
    elif new ['date ']. iloc [ idx ] != new ['date ']. iloc [ idx -1]:
      imagenum = imagenum + 1
    image . append ( imagenum )
  new = new . assign ( image = image )

  # assign 'frame '
  frame = []


  for idx in np . arange (len ( new ) ) :
    if new ['image ']. iloc [ idx ] == 0:
      framenum = 0
    else :
      framenum = max ( frame ) +1
      if new ['image ']. iloc [ idx ] == new ['image ']. iloc [ idx -1]:
        framenum = frame [ idx -1]
      elif new ['image ']. iloc [ idx ] != new ['image ']. iloc [ idx -1]:
  # this part is repetitive and hideous
        subset = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1]])
        subset2 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -1])
        subset3 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -2])
        subset4 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -3])
        subset5 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -4])
        subset6 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -5])
        subset7 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -6])
        subset8 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -7])
        subset9 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -8])
        subset10 = ( new . loc [ new ['image '] == new ['image ']. iloc [ idx-1] -9])
        for i in np . arange ( len ( subset ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset ['name  ']. iloc [ i ]. translate ( deAsterisk )) :
            framenum = frame [ idx -1]
            break
        for i in np . arange ( len ( subset2 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset2 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -1]
            break
        for i in np . arange ( len ( subset3 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset3 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -1]
            break
        for i in np . arange ( len ( subset4 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset4 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -1]
            break
        for i in np . arange ( len ( subset5 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset5 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -len ( subset4 ) -1]
            break
        for i in np . arange ( len ( subset6 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset6 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -len ( subset4 ) -len ( subset5 ) -1]
            break
        for i in np . arange ( len ( subset7 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset7 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -len ( subset4 ) -len ( subset5 ) -len ( subset6 ) -1]
            break
        for i in np . arange ( len ( subset8 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset8 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -len ( subset4 ) -len ( subset5 ) -len ( subset6 ) -len ( subset7 ) -1]
            break
        for i in np . arange ( len ( subset9 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset9 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -len ( subset4 ) -len ( subset5 ) -len ( subset6 ) -len ( subset7 ) -len (subset8 ) -1]
            break
        for i in np . arange ( len ( subset10 ) ) :
          if ( new ['name  ']. iloc [ idx ]. translate ( deAsterisk ) ==subset10 ['name  ']. iloc [ i ]. translate ( deAsterisk ) ) :
            framenum = frame [ idx -( len ( subset ) ) -len ( subset2 ) -len ( subset3 ) -len ( subset4 ) -len ( subset5 ) -len ( subset6 ) -len ( subset7 ) -len (subset8 ) -len ( subset9 ) -1]
            break
    frame . append ( framenum )
  
  new = new . assign ( frame = frame )
  new = new . sort_values ([ 'frame ', 'date  '] , ascending =[ True , True ])
  time = []
  for idx in np . arange (len ( new ) ) :
    if ( new ['frame ']. iloc [ idx ] != new ['frame ']. iloc [ idx -1]) and ( new ['date  ']. iloc [ idx ] != new ['date  ']. iloc [ idx -1]) :
      timenum = 0
    elif ( new ['frame ']. iloc [ idx ] == new ['frame ']. iloc [ idx -1]) and ( new['date  ']. iloc [ idx ] == new ['date  ']. iloc [ idx -1]) :
      imenum = time [ idx -1]
    elif ( new ['frame ']. iloc [ idx ] == new ['frame ']. iloc [ idx -1]) and ( new['date  ']. iloc [ idx ] != new ['date  ']. iloc [ idx -1]) :
      timenum = time [ idx -1] +1
    time . append ( timenum )
  new = new . assign ( time = time )
  new = new . sort_values ( by ='date ')
  return new


def removeStars(filename, df_allSources, StarFile):
    """
    Removes PTF objects that are within 1" of Pan-STARRS sources.
    Pickles dataframe post-star removal. If post-star removal
    file exists, will use that instead.
    """
    if os.path.exists('inputs/%s_dfStarsRemoved.pickle' % (filename)):
        with open('inputs/%s_dfStarsRemoved.pickle' % (filename), 'rb') as f:
            df_allSources = pickle.load(f)
    else:
        print("reading stars")
        stars = pd.read_csv(StarFile)
        print("removing stars")
        for i in trange(len(stars), desc="loop 1"):
            for index, row in tqdm(df_allSources.iterrows(), desc="loop 2"):
                c1 = SkyCoord(ra=row["ra"], dec=row["dec"], unit=(u.deg, u.deg))
                c2 = SkyCoord(ra=stars["raMean"].iloc[i], dec=stars["decMean"].iloc[i], unit=(u.deg, u.deg))
                if c1.separation(c2) < Angle(1, unit=u.arcsec):
                    df_allSources.drop(index, axis=0, inplace=True)
        with open('inputs/%s_dfStarsRemoved.pickle' % (filename), 'wb') as f:
            pickle.dump(df_allSources, f)
    return df_allSources


def tblConvert ( filename , StarFile ) :
  """
  Converts PTF data from IPAC 's . tbl format to Pandas DataFrame
  and MPC 80 - col format for use with linking code and Find_Orb
  respectively . Pandas DataFrame is pickled .
  """
  if not os . path . exists ('inputs ') :
    os . makedirs ('inputs ')
  if os . path . exists ('inputs /% s_df . pickle '%( filename ) ) :
    with open ('inputs /% s_df . pickle '%( filename ) , 'rb ') as f :
      df = pickle . load ( f)
  else :
    raw = ascii . read ('%s.tbl '%( filename ) ,format ='ipac ', guess = False )
    df = raw . to_pandas ()
    with open ('inputs /% s_df . pickle '%( filename ) , 'wb ') as f :
      pickle . dump ( df , f )
  if StarFile :
    df = removeStars ( filename , df , StarFile )
  data = pd . DataFrame ()
  print (" converting .tbl to DataFrame ")
  data ['name ']= df ['sid ']
  data ['date ']= df ['obsmjd ']. apply ( lambda x : datetime . datetime . strptime (Time (x , format ='mjd ', out_subfmt ='date *') . iso , '%Y -%m -%d %H:%M:%S.%f') )
  data ['RA ']= df ['ra ']. apply ( lambda x : Angle (x , u . degree ) . to_string ( unit =u . hourangle , sep =' ', precision =2 , fields = 3) )
  data ['Dec ']= df ['dec ']. apply ( lambda x : Angle (x , u . degree ) . to_string (
  unit = u . degree , sep =' ', precision =1 , alwayssign = True , fields = 3) )
  data ['line ']= np . arange ( len ( df ) )
  data = data . sort_values ( by ='date ')
  image =[]
  imagenum = 0
  print (" labelling data ")
  for idx in np . arange (len ( data ) ) :
    if idx == 0:
      imagenum = 0
    elif ( data ['date ']. iloc [ idx -1] + timedelta ( seconds =1) < data ['date ']. iloc [ idx ]) :
      imagenum = imagenum + 1
    image . append ( imagenum )
  data = data . assign ( image = image )
  data ['frame ']= df ['ptffield '] - min ( df ['ptffield '])
  data = data . sort_values ([ 'frame ', 'date '] , ascending =[ True , True ])
  times = []
  for idx in np . arange (len ( data ) ) :
    if idx == 0 : ### this needs to be added in NEAT library , in label_NEAT function
      timenum = 0
    elif ( data ['frame ']. iloc [ idx ] != data ['frame ']. iloc [ idx -1]) and (data ['date ']. iloc [ idx ] != data ['date ']. iloc [ idx -1]) :
      timenum = 0

    elif ( data ['frame ']. iloc [ idx ] == data ['frame ']. iloc [ idx -1]) and (data ['date ']. iloc [ idx ] == data ['date ']. iloc [ idx -1]) :
      timenum = times [ idx -1]
    elif ( data ['frame ']. iloc [ idx ] == data ['frame ']. iloc [ idx -1]) and (data ['date ']. iloc [ idx ] != data ['date ']. iloc [ idx -1]) :
      timenum = times [ idx -1] +1
    times . append ( timenum )
  data = data . assign ( time = times )
  data = data . sort_values ( by ='date ')

  # make MPC 80 - col format
  print (" converting .tbl to MPC1992 ")
  filename = "% s_MPC1992 "%( filename )
  if os . path . exists ("%s. txt "%( filename ) ) :
    os . remove ("%s.txt"%( filename ) )
  f = open ("%s.txt "%( filename ) ,"a+")
  for idx in np . arange (len ( data ) ) :
    RA = Angle ( df ['ra ']. iloc [ idx ] , u. degree ) . to_string ( unit = u .hourangle , sep =' ', pad = True , precision =2 , fields = 3)
    Dec = Angle ( df ['dec ']. iloc [ idx ] , u . degree ) . to_string ( unit = u . degree, sep =' ', pad = True , precision =1 , alwayssign = True , fields = 3)
    date = datetime . datetime . strptime ( Time ( df ['obsmjd ']. iloc [ idx ] ,format ='mjd ', out_subfmt ='date *') . iso , '%Y -%m -%d %H:%M:%S.%f')
    Year = 'C'+ date . strftime ('%Y')
    Month = date . strftime ('%m')
    dt = timedelta ( hours = date . hour , minutes = date . minute , seconds = date .second )
    secs_per_day = 24*60*60 # hours * mins * secs
    Day = str ( np . around (( dt . total_seconds () / secs_per_day ) , decimals =5) ). ljust (7 , '0')
    Day = str (str ( date . day ) . zfill (2) ) + Day [1:]
    Mag = str ( np . around ( df ['mag_auto ']. iloc [ idx ] , decimals =1) )

    Obs = 'I41 '
    new_line = ' J91tX00B ' + Year + ' ' + Month + ' ' + Day + ' ' + RA + ' ' + Dec + ' ' + Mag + ' ' + Obs +'\n'
  f . write ( new_line )
  f . close ()
  return filename , data


def addNoise(df, noise_lvl, maxSep, filename, lines):
    """
    Function adds noise points to data by randomly choosing an observation
    and placing a point within 1 degree of the chosen observation. The
    noise point uses the chosen observation as a template, so has all the
    non-positional attributes (magnitude, time of observation, etc) of the
    original observation for use in MPC 80-col format. Noise observations
    are appended at the end of the file.
    """
    numNoise = int((len(df) * noise_lvl) / (1 - noise_lvl))
    maxLines = len(lines)
    lineNum = len(lines)
    f = open(f"{filename}.txt", "a")
    maxIm = df['image'].max()
    for i in np.arange(numNoise):
        # generate noise elements
        image = random.randint(0, maxIm)
        field = df[df.image == image]
        field = field[field.line < maxLines]
        template = random.randint(0, len(field) - 1)
        templateCoord = SkyCoord(ra=field['RA'].iloc[template], dec=field['Dec'].iloc[template],unit=(u.hourangle, u.deg), distance=70 * u.kpc)
        position_angle = np.random.uniform(0, 360) * u.deg
        separation = np.random.uniform(0, maxSep) * u.arcsec
        ranCoord = templateCoord.directional_offset_by(position_angle, separation)
        ranRA = ranCoord.to_string(style='hmsdms', sep=' ', precision=2,alwayssign=False, pad=True)[0:11]
        ranDec = ranCoord.to_string(style='hmsdms', sep=' ', precision=2,alwayssign=True, pad=True)[12:]
        # append noise data to DataFrame
        df = df.append({'name': 'FAKE ' + field['name'].iloc[template][4:7],
                        'date': field['date'].iloc[template],
                        'RA': ranRA,
                        'Dec': ranDec,
                        'line': lineNum,
                        'image': field['image'].iloc[template],
                        'frame': field['frame'].iloc[template],
                        'time': field['time'].iloc[template]
                        }, ignore_index=True)
        # append noise data to file
        line_original = lines[field['line'].iloc[template]]
        new_line = line_original[0:5] + 'FAKE ' + line_original[9:32] + ranRA + ' ' + ranDec + line_original[56:]
        # print(line_original)
        print(new_line)
        f.write(new_line)
        lineNum = lineNum + 1

    f.close()
    df = df.sort_values(by='date')
    return df
