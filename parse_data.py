import pandas as pd
from datetime import datetime
import re
from os import listdir
from os.path import isfile, join

def open_file(filename):
    try:
        f = open(filename, "r")
        text = f.read()
    except:
        f = open(filename, "r",encoding='latin-1')
        text = f.read()
        # encoding='latin-1'
    lines = text.split('\n')
    return lines


def get_quotes(lines):
    char_index = [i for i in range(len(lines)) if '\t\t\t\t\t' in lines[i]]
    scenes_index = [j for j in range(len(lines)) if 'INT.' in lines[j] or 'EXT.' in lines[j]]

    data = []

    for i in char_index:
        name = lines[i].replace('\t\t\t\t\t', '')
        if "FADE OUT" in name:
            continue

        j = i+1
        next_line = lines[j]

        quote = ""

        while next_line != '':
            next_line = next_line.replace('\t', ' ')
            quote += re.sub("[\(\[].*?[\)\]]", "", next_line)
            j = j+1
            next_line = lines[j]

        if quote!="":
            try:
                scene = lines[max([x for x in scenes_index if x < i])]
            except:
                scene='INT. VOICE OVER'

            data.append([name, quote,scene])

    test_df = pd.DataFrame(data, columns=['character', 'quote','scene'])
    return (test_df)


def clean_name(name: str) -> str:
    char_add_ons = ['V.O.', "'S COM VOICE",
                    'Cont\'d', 'O.S.', "'S", "VOICE", "INTERCOM"]
    for txt in char_add_ons:
        if txt in name:
            name = name.replace(txt, '')
    return re.sub("[\(\[].*?[\)\]]", "", name.strip())

def get_view(loc:str):
    output = None
    views = ['INT.','EXT.']
    for v in views:
        if v in loc:
            output=v
    return(output)

def clean_location(loc:str):
    views = ['INT.','EXT.']
    output = loc
    for v in views:
        if v in output:
            output = output[output.index(v)+5:]
    if '(' in output:
        output = output[:output.index('(')-1]
    elif '-' in output:
        # why elif? we want space - deep space nine
        output = output[:output.index('-')-1]
    return(output)


def get_title(lines):
    series_ind = 0
    for i in range(len(lines)):
        if "STAR TREK: THE NEXT GENERATION" in lines[i] or 'STAR TREK: DEEP SPACE NINE' in lines[i]:
            series_ind = i
            break
    return str(lines[series_ind+2]).strip().replace('"','')


def get_date(lines):
    draft_ind = 0
    for i in range(len(lines)):
        if "FINAL DRAFT" in lines[i]:
            series_ind = i
            break
    try:
        date = str(lines[series_ind+2])
        date = date.strip()
        final = datetime.strptime(date, '%B %d, %Y')
    except:
        print(lines[series_ind+2])
        final = "AHHH"
    return final


def create_df(filepath: str) -> pd.DataFrame:
    lines = open_file(filepath)
    test_df = get_quotes(lines)
    test_df['location']=test_df['scene'].apply(clean_location)
    test_df['view']=test_df['scene'].apply(get_view)
    test_df['character'] = test_df['character'].apply(clean_name)
    test_df['episode'] = get_title(lines)
    test_df['date']=get_date(lines)
    return test_df


if __name__ == "__main__":
    # folders to iterate through
    folders = {'scripts_ds9/':'Deep Space Nine','scripts_tng/':'The Next Generation'}
    # get the files for each folder/series
    file_dict = {}
    for series in folders.keys():
        onlyfiles = [f for f in listdir(series) if isfile(join(series, f))]
        temp = {f:series for f in onlyfiles}
        # combine dict
        file_dict={**file_dict,**temp}
    
    #
    main_df = pd.DataFrame(
        [], columns=['character', 'quote', 'scene','location','view','episode','date','series','file'])

    for name in file_dict.keys():
        print(name)
        df = create_df(file_dict[name]+name)
        df['series']=folders[file_dict[name]]
        df['file']=name
        df.to_csv(file_dict[name].replace('/','_data/')+name.replace('.txt', '.csv'))
        main_df = pd.concat([main_df, df], axis=0)

    main_df.to_csv('complete_data.csv')
