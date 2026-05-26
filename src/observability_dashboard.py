import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)


app.layout = html.Div([
    
    dcc.Store(id='null-count-table', data={'columns': ['Name', 'Email'], 'nulls': [0, 0]}),
    dcc.Store(id='duplicate-row-table', data={'metrics': ['Unique', 'Duplicate'], 'counts': [12, 0]}),
    
    # Visual graph components
    html.H2("Axiom Pipeline Observability"),
    dcc.Graph(id='null-count-graph'),
    dcc.Graph(id='duplicate-row-graph')
])

#  Callback for Null Counts
@app.callback(
    Output('null-count-graph', 'figure'),
    [Input('null-count-table', 'data')]
)
def update_null_count_graph(data):
    # Map the dictionary data into a real Plotly figure object
    fig = go.Figure(data=[
        go.Bar(x=data['columns'], y=data['nulls'], marker_color='#3498db')
    ])
    fig.update_layout(title="Null Counts per Column", yaxis_title="Count")
    return fig

#  Callback for Duplicate Rows
@app.callback(
    Output('duplicate-row-graph', 'figure'),
    [Input('duplicate-row-table', 'data')]
)
def update_duplicate_row_graph(data):
    # Map the dictionary data into a real Plotly figure object
    fig = go.Figure(data=[
        go.Pie(labels=data['metrics'], values=data['counts'], hole=0.3)
    ])
    fig.update_layout(title="Row Integrity (Duplicates vs Unique)")
    return fig

if __name__ == '__main__':
    print("Starting dashboard server on http://127.0.0.1:8050/")
    app.run(debug=True)