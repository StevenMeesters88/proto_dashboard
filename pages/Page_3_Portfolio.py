import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_prototype_data():
    df = pd.read_excel('Pages/Page_3_data.xlsx')
    df['YEAR'] = df['YEAR'].astype(str)
    return df


df_ = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="Portfolio", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_portf",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_portf', children=[]),
    html.Br(),

    dcc.Graph(id='portf_bar_main', figure={}),
    html.Br(),

    dcc.Graph(id='portf_bar_prod', figure={}),
    html.Br(),

    dcc.Graph(id='portf_pie_prod', figure={}),
    html.Br()

    ]),


@callback(
    [Output(component_id='output_container_portf', component_property='children'),
     Output(component_id='portf_bar_main', component_property='figure'),
     Output(component_id='portf_bar_prod', component_property='figure'),
     Output(component_id='portf_pie_prod', component_property='figure')],
    [Input(component_id='slct_year_portf', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = df_.copy()
    x2 = x.groupby('YEAR').sum()
    x2 = x2.reset_index()
    p_bar = px.bar(data_frame=x2, x='YEAR', y='Exponering', title='Utveckling balans i kronor')
    p_bar_prod = px.bar(data_frame=x, x='YEAR', y='Exponering', color='PRODUCT', title='Utveckling balans per produkt i kronor')

    pie_df = df_.copy()
    pie_df = pie_df[pie_df['YEAR'] == option_slctd]
    p_pie_year = px.pie(data_frame=pie_df, names='PRODUCT', values='Exponering', title=f'Portfölj per {option_slctd}')

    return container, p_bar, p_bar_prod, p_pie_year
