import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy import units as u
from matplotlib import cm
import matplotlib as mpl


# ---------------------------------------------------------------------------
# Created By : Lauren I Biddle
# Created Date: 18 Nov 2021
# Version = 1.0
#
# Description: Reads in a csv file downloaded from NASA Exoplanet Archive and
#              condenses parameters for planets with multiple rows into a
#              single row containing the average value for each respective
#              parameter, while ignoring planets with only one reported row.
#              The script then saves the condensed dataframe to as a new csv.
#
# How to run:  1. Download csv from NASA Exoplanet Archive containing desired
#                 columns, and remove the descriptive header rows.
#                 ['archive_download.csv']
#              2. Create a separate csv with the first column containing the
#                 text in each column header in 'archive_download.csv'. The
#                 second column should include the desired text for the
#                 headers of the condensed dataframe. The third column
#                 contains flags to indicate whether that respective column
#                 should be condensed. 1 = calculate average, 0 = do nothing
#                 ['Column_Labels.csv']
#              3. Specify the path and filename of the the csv file downloaded
#                 from NASA Exoplanet Archive
#              4. Specify the path and filename of the csv containing column
#                 header labels and flags
# ---------------------------------------------------------------------------

def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap
def choose_cmap(custom_cmap):
    # colors1 = [(102/255, 0/255, 204/255), (255/255, 128/255, 0/255), (0/255, 153/255, 153/255)]
    # colors2 = [(204/255, 0/255, 102/255), (51/255, 51/255, 204/255), (153/255, 204/255, 0/255)]
    # colors3 = [(128/255, 0/255, 64/255),(51/255, 51/255, 204/255),(0/255, 255/255, 153/255)]
    # colors4 = [(255/255, 255/255, 255/255),(0/255, 255/255, 204/255),(0/255, 153/255, 204/255),(0/255, 153/255, 255/255),(102/255, 0/255, 204/255)]
    # colors5 = [(255/255, 255/255, 255/255),(153/255, 255/255, 153/255),(255/255, 204/255, 0/255),(255/255, 0/255, 102/255),(115/255, 0/255, 123/255)]
    # colors6 = [(255/255, 255/255, 255/255),(255/255, 204/255, 0/255),(255/255, 0/255, 102/255),(115/255, 0/255, 123/255),(0/255, 0/255, 77/255)]
    colors7 = [(255 / 255, 255 / 255, 255 / 255), (255 / 255, 204 / 255, 0 / 255), (255 / 255, 0 / 255, 102 / 255), (134 / 255, 0 / 255, 179 / 255), (0 / 255, 0 / 255, 77 / 255)]
    # colors8 = [(255 / 255, 255 / 255, 255 / 255), (255 / 255, 0 / 255, 102 / 255), (153 / 255, 0 / 255, 204 / 255), (0 / 255, 0 / 255, 77 / 255)]
    # colors9 = [(255/255, 255/255, 255/255),(255/255, 204/255, 0/255),(255/255, 0/255, 102/255),(115/255, 0/255, 123/255)]
    colors10 = [(0 / 255, 255 / 255, 204 / 255), (255 / 255, 204 / 255, 0 / 255), (255 / 255, 0 / 255, 102 / 255), (134 / 255, 0 / 255, 179 / 255), (0 / 255, 0 / 255, 77 / 255)]
    colors11 = [(0 / 255, 102 / 255, 153 / 255), (255 / 255, 204 / 255, 0 / 255), (255 / 255, 0 / 255, 102 / 255), (134 / 255, 0 / 255, 179 / 255), (0 / 255, 0 / 255, 77 / 255)]

    colors12 = [(255 / 255, 0 / 255, 102 / 255), (153 / 255, 0 / 255, 255 / 255), (0 / 255, 102 / 255, 255 / 255), (0 / 255, 153 / 255, 153 / 255), (102 / 255, 204 / 255, 0 / 255)]
    colors13 = [(158 / 255, 46 / 255, 102 / 255), (138 / 255, 77 / 255, 179 / 255), (57 / 255, 113 / 255, 198 / 255), (38 / 255, 115 / 255, 115 / 255), (89 / 255, 143 / 255, 36 / 255)]
    colors14 = [(158 / 255, 46 / 255, 102 / 255), (138 / 255, 77 / 255, 179 / 255), (57 / 255, 113 / 255, 198 / 255), (38 / 255, 115 / 255, 115 / 255), (89 / 255, 143 / 255, 36 / 255)]


    my_blue_yellow_red = [(0 / 255, 74 / 255, 171 / 255),
                          (255 / 255, 209 / 255, 26 / 255),
                          (178 / 255, 0 / 255, 3 / 255)]

    my_blue_yellow_red_light = [(32 / 255, 101 / 255, 162 / 255),
                                (251 / 255, 253 / 255, 131 / 255),
                                (169 / 255, 40 / 255, 69 / 255)]

    my_blue_green_red = [(0 / 255, 74 / 255, 171 / 255),
                         (0 / 255, 176 / 255, 9 / 255),
                         (178 / 255, 0 / 255, 3 / 255)]

    my_blue_green_red = [(0 / 255, 74 / 255, 171 / 255),
                         (0 / 255, 176 / 255, 9 / 255),
                         (178 / 255, 0 / 255, 3 / 255)]

    my_blue_red_green = [(14 / 255, 0 / 255, 240 / 255),
                         (216 / 255, 0 / 255, 0 / 255),
                         (46 / 255, 251 / 255, 32 / 255)]

    my_yellow_red_purple = [(255 / 255, 209 / 255, 26 / 255),
                            (200 / 255, 5 / 255, 0 / 255),
                            (56 / 255, 5 / 255, 120 / 255)]

    my_yellow_red_blue = [(255 / 255, 209 / 255, 26 / 255),
                          (200 / 255, 5 / 255, 0 / 255),
                          (0 / 255, 0 / 255, 153 / 255)]

    my_vibrant_rainbow = [(234 / 255, 51 / 255, 34 / 255),
                          (241 / 255, 138 / 255, 0 / 255),
                          (88 / 255, 250 / 255, 172 / 255),
                          (33 / 255, 153 / 255, 230 / 255),
                          (116 / 255, 20 / 255, 245 / 255)]

    my_sunset_purples = [(255 / 255, 204 / 255, 0 / 255),
                         (255 / 255, 80 / 255, 80 / 255),
                         (204 / 255, 0 / 255, 153 / 255),
                         (102 / 255, 0 / 255, 102 / 255),
                         (31 / 255, 0 / 255, 77 / 255)]

    my_sunset_melon = [(255 / 255, 204 / 255, 0 / 255),
                       (255 / 255, 71 / 255, 26 / 255),
                       (188 / 255, 49 / 255, 121 / 255),
                       (87 / 255, 49 / 255, 116 / 255),
                       (0 / 255, 52 / 255, 75 / 255)]

    my_black_orange_red = [(0 / 255, 0 / 255, 0 / 255),
                           (230 / 255, 92 / 255, 0 / 255),
                           (230 / 255, 0 / 255, 0 / 255)]

    my_black_red = [(0 / 255, 0 / 255, 0 / 255),
                    (230 / 255, 0 / 255, 0 / 255)]

    my_darkteal_red = [(0 / 255, 52 / 255, 75 / 255),
                       (230 / 255, 0 / 255, 0 / 255)]



    if custom_cmap == 'my_blue_yellow_red':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_blue_yellow_red, position=positions)

    if custom_cmap == 'my_blue_yellow_red_light':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_blue_yellow_red_light, position=positions)

    if custom_cmap == 'my_blue_green_red':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_blue_green_red, position=positions)

    if custom_cmap == 'my_blue_red_green':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_blue_red_green, position=positions)

    if custom_cmap == 'my_yellow_red_purple':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_yellow_red_purple, position=positions)

    if custom_cmap == 'my_yellow_red_blue':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_yellow_red_blue, position=positions)

    if custom_cmap == 'my_vibrant_rainbow':
        positions = [0, 0.25, 0.5, 0.75, 1]
        mycolormap = make_cmap(my_vibrant_rainbow, position=positions)

    if custom_cmap == 'my_sunset_purples':
        positions = [0, 0.25, 0.5, 0.75, 1]
        mycolormap = make_cmap(my_sunset_purples, position=positions)

    if custom_cmap == 'my_sunset_melon':
        positions = [0, 0.25, 0.5, 0.75, 1]
        mycolormap = make_cmap(my_sunset_melon, position=positions)

    if custom_cmap == 'my_black_orange_red':
        positions = [0, 0.5, 1]
        mycolormap = make_cmap(my_black_orange_red, position=positions)

    if custom_cmap == 'my_black_red':
        positions = [0, 1]
        mycolormap = make_cmap(my_black_red, position=positions)

    if custom_cmap == 'my_darkteal_red':
        positions = [0, 1]
        mycolormap = make_cmap(my_darkteal_red, position=positions)


    # 89, 143, 36
    # position = [0, 0.5, 1]
    # position2 = [0, 0.25, 0.5, 0.75, 1]
    # position2_2 = [0, 0.25, 0.5, 0.75, 1]
    # # position3 = [0, 1./3., 2./3., 1]
    # mycolormap = make_cmap(colors12, position=position2_2)

    return mycolormap

def calc_a_over_Rstar(row_df):

    if (np.isnan(row_df['pl_orbsmax'].values[0]) == False) and (np.isnan(row_df['st_rad'].values[0]) == False):
        a_pl = row_df['pl_orbsmax'].values[0]
        a_pl_upper = row_df['pl_orbsmaxerr1'].values[0]
        a_pl_lower = row_df['pl_orbsmaxerr2'].values[0]
        a_pl_err = np.nanmax([a_pl_upper,a_pl_lower])

        Rstar_au = (row_df['st_rad'].values[0] * u.Rsun).to(u.au).value
        Rstar_au_upper = (row_df['st_raderr1'].values[0] * u.Rsun).to(u.au).value
        Rstar_au_lower = (row_df['st_raderr2'].values[0] * u.Rsun).to(u.au).value
        Rstar_au_err = np.nanmax([Rstar_au_upper,Rstar_au_lower])

        a_over_Rstar = a_pl/Rstar_au

        if (np.isnan(a_pl_err) == True) and (np.isnan(Rstar_au_err) == False):
            a_over_Rstar_err = np.sqrt((-a_pl/(Rstar_au**2))**2 * Rstar_au_err**2)
        if (np.isnan(a_pl_err) == False) and (np.isnan(Rstar_au_err) == True):
            a_over_Rstar_err = np.sqrt((1./Rstar_au)**2 * a_pl_err**2)
        if (np.isnan(a_pl_err) == False) and (np.isnan(Rstar_au_err) == False):
            a_over_Rstar_err = np.sqrt(((-a_pl/(Rstar_au**2)) * Rstar_au_err**2) + ((-a_pl/(Rstar_au**2))**2 * Rstar_au_err**2))
        if (np.isnan(a_pl_err) == True) and (np.isnan(Rstar_au_err) == True):
            a_over_Rstar_err = float('nan')

    else:
        a_over_Rstar = float('nan')
        a_over_Rstar_err = float('nan')


    return a_over_Rstar, a_over_Rstar_err
def calc_a_over_Rstar2(row_df):

    if (np.isnan(row_df['Orbit Semi-Major Axis (au))'].values[0]) == False) and (np.isnan(row_df['Stellar Radius (Solar Radius)'].values[0]) == False):
        a_pl = row_df['Orbit Semi-Major Axis (au))'].values[0]
        a_pl_upper = row_df['Orbit Semi-Major Axis Upper Unc. (au)'].values[0]
        a_pl_lower = row_df['Orbit Semi-Major Axis Lower Unc. (au)'].values[0]
        a_pl_err = np.nanmax([a_pl_upper,a_pl_lower])

        # import pdb; pdb.set_trace()

        Rstar_au = (row_df['Stellar Radius (Solar Radius)'].values[0] * u.Rsun).to(u.au).value
        Rstar_au_upper = (row_df['Stellar Radius Upper Unc. (Solar Radius)'].values[0] * u.Rsun).to(u.au).value
        Rstar_au_lower = (row_df['Stellar Radius Lower Unc. (Solar Radius)'].values[0] * u.Rsun).to(u.au).value
        Rstar_au_err = np.nanmax([Rstar_au_upper,Rstar_au_lower])

        a_over_Rstar = a_pl/Rstar_au

        if (np.isnan(a_pl_err) == True) and (np.isnan(Rstar_au_err) == False):
            a_over_Rstar_err = np.sqrt((-a_pl/(Rstar_au**2))**2 * Rstar_au_err**2)
        if (np.isnan(a_pl_err) == False) and (np.isnan(Rstar_au_err) == True):
            a_over_Rstar_err = np.sqrt((1./Rstar_au)**2 * a_pl_err**2)
        if (np.isnan(a_pl_err) == False) and (np.isnan(Rstar_au_err) == False):
            a_over_Rstar_err = np.sqrt(((-a_pl/(Rstar_au**2)) * Rstar_au_err**2) + ((-a_pl/(Rstar_au**2))**2 * Rstar_au_err**2))
        if (np.isnan(a_pl_err) == True) and (np.isnan(Rstar_au_err) == True):
            a_over_Rstar_err = float('nan')

    else:
        a_over_Rstar = float('nan')
        a_over_Rstar_err = float('nan')


    return a_over_Rstar, a_over_Rstar_err
def calc_Mjup(row_df):
    if (np.isnan(row_df['pl_masse'].values[0]) == False):
        pl_Mjup = (row_df['pl_masse'].values[0] * u.Mearth).to(u.Mjup).value
        pl_Mjup_upper = (row_df['pl_masseerr1'].values[0] * u.Mearth).to(u.Mjup).value
        pl_Mjup_lower = (row_df['pl_masseerr2'].values[0] * u.Mearth).to(u.Mjup).value
        pl_Mjup_err = np.nanmax([pl_Mjup_upper, pl_Mjup_lower])
    else:
        pl_Mjup = float('nan')
        pl_Mjup_err = float('nan')
    return pl_Mjup, pl_Mjup_err
def calc_Rjup(row_df):
    if (np.isnan(row_df['pl_rade'].values[0]) == False):
        pl_Rjup = (row_df['pl_rade'].values[0] * u.Rearth).to(u.Rjup).value
        pl_Rjup_upper = (row_df['pl_radeerr1'].values[0] * u.Rearth).to(u.Rjup).value
        pl_Rjup_lower = (row_df['pl_radeerr2'].values[0] * u.Rearth).to(u.Rjup).value
        pl_Rjup_err = np.nanmax([pl_Rjup_upper, pl_Rjup_lower])
    else:
        pl_Rjup = float('nan')
        pl_Rjup_err = float('nan')
    return pl_Rjup, pl_Rjup_err
