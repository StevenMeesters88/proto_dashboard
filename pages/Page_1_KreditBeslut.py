import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots


def create_prototype_data():
    df = pd.read_excel('Pages/Page_1_data.xlsx', sheet_name='general')
    df['YEAR'] = df['YEAR'].astype(str)
    df_beslut = pd.read_excel('Pages/Page_1_data.xlsx', sheet_name='manual')
    df_beslut['YEAR'] = df_beslut['YEAR'].astype(str)
    df_sla = pd.read_excel('Pages/Page_1_data.xlsx', sheet_name='SLA')
    df_sla['YEAR'] = df_sla['YEAR'].astype(str)
    return df, df_beslut, df_sla


df, beslut, sla = create_prototype_data()

dash.register_page(__name__)
# dash.register_page(__name__, title='Custom Page Title', description='Custom Page Description', image='logo.png')


layout = html.Div([

    html.H1(children="Kreditbeslut", style={'text-align': 'center'}),
    html.H2(children='Denna sida visar statistik kring kreditbesluten', style={'text-align': 'center'}),

    dcc.Graph(id='main_graph_v2', figure={}),
    html.Br(),

    dcc.Graph(id='line_beslut_v2', figure={}),
    html.Br(),

    dcc.Dropdown(id='compare_one',
                 options=[
                     {"label": "2019", "value": "2019"},
                     {"label": "2020", "value": "2020"},
                     {"label": "2021", "value": "2021"},
                     {"label": "2022", "value": "2022"}],
                 multi=False,
                 value='2021',
                 style={"width": "40%"}
                 ),

    dcc.Dropdown(id='compare_two',
                 options=[
                     {"label": "2019", "value": "2019"},
                     {"label": "2020", "value": "2020"},
                     {"label": "2021", "value": "2021"},
                     {"label": "2022", "value": "2022"}],
                 multi=False,
                 value="2022",
                 style={"width": "40%"}
                 ),

    dcc.Graph(id='compare_cookie_v2', figure={}),
    html.Br(),

    html.H1(children="SLA Kreditbeslut", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year_kredbes",
                 options=[
                     {"label": "2019", "value": '2019'},
                     {"label": "2020", "value": '2020'},
                     {"label": "2021", "value": '2021'},
                     {"label": "2022", "value": '2022'}],
                 multi=False,
                 value='2022',
                 style={'width': "40%"}
                 ),
    html.Div(id='output_container_v2', children=[]),
    html.Br(),

    dcc.Graph(id='combined_SLA_v2', figure={})

])


@callback(
    [Output(component_id='main_graph_v2', component_property='figure'),
     Output(component_id='line_beslut_v2', component_property='figure'),
     Output(component_id='compare_cookie_v2', component_property='figure'),
     Output(component_id='combined_SLA_v2', component_property='figure'),
     Output(component_id='output_container_v2', component_property='children')],
    [Input(component_id='compare_one', component_property='value'),
     Input(component_id='compare_two', component_property='value'),
     Input(component_id='slct_year_kredbes', component_property='value')]
)
def update_graph(comp1_slctd, comp2_slctd, option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "Visar data för år: {}".format(option_slctd)

    dff = df.copy()
    dff = dff.groupby('YEAR').sum()
    dff = dff.reset_index()
    dff_main = make_subplots(specs=[[{"secondary_y": True}]])
    dff_main.add_trace(
        go.Bar(x=dff['YEAR'], y=dff['NUMBER'], name="Antal inkommande ansökningar"),
        secondary_y=False,
    )
    dff_main.add_trace(
        go.Line(x=dff['YEAR'], y=dff['AMOUNT'], name="Belopp inkommande ansökningar"),
        secondary_y=True,
    )
    dff_main.update_layout(
        title_text="Inkomna ansökningar i antal och belopp"
    ),

    df_bes_line = beslut.copy()
    line_beslut = px.line(df_bes_line, x='YEAR', y='NUMBER', color='TYPE', title='Antal Kreditbeslut per år')

    # Compare cookies
    comp = df.copy()
    comp_one = comp[comp['YEAR'] == comp1_slctd]
    comp_two = comp[comp['YEAR'] == comp2_slctd]
    print(comp_one)
    print(comp_two)
    comp_cookie = make_subplots(1, 2, specs=[[{'type': 'domain'}, {'type': 'domain'}]],
                                subplot_titles=[comp1_slctd, comp2_slctd])
    comp_cookie.add_trace(go.Pie(labels=comp_one['PRODUCT'], values=comp_one['AMOUNT'],
                                 name=f"Data {comp1_slctd}"), 1, 1)
    comp_cookie.add_trace(go.Pie(labels=comp_two['PRODUCT'], values=comp_two['AMOUNT'],
                                 name=f"Data {comp2_slctd}"), 1, 2)
    comp_cookie.update_layout(title_text='Jämför två år')

    # https://plotly.com/python/multiple-axes/
    df_sla = sla.copy()
    df_sla = df_sla[df_sla["YEAR"] == option_slctd]
    sla_comb = make_subplots(specs=[[{"secondary_y": True}]])
    sla_comb.add_trace(
        go.Bar(x=df_sla['MONTH'], y=df_sla['INCOMING'], name="Antal ansökningar"),
        secondary_y=False,
    )
    sla_comb.add_trace(
        go.Line(x=df_sla['MONTH'], y=df_sla['WITHIN SLA'], name="Andel ansökningar inom SLA"),
        secondary_y=True,
    )
    sla_comb.update_layout(
        title_text="Antal inkomna ansökningar och andel hanterade inom SLA"
    )

    return dff_main, line_beslut, comp_cookie, sla_comb, container
