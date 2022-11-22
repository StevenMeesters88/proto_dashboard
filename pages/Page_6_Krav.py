import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    df_rec = pd.read_excel('Pages/Page_5_data.xlsx', sheet_name='recovery')
    df_rec['YEAR'] = df_rec['YEAR'].astype(str)
    df_sena = pd.read_excel('Pages/Page_5_data.xlsx', sheet_name='senabetalare')
    df_sena['YEAR'] = df_sena['YEAR'].astype(str)
    df_sla = pd.read_excel('Pages/Page_5_data.xlsx', sheet_name='SLA')
    df_sla['YEAR'] = df_sla['YEAR'].astype(str)
    return df_rec, df_sena, df_sla


rec, sena, sla = create_prototype_data()

dash.register_page(__name__)

layout = html.Div([

    html.H1(children="Krav", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_krav",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container_krav', children=[]),
    html.Br(),

    dcc.Graph(id='graph_line_rec', figure={}),
    html.Br(),

    dcc.Graph(id='graph_bar_rec', figure={}),
    html.Br(),

    dcc.Dropdown(id='slct_prod_krav',
                 options=[
                     {'label': 'Fritid', 'value': 'FRITID'},
                     {'label': 'Direkt/Lev', 'value': 'DIREKT/LEV'},
                     {'label': 'Maskinfinans', 'value': 'MASKINFINANS'},
                     {'label': 'Partner Företag', 'value': 'PARTNER FÖRETAG'},
                     {'label': 'Bil', 'value': 'BIL'},
                     {'label': 'Bil Kund', 'value': 'BILKUND'}
                 ]),
    html.Br(),

    dcc.Graph(id='graph_choose_pie', figure={}),
    html.Br(),

    dcc.Graph(id='graph_line_sena', figure={}),
    html.Br(),

    html.H1(children='SLA kravavdelningen', style={'text-align': 'center'}),

    dcc.Dropdown(id='slct_prod_krav2',
                 options=[
                     {'label': 'Fritid', 'value': 'FRITID'},
                     {'label': 'Direkt/Lev', 'value': 'DIREKT/LEV'},
                     {'label': 'Maskinfinans', 'value': 'MASKINFINANS'},
                     {'label': 'Partner Företag', 'value': 'PARTNER FÖRETAG'},
                     {'label': 'Bil', 'value': 'BIL'},
                     {'label': 'Bil Kund', 'value': 'BILKUND'}
                 ]),
    html.Br(),

    dcc.Graph(id='graph_sla_comb', figure={})

])


@callback(
    [Output(component_id='output_container_krav', component_property='children'),
     Output(component_id='graph_line_rec', component_property='figure'),
     Output(component_id='graph_bar_rec', component_property='figure'),
     Output(component_id='graph_choose_pie', component_property='figure'),
     Output(component_id='graph_line_sena', component_property='figure'),
     Output(component_id='graph_sla_comb', component_property='figure')],
    [Input(component_id='slct_year_krav', component_property='value'),
     Input(component_id='slct_prod_krav', component_property='value'),
     Input(component_id='slct_prod_krav2', component_property='value')]
)
def update_graph(option_slctd, prod_slctd, prod_slctd2):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    df_rec = rec.copy()
    line_rec = px.line(data_frame=df_rec, x='YEAR', y='RECOVERYRATE', color='PRODUCT', title='Återvinning per produkt')

    df_rec_year = rec.copy()
    df_rec_year = df_rec_year[df_rec_year['YEAR'] == option_slctd]
    bar_rec = px.bar(data_frame=df_rec_year, x='PRODUCT', y='AMOUNT',
                     title=f'Faktisk återvinning per produkt {option_slctd}')

    p = []
    if prod_slctd == 'FRITID': p = [0.2, 0, 0, 0, 0, 0]
    if prod_slctd == 'DIREKT/LEV': p = [0, 0.2, 0, 0, 0, 0]
    if prod_slctd == 'MASKINFINANS': p = [0, 0, 0.2, 0, 0, 0]
    if prod_slctd == 'PARTNER FÖRETAG': p = [0, 0, 0, 0.2, 0, 0]
    if prod_slctd == 'BIL': p = [0, 0, 0, 0, 0.2, 0]
    if prod_slctd == 'BILKUND': p = [0, 0, 0, 0, 0, 0.2]

    choose_pie = go.Figure(data=[go.Pie(labels=df_rec_year['PRODUCT'], values=df_rec_year['AMOUNT'], pull=p)])

    sena_bet = sena.copy()
    line_sena = px.line(data_frame=sena_bet, x='YEAR', y='ANDEL_SENA', color='PRODUCT',
                        title='Sena betalare per produkt')

    # https://plotly.com/python/multiple-axes/
    df_sla = sla.copy()
    df_sla = df_sla[df_sla["YEAR"] == option_slctd]
    # df_sla = df_sla[df_sla['PRODUCT'] == prod_slctd2]
    sla_comb = make_subplots(specs=[[{"secondary_y": True}]])
    sla_comb.add_trace(
        go.Bar(x=df_sla['MONTH'], y=df_sla['INCOMING'], name="Antal inkomna kravärenden"),
        secondary_y=False,
    )
    sla_comb.add_trace(
        go.Line(x=df_sla['MONTH'], y=df_sla['WITHIN SLA'], name="Andel hanterat inom SLA"),
        secondary_y=True,
    )
    sla_comb.update_layout(
        title_text="""Antal inkomna kravärenden och hantering inom SLA.

        OBS! Produkt dropdown ej kopplat till graf än pga prototyp!"""
    )

    return container, line_rec, bar_rec, choose_pie, line_sena, sla_comb
