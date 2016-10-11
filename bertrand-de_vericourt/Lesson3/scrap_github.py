
# Import packages & initialize variables
import requests
from bs4 import BeautifulSoup

url = 'https://gist.github.com/paulmillr/2657075'
page_developers = requests.get(url)
soup = BeautifulSoup(page_developers.text, 'html.parser')
soup.prettify()
devs = soup.select('tbody tr')


# Loop over 256 developers of the table body
for idx, dev in enumerate(devs[:256]):
  try:
    print(dev.select('td:nth-of-type(1)')[0].text + ' : ' + str(idx+1))
  except Exception as e:
    print(str(e) + '    ####################################################################')
    print('error caused by : ' + str(dev.select('td:nth-of-type(1)')))