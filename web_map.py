from geopy.geocoders import Nominatim
import folium


def read_location():

    """
    () -> (list)
    Returns from the file the list that consists of year, name of film and
    the place where it was filmed.

    >>>read_location()
    e.g.
    ['2006', '1 Single', 'Los Angeles, California, USA']
    ['2006', '1 Single', 'New York City, New York, USA']
    ['2017', '2WheelzNHeelz', 'Nashville, Tennessee, USA']
    ['2014', 'ATown', 'Town Lake, Austin, Texas, USA']
    ['2014', 'ATown', 'Texas Rowing Center, Austin, Texas, USA']
    ['2014', 'ATown', 'Mount Bonnell, Austin, Texas, USA']
    ['2014', 'ATown', 'Alamo Drafthouse Ritz, Austin, Texas, USA']
    ['2014', 'ATown', "Red's Porch, Austin, Texas, USA"]
    ['2014', 'ATown', 'Barton Springs, Austin, Texas, USA']
    ['2016', 'ActorsLife', 'New York City, New York, USA']
    """
    films_info = []
    with open('locations.list', encoding='utf-8', errors='ignore') as f:

        for i, line in enumerate(f):
            try:
                if i >= 14:
                    name_otherinfo = line.strip().split('"')
                    if name_otherinfo[2][8] != "{":
                        name = name_otherinfo[1][1:]
                        year = name_otherinfo[2][2:6]
                        loc = name_otherinfo[2].split("\t")
                        if loc[-1][0] != "(":
                            locations = loc[-1]
                        else:
                            locations = loc[-2]
                        films_info.append([year, name, locations])
            except:
                pass

    return films_info


def find_location():
    """

    () -> (list)
    Returns the same list as in the previous function but with the latitude
    and longitude(coordinates).

    >>>find_location()
    e.g
    ['2006', '1 Single', 'Los Angeles, California, USA', [34.0536834, -118.2427669]]
    ['2006', '1 Single', 'New York City, New York, USA', [40.7308619, -73.9871558]]
    ['2017', '2WheelzNHeelz', 'Nashville, Tennessee, USA', [36.1622296, -86.7743531]]
    ['2014', 'ATown', 'Town Lake, Austin, Texas, USA', [30.2507651, -97.7136153]]
    ['2014', 'ATown', 'Texas Rowing Center, Austin, Texas, USA', [30.27213615, -97.7688868111702]]
    ['2014', 'ATown', 'Mount Bonnell, Austin, Texas, USA', [30.3207674, -97.7733474]]
    ['2014', 'ATown', 'Alamo Drafthouse Ritz, Austin, Texas, USA', [30.267301, -97.7396232]]
    ['2014', 'ATown', "Red's Porch, Austin, Texas, USA", [30.240283, -97.7887279]]
    ['2014', 'ATown', 'Barton Springs, Austin, Texas, USA', [30.2020961, -97.6700119]]
    ['2016', 'ActorsLife', 'New York City, New York, USA', [40.7308619, -73.9871558]]
    """
    locs = read_location()
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    for loc in locs:
        try:
            location = geolocator.geocode(loc[2])
            loc.append([location.latitude, location.longitude])
        except:
            pass
    return locs


def films(year):
    """

    (int) -> map
    Returns the map with names of films that are marked in the places where
    they were filmed.
    """
    film_locations = find_location()

    fg = folium.FeatureGroup(name="Films map")
    for loc in film_locations:
        if len(loc) == 4 and str(year) == loc[0]:
            fg.add_child(folium.Marker(location=loc[3], popup=loc[1], icon=folium.Icon()))
    return fg


def popul():
    """

    () -> map
    Returns the map that is coloured by its number of population.
    """
    fg_pp = folium.FeatureGroup(name="Population")
    fg_pp.add_child(folium.GeoJson(data=open('world.json', 'r',
                    encoding='utf-8-sig').read(),
                    style_function=lambda x: {'fillColor':'green'
      if x['properties']['POP2005'] < 10000000
      else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
      else 'red'}))
    return fg_pp


map = folium.Map(location=[36.7014631, -118.7559974], zoom_start=10)


if __name__ == "__main__":
    try:
        year = input("year: ")
        map.add_child(films(year))
        map.add_child(popul())
        map.add_child(folium.LayerControl())
        map.save('Map_with_films.html')
    except:
        print("write the correct year")
