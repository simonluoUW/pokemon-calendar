import requests,re,sys
from ics import Calendar, Event
from datetime import datetime
from bs4 import BeautifulSoup

'''
contains all information related to pokemon distribution event
'''


class Pokemon:
    def __init__(self):
        self.name = None
        self.description = None
        self.type = None
        self.location = None
        self.start_date = None
        self.end_date = None
        self.games = None

'''
uses current year to get the link to current year events
Returns link to event
'''


def get_events_link():
    now = datetime.now()
    year = now.year

    request = requests.get('http://www.serebii.net/events/')
    soup = BeautifulSoup(request.text, "html.parser")
    soup = soup.find('form', attrs={"name": "yra"})
    soup = soup.find('option',attrs={"value": re.compile('{0}'.format(year))})
    if soup is None:
        return None

    return soup.get('value')

'''
given parsed html soup find relevant pokemon information
input:
    pokemon_soup: parsed html soup for pokemon event
Returns a pokemon obj with all relevant event information
'''


def parse_pokemon(pokemon_soup):
    pokemon_obj = Pokemon()
    first_row = pokemon_soup.find('tr')
    pokemon_obj.name = str(first_row.find('td',class_='label').contents[1])

    second_row = first_row.find_next_sibling('tr')
    description_row = second_row.find('tr').find_next_sibling('tr').find_all('td')
    pokemon_obj.description = str(description_row[0].string)
    pokemon_obj.type = str(description_row[1].string)
    pokemon_obj.location = str(description_row[2].string)

    third_row = second_row.find_next_sibling('tr').find_all('tr')
    dates = third_row[1].find_all('td')
    pokemon_obj.start_date = str(dates[0].string).strip()
    pokemon_obj.end_date = str(dates[1].string).strip()
    pokemon_obj.games = str(third_row[2].find_all('td')[1].string)

    return pokemon_obj

'''
creates an ics event given pokemon obj
input:
    pokemon_obj: contains relevant pokemon information
    datetime_obj: datetime obj for event
    start: boolean True if using start date
Returns event obj
'''


def get_event_from_pokemon(pokemon_obj,datetime_obj,start):
    suffix = 'Begins' if start else 'Ends'

    event = Event()
    event.begin = datetime_obj
    event.name = 'Pokemon Distribution ' + pokemon_obj.name + suffix
    event.description = 'Description:{0}\nType:{1}\nLocation:{2}\nGames:{3}'.\
        format(pokemon_obj.description,pokemon_obj.type,pokemon_obj.location,pokemon_obj.games)

    return event

'''
input:
    time_str: given timestamp as string convert to datetime
Return datetime
'''


def convert_string_to_datetime(time_str):
    try:
        datetime_obj = datetime.strptime(time_str, '%d %B %Y')
    except ValueError:
        try:
            datetime_obj = datetime.strptime(time_str, '%B %Y')
        except ValueError:
            return time_str

    return datetime_obj

'''
creates ics file given region wanted
input:
    region: NA for North America (default)
            JPN for Japan
            Other for Other
            EU for Europe
            SK for South Korea

Outputs ics file
'''


def generate_calendar(region_code='NA'):
    region_code_to_region = {'NA':'america','JPN':'japan','EU':'europe','SK':'southkorea','Other':'others'}

    if region_code in region_code_to_region:
        region = region_code_to_region[region_code]
    else:
        return

    event_link = get_events_link()
    if event_link is None:
        return

    request = requests.get('http://www.serebii.net'+event_link)
    soup = BeautifulSoup(request.text, "html.parser")
    pokemon_iter = soup.find('a',attrs={"name": region}).parent.find_next_sibling(['p','table'])

    calendar = Calendar()
    now = datetime.now()
    now = datetime(now.year,now.month,now.day)

    while pokemon_iter.name != 'p':
        pokemon_obj = parse_pokemon(pokemon_iter)
        start_date_obj = convert_string_to_datetime(pokemon_obj.start_date)
        end_date_obj = convert_string_to_datetime(pokemon_obj.end_date)

        if pokemon_obj.end_date == 'No End Date' or now <= end_date_obj:
            if pokemon_obj.end_date != 'No End Date':
                event = get_event_from_pokemon(pokemon_obj,end_date_obj,False)
                calendar.events.append(event)

            if now >= start_date_obj:
                start_date_obj = now

            event = get_event_from_pokemon(pokemon_obj,start_date_obj,True)
            calendar.events.append(event)

        pokemon_iter = pokemon_iter.find_next_sibling(['table','p'])

    with open('pokemon_calendar.ics', 'w') as f:
        f.writelines(calendar)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_calendar(sys.argv[1])
    else:
        generate_calendar()
