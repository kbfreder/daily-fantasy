
FIX_NAME_DICT = {'Patrick Mahomes II': 'Patrick Mahomes'}


def calc_dk_points(row):
    pts = (row['Passing_TD'] * 4 +
           row['Passing_Yds'] * 0.04 +
           row['Passing_Int'] * -1 +
           row['Rushing_TD'] * 6 +
           row['Rushing_Yds'] * 0.01 +
           row['Receiving_TD'] * 6 +
           row['Receiving_Yds'] * 0.01 +
           row['Receiving_Rec'] * 1 +
           row['Rushing_2Pt'] * 2 +
           row['Receiving_2Pt'] * 2 + 
           row['Fumbles_FL'] * -1 + 
           row['Fumbles_TD'] * 6
          )
    if row['Passing_Yds'] > 300:
        pts += 3 
    if row['Rushing_Yds'] > 100:
        pts += 3
    if row['Receiving_Yds'] > 100:
        pts += 3
    
    return pts


def convert_names(name_str):
    try:
        name_list = name_str.split(',')
        last_name = name_list[0]
        first_name = name_list[1].lstrip()
        return f"{first_name} {last_name}"
    except IndexError:
        return name_str


def fix_names(name):
    if name in FIX_NAME_DICT.keys():
        return FIX_NAME_DICT[name]
    else: 
        return name