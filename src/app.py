import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# create a dash app with a interactive map with bubbles
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

#Load data
df = pd.read_csv('sunshine.csv')
month_dict = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April', 'May': 'May', 'Jun': 'June',
              'Jul': 'July', 'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 'Nov': 'November',
              'Dec': 'December'}

#create a figure with a map
fig = go.Figure()

# add a scattermapbox trace to the figure
for i in range(len(df)):
    df_sub = df[df.index == i]
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon = df_sub['lon'],
        lat = df_sub['lat'],
        text = df_sub['city'] + ':Hours of sunshine: ' + df_sub['sunshine'].astype(str),
        name= df_sub['month'][i],
        visible=False,
        showlegend=True,
        mode='markers',
        marker = dict(
            size = df_sub['sunshine']/3.5,
            color = '#EDE8BA',
            line_color='black',
            line_width=0.5,
            sizemode = 'diameter'
        )))

# Set layout properties for the figure
fig.update_layout(
        showlegend = True,
        height=1000,
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1,
        xanchor="center",
        x=0.5
        ),
        geo = dict(
            scope = 'usa',
            landcolor = 'rgb(217, 217, 217)',
            bgcolor = 'black',
            lakecolor = 'lightblue',
            showrivers = True,
            showlakes = True,
            showcountries = True,
            showsubunits = True,
            resolution = 50,
        ),
    )


# create app layout
app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Row(
                [
                    html.Div([html.H1('Sunshine state of the month',
                    style={'text-align': 'center', 'color': 'white', 'padding-top': '100px'})]),

                    dcc.Graph(id='graph', figure=fig,
                    style={'width': '100%', 'color': 'black',
                        'text-color': 'white'})]),md=8),
        dbc.Col(
            dbc.Row(
                [
                    html.Div([html.H3('Select cities:', style={'text-align': 'left', 'color': 'white'})]),
                    dcc.Checklist(
                        id='dropdown_cities',
                        style={'width': '100%', 'text-align': 'left',
                               'border': '0px solid black', 'color': 'white'},
                        options=[{'label': i, 'value': i} for i in df['city'].unique()],
                        value=[i for i in df['city'].unique()]),

                    html.H3('Choose month:',style={'padding': '10px','text-align': 'left', 'color': 'white'}),
                    dcc.RadioItems(
                            id='dropdown',
                            style={'width': '100%','text-align': 'left', 'font_size': '20px', 'color': 'white'},
                            options=[{'label': month_dict[i], 'value': i} for i in df['month'].unique()],
                            value=''
                        ),



                ]),md=4,style={'padding-right': '250px', 'padding-top':'150px', 'background-color': 'black'})]),

], style={'width': '100%', 'background-color': 'black'})

# add callback for dropdown
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
    Input('dropdown_cities', 'value')]
)

# update graph with multi value dropdown in dcc.Graph
def update_graph(month, city_list):
    sunshine_state = ''
    for i in range(len(df)):
        if month == df['month'][i] and df['city'][i] in city_list:
            fig.data[i].visible = True
            fig.data[i].showlegend = False
            df_city_list = df[df['city'].isin(city_list)]
            max_temp_month = df_city_list[df_city_list['month'] == month]['sunshine'].max()
            if df['sunshine'][i] == max_temp_month:
                fig.data[i].marker.color = '#FCE570'
                #Sunshine state of the month is
                sunshine_state = f'Sunshine state of {month_dict[month]} is {df["city"][i]} with {df["sunshine"][i]} hours of sunshine'
            else:
                fig.data[i].marker.color = '#EDE8BA'
        else:
            fig.data[i].visible = 'legendonly'
            fig.data[i].showlegend = False

    # update font and size and position of the title
    fig.update_layout(
        title={
            'text': sunshine_state,
            'font_size': 25,
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    #update background color to black
    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        font_color='white'
    )


    return fig

if __name__ == '__main__':
    app.run_server(debug=True)