def calc_mean_Prot(input_array):

    got_it = 0
    if len(input_array) > 1:
        mean_per = np.mean(input_array)
        std_per = np.std(input_array)
        distance_from_mean = abs(input_array - mean_per)
        max_deviations = 1
        not_outlier = distance_from_mean < max_deviations * std_per
        rot_pers = input_array[not_outlier]

        if len(rot_pers > 2):
            mean_per = np.mean(rot_pers)
            std_per = np.std(rot_pers)
            distance_from_mean = abs(rot_pers - mean_per)
            if len(rot_pers > 2):
                max_deviations = 1
            not_outlier = distance_from_mean < max_deviations * std_per
            rot_pers = rot_pers[not_outlier]

            std_per = np.std(rot_pers)

        if np.isnan(std_per) == False:
            if std_per > 3:
                prot = np.float('nan')
                got_it = 1

    if len(input_array) == 1:
        prot = np.nanmean(input_array)
        got_it = 1

    if got_it != 1:

        prot = np.float('nan')

    return prot
def calc_mean_Age(input_array):

    got_it = 0
    if len(input_array) > 1:
        mean_per = np.mean(input_array)
        std_per = np.std(input_array)
        distance_from_mean = abs(input_array - mean_per)
        max_deviations = 1
        not_outlier = distance_from_mean < max_deviations * std_per
        rot_pers = input_array[not_outlier]

        if len(rot_pers > 2):
            mean_per = np.mean(rot_pers)
            std_per = np.std(rot_pers)
            distance_from_mean = abs(rot_pers - mean_per)
            if len(rot_pers > 2):
                max_deviations = 1
            not_outlier = distance_from_mean < max_deviations * std_per
            rot_pers = rot_pers[not_outlier]

            std_per = np.std(rot_pers)

        if np.isnan(std_per) == False:
            if std_per > 3:
                prot = np.float('nan')
                got_it = 1

    if len(input_array) == 1:
        prot = np.nanmean(input_array)
        got_it = 1

    if got_it != 1:

        prot = np.float('nan')

    return prot

def condense_planet_pars(input_df,col_labs_df,save_name):
    cols = input_df.columns
    condensed_df = pd.DataFrame(columns=input_df.columns)

    col_labels_dict = {}
    for i, old_label in enumerate(col_labs_df['Download Column Head']):
        col_labels_dict[old_label] = col_labs_df['Usable Column Label'][i]

    accounted_for = []

    for planet_i,planet in enumerate(input_df['pl_name']):
        percent_completed = (planet_i+1)/len(input_df['pl_name'])*100
        print(percent_completed)

        # if (percent_completed >= 5) and (np.mod(np.round(percent_completed), 5) == 0):
        #     print(condensed_df)
        #     import pdb; pdb.set_trace()

        if planet not in accounted_for:

            planet_df = input_df.loc[input_df['pl_name'] == planet]
            temp_df = planet_df.loc[planet_df['default_flag'] == 1]
            # temp_df.index[temp_df['default_flag'] == 1].tolist()

            if len(planet_df) > 1:
                for col in cols:
                    temp_col_df = col_labs_df.loc[col_labs_df['Download Column Head'] == col]
                    # print(col)
                    # print(temp_col_df['Combine Pars'].values)
                    # import pdb; pdb.set_trace()
                    if temp_col_df['Combine Pars'].values[0] == 1:

                        colvals = planet_df[col].values
                        # try:
                        colvals = colvals[np.isnan(colvals) == False]
                        # except:
                        #     print(col)
                        #     import pdb; pdb.set_trace()

                        if len(colvals) > 0:
                            if len(colvals) > 1:
                                colval = np.nanmean(colvals)
                            else:
                                colval = colvals[0]

                            # temp_df = temp_df.reset_index()
                            # temp_df.at[0, col] = colval
                            temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], col] = colval

                        else:
                            continue
            if len(temp_df['pl_ratdor'].values) > 0:
                if np.isnan(temp_df['pl_ratdor'].values[0]) == True:
                    a_over_Rstar, a_over_Rstar_err = calc_a_over_Rstar(row_df=temp_df)
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_ratdor'] = a_over_Rstar
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_ratdorerr1'] = a_over_Rstar_err
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_ratdorerr2'] = a_over_Rstar_err
            if len(temp_df['pl_massj'].values) > 0:
                if (np.isnan(temp_df['pl_massj'].values[0]) == False):
                    pl_Mjup, pl_Mjup_err = calc_Mjup(row_df=temp_df)
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_massj'] = pl_Mjup
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_massjerr1'] = pl_Mjup_err
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_massjerr2'] = pl_Mjup_err
            if len(temp_df['pl_radj'].values) > 0:
                if (np.isnan(temp_df['pl_radj'].values[0]) == False):
                    pl_Rjup, pl_Rjup_err = calc_Mjup(row_df=temp_df)
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_radj'] = pl_Rjup
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_radjerr1'] = pl_Rjup_err
                    temp_df.at[temp_df.index[temp_df['default_flag'] == 1].values[0], 'pl_radjerr2'] = pl_Rjup_err

            condensed_df = condensed_df.append(temp_df)

            accounted_for.append(planet)


    condensed_df.rename(columns=col_labels_dict, inplace=True)

    condensed_df.to_csv(save_name, index=False)
    # import pdb; pdb.set_trace()

    return condensed_df
def add_missing_stellar_pars(input_df,star_rots_df,save_name):

    rots_added_df = pd.DataFrame(columns=input_df.columns)

    accounted_for = []

    for star_i, star in enumerate(input_df['Host Name'].values):

        percent_completed = (star_i + 1) / len(input_df['Host Name'].values) * 100
        print(percent_completed)

        if star not in accounted_for:

            star_df = input_df.loc[input_df['Host Name'] == star]

            # if np.isnan(star_df['Stellar Rotational Period (days)'].values[0]) == False:
            #
            #     rots_added_df = rots_added_df.append(star_df)


            if (np.isnan(star_df['Stellar Rotational Period (days)'].values[0]) == True) and (star in star_rots_df['Star'].values):

                print('added rot')

                star_rot_df = star_rots_df.loc[star_rots_df['Star'] == star]
                # if np.isnan(star_df['Stellar Rotational Period (days)'].values[0]) == True:

                if len(star_rot_df) == 1:
                    star_rot = star_rot_df['Prot'].values[0]
                    if star_rot == '--':
                        star_rot = float('nan')
                    if star_rot == '*':
                        star_rot = float('nan')
                    # star_df.at[star_df.index[star_df['Default Parameter Set'] == 1].values[0], 'Stellar Rotational Period (days)'] = float(star_rot)
                    for row_i1 in range(len(star_df)):
                        star_df.at[star_df.index[star_df['Default Parameter Set'] == 1].values[row_i1], 'Stellar Rotational Period (days)'] = float(star_rot)


                if len(star_rot_df) > 1:
                    star_rots = star_rot_df['Prot'].values

                    star_rots = star_rots[star_rots != '--']
                    star_rots = star_rots[star_rots != '*']
                    star_rots = np.array(star_rots).astype(float)
                    star_rots = star_rots[np.isnan(star_rots) == False]

                    mean_star_rot = calc_mean_Prot(input_array=star_rots)

                    # import pdb; pdb.set_trace()

                    for row_i2 in range(len(star_df)):
                        star_df.at[star_df.index[star_df['Default Parameter Set'] == 1].values[row_i2], 'Stellar Rotational Period (days)'] = float(mean_star_rot)

                rots_added_df = rots_added_df.append(star_df)

            else:
                rots_added_df = rots_added_df.append(star_df)

        accounted_for.append(star)

    rots_added_df.to_csv(save_name, index=False)

    return rots_added_df
def add_missing_age_pars(input_df,star_ages_df,save_name):

    ages_added_df = pd.DataFrame(columns=input_df.columns)

    accounted_for = []

    for star_i, star in enumerate(input_df['Host Name'].values):

        percent_completed = (star_i + 1) / len(input_df['Host Name'].values) * 100
        print(percent_completed)

        if star not in accounted_for:

            star_df = input_df.loc[input_df['Host Name'] == star]

            # if np.isnan(star_df['Stellar Rotational Period (days)'].values[0]) == False:
            #
            #     rots_added_df = rots_added_df.append(star_df)


            if (np.isnan(star_df['Stellar Age (Gyr)'].values[0]) == True) and (star in star_ages_df['Star'].values):

                star_age_df = star_ages_df.loc[star_ages_df['Star'] == star]

                # changed = 0
                for index_i, index in enumerate(star_age_df.index):
                    if star_age_df.at[star_age_df.index[index_i], 'Unit'] == 'Myr':
                        # print(star_age_df)
                        # import pdb; pdb.set_trace()
                        # changed = 1
                        if (star_age_df.at[star_age_df.index[index_i], 'Age'] == '--') or (star_age_df.at[star_age_df.index[index_i], 'Age'] == '---'):
                            star_age_df.at[star_age_df.index[index_i], 'Age'] = float('nan')
                        else:
                            star_age_df.at[star_age_df.index[index_i], 'Age'] = float(star_age_df.at[star_age_df.index[index_i], 'Age'])/1000.
                        star_age_df.at[star_age_df.index[index_i], 'Unit'] = 'Gyr'

                    if star_age_df.at[star_age_df.index[index_i], 'Unit'] == 'yr':
                        # print(star_age_df)
                        # import pdb; pdb.set_trace()
                        # changed = 1
                        if (star_age_df.at[star_age_df.index[index_i], 'Age'] == '--') or (star_age_df.at[star_age_df.index[index_i], 'Age'] == '---'):
                            star_age_df.at[star_age_df.index[index_i], 'Age'] = float('nan')
                        else:
                            star_age_df.at[star_age_df.index[index_i], 'Age'] = float(star_age_df.at[star_age_df.index[index_i], 'Age'])/1000000000.
                        star_age_df.at[star_age_df.index[index_i], 'Unit'] = 'Gyr'

                    if star_age_df.at[star_age_df.index[index_i], 'Unit'] == 'None':
                        # print(star_age_df)
                        # import pdb; pdb.set_trace()
                        # changed = 1
                        star_age_df.at[star_age_df.index[index_i], 'Age'] = float('nan')

                # if changed == 1:
                #     print(star_age_df)
                #     import pdb; pdb.set_trace()

                if len(star_age_df) == 1:
                    star_age = star_age_df['Age'].values[0]
                    if star_age == '--':
                        star_age = float('nan')
                    if star_age == '---':
                        star_age = float('nan')
                    if star_age == '*':
                        star_age = float('nan')
                    if star_age == '0.7-4.7':
                        star_age = float('nan')
                    if star_age == '3-6':
                        star_age = float('nan')
                    if star_age == '1.5-3':
                        star_age = float('nan')

                    for row_i1 in range(len(star_df)):
                        star_df.at[star_df.index[star_df['Default Parameter Set'] == 1].values[row_i1], 'Stellar Age (Gyr)'] = float(star_age)

                if len(star_age_df) > 1:
                    star_ages = star_age_df['Age'].values

                    star_ages = star_ages[star_ages != '--']
                    star_ages = star_ages[star_ages != '---']
                    star_ages = star_ages[star_ages != '*']
                    star_ages = star_ages[star_ages != '0.7-4.7']
                    star_ages = star_ages[star_ages != '3-6']
                    star_ages = star_ages[star_ages != '1.5-3']
                    star_ages = np.array(star_ages).astype(float)
                    star_ages = star_ages[np.isnan(star_ages) == False]

                    mean_star_age = calc_mean_Age(input_array=star_ages)

                    # import pdb; pdb.set_trace()

                    for row_i2 in range(len(star_df)):
                        star_df.at[star_df.index[star_df['Default Parameter Set'] == 1].values[row_i2], 'Stellar Age (Gyr)'] = float(mean_star_age)
                    # star_df.at[star_df.index[star_df['Default Parameter Set'] == 1].values[0], 'Stellar Age (Gyr)'] = float(mean_star_age)

                ages_added_df = ages_added_df.append(star_df)

            else:
                ages_added_df = ages_added_df.append(star_df)

        accounted_for.append(star)

    ages_added_df.to_csv(save_name, index=False)

    return ages_added_df
