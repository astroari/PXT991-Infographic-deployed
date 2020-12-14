import pandas as pd     
import datetime as dt

import dash             
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly          
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("testdata1-m.csv")

app = dash.Dash(__name__)


app.layout = html.Div([
    html.Div([
            html.Pre(children= "Radiative forcing Infographic by Arina, Kavian and Mateusz",
            style={"text-align": "center", "font-size":"100%", "color":"black"})
        ]),
    html.Div([
        html.H1("Radiative Forcing")
        ]),
    html.Div([
        html.P("The term 'Radiative Forcing' refers simply to the difference of solar irradiance absorbed by the Earth, compared to how much is radiated back to space. This way a system in thermal equilibrium would have zero radiative forcing. Where solar irradiance is the amount of sun’s energy received per unit area per second with units of Watts per meter squared. A positive radiative forcing means more energy is absorbed by the Earth than reflected back into space, which results in the Earth getting warmer and vice versa. Here we break down radiative forcing into its components often refered to as 'forcing agents', categorising it by the effects responsible.", className="intro"),
        html.P(["Some of the agents are ", html.Span("natural ", style={'color': '#3FA0A0'}), "while others originate from ", html.Span("human ", style={'color': '#bc99e0'}), "activity."], className="agents"),

    ]),
html.Div([
            dcc.Checklist(
                id='my_checklist',                      # used to identify component in callback
                options=[
                         {'label': x, 'value': x, 'disabled':False}
                         for x in df['Source'].unique()
                         ],
                value=['Carbon Dioxide','Methane','Ice/snow Albedo','Solar irradiance' ,'Net total'],    # values chosen by default

                className='my_box_container',           
                style={'display':'flex'},            

                inputClassName='my_box_input',         
                inputStyle={'cursor':'pointer'},      

                labelClassName='my_box_label',        
                
                ),
            #html.Span("Gases consisting of carbon and halogens", className="tooltiptext"),
        ]),

        html.Div([
            dcc.Graph(id='the_graph')
    ]),
   

])

@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_checklist', component_property='value')]
)
def update_graph(options_chosen):

    dff = df[df['Source'].isin(options_chosen)]
    print (dff['Source'].unique())

    fig = go.Figure(go.Waterfall(
    name = "20", orientation = "v",
    measure = dff['Measure'],
    x = dff['Source'],
    textposition = "inside",
    text = dff['Contribution'],
    y = dff['Contribution'],
    increasing = {"marker":{"color":"#8F2738"}},
    decreasing = {"marker":{"color":"#5E8DB0"}},
    totals = {"marker":{"color":"#ffb01f", "line":{"color":"gold", "width":3}}},
    connector = {"line":{"color":"#C0C0C0"}},
    ))
    fig.update_yaxes(visible=True, title_text='W/m<sup>2</sup>')
    return (fig)

'''
def update_graph2(year_chosen):
'''

if __name__ == '__main__':
    app.run_server(debug=True, port=8124)
