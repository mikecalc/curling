These reports compute the scoring efficiency of particular teams during the course of a season.

There are three reports:
<ol>
<li> The overall efficiency of each team expressed in terms of points per end, and a single number comparing that performance to the league average </li>
<li> The efficiency of the team with the hammer, expressed as a probability vector encoding the outcome for each end when the team has the hammer </li>
<li> The efficiency of the team without the hammer, expressed as a probability vector encoding the outcome for each end when the team does not have the hammer. </li>
</ol>
Important caveats: These efficiencies have *not* been adjusted for strength of competition or any notion of league beyond the data reported on CZ, so they reflect the scoring efficiency of a particular team in the games they curled, against whoever they curled against.
Similarly, the league averages reflect all the curling for a particular season done by all teams in all reported events. We did only consider teams that curled at least 10 games in reported events, but not other adjustment was made.

TODO: we plan to adjust these efficiencies based on league environment (e.g., top-level WCT tour teams) and strength of opponents shortly

For code and input data related to these reports, see curling/analysis/code/python/efficiencies
