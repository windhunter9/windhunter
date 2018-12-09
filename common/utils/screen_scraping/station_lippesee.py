from datetime import datetime, timedelta

import pandas as pd
from . import screen_scraping
import numpy as np
import ast

def GetActualWind():
	page = 'http://www.svpb.de/lippesee/wetter-station'
	tree_station = screen_scraping.GetHtmlData(page)
	path_wind_actual = '//*[@id="c962"]/div/div[4]/script/text()'

	path_time_actual = '//*[@id="c962"]/div/div[1]/div/p/text()'

	time_actual = tree_station.xpath(path_time_actual)

	time_actual = time_actual[0][time_actual[0].find(":")+1:]

	time_actual = datetime.strptime(time_actual.strip(),'%d.%m.%y %H:%M')
	#wind_actual_average = get_list(tree_station, path_wind_actual_average)

	wind_actual = tree_station.xpath(
	    path_wind_actual
	    )

	#print(df.index)
	wind_actual = post_process_table_data(wind_actual, time_actual)
	return wind_actual

def post_process_table_data(wind_actual, time_actual):
    
    wind_actual = [s[s.find("[")+1:s.find("]")] for s in wind_actual]
    wind_actual.pop(0)
    wind_actual = np.array([ast.literal_eval(s) for s in wind_actual])


    df = pd.DataFrame(wind_actual)
    df.columns = ['runtime', 'average', 'max']
    df['runtime'] = pd.to_datetime(wind_actual[:,0])

    df.set_index('runtime', inplace=True)
    s = df.index.hour[0:-1]-df.index.hour[1:]
    f = np.where(s >2)[0][0]+1
    x = df.index.tolist()

    x[:f] = [ x[i] - timedelta(days=1) for i in range(f)]
    df.index = x
    df['runtime'] = pd.to_datetime(x)
    #df.set_index('runtime', inplace=True)
    #df['date'][:49] = df['date'][:49] 
    df['average']  = ms_2_knts(wind_actual[:,1].astype(np.float))
    df['max']  = ms_2_knts(wind_actual[:,2].astype(np.float))
    
    #df_p = df.resample('H').mean()
    #df_p = df_p.reset_index()
 
    return df.reset_index(drop=True)


def knts_2_ms(knts):
    return knts/1.94

def ms_2_knts(ms):
    return ms*1.94