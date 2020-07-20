import json
import pandas as pd

jsonFilePath = 'FullListMen2020.json'
jsonOutputFilePath = 'MenPythag2020.json'
csvFilePath = 'MenPythag2020.csv'

with open(jsonFilePath) as jsonFile:
    teams = json.load(jsonFile)

stats = []

for team in teams:
    row = {}

    pf_game = float(teams[team]['PF/G'])
    pa_game = float(teams[team]['PA/G'])
    pythag1 = round(1 / (1 + (pa_game / pf_game)**2), 3)

    pct = round(float(teams[team]['WinPercent']), 3)

    actualWins = int(teams[team]['Wins'])
    expectedWins = round(pythag1 * int(teams[team]['Games']), 1)

    row['TeamName'] = teams[team]['Name']
    row['WinningPct'] = pct
    row['Pythag1'] = pythag1
    row['Wins'] = actualWins
    row['Wins1'] = expectedWins
    row['Delta'] = actualWins - expectedWins
    
    stats.append(row)

# populate a data frame with the stats
df = pd.DataFrame(stats)

with open(jsonOutputFilePath, 'w') as jsonOutputFile:
    jsonOutputFile.write(json.dumps(stats, indent=4))

with open(csvFilePath, 'w') as csvFile:
    csvFile.write(df.to_csv())

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(df)
print('Correlation: ' + str(df['WinningPct'].corr(df['Pythag1'])))

print(df.describe())





































