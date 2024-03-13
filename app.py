from dash import Dash, dcc, html, dash_table
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from pycaret.regression import predict_model, setup
import joblib

data = pd.read_csv("new_cleaned_data.csv")
data["DATETIMEDATA"] = pd.to_datetime(data["DATETIMEDATA"], format="%Y-%m-%d %H:%M:%S")
data.sort_values("DATETIMEDATA", inplace=True)
order = ['PM25', 'O3', 'WS', 'TEMP', 'RH', 'WD']

PAGE_SIZE = 5

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "Prediction"

# Setup PyCaret
setup(data=data, target='PM25', session_id=123)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="😽💨", className="header-emoji"),
                html.H1(
                    children="Air4thai Prediction", className="header-title"
                ),
                html.P(
                    children="Analysis and Prediction from Air4thai",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Parameter", className="menu-title"),
                        dcc.Dropdown(
                            id="parameter-filter",
                            options=[
                                {"label": param, "value": param}
                                for param in ['PM25', 'PM10', 'O3', 'CO', 'NO2', 'SO2', 'WS', 'TEMP', 'RH', 'WD']
                            ],
                            value="PM25",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["DATETIMEDATA"].min().date(),
                            max_date_allowed=data["DATETIMEDATA"].max().date(),
                            start_date=data["DATETIMEDATA"].min().date(),
                            end_date=data["DATETIMEDATA"].max().date(),
                            display_format='YYYY-MM-DD',
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="all-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3(children="Data Analysis", className="header-table colored-background"),
                        dash_table.DataTable(
                            id="analysis",
                            columns=[{"name": i, "id": i} for i in order],
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action="custom",
                            style_cell={"textAlign": "center"},
                            style_header={"backgroundColor": " rgb(174, 180, 196)"},
                            style_cell_conditional=[
                                {"if": {"column_id": c}, "textAlign": "center"}
                                for c in order
                            ],
                            style_as_list_view=True,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="PM-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3(children="PM25-Prediction", className="header-table colored-background"),
                        dash_table.DataTable(
                            id="prediction_pm",
                            columns=[{"name": i, "id": i} for i in ["DATETIMEDATA", "prediction_label"]],
                            style_cell={"textAlign": "center"},
                            style_header={"backgroundColor": " rgb(174, 180, 196)"},
                            style_cell_conditional=[
                                {"if": {"column_id": c}, "textAlign": "center"}
                                for c in ["Date", "Region"]
                            ],
                            style_as_list_view=True,
                        ),
                    ],
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="O3-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                html.Div(
                    children=[
                        html.H3(children="O3-Prediction", className="header-table colored-background"),
                        dash_table.DataTable(
                            id="prediction_O3",
                            columns=[{"name": i, "id": i} for i in ["DATETIMEDATA", "prediction_label"]],
                            style_cell={"textAlign": "center"},
                            style_header={"backgroundColor": " rgb(174, 180, 196)"},
                            style_cell_conditional=[
                                {"if": {"column_id": c}, "textAlign": "center"}
                                for c in ["Date", "Region"]
                            ],
                            style_as_list_view=True,
                        ),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        dcc.Interval(
            id='interval-component',
            interval=60 * 60 * 1000, 
            n_intervals=0
        )
    ]
)

# Load the models
loaded_model_PM25 = pd.read_csv('predictions_PM25.csv')
loaded_model_O3 = pd.read_csv('predictions_O3.csv')

@app.callback(
    Output("all-chart", "figure"),
    [
        Input("parameter-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_chart(parameter, start_date, end_date):
    mask = (data["DATETIMEDATA"] >= start_date) & (data["DATETIMEDATA"] <= end_date)
    filtered_data = data.loc[mask, :]
    all_figure = {
        "data": [
            {
                "x": filtered_data["DATETIMEDATA"],
                "y": filtered_data[parameter],
                "type": "lines",
                "hovertemplate": f"{parameter}: %{{y:.2f}}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": f"{parameter}",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Datetime", "fixedrange": True},
            "yaxis": {"title": parameter, "fixedrange": True},
            "colorway": ["#b8c9b4"],
        },
    }
    return all_figure


@app.callback(
    Output("analysis", "data"),
    [Input('analysis', "page_current"),
    Input('analysis', "page_size")]
)
def update_table(analysis_page_current, analysis_page_size):
    analysis_data = (data[order]
                     .iloc[analysis_page_current * analysis_page_size:
                           (analysis_page_current + 1) * analysis_page_size]
                    .to_dict('records'))
    return analysis_data


@app.callback(
    Output("PM-chart", "figure"),
    Output("O3-chart", "figure"),
    [
        Input('interval-component', 'n_intervals')
    ],
)
def update_chart(n_intervals):
    data['DATETIMEDATA'] = pd.to_datetime(data['DATETIMEDATA'])

    now = pd.Timestamp.now()
    start_date = now.date()
    end_date = start_date + pd.DateOffset(days=7)

    future_dates_PM25 = pd.date_range(start=start_date, end=end_date, freq='D')
    PM_future_data = pd.DataFrame({'DATETIMEDATA': future_dates_PM25})
    PM_future_data['O3'] = data['O3'].mean().round(2)
    PM_future_data['WS'] = data['WS'].mean().round(2)
    PM_future_data['TEMP'] = data['TEMP'].mean().round(2)
    PM_future_data['RH'] = data['RH'].mean().round(2)
    PM_future_data['WD'] = data['WD'].mean().round(2)

    predictions_PM25 = predict_model(loaded_model_PM25, data=PM_future_data)
    predictions_PM25['prediction_label'] = predictions_PM25['Label'].round(2)

    PM_chart = {
        "data": [
            {
                "x": future_dates_PM25,
                "y": predictions_PM25['prediction_label'].round(2),
                "type": "lines",
                'name': 'PM25 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': {
                'text': f'PM25 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'PM25 Forecast', "fixedrange": True},
            "colorway": ["#B5C0D0"],
        },
    }

    future_dates_O3 = pd.date_range(start=start_date, end=end_date, freq='D')
    O3_future_data = pd.DataFrame({'DATETIMEDATA': future_dates_O3})
    O3_future_data['PM10'] = data['PM10'].mean().round(2)
    O3_future_data['O3'] = data['O3'].mean().round(2)
    O3_future_data['WS'] = data['WS'].mean().round(2)
    O3_future_data['TEMP'] = data['TEMP'].mean().round(2)
    O3_future_data['RH'] = data['RH'].mean().round(2)
    O3_future_data['PM25'] = data['WD'].mean().round(2)

    predictions_O3 = predict_model(loaded_model_O3, data=O3_future_data)
    predictions_O3['prediction_label'] = predictions_O3['Label'].round(2)

    O3_chart = {
        "data": [
            {
                "x": future_dates_O3,
                "y": predictions_O3['prediction_label'].round(2),
                "type": "lines",
                'name': 'O3 Forecast',
                "hovertemplate": "%{y:.2f}<extra></extra>",
            },
        ],
        'layout': {
            'title': {
                'text': f'O3 Forecast for Next 7 Days',
                "x": 0.05,
                "xanchor": "left",
            },
            'xaxis': {'title': 'Date', "fixedrange": True},
            'yaxis': {'title': 'O3 Forecast', "fixedrange": True},
            "colorway": ["#B5C0D0"],
        },
    }

    predictions_O3.to_csv('predictions_O3.csv', index=False)
    predictions_PM25.to_csv('predictions_PM25.csv', index=False)

    return PM_chart, O3_chart


@app.callback(
    Output("prediction_pm", "data"),
    Output("prediction_O3", "data"),
    [
        Input('interval-component', 'n_intervals')
    ],
)
def update_chart(n_intervals):
    prediction_pm_df = pd.read_csv('predictions_PM25.csv')
    prediction_O3_df = pd.read_csv('predictions_O3.csv')

    prediction_pm = prediction_pm_df.to_dict('records')
    prediction_O3 = prediction_O3_df.to_dict('records')

    return prediction_pm, prediction_O3


if __name__ == "__main__":
    app.run_server(debug=True)
