
from astroquery.vizier import Vizier
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
from astropy.io import ascii
from astroquery.mast import Catalogs
import re



def clean_data(input_df):

    input_df['Mplanet (Mjup)'].replace('', np.nan, inplace=True)
    input_df['Mplanet (Mjup)'].replace(0, np.nan, inplace=True)
    input_df.dropna(subset=['Mplanet (Mjup)'], inplace=True)

    return input_df
def query_details(input_df):

    vsini_dict = {}

    CustomSimbad = Simbad()

    CustomSimbad.add_votable_fields('sptype','rot') #,'ids') # 'measurements',

    targ_list = []
    ROT_list = []
    ROTerr_list = []
    SPTYPE_list = []
    KICID_list = []

    for targ in input_df['Star']:
        # print(k)
        # percent_complete = (k + 1) / len(data_sectors['RA'])
        # print('\r' + str(np.round(percent_complete,3)) + ' %', end='', flush=True)

        print(targ)
        targ_list.append(targ)

        try:
            result_table = CustomSimbad.query_object(targ)
        except:
            print(' ')
            print('issue with CustomSimbad.query_object(targ)')
            print(' ')
            import pdb; pdb.set_trace()
        id_table = Simbad.query_objectids(targ)
        found_id = False
        try:
            for id in id_table:
                if 'KIC' in id:
                    KICID_list.append(id)
                    found_id = True
                    print(id)
        except:
            pass
        if found_id == False:
            KICID_list.append('')

        #print(result_table[0])

        #import pdb; pdb.set_trace()

        try:
            ROT_list.append(result_table['ROT_Vsini'][0])
        except:
            ROT_list.append('')
        try:
            ROTerr_list.append(result_table['ROT_err'][0])
        except:
            ROTerr_list.append('')
        try:
            SPTYPE_list.append(result_table['SP_TYPE'][0].decode('utf-8'))
        except:
            SPTYPE_list.append('')
        #catalog_data = Catalogs.query_object(result_table[0]['RA'] + ' ' + result_table[0]['DEC'], radius=0.1)

    import pdb; pdb.set_trace()

    vsini_dict['Star'] = targ_list
    vsini_dict['KICID'] = KICID_list
    vsini_dict['ROT'] = ROT_list
    vsini_dict['SPTYPE'] = SPTYPE_list

    vsini_df = pd.DataFrame(data=vsini_dict)
    vsini_df.to_csv('Vsini.csv', index=False)
def query_details_single_targ(targ):

    CustomSimbad = Simbad()

    CustomSimbad.add_votable_fields('sptype','rot') #,'ids') # 'measurements',

    print(targ)

    try:
        result_table = CustomSimbad.query_object(targ)
    except:
        print(' ')
        print('issue with CustomSimbad.query_object(targ)')
        print(' ')
        import pdb; pdb.set_trace()
    id_table = Simbad.query_objectids(targ)
    found_id = False
    try:
        for id in id_table:
            if 'KIC' in id:
                KICID = id
                found_id = True
                print(id)
    except:
        pass
    if found_id == False:
        KICID = ''

    #print(result_table[0])

    #import pdb; pdb.set_trace()

    try:
        VSINI = result_table['ROT_Vsini'][0]
    except:
        VSINI = ''
    try:
        VSINI_err = result_table['ROT_err'][0]
    except:
        VSINI_err = ''
    try:
        SPTYPE = result_table['SP_TYPE'][0].decode('utf-8')
    except:
        SPTYPE = ''
    #catalog_data = Catalogs.query_object(result_table[0]['RA'] + ' ' + result_table[0]['DEC'], radius=0.1)

    #import pdb; pdb.set_trace()


    return VSINI, VSINI_err, SPTYPE, KICID


def scrape_vizier(df_data):

    targets = df_data['Star']

    # possible_heads = ['Vsini','vsini','v_sini','V_sini','vsin_i','Vsin_i','v_sin_i','V_sin_i','vsin(i)','Vsin(i)']
    # possible_heads = ['inclination','Inclination','incl','Incl','i','I']
    # possible_heads = ['Vmag','vmag','V_mag','v_mag','V','v','VMag','vMag','V_Mag','v_Mag']

    possible_heads = ['P_rot','Period','Per','p_rot','period','per','Rot','rot','Prot','P_ROT','ROT','rotation_period',
                      'ROTATION_PERIOD','Rotation_Period','Rotation','rotation','ROTATION','rotation period']

    target_pers = []
    recorded_targs = []
    target_vsini = []
    target_vsini_err = []
    target_sptype = []
    target_kicid = []

    timeout_targs = ['HD 175541','HD 231701','Kepler-749','BD+20 594']

    for j,target in enumerate(targets):

        if (target in recorded_targs) or (target in timeout_targs):
            continue

        print('\n------------------ '+target+' ------------------\n')

        results = Vizier.query_object(target)

        table_pers = []

        for i,table in enumerate(results):

            skipit = 0
            keepit = 0
            for head in possible_heads:
                keys = table.keys()
                if head in keys:

                    for key_i in range(len(keys)):
                        if head == keys[key_i]:
                            break

                    where_head = key_i

                    # import pdb; pdb.set_trace()
                    # print(type(table[head][0]),table[head][0])

                    checkit_flag = 0

                    if isinstance(table[head][0],str) == True:
                        continue

                    if isinstance(table[head][0],np.float64) == True:
                        checkit_flag = 1

                    if isinstance(table[head][0], np.float32) == True:
                        checkit_flag = 1

                    if checkit_flag == 1:
                        print(table[head].description, '  |  ', head, '  |  ', np.float(table[head][0]))

                        skip_words = ['Orbital', 'orbital', 'planet', 'Planet', 'transit', 'Transit', 'interval',
                                      'Interval','Planetary','planetary']
                        for word in skip_words:
                            #import pdb; pdb.set_trace()
                            if word in table[head].description:
                                skipit = 1
                                break

                        # validity = input("Add Period?   :   ")
                        if skipit == 0:
                            keep_words = ['Rotational', 'rotational', 'Rotation', 'rotation', 'star', 'Star', 'Rot ',
                                          'rot ', 'stellar', 'Stellar', 'Prot']
                            for keep_word in keep_words:
                                if keep_word in table[head].description:
                                    keepit = 1
                                    break
                        if keepit == 1:
                            table_pers.append(np.float(table[head][0]))
                            print('Period Added!')


        if len(table_pers) > 0:
            target_pers.append(table_pers)
        else:
            target_pers.append([])

        vsini, vsini_err, sptype, kicid = query_details_single_targ(target)

        target_vsini.append(vsini)
        target_vsini_err.append(vsini_err)
        target_sptype.append(sptype)
        target_kicid.append(kicid)


        recorded_targs.append(target)

        period_dict = {'Star':recorded_targs,
                       'Prot':target_pers,
                       'Vsini':target_vsini,
                       'Vsini_err':target_vsini_err,
                       'SpType':target_sptype,
                       }

        period_df = pd.DataFrame(period_dict)

        #print(period_df)

        #import pdb; pdb.set_trace()
        period_df.to_csv('Periods.csv',index=False)

    return period_df
