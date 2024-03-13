import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("หน้าแรก"),
        # เพิ่มเนื้อหาหน้าแรกที่คุณต้องการ
    ]
)

app.layout = html.Div(
    children=[
        dcc.Tabs(id='tabs', value='tab1', children=[
            dcc.Tab(label='หน้าแรก', value='tab1'),
            dcc.Tab(label='หน้าที่ 2', value='tab2'),
            # เพิ่ม Tab ตามต้องการ
        ]),
        html.Div(id='tabs-content')
    ]
)

@app.callback(Output('tabs-content', 'children'),[Input('tabs', 'value')])
def update_tab(selected_tab):
    if selected_tab == 'tab1':
        return [
            html.H1("หน้าแรก"),
            # เพิ่มเนื้อหาหน้าแรกที่คุณต้องการ
        ]
    elif selected_tab == 'tab2':
        return [
            html.H1("หน้าที่ 2"),
            # เพิ่มเนื้อหาหน้าที่ 2 ที่คุณต้องการ
        ]
    # เพิ่มเงื่อนไขสำหรับ Tabs อื่น ๆ ตามต้องการ

if __name__ == '__main__':
    app.run_server(debug=True)