def add_exoplanets_dot_org_data(input_df,exo_dot_org_df,save_name):
    new_data_added_df = pd.DataFrame(columns=input_df.columns)

    accounted_for = []

    for planet_i, planet in enumerate(input_df['Planet Name'].values):

        percent_completed = (planet_i + 1) / len(input_df['Planet Name'].values) * 100
        print(percent_completed)

        planet_df = input_df.loc[input_df['Planet Name'] == planet]

        star = planet_df['Host Name'].values[0]

        if planet not in accounted_for:

            if star in exo_dot_org_df['STAR'].values:

                star_data_df = exo_dot_org_df.loc[exo_dot_org_df['STAR'] == star]

                star_radius = star_data_df['RSTAR (Rsun)'].values[0]

                if (np.isnan(star_radius) == False) and (np.isnan(planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Radius (Solar Radius)']) == True):
                    print('Added Radius: ' + str(star_radius))
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Radius (Solar Radius)'] = float(star_radius)

                star_mass = star_data_df['MSTAR (Msun)'].values[0]

                if (np.isnan(star_mass) == False) and (np.isnan(planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Mass (Solar mass)']) == True):
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Mass (Solar mass)'] = float(star_mass)

                star_teff = star_data_df['TEFF (K)'].values[0]

                if (np.isnan(star_teff) == False) and (np.isnan(planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Effective Temperature (K)']) == True):
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Effective Temperature (K)'] = float(star_teff)

                star_logg = star_data_df['LOGG'].values[0]

                if (np.isnan(star_teff) == False) and (np.isnan(planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Surface Gravity (log10(cm/s**2))']) == True):
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Stellar Surface Gravity (log10(cm/s**2))'] = float(star_logg)

                if np.isnan(planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Ratio of Semi-Major Axis to Stellar Radius']) == True:
                    # import pdb; pdb.set_trace()
                    a_over_Rstar, a_over_Rstar_err = calc_a_over_Rstar2(row_df=planet_df)
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Ratio of Semi-Major Axis to Stellar Radius'] = a_over_Rstar
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Ratio of Semi-Major Axis to Stellar Radius Upper Unc.'] = a_over_Rstar_err
                    planet_df.at[planet_df.index[planet_df['Default Parameter Set'] == 1].values[0], 'Ratio of Semi-Major Axis to Stellar Radius Lower Unc.'] = a_over_Rstar_err

            new_data_added_df = new_data_added_df.append(planet_df)

            accounted_for.append(planet)

    new_data_added_df.to_csv(save_name, index=False)

    return new_data_added_df


def impose_restrictions(input_df, restriction_dict):
    # dataframe = dataframe[dataframe['Default Flag'] == 1]
    # dataframe = dataframe[pd.isnull(dataframe[restriction_dict['track with']]) == False]
    dataframe = input_df[input_df['Number of Planets'] >= restriction_dict['min number of planets in system']]
    dataframe = dataframe[dataframe['Number of Planets'] <= restriction_dict['max number of planets in system']]

    if restriction_dict['exclude circumbinaries'] == True:
        dataframe = dataframe[dataframe['Circumbinary Flag'] != 1]
    if restriction_dict['exclude multiple star systems'] == True:
        dataframe = dataframe[dataframe['Number of Stars'] == 1]
    if restriction_dict['exclude eccentric planet orbits'] == True:
        dataframe = dataframe[dataframe['Eccentricity'] == 0]
    if restriction_dict['exclude controversial planets'] == True:
        dataframe = dataframe[dataframe['Controversial Flag'] != 1]
    # if restriction_dict['max rotation limit'] != 'None':
    #     dataframe = dataframe[dataframe['Stellar Rotation Period (d)'] <= restriction_dict['max rotation limit']]
    if restriction_dict['max vsini limit'] != 'None':
        dataframe = dataframe[dataframe['Stellar Rotational Velocity (km/s)'] <= restriction_dict['max vsini limit']]
    if restriction_dict['require these detection methods'] != 'None':
        detection_keys = []
        for method in restriction_dict['require these detection methods']:
            detection_keys.append(method+' Flag')
        dataframe = dataframe[dataframe[detection_keys] == 1]
    if restriction_dict['require these discovery methods'] != 'None':
        discovery_keys = []
        for discovery_method in restriction_dict['require these discovery methods']:
            discovery_keys.append(discovery_method + ' Flag')
        dataframe = dataframe[dataframe[discovery_keys] == 1]
    if restriction_dict['Teff limits'] != 'None':
        dataframe = dataframe[dataframe['Stellar Effective Temperature (K)'] >= restriction_dict['Teff limits'][0]]
        dataframe = dataframe[dataframe['Stellar Effective Temperature (K)'] <= restriction_dict['Teff limits'][1]]
    if restriction_dict['Age'] != 'None':
        dataframe = dataframe[dataframe['Stellar Age (Gyr)'] >= restriction_dict['Age'][0]]
        dataframe = dataframe[dataframe['Stellar Age (Gyr)'] <= restriction_dict['Age'][1]]
    if restriction_dict['Mstar'] != 'None':
        dataframe = dataframe[dataframe['Stellar Mass (Solar mass)'] >= restriction_dict['Mstar'][0]]
        dataframe = dataframe[dataframe['Stellar Mass (Solar mass)'] <= restriction_dict['Mstar'][1]]
    if restriction_dict['max orbit semi-major axis (au)'] != 'None':
        dataframe = dataframe[dataframe['Orbit Semi-Major Axis (au))'] <= restriction_dict['max orbit semi-major axis (au)']]


    return dataframe

# def a_vs_Mplanet(input_df, Rot_Max = 50, Num_Segments=3, color_by_star_rot=True):
#
#     df_notnull = input_df[pd.isnull(input_df['Orbit Semi-Major Axis (au))']) == False]
#     df_notnull = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#     if color_by_star_rot == True:
#         df_notnull = df_notnull[pd.isnull(df_notnull['Stellar Rotational Period (days)']) == False]
#         df_notnull = df_notnull[df_notnull['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot = df_notnull['Stellar Rotational Period (days)'].values
#
#         cmap = cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a = df_notnull['Orbit Semi-Major Axis (au))'].values
#     pl_Mjup = df_notnull['Planet Mass (Jupiter Mass)'].values
#
#     # import pdb; pdb.set_trace()
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(6, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a, pl_Mjup, c=st_Rot, cmap=cmap, norm=norm, s=np.pi * (2) ** 2)
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a, pl_Mjup, color='#000000', s=np.pi * (2) ** 2)
#
#     ax.set_xlabel('Orbit Semi-Major Axis (au)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min(pl_Mjup) - 0.001, np.max(pl_Mjup) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     plt.tight_layout()
#     plt.show()
# def aoverRstar_vs_Mplanet(input_df, Rot_Max = 50, Num_Segments=3,color_by_star_rot=True):
#
#     df_notnull = input_df[pd.isnull(input_df['Ratio of Semi-Major Axis to Stellar Radius']) == False]
#     df_notnull = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull = df_notnull[pd.isnull(df_notnull['Stellar Rotational Period (days)']) == False]
#         df_notnull = df_notnull[df_notnull['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot = df_notnull['Stellar Rotational Period (days)'].values
#
#         cmap = cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a = df_notnull['Ratio of Semi-Major Axis to Stellar Radius'].values
#     pl_Mjup = df_notnull['Planet Mass (Jupiter Mass)'].values
#
#     # cmap = cm.rainbow  # cm.brg # cm.winter
#     # map_bounds = np.linspace(np.nanmin(n_planets), np.nanmax(n_planets) + 1, np.max(n_planets))
#     # norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(6, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a, pl_Mjup, c=st_Rot, cmap=cmap, norm=norm, s=np.pi * (2) ** 2)
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a, pl_Mjup, color='#000000', s=np.pi * (2) ** 2)
#
#     ax.set_xlabel('a/Rstar', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min(pl_Mjup) - 0.001, np.max(pl_Mjup) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     plt.tight_layout()
#     plt.show()
# def OrbitalPeriod_vs_Mplanet(input_df, Rot_Max = 50, Num_Segments=3,color_by_star_rot=True):
#
#     df_notnull = input_df[pd.isnull(input_df['Orbital Period (days)']) == False]
#     df_notnull = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull = df_notnull[pd.isnull(df_notnull['Stellar Rotational Period (days)']) == False]
#         df_notnull = df_notnull[df_notnull['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot = df_notnull['Stellar Rotational Period (days)'].values
#
#         cmap = cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_orb = df_notnull['Orbital Period (days)'].values
#     pl_Mjup = df_notnull['Planet Mass (Jupiter Mass)'].values
#
#     # cmap = cm.rainbow  # cm.brg # cm.winter
#     # map_bounds = np.linspace(np.nanmin(n_planets), np.nanmax(n_planets) + 1, np.max(n_planets))
#     # norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(6, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_orb, pl_Mjup, c=st_Rot, cmap=cmap, norm=norm, s=np.pi * (2) ** 2)
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_orb, pl_Mjup, color='#000000', s=np.pi * (2) ** 2)
#
#     ax.set_xlabel('Orbital Period (days)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min(pl_Mjup) - 0.001, np.max(pl_Mjup) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     plt.tight_layout()
#     plt.show()

# def a_vs_MsiniPlanet(input_df, Rot_Max = 50, Num_Segments=3, color_by_star_rot=True):
#
#     df_notnull = input_df[pd.isnull(input_df['Orbit Semi-Major Axis (au))']) == False]
#     df_notnull = df_notnull[pd.isnull(df_notnull['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#     if color_by_star_rot == True:
#         df_notnull = df_notnull[pd.isnull(df_notnull['Stellar Rotational Period (days)']) == False]
#         df_notnull = df_notnull[df_notnull['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot = df_notnull['Stellar Rotational Period (days)'].values
#
#         cmap = cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a = df_notnull['Orbit Semi-Major Axis (au))'].values
#     pl_Mjup = df_notnull['Planet Mass*sin(i) (Jupiter Mass)'].values
#
#     # import pdb; pdb.set_trace()
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(6, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a, pl_Mjup, c=st_Rot, cmap=cmap, norm=norm, s=np.pi * (2) ** 2)
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a, pl_Mjup, color='#000000', s=np.pi * (2) ** 2)
#
#     ax.set_xlabel('Orbit Semi-Major Axis (au)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass*sin(i) (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min(pl_Mjup) - 0.001, np.max(pl_Mjup) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     plt.tight_layout()
#     plt.show()
# def aoverRstar_vs_MsiniPlanet(input_df, Rot_Max = 50, Num_Segments=3,color_by_star_rot=True):
#
#     df_notnull = input_df[pd.isnull(input_df['Ratio of Semi-Major Axis to Stellar Radius']) == False]
#     df_notnull = df_notnull[pd.isnull(df_notnull['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull = df_notnull[pd.isnull(df_notnull['Stellar Rotational Period (days)']) == False]
#         df_notnull = df_notnull[df_notnull['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot = df_notnull['Stellar Rotational Period (days)'].values
#
#         cmap = cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a = df_notnull['Ratio of Semi-Major Axis to Stellar Radius'].values
#     pl_Mjup = df_notnull['Planet Mass*sin(i) (Jupiter Mass)'].values
#
#     # cmap = cm.rainbow  # cm.brg # cm.winter
#     # map_bounds = np.linspace(np.nanmin(n_planets), np.nanmax(n_planets) + 1, np.max(n_planets))
#     # norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(6, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a, pl_Mjup, c=st_Rot, cmap=cmap, norm=norm, s=np.pi * (2) ** 2)
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a, pl_Mjup, color='#000000', s=np.pi * (2) ** 2)
#
#     ax.set_xlabel('a/Rstar', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass*sin(i) (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min(pl_Mjup) - 0.001, np.max(pl_Mjup) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     plt.tight_layout()
#     plt.show()
# def OrbitalPeriod_vs_MsiniPlanet(input_df, Rot_Max = 50, Num_Segments=3,color_by_star_rot=True):
#
#     df_notnull = input_df[pd.isnull(input_df['Orbital Period (days)']) == False]
#     df_notnull = df_notnull[pd.isnull(df_notnull['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull = df_notnull[pd.isnull(df_notnull['Stellar Rotational Period (days)']) == False]
#         df_notnull = df_notnull[df_notnull['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot = df_notnull['Stellar Rotational Period (days)'].values
#
#         cmap = cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_orb = df_notnull['Orbital Period (days)'].values
#     pl_Mjup = df_notnull['Planet Mass*sin(i) (Jupiter Mass)'].values
#
#     # cmap = cm.rainbow  # cm.brg # cm.winter
#     # map_bounds = np.linspace(np.nanmin(n_planets), np.nanmax(n_planets) + 1, np.max(n_planets))
#     # norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(6, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_orb, pl_Mjup, c=st_Rot, cmap=cmap, norm=norm, s=np.pi * (2) ** 2)
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_orb, pl_Mjup, color='#000000', s=np.pi * (2) ** 2)
#
#     ax.set_xlabel('Orbital Period (days)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass*sin(i) (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min(pl_Mjup) - 0.001, np.max(pl_Mjup) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     plt.tight_layout()
#     plt.show()

# def a_vs_bothMplanet(input_df, savehere, colormap, Rot_Max=50, Num_Segments=3, color_by_star_rot=True, include_msini=False):
#
#     df_notnull = input_df[pd.isnull(input_df['Orbit Semi-Major Axis (au))']) == False]
#     df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     if include_msini == True:
#         df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
#         df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         if include_msini == True:
#             df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
#             df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values
#         if include_msini == True:
#             st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values
#
#         cmap = colormap # cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a1 = df_notnull1['Orbit Semi-Major Axis (au))'].values
#     pl_a1_upper = abs(df_notnull1['Orbit Semi-Major Axis Upper Unc. (au)'].values)
#     pl_a1_lower = abs(df_notnull1['Orbit Semi-Major Axis Lower Unc. (au)'].values)
#
#     pl_Mjup1 = df_notnull1['Planet Mass (Jupiter Mass)'].values
#     pl_Mjup1_upper = abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values)
#     pl_Mjup1_lower = abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values)
#
#     if include_msini == True:
#         pl_a2 = df_notnull2['Orbit Semi-Major Axis (au))'].values
#         pl_a2_upper = abs(df_notnull2['Orbit Semi-Major Axis Upper Unc. (au)'].values)
#         pl_a2_lower = abs(df_notnull2['Orbit Semi-Major Axis Lower Unc. (au)'].values)
#
#         pl_Mjup2 = df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values
#         pl_Mjup2_upper = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values)
#         pl_Mjup2_lower = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values)
#         # pl_Mjup2 = pl_Mjup2 + 0.15*pl_Mjup2
#
#     # import pdb; pdb.set_trace()
#
#     font_size = 'medium'
#
#     plt.close()
#
#     fig = plt.figure(1, figsize=(7.5, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     errorbar_alpha_val = 1.0
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a1, pl_Mjup1, c=st_Rot1, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm, s=np.pi * (3) ** 2)
#         ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower,pl_Mjup1_upper], xerr=[pl_a1_lower,pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1,zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_a2, pl_Mjup2, marker='s', c=st_Rot2, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm)
#             ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower,pl_Mjup2_upper], xerr=[pl_a2_lower,pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1,zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a1, pl_Mjup1, color='#000000', s=np.pi * (2.75) ** 2, label='M')
#         ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower, pl_Mjup1_upper], xerr=[pl_a1_lower, pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_a2, pl_Mjup2, marker='s', color='#000000', label='Msini')
#             ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower, pl_Mjup2_upper], xerr=[pl_a2_lower, pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#
#     ax.set_xlabel('Orbit Semi-Major Axis (au)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min([np.min(pl_Mjup1),np.min(pl_Mjup2)]) - 0.002, np.max([np.max(pl_Mjup1),np.max(pl_Mjup2)]) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     ax.legend(loc='upper left')
#     plt.tight_layout()
#     plt.savefig(savehere, dpi=300)
#     plt.show()
# def aoverRstar_vs_bothMplanet(input_df, savehere, colormap, Rot_Max=50, Num_Segments=3, color_by_star_rot=True, include_msini=False):
#
#     df_notnull = input_df[pd.isnull(input_df['Ratio of Semi-Major Axis to Stellar Radius']) == False]
#     df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     if include_msini == True:
#         df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
#         df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         if include_msini == True:
#             df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
#             df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values
#         if include_msini == True:
#             st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values
#
#         cmap = colormap  # cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a1 = df_notnull1['Ratio of Semi-Major Axis to Stellar Radius'].values
#     pl_a1_upper = abs(df_notnull1['Ratio of Semi-Major Axis to Stellar Radius Upper Unc.'].values)
#     pl_a1_lower = abs(df_notnull1['Ratio of Semi-Major Axis to Stellar Radius Lower Unc.'].values)
#
#     pl_Mjup1 = df_notnull1['Planet Mass (Jupiter Mass)'].values
#     pl_Mjup1_upper = abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values)
#     pl_Mjup1_lower = abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values)
#
#     if include_msini == True:
#         pl_a2 = df_notnull2['Ratio of Semi-Major Axis to Stellar Radius'].values
#         pl_a2_upper = abs(df_notnull2['Ratio of Semi-Major Axis to Stellar Radius Upper Unc.'].values)
#         pl_a2_lower = abs(df_notnull2['Ratio of Semi-Major Axis to Stellar Radius Lower Unc.'].values)
#
#         pl_Mjup2 = df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values
#         pl_Mjup2_upper = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values)
#         pl_Mjup2_lower = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values)
#         # pl_Mjup2 = pl_Mjup2 + 0.15*pl_Mjup2
#
#     # import pdb; pdb.set_trace()
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(7.5, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     errorbar_alpha_val = 1.0
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a1, pl_Mjup1, c=st_Rot1, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm, s=np.pi * (3) ** 2)
#         ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower, pl_Mjup1_upper], xerr=[pl_a1_lower, pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_a2, pl_Mjup2, marker='s', c=st_Rot2, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm)
#             ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower, pl_Mjup2_upper], xerr=[pl_a2_lower, pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a1, pl_Mjup1, color='#000000', s=np.pi * (2.75) ** 2, label='M')
#         ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower, pl_Mjup1_upper], xerr=[pl_a1_lower, pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_a2, pl_Mjup2, marker='s', color='#000000', label='Msini')
#             ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower, pl_Mjup2_upper], xerr=[pl_a2_lower, pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#
#
#     ax.set_xlabel('a/Rstar', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min([np.min(pl_Mjup1),np.min(pl_Mjup2)]) - 0.002, np.max([np.max(pl_Mjup1),np.max(pl_Mjup2)]) + 20)
#     ax.set_xlim(np.min([np.min(pl_a1), np.min(pl_a2)]) - 0.002, np.max([np.max(pl_a1), np.max(pl_a2)]) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     ax.legend(loc='upper left')
#     plt.tight_layout()
#     plt.savefig(savehere, dpi=300)
#     plt.show()
# def OrbitalPeriod_vs_bothMplanet(input_df, savehere, colormap, Rot_Max=50, Num_Segments=3, color_by_star_rot=True, include_msini=False):
#
#     df_notnull = input_df[pd.isnull(input_df['Orbital Period (days)']) == False]
#     df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     if include_msini == True:
#         df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#     if color_by_star_rot == True:
#         df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
#         df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         if include_msini == True:
#             df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
#             df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]
#
#         st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values
#         if include_msini == True:
#             st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values
#
#         cmap = colormap  # cm.rainbow
#         max_rot_lim = Rot_Max # np.nanmax(st_Rot)
#         n_segments = Num_Segments
#         # if max_rot_lim == None:
#         bin_segment = max_rot_lim / n_segments
#         map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#             # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
#         # else:
#         #     bin_segment = n_segments
#         #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
#
#         norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
#
#     pl_a1 = df_notnull1['Orbital Period (days)'].values
#     pl_a1_upper = abs(df_notnull1['Orbital Period Upper Unc. (days)'].values)
#     pl_a1_lower = abs(df_notnull1['Orbital Period Lower Unc. (days)'].values)
#
#     pl_Mjup1 = df_notnull1['Planet Mass (Jupiter Mass)'].values
#     pl_Mjup1_upper = abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values)
#     pl_Mjup1_lower = abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values)
#
#     if include_msini == True:
#         pl_a2 = df_notnull2['Orbital Period (days)'].values
#         pl_a2_upper = abs(df_notnull2['Orbital Period Upper Unc. (days)'].values)
#         pl_a2_lower = abs(df_notnull2['Orbital Period Lower Unc. (days)'].values)
#
#         pl_Mjup2 = df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values
#         pl_Mjup2_upper = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values)
#         pl_Mjup2_lower = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values)
#         # pl_Mjup2 = pl_Mjup2 + 0.15*pl_Mjup2
#
#     # import pdb; pdb.set_trace()
#
#     font_size = 'medium'
#
#     fig = plt.figure(1, figsize=(7.5, 5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#
#     errorbar_alpha_val = 1.0
#
#     if color_by_star_rot == True:
#         ax.scatter(pl_a1, pl_Mjup1, c=st_Rot1, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm, s=np.pi * (3) ** 2)
#         ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower, pl_Mjup1_upper], xerr=[pl_a1_lower, pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_a2, pl_Mjup2, marker='s', c=st_Rot2, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm)
#             ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower, pl_Mjup2_upper], xerr=[pl_a2_lower, pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#         cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
#         cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
#                      rotation=270, labelpad=15)
#     else:
#         ax.scatter(pl_a1, pl_Mjup1, color='#000000', s=np.pi * (2.75) ** 2, label='M')
#         ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower, pl_Mjup1_upper], xerr=[pl_a1_lower, pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_a2, pl_Mjup2, marker='s', color='#000000', label='Msini')
#             ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower, pl_Mjup2_upper], xerr=[pl_a2_lower, pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#
#
#     ax.set_xlabel('Planet Orbital Period (days)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#     ax.set_ylim(np.min([np.min(pl_Mjup1),np.min(pl_Mjup2)]) - 0.002, np.max([np.max(pl_Mjup1),np.max(pl_Mjup2)]) + 20)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     ax.legend(loc='upper left')
#     plt.tight_layout()
#     plt.savefig(savehere, dpi=300)
#     plt.show()


def plot_x_vs_bothMplanet(input_df, x_axis, savehere, colormap, Rot_Max=50, Num_Segments=3, color_by_star_rot=True, include_msini=False):


    min_y_axis_pad = 0.0005
    max_y_axis_pad = 5

    if x_axis == 'Orbit Semi-Major Axis (au))':
        x_axis_upper = 'Orbit Semi-Major Axis Upper Unc. (au)'
        x_axis_lower = 'Orbit Semi-Major Axis Lower Unc. (au)'
        x_axis_label = 'Orbit Semi-Major Axis (au)'
        min_x_axis_pad = 0.0005
        max_x_axis_pad = 2

    if x_axis == 'Ratio of Semi-Major Axis to Stellar Radius':
        x_axis_upper = 'Ratio of Semi-Major Axis to Stellar Radius Upper Unc.'
        x_axis_lower = 'Ratio of Semi-Major Axis to Stellar Radius Lower Unc.'
        x_axis_label = r'a/R$_{\star}$'
        min_x_axis_pad = 0.1
        max_x_axis_pad = 300

    if x_axis == 'Orbital Period (days)':
        x_axis_upper = 'Orbital Period Upper Unc. (days)'
        x_axis_lower = 'Orbital Period Lower Unc. (days)'
        x_axis_label = 'Orbital Period (days)'
        min_x_axis_pad = 0.05
        max_x_axis_pad = 3000




    df_notnull = input_df[pd.isnull(input_df[x_axis]) == False]
    df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]

    if include_msini == True:
        df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
        df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]

    if color_by_star_rot == True:
        df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
        df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]

        if include_msini == True:
            df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
            df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]

        st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values
        if include_msini == True:
            st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values

        cmap = colormap # cm.rainbow
        max_rot_lim = Rot_Max # np.nanmax(st_Rot)
        n_segments = Num_Segments
        # if max_rot_lim == None:
        bin_segment = max_rot_lim / n_segments
        map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
            # map_bounds = np.linspace(np.nanmin(map_values), np.nanmax(map_values) + 1, n_segments+1)
        # else:
        #     bin_segment = n_segments
        #     map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)

        norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)

    pl_a1 = df_notnull1[x_axis].values
    pl_a1_upper = abs(df_notnull1[x_axis_upper].values)
    pl_a1_lower = abs(df_notnull1[x_axis_lower].values)

    pl_Mjup1 = df_notnull1['Planet Mass (Jupiter Mass)'].values
    pl_Mjup1_upper = abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values)
    pl_Mjup1_lower = abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values)

    if include_msini == True:
        pl_a2 = df_notnull2[x_axis].values
        pl_a2_upper = abs(df_notnull2[x_axis_upper].values)
        pl_a2_lower = abs(df_notnull2[x_axis_lower].values)

        pl_Mjup2 = df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values
        pl_Mjup2_upper = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values)
        pl_Mjup2_lower = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values)
        # pl_Mjup2 = pl_Mjup2 + 0.15*pl_Mjup2

    # import pdb; pdb.set_trace()

    font_size = 'large'

    plt.close()

    fig = plt.figure(1, figsize=(7.5, 5), facecolor="#ffffff")
    ax = fig.add_subplot(111)

    errorbar_alpha_val = 1.0

    if color_by_star_rot == True:
        ax.scatter(pl_a1, pl_Mjup1, c=st_Rot1, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm, s=np.pi * (3) ** 2)
        ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower,pl_Mjup1_upper], xerr=[pl_a1_lower,pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1,zorder=0)
        ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
        if include_msini == True:
            ax.scatter(pl_a2, pl_Mjup2, marker='s', c=st_Rot2, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm)
            ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower,pl_Mjup2_upper], xerr=[pl_a2_lower,pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1,zorder=0)
            ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
        cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
                     rotation=270, labelpad=15)
    else:
        ax.scatter(pl_a1, pl_Mjup1, color='#000000', s=np.pi * (2.75) ** 2, label='M')
        ax.errorbar(pl_a1, pl_Mjup1, yerr=[pl_Mjup1_lower, pl_Mjup1_upper], xerr=[pl_a1_lower, pl_a1_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
        ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
        if include_msini == True:
            ax.scatter(pl_a2, pl_Mjup2, marker='s', color='#000000', label='Msini')
            ax.errorbar(pl_a2, pl_Mjup2, yerr=[pl_Mjup2_lower, pl_Mjup2_upper], xerr=[pl_a2_lower, pl_a2_upper], ls='None', ecolor='#000000', alpha=errorbar_alpha_val, elinewidth=1, capsize=2, capthick=1, zorder=0)
            ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')

    ax.set_xlabel(x_axis_label, fontsize=font_size, style='normal', family='sans-serif')
    ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
    ax.set_xscale('log')
    ax.set_yscale('log')
    if include_msini == True:
        ax.set_ylim(np.min([np.min(pl_Mjup1),np.min(pl_Mjup2)]) - min_y_axis_pad, np.max([np.max(pl_Mjup1),np.max(pl_Mjup2)]) + max_y_axis_pad)
        ax.set_xlim(np.min([np.min(pl_a1), np.min(pl_a2)]) - min_x_axis_pad, np.max([np.max(pl_a1), np.max(pl_a2)]) + max_x_axis_pad)
    if include_msini == False:
        ax.set_ylim(min(pl_Mjup1) - min_y_axis_pad, np.max(pl_Mjup1) + max_y_axis_pad)
        ax.set_xlim(min(pl_a1) - min_x_axis_pad, np.max(pl_a1) + max_x_axis_pad)
    ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
    ax.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(savehere, dpi=300)
    plt.show()


# def a_vs_Mplanet_stats(input_df, savehere, colormap, Rot_Max = 50, Num_Segments=3, color_by_star_rot=True, include_msini=False):
#     df_notnull = input_df[pd.isnull(input_df['Orbit Semi-Major Axis (au))']) == False]
#     df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
#     df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]
#
#
#     st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values
#
#     pl_a1 = (df_notnull1['Orbit Semi-Major Axis (au))'].values * u.au).to(u.cm).value
#     pl_a1_upper = (abs(df_notnull1['Orbit Semi-Major Axis Upper Unc. (au)'].values) * u.au).to(u.cm).value
#     pl_a1_lower = (abs(df_notnull1['Orbit Semi-Major Axis Lower Unc. (au)'].values) * u.au).to(u.cm).value
#
#     pl_Mjup1 = (df_notnull1['Planet Mass (Jupiter Mass)'].values * u.Mjup).to(u.g).value
#     pl_Mjup1_upper = (abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values) * u.Mjup).to(u.g).value
#     pl_Mjup1_lower = (abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values) * u.Mjup).to(u.g).value
#
#     pl_M_over_a1 = pl_Mjup1 / (pl_a1)
#     pl_M_over_a1_upper = np.sqrt((1. / pl_a1) ** 2 * pl_Mjup1_upper ** 2 + (-pl_Mjup1 / (pl_a1 ** 2)) ** 2 * pl_a1_upper)
#     pl_M_over_a1_lower = np.sqrt((1. / pl_a1) ** 2 * pl_Mjup1_lower ** 2 + (-pl_Mjup1 / (pl_a1 ** 2)) ** 2 * pl_a1_lower)
#
#     pl_M_over_a1 = pl_Mjup1 / (pl_a1**2)
#     pl_M_over_a1_upper = np.sqrt((1. / (pl_a1**2)) ** 2 * pl_Mjup1_upper ** 2 + (-2*pl_Mjup1 / (pl_a1 ** 3)) ** 2 * pl_a1_upper)
#     pl_M_over_a1_lower = np.sqrt((1. / (pl_a1**2)) ** 2 * pl_Mjup1_lower ** 2 + (-2*pl_Mjup1 / (pl_a1 ** 3)) ** 2 * pl_a1_lower)
#
#     tempM_over_a1 = []
#     tempM_over_a1_upper = []
#     tempM_over_a1_lower = []
#     tempRot1 = []
#     # tempRot1_upper = []
#     # tempRot1_lower = []
#     for planet_i in range(len(pl_M_over_a1)):
#         percent_uncertainty_upper = pl_M_over_a1_upper[planet_i] / pl_M_over_a1[planet_i]
#         percent_uncertainty_lower = pl_M_over_a1_lower[planet_i] / pl_M_over_a1[planet_i]
#         percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper,percent_uncertainty_lower])
#         # print(percent_uncertainty_mean)
#         if (percent_uncertainty_mean <= 0.15*pl_M_over_a1[planet_i]) and (np.isnan(percent_uncertainty_mean) == False):
#             tempM_over_a1.append(pl_M_over_a1[planet_i])
#             tempM_over_a1_upper.append(pl_M_over_a1_upper[planet_i])
#             tempM_over_a1_lower.append(pl_M_over_a1_lower[planet_i])
#             tempRot1.append(st_Rot1[planet_i])
#
#     pl_M_over_a1 = np.array(tempM_over_a1)
#     pl_M_over_a1_upper = np.array(tempM_over_a1_upper)
#     pl_M_over_a1_lower = np.array(tempM_over_a1_lower)
#     st_Rot1 = np.array(tempRot1)
#
#
#     # tempM1 = []
#     # tempM1_upper = []
#     # tempM1_lower = []
#     # tempa1 = []
#     # tempa1_upper = []
#     # tempa1_lower = []
#     # tempRot1 = []
#     # tempRot1_upper = []
#     # tempRot1_lower = []
#     # for planet_i in range(len(pl_Mjup1)):
#     #     percent_uncertainty_upper = pl_Mjup1_upper[planet_i] / pl_Mjup1[planet_i]
#     #     percent_uncertainty_lower = pl_Mjup1_lower[planet_i] / pl_Mjup1[planet_i]
#     #     percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper,percent_uncertainty_lower])
#     #     # print(percent_uncertainty_mean)
#     #     if (percent_uncertainty_mean <= 0.50*pl_Mjup1[planet_i]) and (np.isnan(percent_uncertainty_mean) == False):
#     #         tempM1.append(pl_Mjup1[planet_i])
#     #         tempM1_upper.append(pl_Mjup1_upper[planet_i])
#     #         tempM1_lower.append(pl_Mjup1_lower[planet_i])
#     #         tempa1.append(pl_a1[planet_i])
#     #         tempa1_upper.append(pl_a1_upper[planet_i])
#     #         tempa1_lower.append(pl_a1_lower[planet_i])
#     #         tempRot1.append(st_Rot1[planet_i])
#     #
#     # pl_Mjup1 = np.array(tempM1)
#     # pl_Mjup1_upper = np.array(tempM1_upper)
#     # pl_Mjup1_lower = np.array(tempM1_lower)
#     # pl_a1 = np.array(tempa1)
#     # pl_a1_upper = np.array(tempa1_upper)
#     # pl_a1_lower = np.array(tempa1_lower)
#     # st_Rot1 = np.array(tempRot1)
#
#
#
#     # import pdb; pdb.set_trace()
#
#
#
#
#     if include_msini == True:
#         df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
#         df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]
#
#
#         st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values
#
#         pl_a2 = (df_notnull2['Orbit Semi-Major Axis (au))'].values * u.au).to(u.cm).value
#         pl_a2_upper = (abs(df_notnull2['Orbit Semi-Major Axis Upper Unc. (au)'].values) * u.au).to(u.cm).value
#         pl_a2_lower = (abs(df_notnull2['Orbit Semi-Major Axis Lower Unc. (au)'].values) * u.au).to(u.cm).value
#
#         pl_Mjup2 = (df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values * u.Mjup).to(u.g).value
#         pl_Mjup2_upper = (abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values) * u.Mjup).to(u.g).value
#         pl_Mjup2_lower = (abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values) * u.Mjup).to(u.g).value
#
#
#         pl_M_over_a2 = pl_Mjup2 / (pl_a2)
#         pl_M_over_a2_upper = np.sqrt( (1. / pl_a2) ** 2 * pl_Mjup2_upper ** 2 + (-pl_Mjup2 / (pl_a2 ** 2)) ** 2 * pl_a2_upper)
#         pl_M_over_a2_lower = np.sqrt( (1. / pl_a2) ** 2 * pl_Mjup2_lower ** 2 + (-pl_Mjup2 / (pl_a2 ** 2)) ** 2 * pl_a2_lower)
#
#         pl_M_over_a2 = pl_Mjup2 / (pl_a2**2)
#         pl_M_over_a2_upper = np.sqrt((1. / (pl_a2**2)) ** 2 * pl_Mjup2_upper ** 2 + (-2*pl_Mjup2 / (pl_a2 ** 3)) ** 2 * pl_a2_upper)
#         pl_M_over_a2_lower = np.sqrt((1. / (pl_a2**2)) ** 2 * pl_Mjup2_lower ** 2 + (-2*pl_Mjup2 / (pl_a2 ** 3)) ** 2 * pl_a2_lower)
#
#         tempM_over_a2 = []
#         tempM_over_a2_upper = []
#         tempM_over_a2_lower = []
#         tempRot2 = []
#         # tempRot1_upper = []
#         # tempRot1_lower = []
#         for planet_i in range(len(pl_M_over_a2)):
#             percent_uncertainty_upper = pl_M_over_a2_upper[planet_i] / pl_M_over_a2[planet_i]
#             percent_uncertainty_lower = pl_M_over_a2_lower[planet_i] / pl_M_over_a2[planet_i]
#             percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper, percent_uncertainty_lower])
#             # print(percent_uncertainty_mean)
#             if (percent_uncertainty_mean <= 0.15 * pl_M_over_a2[planet_i]) and (
#                     np.isnan(percent_uncertainty_mean) == False):
#                 tempM_over_a2.append(pl_M_over_a2[planet_i])
#                 tempM_over_a2_upper.append(pl_M_over_a2_upper[planet_i])
#                 tempM_over_a2_lower.append(pl_M_over_a2_lower[planet_i])
#                 tempRot2.append(st_Rot2[planet_i])
#
#         pl_M_over_a2 = np.array(tempM_over_a2)
#         pl_M_over_a2_upper = np.array(tempM_over_a2_upper)
#         pl_M_over_a2_lower = np.array(tempM_over_a2_lower)
#         st_Rot2 = np.array(tempRot2)
#
#     font_size = 'medium'
#     plt.close()
#     fig = plt.figure(1, figsize=(5, 7.5), facecolor="#ffffff")
#     ax = fig.add_subplot(111)
#     if color_by_star_rot == True:
#         ax.scatter(pl_M_over_a1, st_Rot1, c='#000000', edgecolor='#000000', linewidth=0.5, s=np.pi * (3) ** 2)
#         ax.errorbar(pl_M_over_a1, st_Rot1, xerr=[pl_M_over_a1_lower, pl_M_over_a1_upper], ls='None', ecolor='#000000', elinewidth=1, capsize=2, capthick=1, zorder=0)
#         ax.scatter([], [], color='#ffffff', edgecolor='#000000', linewidth=1, s=np.pi * (3) ** 2, label='M')
#         if include_msini == True:
#             ax.scatter(pl_M_over_a2, st_Rot2, marker='s', c='#000000', edgecolor='#000000', linewidth=0.5)
#             ax.errorbar(pl_M_over_a2, st_Rot2, xerr=[pl_M_over_a2_lower, pl_M_over_a2_upper], ls='None', ecolor='#000000', elinewidth=1, capsize=2, capthick=1, zorder=0)
#             ax.scatter([], [], marker='s', color='#ffffff', edgecolor='#000000', linewidth=1, label='Msini')
#     # ax.set_xlabel('Planet Mass / Orbit Semi-Major Axis  (g/cm)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xlabel('Planet Mass / Orbit Semi-Major Axis^2  (g/cm^2)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_ylabel('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif')
#     ax.set_xscale('log')
#     # ax.set_yscale('log')
#     if include_msini == True:
#         ax.set_ylim(np.min([np.min(st_Rot1), np.min(st_Rot2)]) - 5, np.max([np.max(st_Rot1), np.max(st_Rot2)]) + 5)
#     else:
#         ax.set_ylim(np.min(st_Rot1) - 5, np.max(st_Rot1) + 5)
#     ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
#     ax.legend(loc='upper left')
#     plt.tight_layout()
#     plt.savefig(savehere, dpi=300)
#     plt.show()

# def isolate_relevant_data_cgs(input_df, x_axis, Rot_Max = 50, include_msini=True):
#     df_notnull = input_df[pd.isnull(input_df[x_axis]) == False]
#     df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]
#
#     df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
#     df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]
#
#
#     st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values
#
#     if x_axis == 'Orbit Semi-Major Axis (au))':
#         x_axis_upper = 'Orbit Semi-Major Axis Upper Unc. (au)'
#         x_axis_lower = 'Orbit Semi-Major Axis Lower Unc. (au)'
#
#     pl_a1 = (df_notnull1[x_axis].values * u.au).to(u.cm).value
#     pl_a1_upper = (abs(df_notnull1[x_axis_upper].values) * u.au).to(u.cm).value
#     pl_a1_lower = (abs(df_notnull1[x_axis_lower].values) * u.au).to(u.cm).value
#
#     pl_Mjup1 = (df_notnull1['Planet Mass (Jupiter Mass)'].values * u.Mjup).to(u.g).value
#     pl_Mjup1_upper = (abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values) * u.Mjup).to(u.g).value
#     pl_Mjup1_lower = (abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values) * u.Mjup).to(u.g).value
#
#     pl_M_over_a1 = pl_Mjup1 / (pl_a1)
#     pl_M_over_a1_upper = np.sqrt((1. / pl_a1) ** 2 * pl_Mjup1_upper ** 2 + (-pl_Mjup1 / (pl_a1 ** 2)) ** 2 * pl_a1_upper)
#     pl_M_over_a1_lower = np.sqrt((1. / pl_a1) ** 2 * pl_Mjup1_lower ** 2 + (-pl_Mjup1 / (pl_a1 ** 2)) ** 2 * pl_a1_lower)
#
#     pl_M_over_a1 = pl_Mjup1 / (pl_a1**2)
#     pl_M_over_a1_upper = np.sqrt((1. / (pl_a1**2)) ** 2 * pl_Mjup1_upper ** 2 + (-2*pl_Mjup1 / (pl_a1 ** 3)) ** 2 * pl_a1_upper)
#     pl_M_over_a1_lower = np.sqrt((1. / (pl_a1**2)) ** 2 * pl_Mjup1_lower ** 2 + (-2*pl_Mjup1 / (pl_a1 ** 3)) ** 2 * pl_a1_lower)
#
#     tempM_over_a1 = []
#     tempM_over_a1_upper = []
#     tempM_over_a1_lower = []
#     tempRot1 = []
#     # tempRot1_upper = []
#     # tempRot1_lower = []
#     for planet_i in range(len(pl_M_over_a1)):
#         percent_uncertainty_upper = pl_M_over_a1_upper[planet_i] / pl_M_over_a1[planet_i]
#         percent_uncertainty_lower = pl_M_over_a1_lower[planet_i] / pl_M_over_a1[planet_i]
#         percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper,percent_uncertainty_lower])
#         # print(percent_uncertainty_mean)
#         if (percent_uncertainty_mean <= 0.15*pl_M_over_a1[planet_i]) and (np.isnan(percent_uncertainty_mean) == False):
#             tempM_over_a1.append(pl_M_over_a1[planet_i])
#             tempM_over_a1_upper.append(pl_M_over_a1_upper[planet_i])
#             tempM_over_a1_lower.append(pl_M_over_a1_lower[planet_i])
#             tempRot1.append(st_Rot1[planet_i])
#
#     pl_M_over_a1 = np.array(tempM_over_a1)
#     pl_M_over_a1_upper = np.array(tempM_over_a1_upper)
#     pl_M_over_a1_lower = np.array(tempM_over_a1_lower)
#     # st_Rot1 = np.array(tempRot1)
#
#
#     tempM1 = []
#     tempM1_upper = []
#     tempM1_lower = []
#     tempa1 = []
#     tempa1_upper = []
#     tempa1_lower = []
#     tempRot1 = []
#     tempRot1_upper = []
#     tempRot1_lower = []
#     for planet_i in range(len(pl_Mjup1)):
#         percent_uncertainty_upper = pl_Mjup1_upper[planet_i] / pl_Mjup1[planet_i]
#         percent_uncertainty_lower = pl_Mjup1_lower[planet_i] / pl_Mjup1[planet_i]
#         percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper,percent_uncertainty_lower])
#         # print(percent_uncertainty_mean)
#         if (percent_uncertainty_mean <= 0.50*pl_Mjup1[planet_i]) and (np.isnan(percent_uncertainty_mean) == False):
#             tempM1.append(pl_Mjup1[planet_i])
#             tempM1_upper.append(pl_Mjup1_upper[planet_i])
#             tempM1_lower.append(pl_Mjup1_lower[planet_i])
#             tempa1.append(pl_a1[planet_i])
#             tempa1_upper.append(pl_a1_upper[planet_i])
#             tempa1_lower.append(pl_a1_lower[planet_i])
#             tempRot1.append(st_Rot1[planet_i])
#
#     pl_Mjup1 = np.array(tempM1)
#     pl_Mjup1_upper = np.array(tempM1_upper)
#     pl_Mjup1_lower = np.array(tempM1_lower)
#     pl_a1 = np.array(tempa1)
#     pl_a1_upper = np.array(tempa1_upper)
#     pl_a1_lower = np.array(tempa1_lower)
#     st_Rot1 = np.array(tempRot1)
#
#
#
#     # import pdb; pdb.set_trace()
#
#
#
#
#     if include_msini == True:
#         df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]
#
#         df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
#         df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]
#
#
#         st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values
#
#         pl_a2 = (df_notnull2[x_axis].values * u.au).to(u.cm).value
#         pl_a2_upper = (abs(df_notnull2[x_axis_upper].values) * u.au).to(u.cm).value
#         pl_a2_lower = (abs(df_notnull2[x_axis_lower].values) * u.au).to(u.cm).value
#
#         pl_Mjup2 = (df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values * u.Mjup).to(u.g).value
#         pl_Mjup2_upper = (abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values) * u.Mjup).to(u.g).value
#         pl_Mjup2_lower = (abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values) * u.Mjup).to(u.g).value
#
#
#         pl_M_over_a2 = pl_Mjup2 / (pl_a2)
#         pl_M_over_a2_upper = np.sqrt( (1. / pl_a2) ** 2 * pl_Mjup2_upper ** 2 + (-pl_Mjup2 / (pl_a2 ** 2)) ** 2 * pl_a2_upper)
#         pl_M_over_a2_lower = np.sqrt( (1. / pl_a2) ** 2 * pl_Mjup2_lower ** 2 + (-pl_Mjup2 / (pl_a2 ** 2)) ** 2 * pl_a2_lower)
#
#         pl_M_over_a2 = pl_Mjup2 / (pl_a2**2)
#         pl_M_over_a2_upper = np.sqrt((1. / (pl_a2**2)) ** 2 * pl_Mjup2_upper ** 2 + (-2*pl_Mjup2 / (pl_a2 ** 3)) ** 2 * pl_a2_upper)
#         pl_M_over_a2_lower = np.sqrt((1. / (pl_a2**2)) ** 2 * pl_Mjup2_lower ** 2 + (-2*pl_Mjup2 / (pl_a2 ** 3)) ** 2 * pl_a2_lower)
#
#         tempM_over_a2 = []
#         tempM_over_a2_upper = []
#         tempM_over_a2_lower = []
#         tempRot2 = []
#         # tempRot1_upper = []
#         # tempRot1_lower = []
#         for planet_i in range(len(pl_M_over_a2)):
#             percent_uncertainty_upper = pl_M_over_a2_upper[planet_i] / pl_M_over_a2[planet_i]
#             percent_uncertainty_lower = pl_M_over_a2_lower[planet_i] / pl_M_over_a2[planet_i]
#             percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper, percent_uncertainty_lower])
#             # print(percent_uncertainty_mean)
#             if (percent_uncertainty_mean <= 0.15 * pl_M_over_a2[planet_i]) and (
#                     np.isnan(percent_uncertainty_mean) == False):
#                 tempM_over_a2.append(pl_M_over_a2[planet_i])
#                 tempM_over_a2_upper.append(pl_M_over_a2_upper[planet_i])
#                 tempM_over_a2_lower.append(pl_M_over_a2_lower[planet_i])
#                 tempRot2.append(st_Rot2[planet_i])
#
#         pl_M_over_a2 = np.array(tempM_over_a2)
#         pl_M_over_a2_upper = np.array(tempM_over_a2_upper)
#         pl_M_over_a2_lower = np.array(tempM_over_a2_lower)
#         # st_Rot2 = np.array(tempRot2)
#
#         tempM2 = []
#         tempM2_upper = []
#         tempM2_lower = []
#         tempa2 = []
#         tempa2_upper = []
#         tempa2_lower = []
#         tempRot2 = []
#         # tempRot2_upper = []
#         # tempRot2_lower = []
#         for planet_i in range(len(pl_Mjup2)):
#             percent_uncertainty_upper = pl_Mjup2_upper[planet_i] / pl_Mjup2[planet_i]
#             percent_uncertainty_lower = pl_Mjup2_lower[planet_i] / pl_Mjup2[planet_i]
#             percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper, percent_uncertainty_lower])
#             # print(percent_uncertainty_mean)
#             if (percent_uncertainty_mean <= 0.15 * pl_Mjup2[planet_i]) and (
#                     np.isnan(percent_uncertainty_mean) == False):
#                 tempM2.append(pl_Mjup2[planet_i])
#                 tempM2_upper.append(pl_Mjup2_upper[planet_i])
#                 tempM2_lower.append(pl_Mjup2_lower[planet_i])
#                 tempa2.append(pl_a2[planet_i])
#                 tempa2_upper.append(pl_a2_upper[planet_i])
#                 tempa2_lower.append(pl_a2_lower[planet_i])
#                 tempRot2.append(st_Rot2[planet_i])
#
#         pl_Mjup2 = np.array(tempM2)
#         pl_Mjup2_upper = np.array(tempM2_upper)
#         pl_Mjup2_lower = np.array(tempM2_lower)
#         pl_a2 = np.array(tempa2)
#         pl_a2_upper = np.array(tempa2_upper)
#         pl_a2_lower = np.array(tempa2_lower)
#         st_Rot2 = np.array(tempRot2)
#
#
#
#
#     combined_separations = {'values': np.concatenate((pl_a1, pl_a2)),
#                             'upper': np.concatenate((pl_a1_upper, pl_a2_upper)),
#                             'lower': np.concatenate((pl_a1_lower, pl_a2_lower)),
#                             }
#
#     combined_masses = {'values': np.concatenate((pl_Mjup1,pl_Mjup2)),
#                        'upper': np.concatenate((pl_Mjup1_upper,pl_Mjup2_upper)),
#                        'lower': np.concatenate((pl_Mjup1_lower,pl_Mjup2_lower)),
#                        }
#
#     combined_rotations = {'values': np.concatenate((st_Rot1, st_Rot2))}
#
#                           # 'upper': np.concatenate((st_Rot1_upper, st_Rot2_upper)),
#                           # 'lower': np.concatenate((st_Rot1_lower, st_Rot2_lower)),
#                           # }
#
#
#     return combined_separations, combined_masses, combined_rotations

def isolate_relevant_data(input_df, x_axis, Rot_Max = 50, include_msini=True):

    if x_axis == 'Orbit Semi-Major Axis (au))':
        x_axis_upper = 'Orbit Semi-Major Axis Upper Unc. (au)'
        x_axis_lower = 'Orbit Semi-Major Axis Lower Unc. (au)'
        dict_header = 'Orbit Semi-Major Axis (au)'
        dict_header_upper = 'Orbit Semi-Major Axis (au) Upper'
        dict_header_lower = 'Orbit Semi-Major Axis (au) Lower'

    if x_axis == 'Ratio of Semi-Major Axis to Stellar Radius':
        x_axis_upper = 'Ratio of Semi-Major Axis to Stellar Radius Upper Unc.'
        x_axis_lower = 'Ratio of Semi-Major Axis to Stellar Radius Lower Unc.'
        dict_header = 'Ratio of Semi-Major Axis to Stellar Radius'
        dict_header_upper = 'Ratio of Semi-Major Axis to Stellar Radius Upper Unc.'
        dict_header_lower = 'Ratio of Semi-Major Axis to Stellar Radius Lower Unc.'

    if x_axis == 'Orbital Period (days)':
        x_axis_upper = 'Orbital Period Upper Unc. (days)'
        x_axis_lower = 'Orbital Period Lower Unc. (days)'
        dict_header = 'Orbital Period (days)'
        dict_header_upper = 'Orbital Period Upper Unc. (days)'
        dict_header_lower = 'Orbital Period Lower Unc. (days)'




    df_notnull = input_df[pd.isnull(input_df['Orbit Semi-Major Axis (au))']) == False]
    df_notnull1 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == False]

    df_notnull1 = df_notnull1[pd.isnull(df_notnull1['Stellar Rotational Period (days)']) == False]
    df_notnull1 = df_notnull1[df_notnull1['Stellar Rotational Period (days)'] <= Rot_Max]


    st_Rot1 = df_notnull1['Stellar Rotational Period (days)'].values

    pl_a1 = df_notnull1[x_axis].values
    pl_a1_upper = abs(df_notnull1[x_axis_upper].values)
    pl_a1_lower = abs(df_notnull1[x_axis_lower].values)

    pl_Mjup1 = df_notnull1['Planet Mass (Jupiter Mass)'].values
    pl_Mjup1_upper = abs(df_notnull1['Planet Mass (Jupiter Mass) Upper Unc.'].values)
    pl_Mjup1_lower = abs(df_notnull1['Planet Mass (Jupiter Mass) Lower Unc.'].values)


    # tempM1 = []
    # tempM1_upper = []
    # tempM1_lower = []
    # tempa1 = []
    # tempa1_upper = []
    # tempa1_lower = []
    # tempRot1 = []
    # tempRot1_upper = []
    # tempRot1_lower = []
    # for planet_i in range(len(pl_Mjup1)):
    #     percent_uncertainty_upper = pl_Mjup1_upper[planet_i] / pl_Mjup1[planet_i]
    #     percent_uncertainty_lower = pl_Mjup1_lower[planet_i] / pl_Mjup1[planet_i]
    #     percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper,percent_uncertainty_lower])
    #     # print(percent_uncertainty_mean)
    #     if (percent_uncertainty_mean <= 0.50*pl_Mjup1[planet_i]) and (np.isnan(percent_uncertainty_mean) == False):
    #         tempM1.append(pl_Mjup1[planet_i])
    #         tempM1_upper.append(pl_Mjup1_upper[planet_i])
    #         tempM1_lower.append(pl_Mjup1_lower[planet_i])
    #         tempa1.append(pl_a1[planet_i])
    #         tempa1_upper.append(pl_a1_upper[planet_i])
    #         tempa1_lower.append(pl_a1_lower[planet_i])
    #         tempRot1.append(st_Rot1[planet_i])
    #
    # pl_Mjup1 = np.array(tempM1)
    # pl_Mjup1_upper = np.array(tempM1_upper)
    # pl_Mjup1_lower = np.array(tempM1_lower)
    # pl_a1 = np.array(tempa1)
    # pl_a1_upper = np.array(tempa1_upper)
    # pl_a1_lower = np.array(tempa1_lower)
    # st_Rot1 = np.array(tempRot1)


    # import pdb; pdb.set_trace()


    if include_msini == True:
        df_notnull2 = df_notnull[pd.isnull(df_notnull['Planet Mass (Jupiter Mass)']) == True]
        df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Planet Mass*sin(i) (Jupiter Mass)']) == False]

        df_notnull2 = df_notnull2[pd.isnull(df_notnull2['Stellar Rotational Period (days)']) == False]
        df_notnull2 = df_notnull2[df_notnull2['Stellar Rotational Period (days)'] <= Rot_Max]


        st_Rot2 = df_notnull2['Stellar Rotational Period (days)'].values

        pl_a2 = df_notnull2[x_axis].values
        pl_a2_upper = abs(df_notnull2[x_axis_upper].values)
        pl_a2_lower = abs(df_notnull2[x_axis_lower].values)

        pl_Mjup2 = df_notnull2['Planet Mass*sin(i) (Jupiter Mass)'].values
        pl_Mjup2_upper = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Upper Unc.'].values)
        pl_Mjup2_lower = abs(df_notnull2['Planet Mass*sin(i) (Jupiter Mass) Lower Unc.'].values)


        # tempM2 = []
        # tempM2_upper = []
        # tempM2_lower = []
        # tempa2 = []
        # tempa2_upper = []
        # tempa2_lower = []
        # tempRot2 = []
        # # tempRot2_upper = []
        # # tempRot2_lower = []
        # for planet_i in range(len(pl_Mjup2)):
        #     percent_uncertainty_upper = pl_Mjup2_upper[planet_i] / pl_Mjup2[planet_i]
        #     percent_uncertainty_lower = pl_Mjup2_lower[planet_i] / pl_Mjup2[planet_i]
        #     percent_uncertainty_mean = np.nanmean([percent_uncertainty_upper, percent_uncertainty_lower])
        #     # print(percent_uncertainty_mean)
        #     if (percent_uncertainty_mean <= 0.50 * pl_Mjup2[planet_i]) and (np.isnan(percent_uncertainty_mean) == False):
        #         tempM2.append(pl_Mjup2[planet_i])
        #         tempM2_upper.append(pl_Mjup2_upper[planet_i])
        #         tempM2_lower.append(pl_Mjup2_lower[planet_i])
        #         tempa2.append(pl_a2[planet_i])
        #         tempa2_upper.append(pl_a2_upper[planet_i])
        #         tempa2_lower.append(pl_a2_lower[planet_i])
        #         tempRot2.append(st_Rot2[planet_i])
        #
        # pl_Mjup2 = np.array(tempM2)
        # pl_Mjup2_upper = np.array(tempM2_upper)
        # pl_Mjup2_lower = np.array(tempM2_lower)
        # pl_a2 = np.array(tempa2)
        # pl_a2_upper = np.array(tempa2_upper)
        # pl_a2_lower = np.array(tempa2_lower)
        # st_Rot2 = np.array(tempRot2)




        combined_separations = {'values': np.concatenate((pl_a1, pl_a2)),
                                'upper': np.concatenate((pl_a1_upper, pl_a2_upper)),
                                'lower': np.concatenate((pl_a1_lower, pl_a2_lower)),
                                }

        combined_masses = {'values': np.concatenate((pl_Mjup1,pl_Mjup2)),
                           'upper': np.concatenate((pl_Mjup1_upper,pl_Mjup2_upper)),
                           'lower': np.concatenate((pl_Mjup1_lower,pl_Mjup2_lower)),
                           }

        combined_rotations = {'values': np.concatenate((st_Rot1, st_Rot2)),
                              }
                              # 'upper': np.concatenate((st_Rot1_upper, st_Rot2_upper)),
                              # 'lower': np.concatenate((st_Rot1_lower, st_Rot2_lower)),
                              # }

        combined_all = {dict_header: np.concatenate((pl_a1, pl_a2)),
                        dict_header_upper: np.concatenate((pl_a1_upper, pl_a2_upper)),
                        dict_header_lower: np.concatenate((pl_a1_lower, pl_a2_lower)),
                        'Planet Mass (Jupiter Mass)': np.concatenate((pl_Mjup1,pl_Mjup2)),
                        'Planet Mass (Jupiter Mass) Upper': np.concatenate((pl_Mjup1_upper,pl_Mjup2_upper)),
                        'Planet Mass (Jupiter Mass) Lower': np.concatenate((pl_Mjup1_lower,pl_Mjup2_lower)),
                        'Stellar Rotation Period (d)': np.concatenate((st_Rot1, st_Rot2)),
                        }
        combined_all = pd.DataFrame.from_dict(combined_all)

    else:
        combined_separations = {'values': pl_a1,
                                'upper': pl_a1_upper,
                                'lower': pl_a1_lower,
                                }

        combined_masses = {'values': pl_Mjup1,
                           'upper': pl_Mjup1_upper,
                           'lower': pl_Mjup1_lower,
                           }

        combined_rotations = {'values': st_Rot1}
        # 'upper': np.concatenate((st_Rot1_upper, st_Rot2_upper)),
        # 'lower': np.concatenate((st_Rot1_lower, st_Rot2_lower)),
        # }

        combined_all = {dict_header: pl_a1,
                        dict_header_upper: pl_a1_upper,
                        dict_header_lower: pl_a1_lower,
                        'Planet Mass (Jupiter Mass)': pl_Mjup1,
                        'Planet Mass (Jupiter Mass) Upper': pl_Mjup1_upper,
                        'Planet Mass (Jupiter Mass) Lower': pl_Mjup1_lower,
                        'Stellar Rotation Period (d)': st_Rot1,
                        }
        combined_all = pd.DataFrame.from_dict(combined_all)


    return combined_separations, combined_masses, combined_rotations, combined_all

def generate_subset_domains(input_x, input_y, input_z, x_axis, savehere, colormap, num_cols = 5, num_rows = 5, Rot_Max=50, Num_Segments=3, color_by_star_rot=True):

    x_values = input_x['values']
    x_upper = input_x['upper']
    x_lower = input_x['lower']
    y_values = input_y['values']
    y_upper = input_y['upper']
    y_lower = input_y['lower']
    z_values = input_z['values']

    min_y_axis_pad = 0.0005
    max_y_axis_pad = 5

    if x_axis == 'Orbit Semi-Major Axis (au))':
        x_axis = 'Orbit Semi-Major Axis (au)'
        min_x_axis_pad = 0.0005
        max_x_axis_pad = 2

    if x_axis == 'Ratio of Semi-Major Axis to Stellar Radius':
        min_x_axis_pad = 0.1
        max_x_axis_pad = 300

    if x_axis == 'Orbital Period (days)':
        min_x_axis_pad = 0.05
        max_x_axis_pad = 3000

    x_values_for_grid = np.concatenate(([min(x_values) - min_x_axis_pad], x_values, [max(x_values) + max_x_axis_pad]))
    y_values_for_grid = np.concatenate(([min(y_values) - min_y_axis_pad], y_values, [max(y_values) + max_y_axis_pad]))

    log_x = np.log(x_values_for_grid)
    max_log_x = np.nanmax(log_x) # + np.log(20)
    min_log_x = np.nanmin(log_x) # - np.log(0.002)
    log_x_diff = (max_log_x - min_log_x) / num_cols
    x_grid = np.exp(np.linspace(min_log_x, max_log_x + log_x_diff, num_cols))
    x_grid = np.exp(np.arange(min_log_x, max_log_x + log_x_diff, log_x_diff))

    if x_axis == 'Orbit Semi-Major Axis (au))':
        x_axis = 'Orbit Semi-Major Axis (au)'
        x_grid = [10e-4, 10e-3, 10e-2, 10e-1, 10e0, 10e1, 10e2, 10e3]

    if x_axis == 'Ratio of Semi-Major Axis to Stellar Radius':
        x_grid = [10e-1, 10e0, 10e1, 10e2, 10e3]

    if x_axis == 'Orbital Period (days)':
        x_grid = [10e-2, 10e-1, 10e-0, 10e1, 10e2, 10e3, 10e4]

    log_y = np.log(y_values_for_grid)
    max_log_y = np.nanmax(log_y) # + np.log(20)
    min_log_y = np.nanmin(log_y) # - np.log(0.002)
    log_y_diff = (max_log_y - min_log_y) / num_rows
    y_grid = np.exp(np.linspace(min_log_y,max_log_y+log_y_diff, num_rows))
    y_grid = np.exp(np.arange(min_log_y, max_log_y + log_y_diff, log_y_diff))

    y_grid = [10e-4, 10e-3, 10e-2, 10e-1, 10e0, 10e1]

    z_diff = Rot_Max / Num_Segments
    z_grid = np.linspace(0, Rot_Max, Num_Segments+1)


    plt.close()

    cmap = colormap
    max_rot_lim = Rot_Max
    bin_segment = max_rot_lim / Num_Segments
    map_bounds = np.arange(0, max_rot_lim + bin_segment, bin_segment)
    norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)

    font_size = 'large'

    fig = plt.figure(1, figsize=(7.5, 5), facecolor="#ffffff")
    ax = fig.add_subplot(111)

    if color_by_star_rot == True:
        ax.scatter(x_values, y_values, c=z_values, edgecolor='#000000', linewidth=0.5, cmap=cmap, norm=norm, s=np.pi * (3) ** 2)
        ax.errorbar(x_values, y_values, yerr=[y_lower,y_upper], xerr=[x_lower,x_upper], ls='None', ecolor='#000000', elinewidth=1, capsize=2, capthick=1,zorder=0)
        cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        cb.set_label('Stellar Rotation Period (d)', fontsize=font_size, style='normal', family='sans-serif',
                     rotation=270, labelpad=15)
    else:
        ax.scatter(x_values, y_values, color='#000000', s=np.pi * (2.75) ** 2, label='M')
        ax.errorbar(x_values, y_values, yerr=[y_lower, y_upper], xerr=[x_lower, x_upper], ls='None', ecolor='#000000', elinewidth=1, capsize=2, capthick=1, zorder=0)

    # ax.vlines(x=x_grid, ymin=min(y_values) - min_y_axis_pad, ymax=max(y_values) + max_y_axis_pad, color='#000000')
    # ax.hlines(y=y_grid, xmin=min(x_values) - min_x_axis_pad, xmax=max(x_values) + max_x_axis_pad, color='#000000')

    ax.vlines(x=x_grid, ymin=min(y_grid), ymax=max(y_grid), color='#000000')
    ax.hlines(y=y_grid, xmin=min(x_grid), xmax=max(x_grid), color='#000000')

    i = 0
    ax.fill_between([x_grid[i],x_grid[i+1]], y_grid[i], y_grid[i+1], color='green', alpha=0.2, zorder=0) # , where=(y1 > y2))

    ax.set_xlabel(x_axis, fontsize=font_size, style='normal', family='sans-serif')
    ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
    ax.set_xscale('log')
    ax.set_yscale('log')
    # ax.set_ylim(min(y_values) - min_y_axis_pad, max(y_values) + min_y_axis_pad)
    # ax.set_xlim(min(x_values) - min_x_axis_pad, max(x_values) + max_x_axis_pad)
    ax.set_ylim(min(y_grid), max(y_grid))
    ax.set_xlim(min(x_grid), max(x_grid))
    ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True)
    plt.tight_layout()
    plt.savefig(savehere, dpi=300)
    plt.show()

    return x_grid, y_grid, z_grid


    # import pdb; pdb.set_trace()

    # full_grid = np.empty((num_separation_cells, num_mass_cells, len(df1))) # num_separation_cells*num_mass_cells))
    # full_grid = full_grid*0
    #
    # for cell_i in range(num_separation_cells):
    #     for cell_j in range(num_mass_cells):
    #
    #         for planet in range(len(df1)):
    #
    #             if cell_i == len(x_grid)-1:
    #                 where_in_x_cell = np.where(x_values >= x_grid[cell_i])[0]
    #             else:
    #                 where_in_x_cell = np.where((x_values >= x_grid[cell_i]) & (x_values < x_grid[cell_i + 1]))[0]
    #
    #             if len(where_in_x_cell) > 0:
    #                 x_values_in_cell_i = x_values[where_in_x_cell]
    #                 y_values_in_cell_i = y_values[where_in_x_cell]
    #                 z_values_in_cell_i = z_values[where_in_x_cell]
    #
    #                 if cell_j == len(y_grid) - 1:
    #                     where_in_y_cell = np.where(y_values_in_cell_i >= y_grid[cell_j])[0]
    #                 else:
    #                     where_in_y_cell = np.where((y_values_in_cell_i >= y_grid[cell_j]) & (y_values_in_cell_i < y_grid[cell_j + 1]))[0]
    #
    #                 if len(where_in_y_cell) > 0:
    #                     x_values_in_cell_ij = x_values_in_cell_i[where_in_y_cell]
    #                     y_values_in_cell_ij = y_values_in_cell_i[where_in_y_cell]
    #                     z_values_in_cell_ij = z_values_in_cell_i[where_in_y_cell]
    #
    #                     z_values_in_cell_ij = z_values_in_cell_ij[z_values_in_cell_ij>0]
    #
    #                     # print(z_values_in_cell_ij)
    #
    #                     full_grid[cell_i, cell_j, 0:len(z_values_in_cell_ij)] = z_values_in_cell_ij
    #
    #                 else:
    #                     full_grid[cell_i,cell_j,:] = 0.0
    #
    #             else:
    #                 full_grid[cell_i, cell_j, :] = 0.0
    #
    # plt.close()
    # # fig = plt.figure(1, figsize=(11, 10), facecolor="#ffffff")
    # # cell_spot = len(full_grid[:, 0, 0])*len(full_grid[0, :, 0])
    # for cell_i in range(len(full_grid[:,0,0])):
    #     for cell_j in range(len(full_grid[0,:,0])):
    #         fig = plt.figure(1, figsize=(6, 4), facecolor="#ffffff")
    #         ax = fig.add_subplot(111)
    #         #ax = fig.add_subplot(len(full_grid[0, :, 0]), len(full_grid[:, 0, 0]), cell_spot)
    #
    #         if np.nanmax(full_grid[cell_i,cell_j,:]) > 0.0:
    #             plot_values = full_grid[cell_i,cell_j,:][full_grid[cell_i,cell_j,:] > 0]
    #             ax.hist(plot_values,bins=z_grid)
    #             ax.set_xlim([0, np.max(z_grid)])
    #             ax.set_title('a/Rstar: ' + str(np.round(x_grid[cell_i],2)) + '-' + str(np.round(x_grid[cell_i+1],2)) + '\nPlanet Mass (Mjup): '+ str(np.round(y_grid[cell_j],2)) + '-' + str(np.round(y_grid[cell_j+1],2)))
    #
    #             fig.tight_layout()
    #             plt.show()
    #         else:
    #             plt.close()


            # cell_spot -= 1



    # fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})


    # import pdb; pdb.set_trace()
