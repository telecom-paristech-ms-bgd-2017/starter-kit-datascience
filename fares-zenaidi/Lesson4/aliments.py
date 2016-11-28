import pandas as pd

# Load data
# url = 'https://github.com/telecom-paristech-ms-bgd-2017/starter-kit-datascience/blob/master/Lessons-Exercices/Lesson4/aliments.csv'
# u_cols = ['mpg', 'cylinders', 'displacement', 'horsepower',
#          'weight', 'acceleration', 'model year', 'origin', 'car name']

path = '~/Desktop/aliments.csv'
# for this dataset na_values are marked as NA.
cols = "   code	url	creator	created_t	created_datetime	last_modified_t	last_modified_datetime	product_name \
           generic_name quantity	packaging	packaging_tags	brands	brands_tags	categories	categories_tags  \
           categories_fr	origins	origins_tags	manufacturing_places	manufacturing_places_tags	labels	labels_tags	labels_fr \
           emb_codes	emb_codes_tags	first_packaging_code_geo	cities	cities_tags	purchase_places	stores	countries \
           countries_tags	countries_fr	ingredients_text	traces	traces_tags	serving_size	no_nutriments	additives_n \
           additives	additives_tags	ingredients_from_palm_oil_n	ingredients_from_palm_oil	ingredients_from_palm_oil_tags \
           ingredients_that_may_be_from_palm_oil_n	ingredients_that_may_be_from_palm_oil	\
           ingredients_that_may_be_from_palm_oil_tags	nutrition_grade_fr	main_category	main_category_fr	image_url \
           image_small_url	energy_100g	proteins_100g	casein_100g	serum-proteins_100g	nucleotides_100g	carbohydrates_100g	\
           sugars_100g	sucrose_100g	glucose_100g	fructose_100g	lactose_100g	maltose_100g	maltodextrins_100g	\
           starch_100g	polyols_100g	fat_100g	saturated-fat_100g	butyric-acid_100g	caproic-acid_100g	caprylic-acid_100g \
           capric-acid_100g	lauric-acid_100g	myristic-acid_100g	palmitic-acid_100g	stearic-acid_100g	arachidic-acid_100g \
           behenic-acid_100g	lignoceric-acid_100g	cerotic-acid_100g	montanic-acid_100g	melissic-acid_100g	\
           monounsaturated-fat_100g	polyunsaturated-fat_100g	omega-3-fat_100g	alpha-linolenic-acid_100g	\
           eicosapentaenoic-acid_100g	docosahexaenoic-acid_100g	omega-6-fat_100g	linoleic-acid_100g	arachidonic-acid_100g	\
           gamma-linolenic-acid_100g	dihomo-gamma-linolenic-acid_100g	omega-9-fat_100g	oleic-acid_100g	elaidic-acid_100g	\
           gondoic-acid_100g	mead-acid_100g	erucic-acid_100g	nervonic-acid_100g	trans-fat_100g	cholesterol_100g	\
           fiber_100g	sodium_100g	alcohol_100g	vitamin-a_100g	vitamin-d_100g	vitamin-e_100g	vitamin-k_100g	vitamin-c_100g \
           vitamin-b1_100g	vitamin-b2_100g	vitamin-pp_100g	vitamin-b6_100g	vitamin-b9_100g	vitamin-b12_100g	biotin_100g \
           pantothenic-acid_100g	silica_100g	bicarbonate_100g	potassium_100g	chloride_100g	calcium_100g	phosphorus_100g	\
           iron_100g	magnesium_100g	zinc_100g	copper_100g	manganese_100g	fluoride_100g	selenium_100g	chromium_100g \
           molybdenum_100g	iodine_100g	caffeine_100g	taurine_100g	ph_100g	fruits-vegetables-nuts_100g	carbon-footprint_100g \
           nutrition-score-fr_100g	nutrition-score-uk_100g"

# res = '" "'.join(cols.split('\t'))
# print(res)
aliments = pd.read_csv(filepath_or_buffer=path, sep='\t', encoding='utf-8', )
aliments.set_index('product_name')
# print(aliments.columns)  # Columns
# print(data.columns[0:20])

aliments_with_packaging = aliments['packaging'].dropna().value_counts() > 30
packaging_to_keep = aliments_with_packaging[aliments_with_packaging]  # Filtrer
# print(packaging_to_keep.shape)

print(aliments.shape)
aliments_with_traces = aliments.dropna(subset=['traces'])
print(aliments_with_traces.shape)

print(aliments[u'sugars_100g'].dropna().value_counts())
# isin

#print(data.head)


# Jeu de données numéro 1: densité de médecins (DREES)
# Directement par départements, spécialité
# Jeu de données numéro 2: remboursement de données (GitHub)
# Skip rows, encoding = "latin-1": afficher les accents,
# remplacer les e accent aigu avec le sans accent
# MELT
# Changer le type: astype
# Table de correspondance. str.replace()
# Merge: créer une colonne key
# df[df['x'].isin(['', ''])
# plotly à voir (dictionnaire python à configurer)
#