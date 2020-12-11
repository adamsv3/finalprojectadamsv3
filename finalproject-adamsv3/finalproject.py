import urllib.request, urllib.error, urllib.parse, json, openfoodfacts
from flask import Flask, render_template, request

app = Flask(__name__)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

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


            # products = openfoodfacts.products.get_by_language("French")
            # if "ingredients" in products[0]:
            #     inglist = products[0]["ingredients"]
            #
            # values = []
            # for i in inglist:
            #     values.append(i.values())
            #
            # for d in values:
            #     for item in d:
            #         if "tomato" in str(item):
            #             print('yes')


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
                    inglist = "none"

    ingvalues = []
    for i in inglist:
        ingvalues.append(i)

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

    if allergen == "Vegan":
        if inglist == "none":
            response = "There are no ingredients available, so we can't check. Sorry!"
        else:
            if "vegan" in inglist:
                if inglist["vegan"] == "no":
                    response = "This product is not vegan"
                else:
                    response = "This product is vegan"
            elif "vegan" not in inglist:
                response = "Not sure if vegan"



    return render_template("allergenornot.html", food = item, response = response, allergen = allergen, ingredient = ingvalues)



if __name__ == "__main__":
    # Used when running locally only.
    # When deploying to Google AppEngine, a webserver process will serve your app
    app.run(host="localhost", port=8080, debug=True)

