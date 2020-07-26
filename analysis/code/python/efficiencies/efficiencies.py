import json
import pandas as pd

jsonFilePath = 'FullListMen2020.json'
jsonOutputFilePath = 'Efficiencies2020.json'
csvFilePath = 'Efficiencies2020.csv'

with open(jsonFilePath) as jsonFile:
    teams = json.load(jsonFile)

def compute_points(iv):
    i_points = iv[0]*3 + iv[1]*2 + iv[2]*1 - iv[3]

    return round(i_points, 3)


#statistics
stats = []

for team in teams:

#make an entry
    row = {}
    row['TeamName'] = teams[team]['Name']
    row['Games'] = int(teams[team]['Games'])
    row['WinningPct'] = round(float(teams[team]['WinPercent']), 3)
    row['HammerEnds'] = int(teams[team]['EndsWithHammer'])
    row['BlanksWith'] = int(teams[team]['Blanksw/Hammer'])
    row['OneWith'] = int(teams[team]['Score1Hammer'])
    row['TwoWith'] = int(teams[team]['Score2Hammer'])
    row['ThreePlusWith'] = int(teams[team]['Score3Hammer']) + int(teams[team]['Score4Hammer'])
    row['StolenEndsAgainst'] = int(teams[team]['Give1Hammer']) + int(teams[team]['Give2Hammer']) + int(teams[team]['Give3Hammer']) + int(teams[team]['Give4Hammer'])
    row['NoHammerEnds'] = int(teams[team]['EndsWithoutHammer'])
    row['BlanksWithout'] = int(teams[team]['Blanksw/oHammer'])
    row['Steals'] = int(teams[team]['Score1Steal']) + int(teams[team]['Score2Steal']) + int(teams[team]['Score3Steal']) + int(teams[team]['Score4Steal'])
    row['GiveOne'] = int(teams[team]['Give1Steal'])
    row['GiveTwo'] = int(teams[team]['Give2Steal'])
    row['GiveThreePlus'] = int(teams[team]['Give3Steal']) + int(teams[team]['Give4Steal'])

    # Hammer Vector <3+, 2, 1, -1, 0>
    h_ends = row['HammerEnds']
    hammer_vector = [ round(row['ThreePlusWith']/h_ends,3), 
                      round(row['TwoWith']/h_ends, 3),
                      round(row['OneWith']/h_ends, 3),
                      round(row['StolenEndsAgainst']/h_ends, 3),
                      round(row['BlanksWith']/h_ends, 3) ]
    row['HammerVector'] = hammer_vector

    # Force Vector <3+, 2, 1, -1, 0>
    f_ends = row['NoHammerEnds']
    force_vector = [ round(row['GiveThreePlus']/f_ends, 3), 
                     round(row['GiveTwo']/f_ends, 3),
                     round(row['GiveOne']/f_ends, 3),
                     round(row['Steals']/f_ends, 3),
                     round(row['BlanksWithout']/f_ends, 3) ]
    row['ForceVector'] = force_vector

    row['ExpHP'] = compute_points(hammer_vector)
    row['ExpSP'] = compute_points(force_vector)

    stats.append(row)

# now that league-independent data population is finished, we can add stats based on comparing to the league average

# populate a data frame with the stats we have so far, so that we can compute some averages
df_full = pd.DataFrame(stats)

# filter the sample based on some criteria; here we use games played
min_games = df_full['Games'] > 10
df = df_full[min_games]

# League Average Vector <3+, 2, 1, -1, 0>
h_ends = df['HammerEnds'].mean()
f_ends = df['NoHammerEnds'].mean()

league_vector = [ round((df['ThreePlusWith'].mean() + df['GiveThreePlus'].mean())/(h_ends + f_ends), 3),
                  round((df['TwoWith'].mean() + df['GiveTwo'].mean())/(h_ends + f_ends), 3),
                  round((df['OneWith'].mean() + df['GiveOne'].mean())/(h_ends + f_ends), 3),
                  round((df['StolenEndsAgainst'].mean() + df['Steals'].mean())/(h_ends + f_ends), 3),
                  round((df['BlanksWith'].mean() + df['BlanksWithout'].mean())/(h_ends + f_ends), 3) ]

# expected points with and without the hammer, on average for our league
hp_l = df['ExpHP'].mean()
sp_l = df['ExpSP'].mean()


# now go through each team and see how they compare to the league, add it to the stats dict
# here, we express a team's strength relative to the baseline scoring environment as a single 
# number, with league average performance being 100
# important! you need to create a new dataframe if you want this new info to appear in reports!

for i in stats:
    i['HF'] = int((i['ExpHP']/hp_l)*100)
    i['SF'] = int((sp_l/i['ExpSP'])*100)

final = pd.DataFrame(stats)

# write the full report to some files to enable further analysis
with open(jsonOutputFilePath, 'w') as jsonOutputFile:
    jsonOutputFile.write(json.dumps(stats, indent=4))

with open(csvFilePath, 'w') as csvFile:
    csvFile.write(final.to_csv())

# filter the sample for the report based on some criteria
min_games = df_full['Games'] > 15
final_filtered = final[min_games]

# select columns for report
# see above for available columns
columns = ['TeamName', 'ExpHP', 'HF', 'ExpSP','SF']
report = final_filtered[columns]

# sort it


# set options for display and print
pd.set_option("display.max_rows", None, "display.max_columns", None)
print("Efficiences for Men's 2020 OOM teams, 15 games minimum")
print("ExpHP: points per end expected for the hammer team when team has the hammer")
print("ExpSP: points expected per end for the hammer team when team does not have the hammer ")
print("Scoring environment: " + str(round((hp_l + sp_l)/2, 2)) + " points per end for the hammer team")
print('\n')
print(report)







































