# pokemon-calendar


#Summary:
Simple python script that will get the pokemon distribution event dates and creates calendar events.

#How it Works: 
Uses requests and beautiful soup to get the dates of pokemon distribution events from http://www.serebii.net/ 
then creates calendar events using python ics library. 

Can run the script using: python pokemon_calendar.py 'region_code'

If no region code provided then defaults to NA. Other codes include JPN(Japan), EU(Europe) ,SK (South Korea), Other

#Why I made this?

After playing the pokemon games on 3DS and putting them away I realized months later that I missed an event where I could have
gotten exclusive pokemon not obtained in the games. I created this so could automate the process of creating calendar events 
to remind me of an upcoming distribution event.

#Requirements:
Python, BeautifulSoup4, requests, ics (http://icspy.readthedocs.io)
