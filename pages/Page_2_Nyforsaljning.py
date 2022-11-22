import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_prototype_data():
    df = pd.read_excel('Pages/Page_2_data.xlsx')
    df['YEAR'] = df['YEAR'].astype(str)
    return df


df_ = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="Nyförsäljning", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_x",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_nyfors', children=[]),
    html.Br(),

    dcc.Graph(id='line_nyfors', figure={}),
    html.Br(),

    dcc.Graph(id='bar_nyfors', figure={}),
    html.Br(),

    dcc.Dropdown(id='slct_prod_x',
                 options=[
                     {'label': 'Fritid', 'value': 'FRITID'},
                     {'label': 'Direkt/Lev', 'value': 'DIREKT/LEV'},
                     {'label': 'Maskinfinans', 'value': 'MASKINFINANS'},
                     {'label': 'Partner Företag', 'value': 'PARTNER FÖRETAG'},
                     {'label': 'Bil', 'value': 'BIL'},
                     {'label': 'Bil Kund', 'value': 'BILKUND'}
                 ]),

    dcc.Graph(id='pie_nyfors_one', figure={}),
    html.Br(),

    dcc.Graph(id='line_nyfors_vikt_pd', figure={}),
    html.Br(),

    dcc.Graph(id='line_nyfors_vikt_el', figure={})
    ]),


@callback(
    [Output(component_id='output_container_nyfors', component_property='children'),
     Output(component_id='line_nyfors', component_property='figure'),
     Output(component_id='bar_nyfors', component_property='figure'),
     Output(component_id='pie_nyfors_one', component_property='figure'),
     Output(component_id='line_nyfors_vikt_pd', component_property='figure'),
     Output(component_id='line_nyfors_vikt_el', component_property='figure')],
    [Input(component_id='slct_year_x', component_property='value'),
     Input(component_id='slct_prod_x', component_property='value')]
)
def update_graph(option_slctd, prod_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = df_.copy()
    line = px.line(data_frame=x, x='YEAR', y='NUMBER', color='PRODUCT', title='Nyförsäljning: Antal avtal')
    bar_data = px.bar(x, x="YEAR", y="AMOUNT", color="PRODUCT", title="Nyförsäljning i kronor")
    # bar_data.update_layout(template='plotly_dark')

    f = df_
    f = f[f['YEAR'] == option_slctd]
    p = []
    if prod_slctd == 'FRITID': p = [0.2, 0, 0, 0, 0, 0]
    if prod_slctd == 'DIREKT/LEV': p = [0, 0.2, 0, 0, 0, 0]
    if prod_slctd == 'MASKINFINANS': p = [0, 0, 0.2, 0, 0, 0]
    if prod_slctd == 'PARTNER FÖRETAG': p = [0, 0, 0, 0.2, 0, 0]
    if prod_slctd == 'BIL': p = [0, 0, 0, 0, 0.2, 0]
    if prod_slctd == 'BILKUND': p = [0, 0, 0, 0, 0, 0.2]
    fig = go.Figure(data=[go.Pie(labels=f['PRODUCT'], values=f['NUMBER'], pull=p)])
    fig.update_layout(title='Antal nya avtal')

    df_pd = df_.copy()
    vikt_pd = px.line(data_frame=df_pd, x='YEAR', y='VIKT_PD', color='PRODUCT', title='Viktat PD Nyförsäljning')

    df_pd['VIKT_EL'] = df_pd['VIKT_PD'] * df_pd['VIKT_LGD']
    vikt_el = px.line(data_frame=df_pd, x='YEAR', y='VIKT_EL', color='PRODUCT', title='Viktat EL Nyförsäljning')

    return container, line, bar_data, fig, vikt_pd, vikt_el
