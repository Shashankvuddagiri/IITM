import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

def create_dashboard(server):
    dash_app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/')

    dash_app.layout = html.Div([
        html.H1('Green Finance Dashboard'),
        
        # Scenario Analysis Section
        html.Div([
            html.H3('Scenario Analysis'),
            html.Div([
                html.Label('Risk Tolerance:'),
                dcc.Slider(id='risk-tolerance', min=1, max=10, step=1, value=5, 
                          marks={i: str(i) for i in range(1, 11)}),
            ], className='mb-4'),
            html.Div([
                html.Label('Investment Horizon (Years):'),
                dcc.Dropdown(id='investment-horizon',
                            options=[{'label': f'{i} Years', 'value': i} for i in [1,3,5,10]],
                            value=5)
            ], className='mb-4'),
            html.Button('Run Scenario', id='run-scenario', className='btn btn-primary')
        ], className='p-4 border rounded mb-4'),

        # ROI and Performance Metrics
        html.Div([
            dcc.Graph(id='roi-projection-chart'),
            html.Div([
                html.Div(id='expected-roi', className='metric-box'),
                html.Div(id='risk-adjusted-return', className='metric-box'),
                html.Div(id='sustainability-impact', className='metric-box')
            ], className='metrics-container')
        ]),

        # Existing charts
        dcc.Graph(id='esg-scores-chart'),
        dcc.Graph(id='optimized-portfolio-chart'),
        dcc.Graph(id='risk-prediction-chart')
    ])

    @dash_app.callback(
        Output('esg-scores-chart', 'figure'),
        Input('esg-scores-chart', 'id')
    )
    def update_esg_scores_chart(_):
        df = pd.DataFrame([
            {"project": "Solar Farm A", "esg_score": 85},
            {"project": "Wind Farm B", "esg_score": 78},
            {"project": "Hydroelectric Plant C", "esg_score": 72},
            {"project": "Geothermal Project D", "esg_score": 80},
        ])
        fig = px.bar(df, x='project', y='esg_score', title='ESG Scores by Project')
        return fig

    @dash_app.callback(
        Output('optimized-portfolio-chart', 'figure'),
        Input('optimized-portfolio-chart', 'id')
    )
    def update_optimized_portfolio_chart(_):
        df = pd.DataFrame([
            {"project": "Solar Farm A", "allocation": 250000},
            {"project": "Wind Farm B", "allocation": 400000},
            {"project": "Hydroelectric Plant C", "allocation": 150000},
            {"project": "Geothermal Project D", "allocation": 200000},
        ])
        fig = px.pie(df, values='allocation', names='project', title='Optimized Portfolio Allocation')
        return fig

    @dash_app.callback(
        Output('risk-prediction-chart', 'figure'),
        Input('risk-prediction-chart', 'id')
    )
    def update_risk_prediction_chart(_):
        projects = ['Solar Farm A', 'Wind Farm B', 'Hydroelectric Plant C', 'Geothermal Project D']
        years = list(range(2023, 2028))
        risk_scores = np.random.randint(1, 10, size=(len(projects), len(years)))
        
        df = pd.DataFrame(risk_scores, columns=years, index=projects)
        df = df.reset_index().melt(id_vars='index', var_name='Year', value_name='Risk Score')
        df.columns = ['Project', 'Year', 'Risk Score']
        
        fig = px.line(df, x='Year', y='Risk Score', color='Project', title='Predicted Risk Scores (2023-2027)')
        return fig

    @dash_app.callback(
        Output('roi-projection-chart', 'figure'),
        [Input('risk-tolerance', 'value'),
         Input('investment-horizon', 'value'),
         Input('run-scenario', 'n_clicks')]
    )
    def update_roi_projection(risk_tolerance, horizon, _):
        # Generate sample ROI projections
        years = list(range(horizon + 1))
        scenarios = ['Conservative', 'Moderate', 'Aggressive']
        
        df = pd.DataFrame()
        for scenario in scenarios:
            base_roi = risk_tolerance * (scenarios.index(scenario) + 1)
            volatility = (scenarios.index(scenario) + 1) * 2
            roi_values = [base_roi * (1 + np.random.normal(0, volatility/100, 1)[0]) ** year 
                         for year in years]
            df[scenario] = roi_values
        
        df['Year'] = years
        df_melted = df.melt(id_vars=['Year'], value_vars=scenarios, 
                           var_name='Scenario', value_name='ROI')
        
        fig = px.line(df_melted, x='Year', y='ROI', color='Scenario',
                     title='Projected ROI by Scenario')
        return fig

    return dash_app

