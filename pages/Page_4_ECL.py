import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd


def create_prototype_data():
    df = pd.read_excel('Pages/Page_4_data.xlsx')
    df['YEAR'] = df['YEAR'].astype(str)
    return df


ecl_df = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="ECL", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_ecl",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_ecl', children=[]),
    html.Br(),

    dcc.Graph(id='ecl_line_one', figure={}),
    html.Br(),

    dcc.Graph(id='ecl_pie_one', figure={}),
    html.Br()

    ])


@callback(
    [Output(component_id='output_container_ecl', component_property='children'),
     Output(component_id='ecl_line_one', component_property='figure'),
     Output(component_id='ecl_pie_one', component_property='figure')],
    [Input(component_id='slct_year_ecl', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = ecl_df.copy()
    line = px.bar(data_frame=x, x='YEAR', y='ECLFINAL', color='PRODUCT', title='ECL över åren per produkt')

    ecl_pie_df = ecl_df.copy()
    ecl_pie_df = ecl_pie_df[ecl_pie_df['YEAR'] == option_slctd]
    ecl_pie_graph = px.pie(data_frame=ecl_pie_df, names='PRODUCT', values='ECLFINAL', title=f'ECL fördelat per {option_slctd}')

    return container, line, ecl_pie_graph
