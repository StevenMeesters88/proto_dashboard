import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    df = pd.read_excel('Pages/Page_6_data.xlsx', sheet_name='data')
    df['YEAR'] = df['YEAR'].astype(str)
    return df


df_ = create_prototype_data()

dash.register_page(__name__)


layout = html.Div([

    html.H1(children="Inkasso", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_dc",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_dc', children=[]),
    html.Br(),

    dcc.Graph(id='dc_bar', figure={}),
    html.Br(),

    dcc.Graph(id='dc_pie', figure={}),
    html.Br(),

    dcc.Graph(id='dc_kfm_dispute', figure={}),
    html.Br()
    ]),

@callback(
    [Output(component_id='output_container_dc', component_property='children'),
     Output(component_id='dc_bar', component_property='figure'),
     Output(component_id='dc_pie', component_property='figure'),
     Output(component_id='dc_kfm_dispute', component_property='figure')],
    [Input(component_id='slct_year_dc', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    x = df_.copy()
    dc_bar = px.bar(data_frame=x, x='YEAR', y='CASES', color='PRODUCT', title='Inkassoärenden per produkt')

    df_pie = df_.copy()
    df_pie = df_pie[df_pie['YEAR'] == option_slctd]
    dc_pie = px.pie(data_frame=df_pie, names='PRODUCT', values='AMOUNT', title='Kapitalbelopp per produkt')

    df_kfm_disp = x.groupby('YEAR').sum()
    df_kfm_disp = df_kfm_disp.reset_index()
    kfm_dispute = make_subplots(specs=[[{"secondary_y": True}]])
    kfm_dispute.add_trace(
        go.Line(x=df_kfm_disp['YEAR'], y=df_kfm_disp['KFM'], name="Antal KFM ärenden"),
        secondary_y=False,
    )
    kfm_dispute.add_trace(
        go.Line(x=df_kfm_disp['YEAR'], y=df_kfm_disp['DISPUTE'], name="Antal bestridanden"),
        secondary_y=True,
    )
    kfm_dispute.update_layout(
        title_text="Antal KFM ärenden och bestridna fordringar"
    )

    return container, dc_bar, dc_pie, kfm_dispute