def calc_probabilities_in_cells(input_xyz, x_grid, y_grid, z_grid, x_axis, savehere, colormap, Rot_Max=50, Num_Segments=3, color_by_star_rot=True):


    min_y_axis_pad = 0.0005
    max_y_axis_pad = 5

    if x_axis == 'Orbit Semi-Major Axis (au))':
        x_axis = 'Orbit Semi-Major Axis (au)'
        min_x_axis_pad = 0.0005
        max_x_axis_pad = 2

    if x_axis == 'Ratio of Semi-Major Axis to Stellar Radius':
        min_x_axis_pad = 0.1
        max_x_axis_pad = 300

    if x_axis == 'Orbital Period (days)':
        min_x_axis_pad = 0.05
        max_x_axis_pad = 3000

    # combined_all = {'Orbit Semi-Major Axis (au)': np.concatenate((pl_a1, pl_a2)),
    #                 'Orbit Semi-Major Axis (au) Upper': np.concatenate((pl_a1_upper, pl_a2_upper)),
    #                 'Orbit Semi-Major Axis (au) Lower': np.concatenate((pl_a1_lower, pl_a2_lower)),
    #                 'Planet Mass (Jupiter Mass)': np.concatenate((pl_Mjup1, pl_Mjup2)),
    #                 'Planet Mass (Jupiter Mass) Upper': np.concatenate((pl_Mjup1_upper, pl_Mjup2_upper)),
    #                 'Planet Mass (Jupiter Mass) Lower': np.concatenate((pl_Mjup1_lower, pl_Mjup2_lower)),
    #                 'Stellar Rotation Period (d)': np.concatenate((st_Rot1, st_Rot2)),
    #                 }

    x_values = input_xyz[x_axis]
    # x_upper = input_xyz['Orbit Semi-Major Axis (au) Upper']
    # x_lower = input_xyz['Orbit Semi-Major Axis (au) Lower']
    y_values = input_xyz['Planet Mass (Jupiter Mass)']
    # y_upper = input_xyz['Planet Mass (Jupiter Mass) Upper']
    # y_lower = input_xyz['Planet Mass (Jupiter Mass) Lower']
    # z_values = input_xyz['Stellar Rotation Period (d)']


    prob_cube = np.zeros( (len(z_grid) - 1, (len(y_grid) - 1)*(len(x_grid)-1)) )
    for rot in range(len(z_grid) - 1):
        # reset cell number
        # print('--------------------------------------')
        # print('--------------------------------------')
        # print('CHECK ON CUBE: ')
        # print(prob_cube)
        # print('--------------------------------------')
        # print('--------------------------------------')
        # import pdb; pdb.set_trace()
        cell_number = 0
        for row in range(len(y_grid) - 1):
            for col in range(len(x_grid)-1):

                systems_within_cell = input_xyz
                systems_within_cell = systems_within_cell[(systems_within_cell[x_axis] > x_grid[col]) & (systems_within_cell[x_axis] <= x_grid[col+1])]
                systems_within_cell = systems_within_cell[(systems_within_cell['Planet Mass (Jupiter Mass)'] >= y_grid[row]) & (systems_within_cell['Planet Mass (Jupiter Mass)'] < y_grid[row+1])]

                if (len(systems_within_cell) == 0) or (len(systems_within_cell) == 1):
                    prob = float('nan')
                    # n_systems_within_specified_rot_window = 0
                    prob_cube[rot,cell_number] = prob
                else:
                    n_systems_within_cell = len(systems_within_cell)
                    systems_within_specified_rot_window = systems_within_cell[(systems_within_cell['Stellar Rotation Period (d)'] >= z_grid[rot]) & (systems_within_cell['Stellar Rotation Period (d)'] < z_grid[rot+1])]

                    if len(systems_within_specified_rot_window) == 0:
                        prob = 0
                        # n_systems_within_specified_rot_window = 0
                        prob_cube[rot, cell_number] = prob
                    else:
                        n_systems_within_specified_rot_window = len(systems_within_specified_rot_window)
                        frac_cell = n_systems_within_specified_rot_window / n_systems_within_cell

                        total_systems_within_specified_rot_window = input_xyz[(input_xyz['Stellar Rotation Period (d)'] >= z_grid[rot]) & (input_xyz['Stellar Rotation Period (d)'] < z_grid[rot + 1])]
                        frac_total = len(total_systems_within_specified_rot_window) / len(input_xyz)

                        prob = frac_cell / frac_total
                        prob_cube[rot, cell_number] = prob

                # print('--------------------------------------')
                # print('CHECK ON CELL: ')
                # print('row: ' + str(row) + '  col: ' + str(col))
                # print('cell num: ' + str(cell_number))
                # print('systems within cell: ' + str(n_systems_within_cell))
                # print('systems within specified rot window: ' + str(n_systems_within_specified_rot_window))
                # print('calculated probability: ' + str(prob))
                # print('--------------------------------------')
                # import pdb; pdb.set_trace()

                cell_number += 1








    plt.close()

    cmap = colormap
    max_lim = 4
    bin_segment = max_lim / 255
    map_bounds = np.arange(0, max_lim+bin_segment, bin_segment)# *max_lim # max_rot_lim + bin_segment, bin_segment)
    # map_bounds = np.linspace(0, max_lim + max_lim/255, 255)
    norm = mpl.colors.BoundaryNorm(map_bounds, cmap.N)
    # norm = mpl.colors.Normalize(vmin=0, vmax=max_lim)

    font_size = 'medium'

    fig = plt.figure(1, figsize=(10, 6), facecolor="#ffffff")
    for rot in range(len(z_grid) - 1):

        ax = fig.add_subplot(2, 3, rot + 1)
        ax.set_title(str(z_grid[rot]) + r' < P$_{rot}$ (d) $\leq$ ' + str(z_grid[rot+1]), fontsize=font_size, style='normal', family='sans-serif')

        cell_number = 0
        for row in range(len(y_grid) - 1):
            for col in range(len(x_grid)-1):

                cell_color = prob_cube[rot][cell_number]

                text_x = np.nanmean([x_grid[col], x_grid[col + 1]])*0.58
                text_y = np.nanmean([y_grid[row], y_grid[row + 1]])*0.60

                # text_x = np.mod(col, len(x_grid)-1) + 0.5*(1./len(x_grid)-1) * (max(x_grid) - min(x_grid))
                # text_y = np.mod(row, len(y_grid)-1) + 0.5*(1./len(y_grid)-1) * (max(y_grid) - min(y_grid))

                if np.isnan(cell_color) == True:
                    ax.fill_between([x_grid[col], x_grid[col + 1]], y_grid[row], y_grid[row + 1],
                                    facecolor='none', edgecolor='grey', hatch='///', norm=norm, cmap=cmap,
                                    zorder=0)
                    # ax.text(x=text_x, y=text_y, s='--', color='#000000',
                    #         horizontalalignment='center', verticalalignment='center', fontsize=font_size, weight='bold')
                else:
                    ax.fill_between([x_grid[col], x_grid[col+1]], y_grid[row], y_grid[row+1], color=cmap(cell_color/max_lim),
                                    norm=norm, cmap=cmap, zorder=0)
                    ax.text(x=text_x, y=text_y, s=str(np.round(cell_color, 2)), color='#ffffff',
                            horizontalalignment='center', verticalalignment='center', fontsize='x-small', weight='bold')

                cell_number += 1

        # ax.vlines(x=x_grid[1:-1], ymin=min(y_values) - min_y_axis_pad, ymax=max(y_values) + max_y_axis_pad, lw=1, color='#ffffff')
        # ax.hlines(y=y_grid[1:-1], xmin=min(x_values) - min_x_axis_pad, xmax=max(x_values) + max_x_axis_pad, lw=1, color='#ffffff')

        ax.vlines(x=x_grid[1:-1], ymin=min(y_grid), ymax=max(y_grid), lw=1, color='#ffffff')
        ax.hlines(y=y_grid[1:-1], xmin=min(x_grid), xmax=max(x_grid), lw=1, color='#ffffff')

        ax.scatter(x_values, y_values, c='grey', edgecolor=None, linewidth=None, s=np.pi * (1) ** 2)
        # ax.errorbar(x_values, y_values, yerr=[y_lower,y_upper], xerr=[x_lower,x_upper], ls='None', ecolor='#ffffff', elinewidth=1, capsize=2, capthick=1, zorder=0)
        # cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        # cb.set_label('Probability', fontsize=font_size, style='normal', family='sans-serif', rotation=270, labelpad=15)
        # cb.set_ticks([0,0.2, 0.4, 0.6, 0.8, 1.0])

        if (rot+1 == 4) or (rot+1 == 5):
            ax.set_xlabel(x_axis, fontsize=font_size, style='normal', family='sans-serif')
        if (rot+1 == 1) or (rot+1 == 4):
            ax.set_ylabel('Planet Mass (Jupiter Mass)', fontsize=font_size, style='normal', family='sans-serif')
        ax.set_xscale('log')
        ax.set_yscale('log')
        # ax.set_ylim(min(y_values) - min_y_axis_pad, max(y_values) + max_y_axis_pad)
        # ax.set_xlim(min(x_values) - min_x_axis_pad, max(x_values) + max_x_axis_pad)
        ax.set_ylim(min(y_grid), max(y_grid))
        ax.set_xlim(min(x_grid), max(x_grid))
        ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, top=True, right=True, color='grey')
        if (rot+1 == 2) or (rot+1 == 3) or (rot+1 == 5):
            ax.set_yticks([])
        if (rot+1 == 1) or (rot+1 == 2):
            ax.set_xticks([])

    ax = fig.add_subplot(2, 3, rot + 2)
    ax.set_axis_off()
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axin = inset_axes(ax, width="95%", height="8%", loc='center')

    cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), cax=axin, orientation='horizontal') # , anchor=(0.5,0.5)) #location='middle') # aspect=0.50,
    cb.set_label('Fraction in Cell / Fraction of Total', fontsize='medium', style='normal', family='sans-serif', rotation=0, labelpad=10)
    cb.ax.xaxis.set_ticks_position('top')
    cb.ax.xaxis.set_label_position('top')
    cb.set_ticks(np.round(np.arange(0, max_lim + max_lim/5, max_lim/5),1))
    cb.ax.set_xticklabels(np.round(np.arange(0, max_lim + max_lim/5, max_lim/5),1), fontsize=font_size)

    plt.tight_layout()
    plt.savefig(savehere, dpi=300)
    plt.show()

    # import pdb; pdb.set_trace()

    return prob_cube

    # return x_grid, y_grid, z_grid


    # import pdb; pdb.set_trace()

    # full_grid = np.empty((num_separation_cells, num_mass_cells, len(df1))) # num_separation_cells*num_mass_cells))
    # full_grid = full_grid*0
    #
    # for cell_i in range(num_separation_cells):
    #     for cell_j in range(num_mass_cells):
    #
    #         for planet in range(len(df1)):
    #
    #             if cell_i == len(x_grid)-1:
    #                 where_in_x_cell = np.where(x_values >= x_grid[cell_i])[0]
    #             else:
    #                 where_in_x_cell = np.where((x_values >= x_grid[cell_i]) & (x_values < x_grid[cell_i + 1]))[0]
    #
    #             if len(where_in_x_cell) > 0:
    #                 x_values_in_cell_i = x_values[where_in_x_cell]
    #                 y_values_in_cell_i = y_values[where_in_x_cell]
    #                 z_values_in_cell_i = z_values[where_in_x_cell]
    #
    #                 if cell_j == len(y_grid) - 1:
    #                     where_in_y_cell = np.where(y_values_in_cell_i >= y_grid[cell_j])[0]
    #                 else:
    #                     where_in_y_cell = np.where((y_values_in_cell_i >= y_grid[cell_j]) & (y_values_in_cell_i < y_grid[cell_j + 1]))[0]
    #
    #                 if len(where_in_y_cell) > 0:
    #                     x_values_in_cell_ij = x_values_in_cell_i[where_in_y_cell]
    #                     y_values_in_cell_ij = y_values_in_cell_i[where_in_y_cell]
    #                     z_values_in_cell_ij = z_values_in_cell_i[where_in_y_cell]
    #
    #                     z_values_in_cell_ij = z_values_in_cell_ij[z_values_in_cell_ij>0]
    #
    #                     # print(z_values_in_cell_ij)
    #
    #                     full_grid[cell_i, cell_j, 0:len(z_values_in_cell_ij)] = z_values_in_cell_ij
    #
    #                 else:
    #                     full_grid[cell_i,cell_j,:] = 0.0
    #
    #             else:
    #                 full_grid[cell_i, cell_j, :] = 0.0
    #
    # plt.close()
    # # fig = plt.figure(1, figsize=(11, 10), facecolor="#ffffff")
    # # cell_spot = len(full_grid[:, 0, 0])*len(full_grid[0, :, 0])
    # for cell_i in range(len(full_grid[:,0,0])):
    #     for cell_j in range(len(full_grid[0,:,0])):
    #         fig = plt.figure(1, figsize=(6, 4), facecolor="#ffffff")
    #         ax = fig.add_subplot(111)
    #         #ax = fig.add_subplot(len(full_grid[0, :, 0]), len(full_grid[:, 0, 0]), cell_spot)
    #
    #         if np.nanmax(full_grid[cell_i,cell_j,:]) > 0.0:
    #             plot_values = full_grid[cell_i,cell_j,:][full_grid[cell_i,cell_j,:] > 0]
    #             ax.hist(plot_values,bins=z_grid)
    #             ax.set_xlim([0, np.max(z_grid)])
    #             ax.set_title('a/Rstar: ' + str(np.round(x_grid[cell_i],2)) + '-' + str(np.round(x_grid[cell_i+1],2)) + '\nPlanet Mass (Mjup): '+ str(np.round(y_grid[cell_j],2)) + '-' + str(np.round(y_grid[cell_j+1],2)))
    #
    #             fig.tight_layout()
    #             plt.show()
    #         else:
    #             plt.close()


            # cell_spot -= 1



    # fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})


    # import pdb; pdb.set_trace()







