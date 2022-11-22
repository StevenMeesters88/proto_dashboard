# import dash
# from dash import html, dcc, callback, Input, Output
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from plotly.subplots import make_subplots
#
#
# def create_prototype_data():
#     df = pd.read_excel('Pages/Page_1_data.xlsx', sheet_name='general')
#     df['YEAR'] = df['YEAR'].astype(str)
#     df_beslut = pd.read_excel('Pages/Page_1_data.xlsx', sheet_name='manual')
#     df_beslut['YEAR'] = df_beslut['YEAR'].astype(str)
#     df_sla = pd.read_excel('Pages/Page_1_data.xlsx', sheet_name='SLA')
#     df_sla['YEAR'] = df_sla['YEAR'].astype(str)
#     return df, df_beslut, df_sla
#
#
# df, beslut, sla = create_prototype_data()
#
# dash.register_page(__name__)
# # dash.register_page(__name__, title='Custom Page Title', description='Custom Page Description', image='logo.png')
#
#
# layout = html.Div([
#
#     html.H1(children="Kreditbeslut", style={'text-align': 'center'}),
#     html.H2(children='Denna sida visar statistik kring kreditbesluten', style={'text-align': 'center'}),
#
#     dcc.Dropdown(id="slct_year",
#                  options=[
#                      {"label": "2019", "value": '2019'},
#                      {"label": "2020", "value": '2020'},
#                      {"label": "2021", "value": '2021'},
#                      {"label": "2022", "value": '2022'}],
#                  multi=False,
#                  value='2022',
#                  style={'width': "40%"}
#                  ),
#
#     html.Div(id='output_container', children=[]),
#     html.Br(),
#
#     dcc.Graph(id='pie_number', figure={}),
#     html.Br(),
#
#     dcc.Graph(id='pie_amount', figure={}),
#     html.Br(),
#
#     dcc.Graph(id='pie_beslut', figure={}),
#     html.Br(),
#
#     dcc.Graph(id='line_beslut', figure={}),
#
#     html.H1(children="SLA Kreditbeslut", style={'text-align': 'center'}),
#
#     dcc.Graph(id='combined_SLA', figure={})
#
# ])
#
#
# @callback(
#     [Output(component_id='output_container', component_property='children'),
#      Output(component_id='pie_number', component_property='figure'),
#      Output(component_id='pie_amount', component_property='figure'),
#      Output(component_id='pie_beslut', component_property='figure'),
#      Output(component_id='line_beslut', component_property='figure'),
#      Output(component_id='combined_SLA', component_property='figure')],
#     [Input(component_id='slct_year', component_property='value')]
# )
# def update_graph(option_slctd):
#     print(option_slctd)
#     print(type(option_slctd))
#
#     container = "Visar data för år: {}".format(option_slctd)
#
#     dff = df.copy()
#     dff = dff[dff["YEAR"] == option_slctd]
#     pie_chart_n = px.pie(dff, names='PRODUCT', values='NUMBER', title='Inkommande ansökningar per produkt (antal)')
#     pie_chart_amount = px.pie(dff, names='PRODUCT', values='NUMBER',
#                               title='Inkommande ansökningar per produkt (belopp)')
#
#     df_bes = beslut.copy()
#     df_bes = df_bes[df_bes["YEAR"] == option_slctd]
#     pie_beslut = px.pie(df_bes, names='TYPE', values='NUMBER', title='Antal Kreditbeslut')
#
#     df_bes_line = beslut.copy()
#     line_beslut = px.line(df_bes_line, x='YEAR', y='NUMBER', color='TYPE', title='Antal Kreditbeslut per år')
#
#     # https://plotly.com/python/multiple-axes/
#     df_sla = sla.copy()
#     df_sla = df_sla[df_sla["YEAR"] == option_slctd]
#     sla_comb = make_subplots(specs=[[{"secondary_y": True}]])
#     sla_comb.add_trace(
#         go.Bar(x=df_sla['MONTH'], y=df_sla['INCOMING'], name="Antal ansökningar"),
#         secondary_y=False,
#     )
#     sla_comb.add_trace(
#         go.Line(x=df_sla['MONTH'], y=df_sla['WITHIN SLA'], name="Andel ansökningar inom SLA"),
#         secondary_y=True,
#     )
#     sla_comb.update_layout(
#         title_text="Antal inkomna ansökningar och andel hanterade inom SLA"
#     )
#
#     return container, pie_chart_n, pie_chart_amount, pie_beslut, line_beslut, sla_comb