# idek = [{'text': 'Farine de riz', 'vegan': 'yes', 'percent': 24, 'percent_estimate': 24, 'percent_min': 24, 'percent_max': 24, 'id': 'en:rice-flour', 'rank': 1, 'vegetarian': 'yes'}, {'percent_estimate': '16.2222222222222', 'text': 'huiles végétales', 'vegan': 'yes', 'from_palm_oil': 'maybe', 'rank': 2, 'vegetarian': 'yes', 'percent_max': 24, 'id': 'en:vegetable-oil', 'has_sub_ingredients': 'yes', 'percent_min': '8.44444444444444'}, {'vegan': 'yes', 'text': 'pommes de terre déshydratées', 'percent_estimate': '15.25', 'percent_max': 24, 'id': 'en:potato-powder', 'rank': 3, 'vegetarian': 'yes', 'percent_min': '6.5'}, {'percent_estimate': 14, 'vegan': 'yes', 'text': 'farine de mais', 'percent_min': 4, 'rank': 4, 'vegetarian': 'yes', 'percent_max': 24, 'id': 'en:corn-flour'}, {'vegan': 'yes', 'text': 'amidon de riz modifié', 'percent_estimate': '10.3333333333333', 'id': 'en:modified-rice-starch', 'percent_max': 20, 'vegetarian': 'yes', 'rank': 5, 'percent_min': '0.666666666666667'}, {'percent_estimate': '7.86111111111111', 'text': 'assaisonnement gout poulet tikka masala', 'percent_min': 0, 'rank': 6, 'percent_max': '15.7222222222222', 'id': 'fr:assaisonnement gout poulet tikka masala', 'has_sub_ingredients': 'yes'}, {'text': 'maltodextrine', 'vegan': 'yes', 'percent_estimate': '6.16666666666666', 'percent_max': '12.5777777777778', 'id': 'en:maltodextrins', 'rank': 7, 'vegetarian': 'yes', 'percent_min': 0}, {'rank': 8, 'percent_max': '10.4814814814815', 'id': 'en:emulsifier', 'has_sub_ingredients': 'yes', 'percent_min': 0, 'percent_estimate': '3.08333333333333', 'text': 'émulsifiant'}, {'percent_min': 0, 'percent_max': '8.98412698412698', 'id': 'en:wheat-starch', 'rank': 9, 'vegetarian': 'yes', 'text': 'amidon de BLE', 'vegan': 'yes', 'percent_estimate': '1.54166666666666'}, {'id': 'en:salt', 'percent_max': '7.86111111111111', 'vegetarian': 'yes', 'rank': 10, 'percent_min': 0, 'text': 'sel', 'vegan': 'yes', 'percent_estimate': '1.54166666666666'}, {'percent_min': '4.22222222222222', 'id': 'en:sunflower', 'vegan': 'yes', 'text': 'tournesol', 'percent_max': 24, 'percent_estimate': '10.2222222222222', 'vegetarian': 'yes'}, {'percent_min': 0, 'percent_estimate': 6, 'vegetarian': 'yes', 'percent_max': 12, 'text': 'mais', 'vegan': 'yes', 'id': 'en:corn'}, {'vegan': 'yes', 'text': 'sucre', 'id': 'en:sugar', 'percent_max': '15.7222222222222', 'percent_estimate': '3.93055555555556', 'vegetarian': 'yes', 'percent_min': 0}, {'percent_min': 0, 'percent_estimate': '1.96527777777778', 'id': 'fr:lactose en poudre LAIT', 'text': 'lactose en poudre LAIT', 'percent_max': '7.86111111111111'}, {'percent_estimate': '0.982638888888889', 'percent_max': '5.24074074074074', 'text': 'exhausteurs de gout églutamate monosodique', 'id': 'fr:exhausteurs de gout églutamate monosodique', 'percent_min': 0}, {'percent_max': '3.93055555555556', 'id': 'en:e635', 'text': "5'-ribonucléotide disodique", 'vegan': 'maybe', 'percent_estimate': '0.491319444444444', 'vegetarian': 'maybe', 'percent_min': 0}, {'percent_min': 0, 'text': 'sel', 'vegan': 'yes', 'id': 'en:salt', 'percent_max': '3.14444444444444', 'vegetarian': 'yes', 'percent_estimate': '0.245659722222222'}, {'vegetarian': 'yes', 'percent_estimate': '0.122829861111111', 'vegan': 'yes', 'text': 'maltodextrine', 'id': 'en:maltodextrins', 'percent_max': '2.62037037037037', 'percent_min': 0}, {'percent_min': 0, 'percent_estimate': '0.0614149305555558', 'id': 'fr:épices égraines de coriandre', 'text': 'épices égraines de coriandre', 'percent_max': '2.24603174603175'}, {'percent_min': 0, 'percent_estimate': '0.0307074652777781', 'vegetarian': 'yes', 'id': 'en:ginger-powder', 'text': 'gingembre moulu', 'vegan': 'yes', 'percent_max': '1.96527777777778'}, {'vegetarian': 'yes', 'percent_estimate': '0.0153537326388888', 'id': 'en:cumin-seeds', 'vegan': 'yes', 'text': 'cumin', 'percent_max': '1.74691358024691', 'percent_min': 0}, {'percent_min': 0, 'vegetarian': 'yes', 'percent_estimate': '0.0076768663194442', 'text': 'piment de cayenne', 'vegan': 'yes', 'id': 'en:cayenne-pepper', 'percent_max': '1.57222222222222'}, {'text': 'curcuma', 'vegan': 'yes', 'id': 'en:turmeric', 'percent_max': '1.42929292929293', 'percent_estimate': '0.00383843315972188', 'vegetarian': 'yes', 'percent_min': 0}, {'vegetarian': 'yes', 'percent_estimate': '0.00191921657986116', 'text': 'cannelle moulue', 'vegan': 'yes', 'id': 'en:cinnamon-powder', 'percent_max': '1.31018518518519', 'percent_min': 0}, {'percent_min': 0, 'vegetarian': 'yes', 'percent_estimate': '0.000959608289930802', 'id': 'en:clove', 'text': 'clous de girofle', 'vegan': 'yes', 'percent_max': '1.20940170940171'}, {'processing': 'en:ground', 'percent_estimate': '0.000479804144965623', 'vegan': 'yes', 'text': 'graines de fenugrec', 'percent_min': 0, 'vegetarian': 'yes', 'id': 'en:fenugreek-seed', 'percent_max': '1.12301587301587'}, {'percent_max': '1.04814814814815', 'vegan': 'yes', 'text': 'cardamone', 'id': 'en:cardamom', 'vegetarian': 'yes', 'percent_estimate': '0.00023990207248259', 'percent_min': 0}, {'percent_max': '0.982638888888889', 'id': 'en:black-pepper', 'vegan': 'yes', 'text': 'poivre noir', 'percent_estimate': '0.000119951036241073', 'vegetarian': 'yes', 'percent_min': 0}, {'vegetarian': 'yes', 'percent_estimate': '5.99755181203143e-05', 'id': 'en:onion-powder', 'vegan': 'yes', 'text': 'oignon en poudre', 'percent_max': '0.92483660130719', 'percent_min': 0}, {'percent_estimate': '2.99877590603792e-05', 'vegetarian': 'yes', 'vegan': 'yes', 'text': 'dextrose', 'id': 'en:dextrose', 'percent_max': '0.873456790123457', 'percent_min': 0}, {'vegetarian': 'yes', 'percent_estimate': '1.49938795304116e-05', 'percent_max': '0.873456790123457', 'id': 'en:tomato-powder', 'text': 'tomate en poudre', 'vegan': 'yes', 'percent_min': 0}, {'percent_min': 0, 'percent_max': '0.786111111111111', 'vegan': 'yes', 'id': 'en:garlic-powder', 'text': 'ail en poudre', 'vegetarian': 'yes', 'percent_estimate': '7.49693976542787e-06'}, {'vegetarian': 'yes', 'percent_max': '0.748677248677249', 'id': 'en:cream-powder', 'has_sub_ingredients': 'yes', 'percent_min': 0, 'percent_estimate': '3.74846988249189e-06', 'vegan': 'no', 'text': 'crème en poudre'}, {'percent_min': 0, 'percent_estimate': '1.8742349410239e-06', 'text': "correcteurs d'acidité acide citrique", 'id': "fr:correcteurs d'acidité acide citrique", 'percent_max': '0.748677248677249'}, {'percent_max': '0.683574879227053', 'text': 'acide lactique', 'id': 'en:e270', 'vegan': 'yes', 'vegetarian': 'yes', 'percent_estimate': '9.37117470289905e-07', 'percent_min': 0}, {'vegan': 'no', 'text': 'lactosérum en poudre', 'percent_estimate': '4.68558735366997e-07', 'percent_max': '0.655092592592593', 'has_sub_ingredients': 'yes', 'id': 'en:whey-powder', 'vegetarian': 'maybe', 'percent_min': 0}, {'percent_min': 0, 'vegetarian': 'maybe', 'percent_estimate': '2.34279367905543e-07', 'vegan': 'maybe', 'id': 'en:flavouring', 'text': 'aromes', 'percent_max': '0.655092592592593'}, {'percent_min': 0, 'percent_estimate': '1.17139684174816e-07', 'vegetarian': 'yes', 'id': 'en:yeast-extract', 'vegan': 'yes', 'text': 'extrait de levure', 'percent_max': '0.655092592592593'}, {'percent_estimate': '5.85698418653635e-08', 'vegetarian': 'yes', 'percent_max': '0.582304526748971', 'text': 'LAIT écrémé en poudre', 'id': 'en:skimmed-milk-powder', 'vegan': 'no', 'percent_min': 0}, {'percent_min': 0, 'percent_estimate': '5.85698414212743e-08', 'percent_max': '0.561507936507937', 'id': 'en:colour', 'has_sub_ingredients': 'yes', 'text': 'colorant'}, {'vegetarian': 'maybe', 'id': 'en:e471', 'percent_max': '10.4814814814815', 'percent_min': 0, 'percent_estimate': '3.08333333333333', 'vegan': 'maybe', 'text': 'e471', 'from_palm_oil': 'maybe'}, {'percent_min': 0, 'vegetarian': 'yes', 'percent_estimate': '3.74846988249189e-06', 'id': 'en:milk', 'vegan': 'no', 'text': 'LAIT', 'percent_max': '0.748677248677249'}, {'vegetarian': 'yes', 'percent_estimate': '4.68558735366997e-07', 'percent_max': '0.655092592592593', 'text': 'LAIT', 'vegan': 'no', 'id': 'en:milk', 'percent_min': 0}, {'percent_min': 0, 'text': 'extrait de paprika', 'vegan': 'yes', 'id': 'en:e160c', 'percent_max': '0.561507936507937', 'vegetarian': 'yes', 'percent_estimate': '5.85698414212743e-08'}]
#
# for word in idek:
#     for each in word.values():
#         line = str(each)
#         if "milk" in line.lower():
#             print("yes")

#
# products = openfoodfacts.products.get_by_language("English")
# item = "Rice Fusion Indian Chicken Tikka Masala"
# for thing in products:
#     if "product_name" in thing:
#         if thing["product_name"] == item:
#             if "ingredients" in thing:
#                 inglist = thing["ingredients"]
#             else:
#                 inglist = "none"
#
# print(inglist)