archive_download_date = '04Jan2022'
exoplanets_dot_org_download_date = '04Jan2022'

original_download_filename = 'Planetary_System_Files/exoplanet_archive_' + archive_download_date + '.csv'

column_labels_filename = 'Column_Labels.csv'
stellar_rotations_filename = 'Planetary_System_Files/StellarRotation.csv'
stellar_ages_filename = 'Planetary_System_Files/StellarAges.csv'
exoplanets_dot_org_filename = 'Planetary_System_Files/exoplanets_dot_org_' + exoplanets_dot_org_download_date + '.csv'

save_path_and_filename_for_organized = 'Planetary_System_Files/exoplanet_archive_' + archive_download_date + '_condensed.csv'
save_path_and_filename_for_organized_added_starpers = 'Planetary_System_Files/exoplanet_archive_' + archive_download_date + '_condensed_added_starpers.csv'
save_path_and_filename_for_organized_added_starpers_ages = 'Planetary_System_Files/exoplanet_archive_' + archive_download_date + '_condensed_added_starpers_ages.csv'
save_path_and_filename_for_organized_added_starpers_ages_exoplanetsdotorg = 'Planetary_System_Files/exoplanet_archive_' + archive_download_date + '_condensed_added_starpers_ages_exoplanetsdotorg.csv'

