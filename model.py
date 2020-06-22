## Imports
## NOTE: GOING TO HARDCODE THE PATH FOR THE TIME BEING, MUST BE CHANGED AS NEEDED
import numpy as np
import pandas as pd
from os.path import join as oj
import os
import pandas as pd
import sys
import inspect
import datetime
from scipy.stats import percentileofscore
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
parentdir = "/home/ubuntu/new_uploader"
sys.path.append(parentdir)
sys.path.append(parentdir + '/modeling')
import load_data
from fit_and_predict import add_preds
from functions import merge_data
from viz import  viz_interactive
import numpy as np
import pandas as pd
from os.path import join as oj
import os
import pandas as pd
import sys
import matplotlib as plt
from scipy.stats import percentileofscore
from sklearn.metrics import mean_absolute_error
import statsmodels.api as sm


# CHANGE THIS
from exponential_modeling import *
from fit_and_predict import *



# Function to Train CLEP on your Hospital Data
# Default: 7 Days Prediction
exponential = {'model_type':'exponential'}
shared_exponential = {'model_type':'shared_exponential'}
linear = {'model_type':'linear'}
advanced_model = {'model_type':'advanced_shared_model'}

def predict_kth_day(df, k, output_var = "hospitalizations"):
        
    hospitz = df[output_var].values
        
    df_h = pd.DataFrame({"Hospital": ["Hospital_Name"], "hospitalizations": [hospitz]})

    ensemble_prediction = fit_and_predict_ensemble(df_h,target_day = np.array([k]),
                outcome = 'hospitalizations', 
                methods = [shared_exponential,linear],
                mode = 'predict_future', 
                verbose = False)['predicted_hospitalizations_ensemble_' + str(k)].values
    
    ensemble_prediction = [max(x[0], 0) for x in ensemble_prediction]
    
    return round(ensemble_prediction[0], 2)
    

def predict(df, output_var = ['hospitalizations'],k = 7):
    return [[predict_kth_day(df, i, c) for i in range(1,k+1)] for c in output_var]