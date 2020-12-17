import urllib.request, urllib.error, urllib.parse, json, openfoodfacts
from flask import Flask, render_template, request

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

# Generates the list of products from the API in English. Accounts for the fact that sometimes products
# aren't given names but still have ingredients in them.

@app.route('/')
def main():
    products = openfoodfacts.products.get_by_language("English")
    foods = []
    for item in products:
        if "product_name" in item:
            foods.append(item["product_name"])
        else:
            foods.append("No product name")

    return render_template("mainpage.html", list = foods)


# Takes the product chosen by the user from the main page and reads through the ingredients

@app.route('/allergenornot', methods = ['POST'])
def allergen():
    item = request.form['food']
    allergen = request.form['allergen']
    products = openfoodfacts.products.get_by_language("English")
    for thing in products:
        if "product_name" in thing:
            if thing["product_name"] == item:
                if "ingredients" in thing:
                    inglist = thing["ingredients"]
                else:
                    inglist = "none" #sometimes there are no ingredients listed for products so this checks for that error

# Creates a dictionary of the ingredients in the product
    ingvalues = []
    for i in inglist:
        ingvalues.append(i)

#Checks for keywords for gluten allergies in products
    if allergen == "Gluten":
        if inglist == "none":
            response = "There are no ingredients available, so we can't check. Sorry!"
        else:
            for word in ingvalues:
                for each in word.values():
                    line = str(each)
                    if "flour" or "wheat" in line.lower():
                        response = "There is gluten in this product"
                    else:
                        response = "There is no gluten in this product"

# Checks for keywords for dairy allergies in products
    if allergen == "Dairy":
        if inglist == "none":
            response = "There are no ingredients available, so we can't check. Sorry!"
        else:
            for word in ingvalues:
                for each in word.values():
                    line = str(each)
                    if "milk" in line.lower():
                        response = "There is dairy in this product"
                    else:
                        response = "There is no dairy in this product"

# Checks for keywords for egg allergies in products
    if allergen == "Eggs":
        if inglist == "none":
            response = "There are no ingredients available, so we can't check. Sorry!"
        else:
            for word in ingvalues:
                for each in word.values():
                    line = str(each)
                    if "egg" in line.lower():
                        response = "There are eggs in this product"
                    else:
                        response = "There are no eggs in this product"




    return render_template("allergenornot.html", food = item, response = response, allergen = allergen, ingredient = ingvalues)



if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