original_download_df = pd.read_csv(original_download_filename)
column_labels_df = pd.read_csv(column_labels_filename)
stellar_rotations_df = pd.read_csv(stellar_rotations_filename)
stellar_ages_df = pd.read_csv(stellar_ages_filename)
exoplanets_dot_org_df = pd.read_csv(exoplanets_dot_org_filename)

save_path_for_figures = 'Figures/'

do_organize = False
if do_organize == True:
    do_condense = True
    do_add_star_rots = True
    do_add_star_ages = True
    do_add_exoplanets_dot_org_data = True # currently stellar data only


    if do_condense == True:
        organized_parameter_df = condense_planet_pars(input_df=original_download_df, col_labs_df=column_labels_df,
                                                      save_name=save_path_and_filename_for_organized)
    if do_add_star_rots == True:
        organized_with_starpers_added_df = add_missing_stellar_pars(input_df=organized_parameter_df,
                                                                    star_rots_df=stellar_rotations_df,
                                                                    save_name=save_path_and_filename_for_organized_added_starpers)
    if do_add_star_ages == True:
        organized_with_starpers_ages_added_df = add_missing_age_pars(input_df=organized_with_starpers_added_df,
                                                                     star_ages_df=stellar_ages_df,
                                                                     save_name=save_path_and_filename_for_organized_added_starpers_ages)
    if do_add_exoplanets_dot_org_data == True:
        organized_with_starpers_ages_exoplanetsdotorg_added_df = add_exoplanets_dot_org_data(input_df=organized_with_starpers_ages_added_df,
                                                                                              exo_dot_org_df=exoplanets_dot_org_df,
                                                                                              save_name=save_path_and_filename_for_organized_added_starpers_ages_exoplanetsdotorg)

    to_plot_df = organized_with_starpers_ages_exoplanetsdotorg_added_df  # organized_parameter_df # organized_with_starpers_ages_exoplanetsdotorg_added_df

