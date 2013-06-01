import itertools
import bs4

def parse(html):
    """Parses marctracker.com status.jsp

    Arguments:
        html : page contents

    Return:
        Array of dictionaries
    """
    entries = []

    soup = bs4.BeautifulSoup(html)

    soup = soup.find(id='sublink_table')   # Submenu
    soup = soup.find_next_sibling('table') # Main body
    soup = soup.find_next('tr')            # Menu
    soup = soup.find_next('tr')            # Content

    # one table per (line, direction)
    for table in soup.find_all('table', width="950"):

        # line and direction
        table = table.find_next('td', class_="textStatusLine")
        line, direction = table.text.lower().split()

        # header
        table = table.find_next('tr', class_="textStatusHdr")

        # trains
        for table in table.find_next_siblings('tr', class_="textStatusAll"):
            entry = dict()

            entry['line'] = str(line)
            entry['direction'] = str(direction)

            # unused
            table = table.find_next('td')

            # train number
            table = table.find_next_sibling('td')
            entry['trainNumber'] = str(table.text.strip())

            # next station
            table = table.find_next_sibling('td')
            entry['nextStation'] = str(table.text.lower().strip())

            # estimated departure
            table = table.find_next_sibling('td')
            entry['estimatedDeparture'] = str(table.text.strip())

            # status
            table = table.find_next_sibling('td')
            entry['status'] = str(table.text.lower().strip())

            # delay
            table = table.find_next_sibling('td')
            entry['delay'] = str(table.text.lower().strip())

            # last update
            table = table.find_next_sibling('td')
            entry['lastUpdated'] = str(table.text.strip())

            # message
            table = table.find_next_sibling('td')
            entry['message'] = str(table.text.lower().strip())

            entries.append(entry)

    return entries

if __name__ == '__main__':

    f = open('status.jsp')
    for entry in parse(f.read()):
        print entry