#print(table[head][0])

#import pdb; pdb.set_trace()

# string = results.keys()[i] #.encode('ascii', 'ignore')
# # string = str(string)
# # string = string.replace("'","")
# # if string[0] == 'b'
# split_str = string.split('/')
# search_str = '/'.join(split_str[:-1])
#
# cat = Vizier.find_catalogs(search_str)
# cat_dict = ({k: v.description for k, v in cat.items()})
# #print({k: v.description for k, v in cat.items()})
#
# import pdb; pdb.set_trace()
#
# print(results[results.keys()[i]])
#
# # print 'Printing...'
# #
# # f = open(target+'.txt', 'a+')
# # f.write(string+'\n')
# # #f.write(cat_dict.keys()[0].encode('ascii', 'ignore')+'\n')
# # f.write(cat_dict[cat_dict.keys()[0]].encode('ascii', 'ignore')+'\n')
# # f.write(tabulate(results[results.keys()[i]],headers=table.keys()))
# # f.write('\n\n\n')
# # f.close()
#
# # print ' '
# # print ' '


def table_to_df(input_table):
    data_dict = {}
    for col in input_table.columns:
        data_dict[col] = list(input_table[col])
    df = pd.DataFrame(data=data_dict)

    return df
def trim_keystring(input_key):
    input_key_split = re.split('(\W)', input_key)
    input_key_split2 = input_key_split[0:-2]
    output_key = ''.join(input_key_split2)
    return output_key
def flatten_list(input_list):
    return [item for sublist in input_list for item in sublist]



# from tabulate import tabulate

archive_download_date = '04Jan2022'

fileloc = '/Users/lbiddle/PycharmProjects/Exoplanets/Planetary_System_Files/'
filename = 'exoplanet_archive_' + archive_download_date + '_condensed.csv'

# very useful : Simbad.list_votable_fields()

df_data = pd.read_csv(fileloc+filename)


# df_data = clean_data(input_df=df_data)

targets = df_data['Host Name']


#
# table_data = ascii.read(fileloc+filename2)
# table_data = table_to_df(input_table=table_data)

# period_df = scrape_vizier(df_data)
#
#
# targets = df_data['Star']
#
# # possible_heads = ['Vsini','vsini','v_sini','V_sini','vsin_i','Vsin_i','v_sin_i','V_sin_i','vsin(i)','Vsin(i)']
# # possible_heads = ['inclination','Inclination','incl','Incl','i','I']
# # possible_heads = ['Vmag','vmag','V_mag','v_mag','V','v','VMag','vMag','V_Mag','v_Mag']
#
# possible_rot_heads = ['P_rot', 'Period', 'Per', 'p_rot', 'period', 'per', 'Rot', 'rot', 'Prot', 'P_ROT', 'ROT',
#                       'rotation_period', 'ROTATION_PERIOD', 'Rotation_Period', 'Rotation', 'rotation', 'ROTATION',
#                       'rotation period']
#
# target_pers = []
# recorded_targs = []
# target_vsini = []
# target_vsini_err = []
# target_sptype = []
# target_kicid = []
#
# timeout_targs = ['HD 175541', 'HD 231701', 'Kepler-749', 'BD+20 594','Kepler-450']
#
# for j, target in enumerate(targets):
#
#     if (target in recorded_targs) or (target in timeout_targs):
#         continue
#
#     print('\n------------------ ' + target + ' ------------------\n')
#
#     results = Vizier.query_object(target)
#
#     table_pers = []
#
#     for i, table in enumerate(results):
#
#         skipit = 0
#         keepit = 0
#         for head in possible_rot_heads:
#             keys = table.keys()
#             if head in keys:
#
#                 for key_i in range(len(keys)):
#                     if head == keys[key_i]:
#                         break
#
#                 where_head = key_i
#
#                 # import pdb; pdb.set_trace()
#                 # print(type(table[head][0]),table[head][0])
#
#                 checkit_flag = 0
#
#                 if isinstance(table[head][0], str) == True:
#                     continue
#
#                 if isinstance(table[head][0], np.float64) == True:
#                     checkit_flag = 1
#
#                 if isinstance(table[head][0], np.float32) == True:
#                     checkit_flag = 1
#
#                 if checkit_flag == 1:
#                     print(table[head].description, '  |  ', head, '  |  ', np.float(table[head][0]))
#
#                     skip_words = ['Orbital', 'orbital', 'planet', 'Planet', 'transit', 'Transit', 'interval',
#                                   'Interval', 'Planetary', 'planetary']
#                     for word in skip_words:
#                         # import pdb; pdb.set_trace()
#                         if word in table[head].description:
#                             skipit = 1
#                             break
#
#                     # validity = input("Add Period?   :   ")
#                     if skipit == 0:
#                         keep_words = ['Rotational', 'rotational', 'Rotation', 'rotation', 'star', 'Star', 'Rot ',
#                                       'rot ', 'stellar', 'Stellar', 'Prot']
#                         for keep_word in keep_words:
#                             if keep_word in table[head].description:
#                                 keepit = 1
#                                 break
#                     if keepit == 1:
#                         table_pers.append(np.float(table[head][0]))
#                         print('Period Added!')
#
#     if len(table_pers) > 0:
#         target_pers.append(table_pers)
#     else:
#         target_pers.append([])
#
#     vsini, vsini_err, sptype, kicid = query_details_single_targ(target)
#
#     target_vsini.append(vsini)
#     target_vsini_err.append(vsini_err)
#     target_sptype.append(sptype)
#     target_kicid.append(kicid)
#
#     recorded_targs.append(target)
#
#     period_dict = {'Star': recorded_targs,
#                    'Prot': target_pers,
#                    'Vsini': target_vsini,
#                    'Vsini_err': target_vsini_err,
#                    'SpType': target_sptype,
#                    }
#
#     period_df = pd.DataFrame(period_dict)
#
#     # print(period_df)
#
#     # import pdb; pdb.set_trace()
#     period_df.to_csv('Periods3.csv', index=False)



