import dash
from pages.home.layout import create_layout

dash.register_page(__name__, path="/")

layout = create_layout()