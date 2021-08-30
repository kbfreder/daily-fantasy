
import argparse
import pandas as pd
import numpy as np

from .util.funcs import *


data_dir = paths.SCRAPED_DATA
data_filename = "dk_20210821.csv"
dk_df = pd.read_csv(os.path.join(data_dir, data_filename))

data_filename = "fbdb_2020.csv"
stats_df = pd.read_csv(os.path.join(data_dir, data_filename))


dk_df['Player'] = dk_df['player_name'].apply(lambda x: convert_names(x))
dk_df['Player'] = dk_df['Player'].apply(fix_names)

stats_df['dk_pts'] = stats_df.apply(dk_calc_points, axis=1)
stm = stats_df[['Player', 'Game', 'Pts*', 'dk_pts']]

merge_df = pd.merge(dk_df, stm, on='Player', how='outer')
merge_no_nan = merge_df.dropna(subset=['dk_pts'])
print(f"Merge df size before drop na: {len(merge_df)}, after: {len(merge_no_nan)}")

# corr = np.corrcoef(merge_no_nan['points'], merge_no_nan['dk_pts'])
