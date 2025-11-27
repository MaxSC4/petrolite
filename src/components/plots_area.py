from dash import html, dcc
import dash_bootstrap_components as dbc


def create_plots_card() -> dbc.Card:
    return dbc.Card(
        [
            dbc.CardHeader("Data Preview & Plot"),
            dbc.CardBody(
                [
                    html.H6("Data preview"),
                    html.Div(id="data-preview", className="mb-3"),
                    html.H6("Diagram"),
                    dcc.Graph(
                        id="main-graph",
                        figure={},
                        style={"height": "500px"},
                        mathjax=True,  # 👈 IMPORTANT
                        config={
                            "toImageButtonOptions": {
                                "format": "svg",
                                "scale": 2,
                            },
                            "displaylogo": False,
                            "modeBarButtonsToRemove": [
                                "select2d",
                                "lasso2d",
                                "autoScale2d",
                            ],
                        },
                    ),
                ]
            ),
        ],
        className="h-100",
    )