if do_organize == False:
    analyze_this_csv = 'Planetary_System_Files/exoplanet_archive_04Jan2022_condensed_added_starpers_ages_exoplanetsdotorg.csv'
    to_plot_df = pd.read_csv(analyze_this_csv)



do_plots = False
do_stats = True

restrictions = {'min number of planets in system': 1,
                'max number of planets in system': 10000,
                'max rotation limit': 50,
                'max vsini limit': 'None',
                'exclude circumbinaries': True,
                'exclude multiple star systems': True,
                'exclude eccentric planet orbits': False,
                'exclude controversial planets': True,
                'require these detection methods': 'None',
                'require these discovery methods': 'None',
                'Teff limits': 'None',
                'Age': [0.5,10000],
                'Mstar': 'None',
                'max orbit semi-major axis (au)': 100,
                }

df_with_restrictions = impose_restrictions(input_df=to_plot_df, restriction_dict=restrictions)



x_axis_type = 'Orbit Semi-Major Axis (au))'
x_axis_type = 'Ratio of Semi-Major Axis to Stellar Radius'
x_axis_type = 'Orbital Period (days)'

if x_axis_type == 'Orbit Semi-Major Axis (au))':
    save_label = 'semi_major_axis_vs_M'
if x_axis_type == 'Ratio of Semi-Major Axis to Stellar Radius':
    save_label = 'a_over_Rstar_vs_M'
