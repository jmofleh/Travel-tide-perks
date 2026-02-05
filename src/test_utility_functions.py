
import numpy as np
import pandas as pd
from utility_functions import *

def test_discount():
    assert calculate_discount_percentage(np.array([10]),np.array([100]))[0]==10

def test_index():
    assert hotel_hunter_index(5,10)==5/11

print("Tests passed")
