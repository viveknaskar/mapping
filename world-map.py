import folium
import pandas

data = pandas.read_csv("volcanoes.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
ele = list(data["ELEV"])

def color_producer(elevation):
    if elevation < 1000:
        return (
            "green"  # if the volcano is less than 1000m, it should be marked as green
        )
    elif 1000 <= elevation < 3000:
        return "orange"  # if the volcano is between 1000m and 3000m, it should be marked as orange
    else:
        return "red"  # if the volcano is more than 3000m, it should be marked as red

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name="Volcanoes of USA")

for lt, ln, el in zip(lat, lon, ele):
    fgv.add_child(
        folium.Marker(
            location=[lt, ln],
            popup=str(el) + "m",
            icon=folium.Icon(color=color_producer(el)),
        )
    )

fgp = folium.FeatureGroup(name="Population of the World")

fgp.add_child(
    folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "orange"
            if 10000000 <= x["properties"]["POP2005"] < 20000000
            else "red"
        },
    )
)

fgc = folium.FeatureGroup(name="Indian Metropolitan Cities")

coordinates_list = [
    [28.6139, 77.209],
    [22.5726, 88.3639],
    [13.0827, 80.2707],
    [19.0760, 72.8777],
]
cities_list = ["New Delhi", "Kolkata", "Chennai", "Mumbai"]

for coordinates, cities in zip(coordinates_list, cities_list):
    fgc.add_child(
        folium.Marker(
            location=coordinates, popup=cities, icon=folium.Icon(color="green")
        )
    )

map.add_child(fgv)
map.add_child(fgp)
map.add_child(fgc)

# Layer Control enables you to choose different features of the map
map.add_child(folium.LayerControl())

map.save("WorldMap.html")