possible_age_heads = ['Age', 'age','logAge','log_age','log_Age','LogAge','Log_age']
possible_vsini_heads = ['Vsini','vsini','v_sini','V_sini','vsin_i','Vsin_i','v_sin_i','V_sin_i','vsin(i)','Vsin(i)']
possible_incl_heads = ['inclination','Inclination','incl','Incl','i','I']
possible_log_luminosity_heads = ['logL','log_Luminosity','log_luminosity','logLum','log_L_']
possible_luminosity_heads = ['L_','L_Lsun','L','luminosity','Luminosity', 'lum', 'Lum']
possible_Teff_heads = ['Teff','Teffective','T_eff','T_effective','Effective_Temp','Tefftemp','T','T_','Teff_','T_eff_']
possible_mass_heads = ['Mass','M_','Mstar','M_star','M']
possible_radius_heads = ['Radius','Rstar','R_','R_star','R_rad','radius','Rad','rad','R']
possible_metal_heads = ['__Fe_H_','metallicity','Metallicity','[Fe/H]']
possible_logg_heads = ['logg','log(g)','log_g','log_g_']
possible_logRHK_heads = ['logRhk','LogRhk','logRHK','LogRHK','log_RHK','Log_RHK','log_rhk','Log_rhk']
possible_rot_heads = ['P_rot', 'Period', 'Per', 'p_rot', 'period', 'per', 'Rot', 'rot', 'Prot', 'P_ROT', 'ROT',
                      'rotation_period', 'ROTATION_PERIOD', 'Rotation_Period', 'Rotation', 'rotation', 'ROTATION',
                      'rotation period']

identifier_descriptions = ['Stellar identifier (HD NNNNNN)']

identifiers = ['TIC','HD','HR','HIP','GAIA','SDSS','Gaia']
target_col = ['Target','Name','Star','ID','Host','Ident']

extra_cols = ['Notes','Remarks']

master_heads = ['Age', 'age','logAge','log_age','log_Age','LogAge','Log_age','__Fe_H_','metallicity','Metallicity','[Fe/H]','logRhk','LogRhk','logRHK','LogRHK','log_RHK','Log_RHK','log_rhk','Log_rhk']




rotstar_list = []
rotstar_unit_list = []
rotstar_source_list = []
rotstar_recorded_targs = []

age_list = []
log_age_list = []
age_unit_list = []
age_log_unit_list = []
age_source_list = []
age_log_source_list = []
age_recorded_targs = []
age_log_recorded_targs = []

metallicity_list = []
metallicity_unit_list = []
metallicity_source_list = []
metallicity_recorded_targs = []

logRHK_list = []
logRHK_unit_list = []
logRHK_source_list = []
logRHK_recorded_targs = []

mstar_list = []
mstar_unit_list = []
mstar_source_list = []
mstar_recorded_targs = []

rstar_list = []
rstar_unit_list = []
rstar_source_list = []
rstar_recorded_targs = []

general_recorded_targets = []






do_rotation_search = False
do_age_search = False
do_metallicity_search = True
do_logRHK_search = False
do_mass_search = False
do_radius_search = False

timeout_targs = ['HD 175541', 'HD 231701', 'Kepler-749', 'BD+20 594', 'Kepler-450', 'EPIC 206032309','HATS-63',
                 'HD 111998', 'HD 124330', 'HD 216435', 'K2-102', 'K2-151']
