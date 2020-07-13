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
parentdir = "/home/ubuntu/modeling_copied"
sys.path.append(parentdir)
from fit_and_predict import add_preds
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
import plotly.graph_objects as go
import plotly.io as pio
from exponential_modeling import *
from fit_and_predict import *
import plotly
# Function to Train CLEP on your Hospital Data
# Default: 7 Days Prediction
exponential = {'model_type':'exponential'}
shared_exponential = {'model_type':'shared_exponential'}
linear = {'model_type':'linear'}
advanced_model = {'model_type':'advanced_shared_model'}
predictors = [linear, shared_exponential]

##  Generate the plot with prediction results
def generate_plot(d, date, data, k):
    fig = go.Figure()
    r = '179,74,71'
    b = '111,136,190'
    red ='rgb(' + r + ')'
    blue = 'rgb(' + b + ')'
    red_fill = 'rgba(' + r + ',0.4)'
    blue_fill = 'rgba(' + b + ',0.4)'
    new_dates = ['+' +str(i + 1)+' day(s)' for i in range(k)]
    # Add traces
    lower = [x[0] for x in d[3].values[0]]
    upper = [x[1] for x in d[3].values[0]]
    fig.add_trace(go.Scatter(x = date, y = data,
                    mode='lines + markers',
                    name='Data',line_color = blue))
    fig.add_trace(go.Scatter(x = new_dates, y = lower, mode = 'lines', line_color = red_fill, showlegend = False))
    fig.add_trace(go.Scatter(x = new_dates, y = d[2].values[0],
                    mode = 'lines', fill = 'tonexty', fillcolor = red_fill, line_color = red, name = 'Future Prediction'))

    fig.add_trace(go.Scatter(x = new_dates, y = upper, fill = 'tonexty', mode = 'lines', fillcolor = red_fill, line_color = red_fill, showlegend = False))
    
    old_dates = date[-len(d[0]):]
    fig.add_trace(go.Scatter(x = old_dates, y = [x[0] for x in d[1]], mode = 'lines', line_color = blue_fill,showlegend = False))
    fig.add_trace(go.Scatter(x = old_dates, y = d[0], fill = 'tonexty', mode = 'lines', line={'dash': 'dash', 'color': blue}, fillcolor = blue_fill, name = 'Past Prediction'))
    fig.add_trace(go.Scatter(x = old_dates, y = [x[1] for x in d[1]], fill = 'tonexty', mode = 'lines', fillcolor = blue_fill, line_color = blue_fill, showlegend = False))
    fig.update_layout(
        title="Hospitalization prediction",
        xaxis_title="Date",
        yaxis_title="Counts",
        title_font = dict(size = 20),
        font=dict(
            family = "Lora,Helvetica Neue,Helvetica,Arial,sans-serif",
            size=12,
            color="white"
        ),
        template = 'plotly_dark'
    )
    return plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')
    
## Return prediction/prediction intervals and plot
def predict(df, k, output_var = "hospitalizations"):
        
    hospitz = df[output_var].values
        
    df_h = pd.DataFrame({"Hospital": ["Hospital_Name"], "hospitalizations": [hospitz]})
    ## Add prediction and interval for future prediction 
    ## results are saved as "new_predictions" and "prediction_intervals", respectively.
    xx = add_prediction_intervals(df_h, 
                             target_day=np.array(np.array([i + 1 for i in range(k)])),
                             outcome="hospitalizations", 
                             methods=[shared_exponential,linear],
                             interval_type='local',
                             output_key = 'prediction_intervals')
    ## Add past performance in dataframe
    start_day = max(len(df) - 13, 0)
    past_predictions = []
    past_intervals = []
    for i in range(start_day,len(df)-7+1):
        hosp_data = hospitz[:i]
        dicti = {"hosp":["Hospital_Name"],"hospitalizations" : [hosp_data]}
        df_shared = pd.DataFrame(dicti)
        x = add_prediction_intervals(df_shared, 
                             target_day = np.array([k]),
                             outcome = 'hospitalizations', 
                             methods = predictors,
                             interval_type = 'local',
                             output_key = "hospital_intervals")
        past_predictions.append(x['new_predictions'][0][0])
        past_intervals.append(x['hospital_intervals'][0][0])
    d = [past_predictions, past_intervals, xx['new_predictions'], xx['prediction_intervals']]
    fig = generate_plot(d, df[df.columns[0]], hospitz, k)
    return fig, xx['new_predictions'].values[0].tolist(), [(round(x[0],1), round(x[1],1)) for x in xx['prediction_intervals'].values[0]]

    