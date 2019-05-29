from bs4 import BeautifulSoup
import subprocess

# this fails
# res = requests.get('https://www.congress.gov/resources/display/content/Most-Viewed+Bills')
# soup = BeautifulSoup(res.content, 'html.parser')
# print(res.content)
# h2s = soup.find('h2')
#
# print(h2s)

# this does work... though is much sketchier and circumvents the robots.txt of the site, seek alternatives
out = subprocess.check_output(['curl','https://www.congress.gov/resources/display/content/Most-Viewed+Bills'])

print(out)
print(out.decode('utf-8'))
soup = BeautifulSoup(out, '')
h2s = soup.find('h2')

print(h2s)