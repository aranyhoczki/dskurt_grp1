# Receptek

## forrás adatok

### allrecipes.com
Egy szkript segítségével le scraper-eltem a recepteket.

A kimeneti forma ndjson (= egy sor egy json rekord)

### szkript

A szkript: get_recipies.py

Kell hozzá:
pip install ndjson, wget, recipe_scrapers

### kiment : ndjson 
Ilyen formában vannak a receptek:
```
{
    "url": "https://www.allrecipes.com/recipe/213700/enchiladas-verdes/",
    "baseurl": "https://www.allrecipes.com/recipes/1470/world-cuisine/latin-american/mexican/authentic/",
    "cuisine": "mexican",
    "ingredients": [
        "2 cloves garlic",
        "3 serrano peppers",
        "2 \u00bc pounds small green tomatillos, husks removed",
        "1 cup vegetable oil for frying",
        "9 corn tortillas",
        "3 cups water",
        "4 teaspoons chicken bouillon granules",
        "\u00bd store-bought rotisserie chicken, meat removed and shredded",
        "\u00bc head iceberg lettuce, shredded",
        "1 cup cilantro leaves",
        "1 (8 ounce) container Mexican crema, crema fresca",
        "1 cup grated cotija cheese"
    ],
    "title": "Enchiladas Verdes",
    "instructions": "Step 1 Cover a large griddle with aluminum foil and preheat to medium-high. Advertisement\nStep 2 Cook the garlic, serrano peppers, and tomatillos on the hot griddle until toasted and blackened, turning occasionally, about 5 minutes for the garlic, 10 minutes for the peppers, and 15 minutes for the tomatillos. Remove to a bowl and allow to cool.\nStep 3 Heat oil in a small, deep skillet to 350 degrees F (175 degrees C). Using kitchen tongs, fry the tortillas individually, turning them once. They shouldn't be in the hot oil for more than 5 seconds per side. Remove excess oil with paper towels and keep warm. Remember that the hotter the oil, the less that the tortillas will absorb.\nStep 4 Place the toasted garlic, serrano peppers, tomatillos, and the water in a blender and blend until smooth; pour into a saucepan over medium heat and bring to a boil. Dissolve the chicken bouillon into the mixture, reduce heat to medium-low, and cook at a simmer until slightly thickened, about 10 minutes. The sauce shouldn't be too thick.\nStep 5 Soak three tortillas in the sauce, one at a time, for a few seconds, fill them with shredded chicken, sprinkle the meat with some of the sauce, roll them and place them seam side down on a pasta bowl. Spoon a generous amount of sauce over them and top them with lettuce, cilantro, crema, and cotija cheese. Pour a little more sauce over the whole thing if desired. Repeat the procedure twice more. Serve immediately.",
    "total_time": 60
}
```

## data preparation
### Összetevők
1) Ahhoz, hogy az összetevőkből a recepet meg tudjuk találni, szükség van egy 'ismert összetevők' listára.
Pl:
```
ismert összetevők = ['peppers', 'garlic', 'oil', 'vegetable oil', 'water' ... ]
```
Itt majd érdekes lesz az 'oil' és 'vegetable oil' kérdése, de ezt majd az összetevők keresésében oldjuk meg

2) Az ismert összetevők előfordulását fogjuk keresni a recept összetevők szövegeiben.
Tehát 
```
{
...
    "ingredients": [
        "2 cloves garlic",
        "3 serrano peppers",
        "1 cup grated cotija cheese"
    ],
    "title": "Enchiladas Verdes",
    ...
}
```
Ebből annak kellene kiesnie, hogy
```
{
"Enchiladas Verdes" : ['garlic', 'peppers', 'cheese']
...
}
```
Ezzel meglenne, hogy milyen recept milyen ismert összetevőket tartalmaz
Itt figyelni kellene, hogy:
ha 'vegetable oil' -t  tartalmaz egy összetevő, akkor ne legyen 'oil' + 'vegetable oil' is benne.

3) Az ajánló motor az alap összetevők alapján kikeresi azokat a recepteket, amelyekben a legtöbb összetevő megtalálható
...


### Recept adatbázis
Az eredeti recept adatbázisban láthatóan több helyen (jellemzően a mennyiségeknél) az unicode használat miatt kódok vannak. Ezeket nice-to-have lenne javítani.
Ez azért kellene, mert terv szerint visszaküljük a recepet valamilyen formában (pl. email) ami nem olyan szép, ha ilyet tartalmaz

u00bc
Tehát pl::
```
        "2 \u00bc pounds small green tomatillos, husks removed",
```
helyett
```
        "2 1/4 pounds small green tomatillos, husks removed",
```






