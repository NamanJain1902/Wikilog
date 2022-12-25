
import requests as r
from bs4 import BeautifulSoup as soup
import re


def get_flag_link(soupObj):
    """Extracts src attrubute from Flag img tag and
    returns in the required format.

    Parameters:
        Soup object
    
    Returns:
        Link to svg file of flag.

    Why get(src) over ['src] in extracting src attribute from img tag?
        get() method to safely get the attribute out of the element.
        The method returns the attribute value if it’s found, and 
        None value otherwise.
    """
    flag_tag_link = soupObj.find("a", {"class": "image"})
    flag_url = flag_tag_link.find('img').get('src') 
    flag_url = re.sub("/thumb", "", flag_url)
    flag_url = "/".join(flag_url.split('/')[:-1])
    flag_link = f"https:{flag_url}"
    return flag_link


def fix_format(l):
    if len(l) < 2:
        l = "".join(l)
    return l


def fetchData(country):

    url = f"https://en.wikipedia.org/wiki/{country}"
    html = r.get(url)
    content = html.content
    s = soup(content, "html.parser")


    table  = s.find('table')
    all_th = table.find_all('th')
    all_tr = table.find_all('tr')


    largest_cities = []
    capitals = []
    official_languages = []

    for idx, row in enumerate(all_tr, start=1):

        l = list(row.children)
        headers = l[0].text.lower().strip()

        if "capital" in headers:
            all_a = l[1].find_all('a')
            for a in all_a:
                t = a.attrs.get('title')
                if t is not None:
                    capitals.append(t)

        elif "largest city" in headers:
            for item in list(l[1].children):            
                cities = item.find_all('a')
                if cities is not None:
                    for city in cities:
                        t = city.attrs.get('title')
                        if t is not None:
                            largest_cities.append(t)

        elif "official languages" in headers:
            print("official_languages")
            all_a = l[1].find_all('a')
            for a in all_a:
                t = a.attrs.get('title')
                if t is not None:
                    official_languages.append(t)


        elif "gdp" in headers and "nominal" in headers:
            ll = list(all_tr[idx].children)
            for item in list(ll[1].children):            
                if '$' in item.text:
                    GDP_nominal = item.text.strip()
                    break

        elif "population" in headers:
            ll = list(all_tr[idx].children)
            for item in list(ll[1].children):            
                popu = item.text
                popu = popu.split()
                popu = ",".join(popu)
                Population = popu
                break

        elif "area" in headers:
            ll = list(all_tr[idx].children)
            for item in list(ll[1].children):            
                area = item.text
                area = re.findall('\d+', area)
                area = ''.join(area)
                break



    
    d = {}
    d["flag_link"]    = get_flag_link(s)
    d["capital"]      = fix_format(capitals)
    d["largest_city"] = fix_format(largest_cities)
    d["official_languages"] = official_languages
    d["area_total"] = area
    d["Population"]   = Population
    d["GDP_nominal"]  = GDP_nominal


    return d