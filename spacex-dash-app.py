# Package for handle the data
import pandas as pd

# Packages for make interactive graphs
import plotly.express as px
import plotly.graph_objects as go

# Packages for create the dashboard
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Getting the dataset
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
df = pd.read_csv(url)

# Creating the connection
app = dash.Dash(__name__)

# Creating the options for the dropdown
options = [{"label": i, "value": i} for i in df["Launch Site"].unique()]
options.append({"label": "All Sites", "value": "All Sites"})

# Creating the dashboard
app.layout = html.Div(children=[
    # Title
    html.Div([
        html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center", "color": "#503D36", "font-size": 36}),
    ]),
    # Line Break
    html.Br(),
    # Dropdown
    html.Div(
        dcc.Dropdown(id="site-dropdown",
                    options=options,
                    value="All Sites",
                    searchable=True)
    ),
    # Pie chart skeleton
    html.Div([dcc.Graph(id="success-pie-chart")]),
    # Line Break
    html.Br(),
    # Slider
    html.Div(
        dcc.RangeSlider(
            id="payload-slider", 
            min=0,
            max=10000,
            step=1000,
            marks={i: str(i) for i in range(0, 11000, 2500)},
            value=[0, 10000])
    ),
    # Scatter plot skeleton
    html.Div([dcc.Graph(id="success-payload-scatter-chart")])
])

# Creating the decorations for the interactivity
@app.callback([Output(component_id="success-pie-chart", component_property="figure"),
              Output(component_id="success-payload-scatter-chart", component_property="figure")], 
              [Input(component_id="site-dropdown", component_property="value"),
              Input(component_id="payload-slider", component_property="value")])

# Function for create the graphs
def get_charts(entered_site, payload_range):
    filtered_df = df.copy()
    if entered_site == "All Sites":
        # Pie chart of all sites
        success = filtered_df[filtered_df["class"] == 1]
        success = success.groupby("Launch Site")["class"].sum().reset_index()
        fig1 = px.pie(success, values="class", names="Launch Site", title="Total Success Launches By Site")
        # Scatter plot of all sites and selected range
        mass_range = filtered_df[
            (filtered_df["Payload Mass (kg)"] >= payload_range[0]) & 
            (filtered_df["Payload Mass (kg)"] <= payload_range[1])]
        fig2 = px.scatter(mass_range, x="Payload Mass (kg)", y="class", color="Booster Version Category", 
                          title="Correlation Between Payload and Success for all Sites", range_x=[0, 10000])
        return [fig1, fig2]
    else:
        # Pie chart of a selected site
        filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
        site = filtered_df["class"].value_counts().reset_index()
        fig1 = px.pie(site, values="count", names="class", title=f"Total Success Launches for site {entered_site}")
        # Scatter plot of a selected site and range
        mass_range = filtered_df[
            (filtered_df["Payload Mass (kg)"] >= payload_range[0]) & 
            (filtered_df["Payload Mass (kg)"] <= payload_range[1])]
        fig2 = px.scatter(mass_range, x="Payload Mass (kg)", y="class", color="Booster Version Category", 
                          title=f"Correlation Between Payload and Success for site {entered_site}", range_x=[0, 10000])
        return [fig1, fig2]

# Deploying the app
if __name__ == "__main__":
    app.run()