from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from pyrosm import OSM

colours = ["orange", "purple", "green", "navy", "red", "cyan"]

categories = {
    "amenity": ["bar", "bathroom", "cafe", "childcare", "clinic", "fast_food", "internet_cafe",
                "marketplace", "place_of_worship", "pharmacy", "restaurant", "social_facility", "telephone", "toilets"],
    "shop": ["alcohol", "antiques", "bakery", "beverages", "bicycle", "boutique", "cannabis", "car",
             "clothes", "computer", "convenience", "deli", "department_store", "e-cigarette", "electronics", "erotic",
             "florist", "furniture", "funeral_directors", "garden_centre", "general", "greengrocer", "hairdresser", "hardware",
             "health_food", "herbalist", "ice_cream", "jewelry", "money_lender", "music",
             "musical_instrument", "organic", "outdoor", "second_hand", "shoes", "sports",
             "supermarket", "tailor", "travel_agency", "vacant"],
    "tourism": []
}

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/generateMap', methods=['POST'])
def get_image():
    colour_index = 0
    osmOld = OSM("static/mtlold.osm.pbf")
    drive_net = osmOld.get_network(network_type="driving")
    ax = drive_net.plot(color="black", figsize=(12, 12), lw=0.9, alpha=0.15)  # to see what is plotted
    print(request.form)
    for category in categories.keys():
        for poi in categories[category]:
            if poi in request.form.keys():
                custom_filter = {category: [poi]}
                pois = osmOld.get_pois(custom_filter=custom_filter)
                pois["poi_type"] = pois[category]
                ax = pois.plot(ax=ax, color=colours[colour_index % 6], markersize=25, figsize=(12, 12), legend=True, legend_kwds=dict(loc='upper left', ncol=5, bbox_to_anchor=(1, 1)))
                colour_index += 1
    plt.savefig('static/mapOld.png')

    colour_index = 0
    osmNew = OSM("static/mtlnew.osm.pbf")
    drive_net = osmNew.get_network(network_type="driving")
    ax = drive_net.plot(color="black", figsize=(12, 12), lw=0.9, alpha=0.15)  # to see what is plotted
    print(request.form)
    for category in categories.keys():
        for poi in categories[category]:
            if poi in request.form.keys():
                custom_filter = {category: [poi]}
                pois = osmNew.get_pois(custom_filter=custom_filter)
                pois["poi_type"] = pois[category]
                ax = pois.plot(ax=ax, color=colours[colour_index % 6], markersize=25, figsize=(12, 12), legend=True,
                               legend_kwds=dict(loc='upper left', ncol=5, bbox_to_anchor=(1, 1)))
                colour_index += 1
    plt.savefig('static/mapNew.png')
    return index()


if __name__ == '__main__':
    app.run()
