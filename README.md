# Final Project for Social Networks (NYU), Herbert Li

## Thanks to...
- OpenSecrets.org and the Center for Responsive Politics (donation data)
- govtrack.us (voting data)

## Hypothesis:
Can the political spectrum of US Senators be modeled through a network created by relationships between senator and senator

## Methodology:
Networks created from voting trends and bill cosponsorship are too dense and too connected,
see http://www.slate.com/articles/news_and_politics/politics/2009/04/the_senate_social_network.html
and http://jhfowler.ucsd.edu/legislative_cosponsorship_networks.pdf

Instead, let's create a network based on the donations senators have received from certain industries,
where Senator A ~ Senator B if they have received significant donations from x% of the same industries,
x is some threshold value

## Directory Overview:
- money_data/ - contains donation data for each senator (current congress)
- vote_data/ - contains voting data for the current congress
- **get_stats.py** - statistics for the graph
- **industry.html** - open in a browser to see data visualization of donation network
- main.js - misc. file for scraping data
- mgraph.json - graph representation of donation network
- read_data.py - converts raw data in money_data and vote_data into something nicer
- senators.json - list of parties and senators
- vgraph.json - graph representation of network created by voting trends
- **voting.html** - open in a browser to see data visualization of network created by voting trends

**Bolded** files are probably the more interesting ones to look at

Usage:
- industry.html/voting.html: open in a browser and play around with it
- get_stats.py: in a shell

> python3 get_stats.py

To get graph statistics for voting/donation network using a user-specified threshold
