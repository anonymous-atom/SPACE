from analysis_forecasy_runf import fit_model
from analysis_forecasy_runf import df
from analysis_forecasy_runf import df_year
import pandas as pd
from dash import Dash, dcc, html
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from dash_bootstrap_components._components.Row import Row

pio.renderers.default = "browser"

model = fit_model()
df = df

# Create validation set
valid = df['2022-06-01':]

# Make predictions
pred = fit_model().predict(start=valid.index[0], end=valid.index[-1])

# DataFrame for count of NEOs per year
df_year = df_year


def create_init_plots():
    # Plot NEOs per year using plotly
    import plotly.graph_objects as go
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_year.index, y=df_year['count'],
                              mode='lines',
                              name='NEOs'))
    fig1.update_layout(title='Number of NEOs per Year',
                       xaxis_title='Date',
                       yaxis_title='Number of NEOs',
                       )

    # Save this as a html file
    fig1.write_html("NEOs_per_year.html")

    # Plot average number of NEOs per year using plotly
    import plotly.graph_objects as go
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=df_year.index, y=df_year['count'] / df_year['count'].max(),
                              mode='lines',
                              name='NEOs'))
    fig2.update_layout(title='Average Number of NEOs per Year',
                       xaxis_title='Date',
                       yaxis_title='Number of NEOs', )
    # paper_bgcolor='rgba(0,0,0,0)',
    # plot_bgcolor='#3b3a39')
    # Save this as a html file
    fig2.write_html("NEOs_per_year_avg.html")

    return [fig1, fig2]


def create_pred_plot():
    # Interactive prediction plot with validation set using plotly and display on webpage
    import plotly.graph_objects as go
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df.index, y=df['count'],
                              mode='lines',
                              name='Train'))
    fig3.add_trace(go.Scatter(x=valid.index, y=valid['count'],
                              mode='lines',
                              name='Valid'))
    fig3.add_trace(go.Scatter(x=pred.index, y=pred,
                              mode='lines',
                              name='Predicted'))
    fig3.update_layout(title='Holt-Winters Model',
                       xaxis_title='Date',
                       yaxis_title='Number of NEOs',
                       height=500)
    # Save this as a html file
    fig3.write_html("Holt_Winters.html")

    return fig3


# Create a cool website with all the plots above
app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search", size="md")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="me-md-2", id="search-button", n_clicks=0, size="md"),
            width="auto", style={"padding": "10px"}
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    # Navbar with all elements perfectly aligned
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            # Make sure everything is centered
            dbc.Row(
                [
                    dbc.Col(html.Img(src="https://www.nasa.gov/sites/all/themes/custom/nasatwo/images/nasa-logo.svg",
                                     height="30px")),
                    dbc.Col(dbc.NavbarBrand("NASA NEO Dashboard", className="ms-2")),
                ],
                align="center",
                className="g-0",
            ),
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ]
)

breadcrumb = dbc.Breadcrumb(
    items=[
        {"label": "Docs", "href": "/docs", "external_link": True},
        {
            "label": "Components",
            "href": "/docs/components",
            "external_link": True,
        },
        {"label": "Breadcrumb", "active": True},
    ],
)

# Fig1 and Fig2
figdash1 = dbc.Card(
    [
        dbc.CardHeader("Figure 1"),

        dbc.CardBody(
            [
                html.H5("Number of NEOs per Year", className="card-title"),
                html.P(
                    "This is a plot of the number of NEOs per year. The number of NEOs has been increasing over the "
                    "years. The number of NEOs in 2020 is the highest so far.",
                    className="card-text",
                ),
                dcc.Graph(figure=create_init_plots()[0]),
            ]
        )
    ], color="primary", outline=True
)
figdash2 = dbc.Card(
    [
        dbc.CardHeader("Figure 1"),

        dbc.CardBody(
            [
                html.H5("Average Number of NEOs per Year", className="card-title"),
                html.P(
                    "This is a plot of the average number of NEOs per year. The average number of NEOs per year has "
                    "been increasing over the years. The average number of NEOs per year in 2020 is the highest so "
                    "far.",
                    className="card-text",
                ),
                dcc.Graph(figure=create_init_plots()[1]),
            ]
        )

    ], color="primary", outline=True
)
figdash3 = dbc.Card(
    [
        dbc.CardHeader("Figure 1"),

        dbc.CardBody(
            [
                html.H5("Holt-Winters Model", className="card-title"),
                html.P(
                    "This is a plot of the Holt-Winters model. The Holt-Winters model is a time series model that is "
                    "used to predict future values based on past values. The model is trained on the data from 2010 "
                    "to 2018. The model is then used to predict the number of NEOs in 2019 and 2020. The model is "
                    "able to predict the number of NEOs in 2019 and 2020 quite well.",
                    className="card-text",
                ),
                dcc.Graph(figure=create_pred_plot()),
            ]
        )

    ], color="primary", outline=True
)
cards1x2 = dbc.Row(
    [
        dbc.Col(figdash1, width=6),
        dbc.Col(figdash2, width=6),
    ]
)

app.layout = html.Div(
    [
        navbar,
        html.Div(id="breadcrumbs", children=breadcrumb, style={"padding": "20px 28px 10px 28px"}),
        html.Div(id="figdash3", children=figdash3, style={"padding": "20px 28px 20px 28px"}),
        html.Div(id="cards1x2", children=cards1x2, style={"padding": "20px 28px 20px 28px"}),
    ]
)


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server()
