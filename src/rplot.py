"""
Created: Tuesday 1st December 2020
@author: John Moncrieff (j.moncrieff@ed.ac.uk)
Last Modified on 5 Feb 2021 16:30 

DESCRIPTION
===========
This package contains the python for plotting RLINE output 
in the RLINE/EFT Jupyter notebook

"""
import pandas as pd
import matplotlib.gridspec as gridspec

sites = []
max = min = 0
gs = gridspec.GridSpec(4, 4)
gs.update(left=0.10, right=0.95, hspace=0.05)
hourly_stab = ['stable','weakly stable','weakly convective','convective']
sitenames = ['site 1','site 2','site 3','site 4']
infilename = 'Output_Example_Numerical.csv'
infilename2 = 'Met_Example.csv'   
# use Pandas to read in concentration data


def plotrw():
    dfc=pd.read_csv(infilename, header=10, skipinitialspace=True)
    #print(dfc)
    # use Pandas to read in meteorology data
    dfm=pd.read_csv(infilename2, skip_blank_lines=True, skipinitialspace=True)
    #dfm.head(4)
    # NB - RLINE has calculated the concentrations based on unit emission
    # so we need to multiply the predicted concentrations by the actual emissions
    hourlist=[]
    methourlist=[]
    # Split into hourly dataframes for graphing
    # https://stackoverflow.com/questions/54046707/pandas-split-one-dataframe-into-multiple-dataframes
    for h in dfc['Hour'].unique():
        temp = 'dfc_{}'.format(h)
        #hourlist.append(temp)  # keep track of data files to process
        vars()[temp] = dfc[dfc['Hour']==h]
        
    hourlist=[dfc_1, dfc_2, dfc_3, dfc_4]

    for h in dfm['Hour'].unique():
        temp = 'dfm_{}'.format(h)  
        vars()[temp] = dfm[dfm['Hour']==h]
        
    methourlist=[dfm_1, dfm_2, dfm_3, dfm_4]
    #plm.plm(gs, vars()[temp], sites)
    i=0 
    # extract the x, y, z-values to 1-D arrays for plotting
    xx = dfc_1['X-Coordinate'].to_numpy()
    yy = dfc_1['Y-Coordinate'].to_numpy()
    siteinfo = pd.DataFrame(sitenames)
    
    for dfhn in hourlist:
        dfh = pd.DataFrame(dfhn)
        hour=i
        stab=hourly_stab[i]
        print(stab)
        # Particulate matter
        zzp = (dfh['C_G1']*hwpme+dfh['C_G2']*hwpme).to_numpy()
        # NOx
        zzn = (dfh['C_G1']*hwnxe+dfh['C_G2']*hwnxe).to_numpy()

        max = (dfh['C_G1']*hwpme+dfh['C_G2']*hwpme).max()
        min = (dfh['C_G1']*hwpme+dfh['C_G2']*hwpme).min()

        # get the concentration values at the 4 receptor sites
        dfs1 = dfh[((dfh['X-Coordinate'] == 20.000) & (dfh['Y-Coordinate'] == 20.000))]
        dfs2 = dfh[((dfh['X-Coordinate'] == 20.000) & (dfh['Y-Coordinate'] == -20.000))]
        dfs3 = dfh[((dfh['X-Coordinate'] == -20.000) & (dfh['Y-Coordinate'] == -20.000))]
        dfs4 = dfh[((dfh['X-Coordinate'] == -20.000) & (dfh['Y-Coordinate'] == 20.000))]
        # Get the concentration values at the 4 receptor sites
        # Particulates first
        s1zp = dfs1.iloc[0]['C_G1']*hwpme+dfs1.iloc[0]['C_G2']*hwpme
        s2zp = dfs2.iloc[0]['C_G1']*hwpme+dfs2.iloc[0]['C_G2']*hwpme
        s3zp = dfs3.iloc[0]['C_G1']*hwpme+dfs3.iloc[0]['C_G2']*hwpme
        s4zp = dfs4.iloc[0]['C_G1']*hwpme+dfs4.iloc[0]['C_G2']*hwpme
        # Next NOx
        s1zn = dfs1.iloc[0]['C_G1']*hwnxe+dfs1.iloc[0]['C_G2']*hwnxe
        s2zn = dfs2.iloc[0]['C_G1']*hwnxe+dfs2.iloc[0]['C_G2']*hwnxe
        s3zn = dfs3.iloc[0]['C_G1']*hwnxe+dfs3.iloc[0]['C_G2']*hwnxe
        s4zn = dfs4.iloc[0]['C_G1']*hwnxe+dfs4.iloc[0]['C_G2']*hwnxe
    
        sitesp = [s1zp, s2zp, s3zp, s4zp]
        sitesn = [s1zn, s2zn, s3zn, s4zn]
        # Put the Conc data into a Pandas DataFrame so you can display it
        siteinfo = pd.DataFrame(index=sitenames)
        siteinfo['PM']  = sitesp
        siteinfo['NOx']  = sitesn
        siteinfo['PM'] = pd.Series([np.round(val, 2) for val in siteinfo['PM']], index = siteinfo.index)
        siteinfo['NOx'] = pd.Series([np.round(val, 2) for val in siteinfo['NOx']], index = siteinfo.index)
        print(siteinfo)
        # pass to plotting routine
        pls.pls(gs, xx, yy, zzp, hour, min, max, methourlist[i], sitesp, stab)
        i=i+1
        print('-----------------------------------------------------')