if x_axis_type == 'Orbital Period (days)':
    save_label = 'orbital_period_vs_M'


if do_plots == True:
    max_rotation_limit = restrictions['max rotation limit']
    number_of_segments = 5
    color_by_star_rotation = True
    # input_colormap = cm.RdYlBu_r # cm.plasma_r # cm.viridis_r # cm.inferno_r # cm.RdYlBu_r # choose_cmap() # cm.rainbow
    input_colormap = choose_cmap(custom_cmap='my_sunset_melon')

    plot_x_vs_bothMplanet(input_df=df_with_restrictions, x_axis=x_axis_type, savehere=save_path_for_figures+save_label+'.pdf', colormap=input_colormap, Rot_Max=max_rotation_limit, Num_Segments=number_of_segments,color_by_star_rot=color_by_star_rotation,include_msini=True)

    # a_vs_bothMplanet(input_df=df_with_restrictions, savehere=save_path_for_figures+'a_vs_bothMplanet.pdf', colormap=input_colormap, Rot_Max=max_rotation_limit, Num_Segments=number_of_segments,color_by_star_rot=color_by_star_rotation,include_msini=True)
    # aoverRstar_vs_bothMplanet(input_df=df_with_restrictions, savehere=save_path_for_figures+'aoverRstar_vs_bothMplanet.pdf', colormap=input_colormap, Rot_Max=max_rotation_limit, Num_Segments=number_of_segments,color_by_star_rot=color_by_star_rotation,include_msini=True)
    # OrbitalPeriod_vs_bothMplanet(input_df=df_with_restrictions, savehere=save_path_for_figures+'OrbitalPeriod_vs_bothMplanet.pdf', colormap=input_colormap, Rot_Max=max_rotation_limit, Num_Segments=number_of_segments,color_by_star_rot=color_by_star_rotation,include_msini=True)


if do_stats == True:
    max_rotation_limit = restrictions['max rotation limit']
    number_of_segments = 5
    input_colormap = choose_cmap(custom_cmap='my_sunset_melon')
    ncols = 4
    nrows = 4
    probability_colormap = choose_cmap(custom_cmap='my_darkteal_red')

    separations, masses, rotations, all_seps_masses_rots = isolate_relevant_data(input_df=df_with_restrictions, x_axis=x_axis_type, Rot_Max=max_rotation_limit, include_msini=True)

    X_grid, Y_grid, Z_grid = generate_subset_domains(input_x=separations, input_y=masses, input_z=rotations, x_axis=x_axis_type, savehere=save_path_for_figures+'test_grid_' + save_label +'.pdf',colormap=input_colormap, num_cols=ncols, num_rows=nrows, Rot_Max=max_rotation_limit, Num_Segments=number_of_segments, color_by_star_rot=True)

    rotation_probabilities = calc_probabilities_in_cells(input_xyz=all_seps_masses_rots, x_grid=X_grid, y_grid=Y_grid, z_grid=Z_grid, x_axis=x_axis_type, savehere=save_path_for_figures+'fractions_' + save_label +'.pdf',colormap=probability_colormap, Rot_Max=max_rotation_limit, Num_Segments=number_of_segments, color_by_star_rot=True)











