# -*- coding: utf8 -*-
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import re
import pdb

insee1 = pd.read_csv('/Users/mayliscotadze/starter-kit-datascience/maylis-cotadze/Lesson5/base-cc-evol-struct-pop-2011.csv',encoding = "ISO-8859-1")
insee2 = pd.read_csv('/Users/mayliscotadze/starter-kit-datascience/maylis-cotadze/Lesson5/base-cc-rev-fisc-loc-menage-10.csv',encoding = "ISO-8859-1")