for j, target in enumerate(targets):

    if (target in general_recorded_targets) or (target in timeout_targs):
        continue

    print('\n------------------ ' + target + ' ------------------\n')

    if do_rotation_search == True:
        targ_df = df_data.loc[df_data['Host Name'] == target]
        if np.isnan(targ_df['Stellar Rotational Period (days)'].values[0]) == False:
            print('Rotation of target known.')
            continue
    if do_age_search == True:
        targ_df = df_data.loc[df_data['Host Name'] == target]
        if np.isnan(targ_df['Stellar Age (Gyr)'].values[0]) == False:
            print('Age of target known.')
            continue
    if do_metallicity_search == True:
        targ_df = df_data.loc[df_data['Host Name'] == target]
        if np.isnan(targ_df['Stellar Metallicity (dex)'].values[0]) == False:
            print('Metallicity of target known.')
            continue
    if do_mass_search == True:
        targ_df = df_data.loc[df_data['Host Name'] == target]
        if np.isnan(targ_df['Stellar Mass (Solar Mass)'].values[0]) == False:
            print('Mass of target known.')
            continue
    if do_radius_search == True:
        targ_df = df_data.loc[df_data['Host Name'] == target]
        if np.isnan(targ_df['Stellar Radius (Solar Radius)'].values[0]) == False:
            print('Radius of target known.')
            continue

    results = Vizier.query_object(target)
    results_keys = results.keys()

    for i, table in enumerate(results):


        results_key = results_keys[i]
        # results_key = trim_keystring(input_key=results_key)

        # if (results_key[0:2] == 'I/') or (results_key[0:3] == 'II/') or (results_key[0:4] == 'III/') or (results_key[0:2] == 'V/'):
        #     continue

        keys = table.keys()

        if do_rotation_search == True:

            for head in possible_rot_heads:
                rotstar_avoid_flag = 0
                if head in keys:
                    #print(head)
                    for key in keys:
                        print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
                        if key == head:

                            avoid_these_descriptions = ['Orbital', 'orbital', 'planet', 'Planet', 'transit', 'Transit',
                                                        'interval', 'Interval', 'Planetary', 'planetary', 'pl','Pl']
                            keep_these_descriptions = ['Rotational', 'rotational', 'Rotation', 'rotation', 'star', 'Star',
                                                       'Rot ', 'Rot', 'rot ', 'stellar', 'Stellar', 'Prot']

                            column_unit = str(table[key].info.unit)
                            column_unit = column_unit.replace('[', '')
                            column_unit = column_unit.replace(']', '')
                            column_unit = column_unit.replace('(', '')
                            column_unit = column_unit.replace(')', '')

                            for avoid in avoid_these_descriptions:
                                if (avoid in table[key].description) or (avoid in column_unit):
                                    rotstar_avoid_flag = 1
                                    break
                                else:
                                    for keep in keep_these_descriptions:
                                        if keep in table[key].description:
                                            rotstar_avoid_flag = 0
                                            break
                                        else:
                                            rotstar_avoid_flag = 1

                            # import pdb; pdb.set_trace()

                            if rotstar_avoid_flag == 0:
                                rotstar_list.append(table[key][0])
                                rotstar_unit_list.append(column_unit)
                                rotstar_source_list.append(results_key)
                                rotstar_recorded_targs.append(target)
        if do_age_search == True:
            for head in possible_age_heads:
                if head in keys:
                    print(head)
                    for key in keys:
                        print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)

                        if head == key:
                            column_unit = str(table[key].info.unit)
                            column_unit = column_unit.replace('[', '')
                            column_unit = column_unit.replace(']', '')
                            column_unit = column_unit.replace('(', '')
                            column_unit = column_unit.replace(')', '')
                            print(column_unit)
                            if ('log' in key) or ('Log' in key):
                                log_age_list.append(table[key][0])
                                age_log_unit_list.append(column_unit)
                                age_log_source_list.append(results_key)
                                age_log_recorded_targs.append(target)
                            else:
                                age_list.append(table[key][0])
                                age_unit_list.append(column_unit)
                                age_source_list.append(results_key)
                                age_recorded_targs.append(target)
        if do_metallicity_search == True:
            for head in possible_metal_heads:
                if head in keys:
                    print(head)
                    for key in keys:
                        print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)

                        if key == head:
                            column_unit = str(table[key].info.unit)
                            column_unit = column_unit.replace('[', '')
                            column_unit = column_unit.replace(']', '')
                            column_unit = column_unit.replace('(', '')
                            column_unit = column_unit.replace(')', '')
                            metallicity_list.append(table[key][0])
                            metallicity_unit_list.append(column_unit)
                            metallicity_source_list.append(results_key)
                            metallicity_recorded_targs.append(target)
        if do_logRHK_search == True:
            for head in possible_logRHK_heads:
                if head in keys:
                    print(head)
                    for key in keys:
                        print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)

                        if key == head:
                            column_unit = str(table[key].info.unit)
                            column_unit = column_unit.replace('[', '')
                            column_unit = column_unit.replace(']', '')
                            column_unit = column_unit.replace('(', '')
                            column_unit = column_unit.replace(')', '')
                            logRHK_list.append(table[key][0])
                            logRHK_unit_list.append(column_unit)
                            logRHK_source_list.append(results_key)
                            logRHK_recorded_targs.append(target)
        if do_mass_search == True:
            for head in possible_mass_heads:
                mstar_avoid_flag = 0
                if head in keys:
                    #print(head)
                    for key in keys:
                        print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
                        if key == head:
                            avoid_these_descriptions = ['Planet','planet','pl','Pl','jov','Jov','geo','Geo','jup','Jup','earth','Earth']
                            keep_these_descriptions = ['Mass', 'mass']

                            column_unit = str(table[key].info.unit)
                            column_unit = column_unit.replace('[', '')
                            column_unit = column_unit.replace(']', '')
                            column_unit = column_unit.replace('(', '')
                            column_unit = column_unit.replace(')', '')

                            for avoid in avoid_these_descriptions:
                                if (avoid in table[key].description) or (avoid in column_unit):
                                    mstar_avoid_flag = 1
                                    break
                                else:
                                    for keep in keep_these_descriptions:
                                        if keep in table[key].description:
                                            rotstar_avoid_flag = 0
                                            break
                                        else:
                                            rotstar_avoid_flag = 1

                            if mstar_avoid_flag == 0:
                                mstar_list.append(table[key][0])
                                mstar_unit_list.append(column_unit)
                                mstar_source_list.append(results_key)
                                mstar_recorded_targs.append(target)
        if do_radius_search == True:
            for head in possible_radius_heads:
                rstar_avoid_flag = 0
                if head in keys:
                    #print(head)
                    for key in keys:
                        print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
                        if key == head:
                            avoid_these_descriptions = ['Planet','planet','pl','Pl','jov','Jov','geo','Geo','jup','Jup','earth','Earth']
                            keep_these_descriptions = ['Radius','radius','rad','Rad']

                            column_unit = str(table[key].info.unit)
                            column_unit = column_unit.replace('[', '')
                            column_unit = column_unit.replace(']', '')
                            column_unit = column_unit.replace('(', '')
                            column_unit = column_unit.replace(')', '')

                            for avoid in avoid_these_descriptions:
                                if (avoid in table[key].description) or (avoid in column_unit):
                                    rstar_avoid_flag = 1
                                    break
                                else:
                                    for keep in keep_these_descriptions:
                                        if keep in table[key].description:
                                            rotstar_avoid_flag = 0
                                            break
                                        else:
                                            rotstar_avoid_flag = 1

                            if rstar_avoid_flag == 0:
                                rstar_list.append(table[key][0])
                                rstar_unit_list.append(column_unit)
                                rstar_source_list.append(results_key)
                                rstar_recorded_targs.append(target)

    # if do_rotation_search == True:
    #     if len(rotstar_list) == 0:
    #         rotstar_list.append(np.float('nan'))
    #         rotstar_unit_list.append('')
    #         rotstar_source_list.append('')
    #         rotstar_recorded_targs.append(target)
    # if do_age_search == True:
    #     if len(log_age_list) == 0:
    #         log_age_list.append(np.float('nan'))
    #         age_log_unit_list.append('')
    #         age_log_source_list.append('')
    #
    #     if len(age_list) == 0:
    #         age_list.append(np.float('nan'))
    #         age_unit_list.append('')
    #         age_source_list.append('')
    # if do_metallicity_search == True:
    #     if len(metallicity_list) == 0:
    #         metallicity_list.append(np.float('nan'))
    #         metallicity_unit_list.append('')
    #         metallicity_source_list.append('')
    # if do_logRHK_search == True:
    #     if len(logRHK_list) == 0:
    #         logRHK_list.append(np.float('nan'))
    #         logRHK_unit_list.append('')
    #         logRHK_source_list.append('')
    #         logRHK_recorded_targs.append(target)
    # if do_mass_search == True:
    #     if len(mstar_list) == 0:
    #         mstar_list.append(np.float('nan'))
    #         mstar_unit_list.append('')
    #         mstar_source_list.append('')
    #         mstar_recorded_targs.append(target)
    # if do_radius_search == True:
    #     if len(rstar_list) == 0:
    #         rstar_list.append(np.float('nan'))
    #         rstar_unit_list.append('')
    #         rstar_source_list.append('')
    #         rstar_recorded_targs.append(target)


    if do_rotation_search == True:
        rotstar_dict = {'Star': rotstar_recorded_targs,
                   'Prot': rotstar_list,
                   'Unit': rotstar_unit_list,
                   'LitSource': rotstar_source_list,
                   }

        rotstar_df = pd.DataFrame(rotstar_dict)
        rotstar_df.to_csv(fileloc + 'StellarRotation.csv', index=False)
    if do_age_search == True:
        ages_dict = {'Star': age_recorded_targs,
                     'Age': age_list,
                     'Unit': age_unit_list,
                     'LitSource': age_source_list,
                     }
        log_ages_dict = {'Star': age_log_recorded_targs,
                         'Log(Age)': log_age_list,
                         'Unit': age_log_unit_list,
                         'LitSource': age_log_source_list,
                         }

        log_ages_df = pd.DataFrame(log_ages_dict)
        log_ages_df.to_csv(fileloc + 'StellarlogAges_' + archive_download_date + '.csv', index=False)

        ages_df = pd.DataFrame(ages_dict)
        ages_df.to_csv(fileloc + 'StellarAges_' + archive_download_date + '.csv', index=False)
    if do_metallicity_search == True:
        metallicity_dict = {'Star': metallicity_recorded_targs,
                        'Age': metallicity_list,
                        'Unit': metallicity_unit_list,
                        'LitSource': metallicity_source_list,
                        }

        metallicity_df = pd.DataFrame(metallicity_dict)
        metallicity_df.to_csv(fileloc + 'StellarMetallicity_' + archive_download_date + '.csv', index=False)
    if do_logRHK_search == True:
        logRHK_dict = {'Star': logRHK_recorded_targs,
                   'Log(RHK)': logRHK_list,
                   'Unit': logRHK_unit_list,
                   'LitSource': logRHK_source_list,
                   }

        logRHK_df = pd.DataFrame(logRHK_dict)
        logRHK_df.to_csv(fileloc + 'StellarlogRHK_' + archive_download_date + '.csv', index=False)
    if do_mass_search == True:
        mstar_dict = {'Star': mstar_recorded_targs,
                   'Mstar': mstar_list,
                   'Unit': mstar_unit_list,
                   'LitSource': mstar_source_list,
                   }

        mstar_df = pd.DataFrame(mstar_dict)
        mstar_df.to_csv(fileloc + 'StellarMass_' + archive_download_date + '.csv', index=False)
    if do_radius_search == True:
        rstar_dict = {'Star': rstar_recorded_targs,
                   'Rstar': rstar_list,
                   'Unit': rstar_unit_list,
                   'LitSource': rstar_source_list,
                   }

        rstar_df = pd.DataFrame(rstar_dict)
        rstar_df.to_csv(fileloc + 'StellarRadius_' + archive_download_date + '.csv', index=False)


    general_recorded_targets.append(target)

    # import pdb; pdb.set_trace()


    #
    # # print(period_df)
    # import pdb; pdb.set_trace()
    #             for key_i in range(len(keys)):
    #                 if head == keys[key_i]:
    #                     break
    #
    #             where_head = key_i
    #
    #             # import pdb; pdb.set_trace()
    #             # print(type(table[head][0]),table[head][0])
    #
    #             checkit_flag = 0
    #
    #             if isinstance(table[head][0], str) == True:
    #                 continue
    #
    #             if isinstance(table[head][0], np.float64) == True:
    #                 checkit_flag = 1
    #
    #             if isinstance(table[head][0], np.float32) == True:
    #                 checkit_flag = 1
    #
    #             if checkit_flag == 1:
    #                 print(table[head].description, '  |  ', head, '  |  ', np.float(table[head][0]))
    #
    #                 skip_words = ['Orbital', 'orbital', 'planet', 'Planet', 'transit', 'Transit', 'interval',
    #                               'Interval', 'Planetary', 'planetary']
    #                 for word in skip_words:
    #                     # import pdb; pdb.set_trace()
    #                     if word in table[head].description:
    #                         skipit = 1
    #                         break
    #
    #                 # validity = input("Add Period?   :   ")
    #                 if skipit == 0:
    #                     keep_words = ['Rotational', 'rotational', 'Rotation', 'rotation', 'star', 'Star', 'Rot ',
    #                                   'rot ', 'stellar', 'Stellar', 'Prot']
    #                     for keep_word in keep_words:
    #                         if keep_word in table[head].description:
    #                             keepit = 1
    #                             break
    #                 if keepit == 1:
    #                     table_pers.append(np.float(table[head][0]))
    #                     print('Period Added!')
    #
    # if len(table_pers) > 0:
    #     target_pers.append(table_pers)
    # else:
    #     target_pers.append([])
    #
    # vsini, vsini_err, sptype, kicid = query_details_single_targ(target)
    #
    # target_vsini.append(vsini)
    # target_vsini_err.append(vsini_err)
    # target_sptype.append(sptype)
    # target_kicid.append(kicid)
    #
    # recorded_targs.append(target)
    #
    # period_dict = {'Star': recorded_targs,
    #                'Prot': target_pers,
    #                'Vsini': target_vsini,
    #                'Vsini_err': target_vsini_err,
    #                'SpType': target_sptype,
    #                }
    #
    # period_df = pd.DataFrame(period_dict)
    #
    # # print(period_df)
    #
    # # import pdb; pdb.set_trace()
    # period_df.to_csv('Ages.csv', index=False)
    #
    #
    #
    #
    #
    #





