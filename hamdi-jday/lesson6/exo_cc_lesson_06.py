import pandas as pd
import re


aliments = pd.read_csv('aliments.csv', delimiter='\t')
aliments = aliments.set_index('product_name')
# aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True)
# aliments.dropna(subset=['traces'])['traces'].str.split(',', expand=True).to_csv('traces.csv')

# ==> Check cheet_sheet in lesson6
