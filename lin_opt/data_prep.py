
data_dir = paths.SCRAPED_DATA
data_filename = "dk_20210821.csv"
df = pd.read_csv(os.path.join(data_dir, data_filename))

wk_df = df[(df['week'] == 1) & (df['year'] == 2020)]
wk_df.reset_index(inplace=True, drop=True)
wk_dict = wk_df.to_dict(orient='index')