# for j, target in enumerate(targets):
#
#     if (target in general_recorded_targets) or (target in timeout_targs):
#         continue
#
#     print('\n------------------ ' + target + ' ------------------\n')
#
#     results = Vizier.query_object(target)
#     results_keys = results.keys()
#
#     for i, table in enumerate(results):
#
#         skipit = 0
#         keepit = 0
#
#         results_key = results_keys[i]
#         results_key = trim_keystring(input_key=results_key)
#
#         if (results_key[0:2] == 'I/') or (results_key[0:3] == 'II/') or (results_key[0:4] == 'III/') or (results_key[0:2] == 'V/'):
#             continue
#
#         keys = table.keys()
#
#         for master_head in master_heads:
#             if master_head in keys:
#
#                 try:
#                     catalog = Vizier.find_catalogs(results_key)
#                 except:
#                     # print('issue with catalog')
#
#                     for head in possible_age_heads:
#                         if head in keys:
#                             print(head)
#                             for key in keys:
#                                 print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#
#                                 if head == key:
#                                     column_unit = str(table[key].info.unit)
#                                     column_unit = column_unit.replace('[', '')
#                                     column_unit = column_unit.replace(']', '')
#                                     column_unit = column_unit.replace('(', '')
#                                     column_unit = column_unit.replace(')', '')
#                                     print(column_unit)
#                                     if ('log' in key) or ('Log' in key):
#                                         log_age_list.append(table[key][0])
#                                         age_log_unit_list.append(column_unit)
#                                         age_log_source_list.append(results_key)
#                                         age_log_recorded_targs.append(target)
#                                     else:
#                                         age_list.append(table[key][0])
#                                         age_unit_list.append(column_unit)
#                                         age_source_list.append(results_key)
#                                         age_recorded_targs.append(target)
#                     # for head in possible_metal_heads:
#                     #     if head in keys:
#                     #         print(head)
#                     #         for key in keys:
#                     #             print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                     #
#                     #             if key == head:
#                     #                 column_unit = str(table[key].info.unit)
#                     #                 column_unit = column_unit.replace('[', '')
#                     #                 column_unit = column_unit.replace(']', '')
#                     #                 column_unit = column_unit.replace('(', '')
#                     #                 column_unit = column_unit.replace(')', '')
#                     #                 metallicity_list.append(table[key][0])
#                     #                 metallicity_unit_list.append(column_unit)
#                     #                 metallicity_source_list.append(results_key)
#                     #                 metallicity_recorded_targs.append(target)
#                     for head in possible_logRHK_heads:
#                         if head in keys:
#                             print(head)
#                             for key in keys:
#                                 print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#
#                                 if key == head:
#                                     column_unit = str(table[key].info.unit)
#                                     column_unit = column_unit.replace('[', '')
#                                     column_unit = column_unit.replace(']', '')
#                                     column_unit = column_unit.replace('(', '')
#                                     column_unit = column_unit.replace(')', '')
#                                     logRHK_list.append(table[key][0])
#                                     logRHK_unit_list.append(column_unit)
#                                     logRHK_source_list.append(results_key)
#                                     logRHK_recorded_targs.append(target)
#
#                 else:
#
#                     if len(catalog) > 0:
#
#                         catalog_dict = ({k: v.description for k, v in catalog.items()})
#                         catalog_description = catalog_dict[results_key]
#                         try:
#                             year = int(catalog_description[-5:-1])
#                             if year < 2000:
#                                 continue
#                         except:
#                             try:
#                                 year = int(catalog_description[-3:-1])
#                             except:
#                                 continue
#                             else:
#                                 if year <= 99:
#                                     continue
#
#                         for head in possible_age_heads:
#                             if head in keys:
#                                 print(head)
#                                 for key in keys:
#                                     print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                                     if key == head:
#                                         # print(table[key])
#                                         column_unit = str(table[key].info.unit)
#                                         column_unit = column_unit.replace('[', '')
#                                         column_unit = column_unit.replace(']', '')
#                                         column_unit = column_unit.replace('(', '')
#                                         column_unit = column_unit.replace(')', '')
#                                         if ('log' in key) or ('Log' in key):
#                                             log_age_list.append(table[key][0])
#                                             age_log_unit_list.append(column_unit)
#                                             age_log_source_list.append(catalog_dict[results_key])
#                                             age_log_recorded_targs.append(target)
#                                         else:
#                                             age_list.append(table[key][0])
#                                             age_unit_list.append(column_unit)
#                                             age_source_list.append(catalog_dict[results_key])
#                                             age_recorded_targs.append(target)
#                         # for head in possible_metal_heads:
#                         #     if head in keys:
#                         #         print(head)
#                         #         for key in keys:
#                         #             print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                         #             if key == head:
#                         #                 # print(table[key])
#                         #                 column_unit = str(table[key].info.unit)
#                         #                 column_unit = column_unit.replace('[', '')
#                         #                 column_unit = column_unit.replace(']', '')
#                         #                 column_unit = column_unit.replace('(', '')
#                         #                 column_unit = column_unit.replace(')', '')
#                         #                 metallicity_list.append(table[key][0])
#                         #                 metallicity_unit_list.append(column_unit)
#                         #                 metallicity_source_list.append(catalog_dict[results_key])
#                         #                 metallicity_recorded_targs.append(target)
#                         for head in possible_logRHK_heads:
#                             if head in keys:
#                                 print(head)
#                                 for key in keys:
#                                     print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                                     if key == head:
#                                         # print(table[key])
#                                         column_unit = str(table[key].info.unit)
#                                         column_unit = column_unit.replace('[', '')
#                                         column_unit = column_unit.replace(']', '')
#                                         column_unit = column_unit.replace('(', '')
#                                         column_unit = column_unit.replace(')', '')
#                                         logRHK_list.append(table[key][0])
#                                         logRHK_unit_list.append(column_unit)
#                                         logRHK_source_list.append(catalog_dict[results_key])
#                                         logRHK_recorded_targs.append(target)
#                 break
#
#                 # for head in possible_age_heads:
#                 #     if head in keys:
#                 #         print(head)
#                 #         try:
#                 #             catalog = Vizier.find_catalogs(results_key)
#                 #         except:
#                 #             # print('issue with catalog')
#                 #             for key in keys:
#                 #                 print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                 #                 if key == head:
#                 #                     print(table[key])
#                 #                     # try:
#                 #                     column_unit = str(table[key].info.unit)
#                 #                     # except:
#                 #                     #     if 'log' in key:
#                 #                     #         column_unit = 'yr'
#                 #                     #     else:
#                 #                     #         column_unit = ' '
#                 #                     # else:
#                 #                     column_unit = column_unit.replace('[', '')
#                 #                     column_unit = column_unit.replace(']', '')
#                 #                     column_unit = column_unit.replace('(', '')
#                 #                     column_unit = column_unit.replace(')', '')
#                 #                     print(column_unit)
#                 #                     if ('log' in key) or ('Log' in key):
#                 #                         log_age_list.append(table[key][0])
#                 #                         age_log_unit_list.append(column_unit)
#                 #                         age_log_source_list.append(results_key)
#                 #                         age_log_recorded_targs.append(target)
#                 #                     else:
#                 #                         age_list.append(table[key][0])
#                 #                         age_unit_list.append(column_unit)
#                 #                         age_source_list.append(results_key)
#                 #                         age_recorded_targs.append(target)
#                 #         else:
#                 #
#                 #             if len(catalog) > 0:
#                 #
#                 #                 catalog_dict = ({k: v.description for k, v in catalog.items()})
#                 #                 catalog_description = catalog_dict[results_key]
#                 #
#                 #                 print(catalog_description)
#                 #                 try:
#                 #                     year = int(catalog_description[-5:-1])
#                 #                     if year < 2000:
#                 #                         continue
#                 #                 except:
#                 #                     try:
#                 #                         year = int(catalog_description[-3:-1])
#                 #                     except:
#                 #                         continue
#                 #                     else:
#                 #                         if year <= 99:
#                 #                             continue
#                 #
#                 #                 for key in keys:
#                 #                     print('catalog description:', catalog_dict[results_key], '  |  ', 'results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                 #                     if key == head:
#                 #                         print(table[key])
#                 #                         # try:
#                 #                         column_unit = str(table[key].info.unit)
#                 #                         # except:
#                 #                         #     if 'log' in key:
#                 #                         #         column_unit = 'yr'
#                 #                         #     else:
#                 #                         #         column_unit = ' '
#                 #                         # else:
#                 #                         column_unit = column_unit.replace('[', '')
#                 #                         column_unit = column_unit.replace(']', '')
#                 #                         column_unit = column_unit.replace('(', '')
#                 #                         column_unit = column_unit.replace(')', '')
#                 #                         print(column_unit)
#                 #                         if ('log' in key) or ('Log' in key):
#                 #                             # log_age_list.append([table[key][0], column_unit, catalog_dict[results_key]])
#                 #                             log_age_list.append(table[key][0])
#                 #                             age_log_unit_list.append(column_unit)
#                 #                             age_log_source_list.append(catalog_dict[results_key])
#                 #                             age_log_recorded_targs.append(target)
#                 #                         else:
#                 #                             # age_list.append([table[key][0], column_unit, catalog_dict[results_key]])
#                 #                             age_list.append(table[key][0])
#                 #                             age_unit_list.append(column_unit)
#                 #                             age_source_list.append(catalog_dict[results_key])
#                 #                             age_recorded_targs.append(target)
#                 # for head in possible_metal_heads:
#                 #     if head in keys:
#                 #         print(head)
#                 #         try:
#                 #             catalog = Vizier.find_catalogs(results_key)
#                 #         except:
#                 #             # print('issue with catalog')
#                 #             for key in keys:
#                 #                 print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                 #                 if key == head:
#                 #                     print(table[key])
#                 #                     # try:
#                 #                     column_unit = str(table[key].info.unit)
#                 #                     # except:
#                 #                     #     if 'log' in key:
#                 #                     #         column_unit = 'yr'
#                 #                     #     else:
#                 #                     #         column_unit = ' '
#                 #                     # else:
#                 #                     column_unit = column_unit.replace('[', '')
#                 #                     column_unit = column_unit.replace(']', '')
#                 #                     column_unit = column_unit.replace('(', '')
#                 #                     column_unit = column_unit.replace(')', '')
#                 #                     print(column_unit)
#                 #
#                 #                     metallicity_list.append(table[key][0])
#                 #                     metallicity_unit_list.append(column_unit)
#                 #                     metallicity_source_list.append(results_key)
#                 #                     metallicity_recorded_targs.append(target)
#                 #         else:
#                 #
#                 #             if len(catalog) > 0:
#                 #
#                 #                 catalog_dict = ({k: v.description for k, v in catalog.items()})
#                 #                 catalog_description = catalog_dict[results_key]
#                 #
#                 #                 print(catalog_description)
#                 #                 try:
#                 #                     year = int(catalog_description[-5:-1])
#                 #                     if year < 2000:
#                 #                         continue
#                 #                 except:
#                 #                     try:
#                 #                         year = int(catalog_description[-3:-1])
#                 #                     except:
#                 #                         continue
#                 #                     else:
#                 #                         if year <= 99:
#                 #                             continue
#                 #
#                 #                 for key in keys:
#                 #                     print('catalog description:', catalog_dict[results_key], '  |  ', 'results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                 #                     if key == head:
#                 #                         print(table[key])
#                 #                         # try:
#                 #                         column_unit = str(table[key].info.unit)
#                 #                         # except:
#                 #                         #     if 'log' in key:
#                 #                         #         column_unit = 'yr'
#                 #                         #     else:
#                 #                         #         column_unit = ' '
#                 #                         # else:
#                 #                         column_unit = column_unit.replace('[', '')
#                 #                         column_unit = column_unit.replace(']', '')
#                 #                         column_unit = column_unit.replace('(', '')
#                 #                         column_unit = column_unit.replace(')', '')
#                 #                         print(column_unit)
#                 #
#                 #                         metallicity_list.append(table[key][0])
#                 #                         metallicity_unit_list.append(column_unit)
#                 #                         metallicity_source_list.append(catalog_dict[results_key])
#                 #                         metallicity_recorded_targs.append(target)
#                 # for head in possible_logRHK_heads:
#                 #     if head in keys:
#                 #         print(head)
#                 #         try:
#                 #             catalog = Vizier.find_catalogs(results_key)
#                 #         except:
#                 #             # print('issue with catalog')
#                 #             for key in keys:
#                 #                 print('results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                 #                 if key == head:
#                 #                     print(table[key])
#                 #                     # try:
#                 #                     column_unit = str(table[key].info.unit)
#                 #                     # except:
#                 #                     #     if 'log' in key:
#                 #                     #         column_unit = 'yr'
#                 #                     #     else:
#                 #                     #         column_unit = ' '
#                 #                     # else:
#                 #                     column_unit = column_unit.replace('[', '')
#                 #                     column_unit = column_unit.replace(']', '')
#                 #                     column_unit = column_unit.replace('(', '')
#                 #                     column_unit = column_unit.replace(')', '')
#                 #                     print(column_unit)
#                 #
#                 #                     logRHK_list.append(table[key][0])
#                 #                     logRHK_unit_list.append(column_unit)
#                 #                     logRHK_source_list.append(results_key)
#                 #                     logRHK_recorded_targs.append(target)
#                 #         else:
#                 #
#                 #             if len(catalog) > 0:
#                 #
#                 #                 catalog_dict = ({k: v.description for k, v in catalog.items()})
#                 #                 catalog_description = catalog_dict[results_key]
#                 #
#                 #                 print(catalog_description)
#                 #                 try:
#                 #                     year = int(catalog_description[-5:-1])
#                 #                     if year < 2000:
#                 #                         continue
#                 #                 except:
#                 #                     try:
#                 #                         year = int(catalog_description[-3:-1])
#                 #                     except:
#                 #                         continue
#                 #                     else:
#                 #                         if year <= 99:
#                 #                             continue
#                 #
#                 #                 for key in keys:
#                 #                     print('catalog description:', catalog_dict[results_key], '  |  ', 'results_key:', results_key, '  |  ', key, '  |  ', table[key].description)
#                 #                     if key == head:
#                 #                         print(table[key])
#                 #                         # try:
#                 #                         column_unit = str(table[key].info.unit)
#                 #                         # except:
#                 #                         #     if 'log' in key:
#                 #                         #         column_unit = 'yr'
#                 #                         #     else:
#                 #                         #         column_unit = ' '
#                 #                         # else:
#                 #                         column_unit = column_unit.replace('[', '')
#                 #                         column_unit = column_unit.replace(']', '')
#                 #                         column_unit = column_unit.replace('(', '')
#                 #                         column_unit = column_unit.replace(')', '')
#                 #                         print(column_unit)
#                 #
#                 #                         logRHK_list.append(table[key][0])
#                 #                         logRHK_unit_list.append(column_unit)
#                 #                         logRHK_source_list.append(catalog_dict[results_key])
#                 #                         logRHK_recorded_targs.append(target)
#
#
#     if len(log_age_list) == 0:
#         log_age_list.append(np.float('nan'))
#         age_log_unit_list.append('')
#         age_log_source_list.append('')
#     if len(age_list) == 0:
#         age_list.append(np.float('nan'))
#         age_unit_list.append('')
#         age_source_list.append('')
#
#     # if len(metallicity_list) == 0:
#     #     metallicity_list.append(np.float('nan'))
#     #     metallicity_unit_list.append('')
#     #     metallicity_source_list.append('')
#
#     if len(logRHK_list) == 0:
#         logRHK_list.append(np.float('nan'))
#         logRHK_unit_list.append('')
#         logRHK_source_list.append('')
#         logRHK_recorded_targs.append(target)
#
#     #import pdb; pdb.set_trace()
#
#     ages_dict = {'Star': age_recorded_targs,
#                  'Age': age_list,
#                  'Unit': age_unit_list,
#                  'LitSource': age_source_list,
#                  }
#     log_ages_dict = {'Star': age_log_recorded_targs,
#                      'Log(Age)': log_age_list,
#                      'Unit': age_log_unit_list,
#                      'LitSource': age_log_source_list,
#                      }
#     # metallicity_dict = {'Star': metallicity_recorded_targs,
#     #                     'Age': metallicity_list,
#     #                     'Unit': metallicity_unit_list,
#     #                     'LitSource': metallicity_source_list,
#     #                     }
#     logRHK_dict = {'Star': logRHK_recorded_targs,
#                    'Log(RHK)': logRHK_list,
#                    'Unit': logRHK_unit_list,
#                    'LitSource': logRHK_source_list,
#                    }
#
#     log_ages_df = pd.DataFrame(log_ages_dict)
#     log_ages_df.to_csv('logAges2.csv', index=False)
#
#     ages_df = pd.DataFrame(ages_dict)
#     ages_df.to_csv('Ages2.csv', index=False)
#
#     # metallicity_df = pd.DataFrame(metallicity_dict)
#     # metallicity_df.to_csv('Metallicity.csv', index=False)
#
#     logRHK_df = pd.DataFrame(logRHK_dict)
#     logRHK_df.to_csv('logRHK2.csv', index=False)
#
#
#     general_recorded_targets.append(target)
#
#
#     #
#     # # print(period_df)
#     # import pdb; pdb.set_trace()
#     #             for key_i in range(len(keys)):
#     #                 if head == keys[key_i]:
#     #                     break
#     #
#     #             where_head = key_i
#     #
#     #             # import pdb; pdb.set_trace()
#     #             # print(type(table[head][0]),table[head][0])
#     #
#     #             checkit_flag = 0
#     #
#     #             if isinstance(table[head][0], str) == True:
#     #                 continue
#     #
#     #             if isinstance(table[head][0], np.float64) == True:
#     #                 checkit_flag = 1
#     #
#     #             if isinstance(table[head][0], np.float32) == True:
#     #                 checkit_flag = 1
#     #
#     #             if checkit_flag == 1:
#     #                 print(table[head].description, '  |  ', head, '  |  ', np.float(table[head][0]))
#     #
#     #                 skip_words = ['Orbital', 'orbital', 'planet', 'Planet', 'transit', 'Transit', 'interval',
#     #                               'Interval', 'Planetary', 'planetary']
#     #                 for word in skip_words:
#     #                     # import pdb; pdb.set_trace()
#     #                     if word in table[head].description:
#     #                         skipit = 1
#     #                         break
#     #
#     #                 # validity = input("Add Period?   :   ")
#     #                 if skipit == 0:
#     #                     keep_words = ['Rotational', 'rotational', 'Rotation', 'rotation', 'star', 'Star', 'Rot ',
#     #                                   'rot ', 'stellar', 'Stellar', 'Prot']
#     #                     for keep_word in keep_words:
#     #                         if keep_word in table[head].description:
#     #                             keepit = 1
#     #                             break
#     #                 if keepit == 1:
#     #                     table_pers.append(np.float(table[head][0]))
#     #                     print('Period Added!')
#     #
#     # if len(table_pers) > 0:
#     #     target_pers.append(table_pers)
#     # else:
#     #     target_pers.append([])
#     #
#     # vsini, vsini_err, sptype, kicid = query_details_single_targ(target)
#     #
#     # target_vsini.append(vsini)
#     # target_vsini_err.append(vsini_err)
#     # target_sptype.append(sptype)
#     # target_kicid.append(kicid)
#     #
#     # recorded_targs.append(target)
#     #
#     # period_dict = {'Star': recorded_targs,
#     #                'Prot': target_pers,
#     #                'Vsini': target_vsini,
#     #                'Vsini_err': target_vsini_err,
#     #                'SpType': target_sptype,
#     #                }
#     #
#     # period_df = pd.DataFrame(period_dict)
#     #
#     # # print(period_df)
#     #
#     # # import pdb; pdb.set_trace()
#     # period_df.to_csv('Ages.csv', index=False)
#     #
#     #
#     #
#     #
#     #
#     #
