These are the code and data files behind the efficiency reports at curling/analysis/efficiencies

The main input file is FullListMen2020.json which is derived from a spreadsheet created by Derrick McLean, which itself is backed by data from CurlingZone

The file csv2json converts the master spreadsheet to the relevant json file, if you want to try it on another league

The main code for the project is in efficiencies.py, and this will create both a csv and json file to use as input to further analysis
The files hammer_efficiency.py and force_efficiency.py both more detailed produce specialized reports, but no additional csv or json file
