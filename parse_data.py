import pandas as pd
from datetime import datetime
import re

def open_file(filename):
    f = open(filename, "r")
    text = f.read()
    lines = text.split('\n')
    return lines


def get_quotes(lines):
    characters = [x for x in lines if '\t\t\t\t\t' in x]
    char_index = [i for i in range(len(lines)) if '\t\t\t\t\t' in lines[i]]

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

        data.append([name, quote])

    test_df = pd.DataFrame(data, columns=['character', 'quote'])
    return (test_df)


def clean_name(name: str) -> str:
    char_add_ons = ['V.O.', "'S COM VOICE",
                    'Cont\'d', 'O.S.', "'S", "VOICE", "INTERCOM"]
    for txt in char_add_ons:
        if txt in name:
            name = name.replace(txt, '')
    return re.sub("[\(\[].*?[\)\]]", "", name.strip())


def get_title(lines):
    series_ind = 0
    for i in range(len(lines)):
        if "STAR TREK: THE NEXT GENERATION" in lines[i]:
            series_ind = i
            break
    return str(lines[series_ind+2]).strip()


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
    test_df['character'] = test_df['character'].apply(clean_name)
    test_df['episode'] = get_title(lines)
    return test_df


if __name__ == "__main__":
    file_list = [
        '102.txt', '120.txt', '138.txt', '156.txt', '174.txt', '192.txt', '210.txt', '228.txt', '246.txt', '264.txt',
        '103.txt', '121.txt', '139.txt', '157.txt', '175.txt', '193.txt', '211.txt', '229.txt', '247.txt', '265.txt',
        '104.txt', '122.txt', '140.txt', '158.txt', '176.txt', '194.txt', '212.txt', '230.txt', '248.txt', '266.txt',
        '105.txt', '123.txt', '141.txt', '159.txt', '177.txt', '195.txt', '213.txt', '231.txt', '249.txt', '267.txt',
        '106.txt', '124.txt', '142.txt', '160.txt', '178.txt', '196.txt', '214.txt', '232.txt', '250.txt', '268.txt',
        '107.txt', '125.txt', '143.txt', '161.txt', '179.txt', '197.txt', '215.txt', '233.txt', '251.txt', '269.txt',
        '108.txt', '126.txt', '144.txt', '162.txt', '180.txt', '198.txt', '216.txt', '234.txt', '252.txt', '270.txt',
        '109.txt', '127.txt', '145.txt', '163.txt', '181.txt', '199.txt', '217.txt', '235.txt', '253.txt', '271.txt',
        '110.txt', '128.txt', '146.txt', '164.txt', '182.txt', '200.txt', '218.txt', '236.txt', '254.txt', '272.txt',
        '111.txt', '129.txt', '147.txt', '165.txt', '183.txt', '201.txt', '219.txt', '237.txt', '255.txt', '273.txt',
        '112.txt', '130.txt', '148.txt', '166.txt', '184.txt', '202.txt', '220.txt', '238.txt', '256.txt', '274.txt',
        '113.txt', '131.txt', '149.txt', '167.txt', '185.txt', '203.txt', '221.txt', '239.txt', '257.txt', '275.txt',
        '114.txt', '132.txt', '150.txt', '168.txt', '186.txt', '204.txt', '222.txt', '240.txt', '258.txt', '276.txt',
        '115.txt', '133.txt', '151.txt', '169.txt', '187.txt', '205.txt', '223.txt', '241.txt', '259.txt', '277.txt',
        '116.txt', '134.txt', '152.txt', '170.txt', '188.txt', '206.txt', '224.txt', '242.txt', '260.txt',
        '117.txt', '135.txt', '153.txt', '171.txt', '189.txt', '207.txt', '225.txt', '243.txt', '261.txt',
        '118.txt', '136.txt', '154.txt', '172.txt', '190.txt', '208.txt', '226.txt', '244.txt', '262.txt',
        '119.txt', '137.txt', '155.txt', '173.txt', '191.txt', '209.txt', '227.txt', '245.txt', '263.txt'
    ]

    main_df = pd.DataFrame(
        [], columns=['character', 'quote', 'episode'])

    for name in file_list:
        print(name)
        df = create_df(name)
        df.to_csv(name.replace('.txt', '.csv'))
        main_df = pd.concat([main_df, df], axis=0)

    main_df.to_csv('complete_data.csv')
