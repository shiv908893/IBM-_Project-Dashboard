from __future__ import annotations

import pandas as pd
import plotly.express as px


def line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    fig = px.line(df, x=x_col, y=y_col, title=title, markers=True)
    fig.update_layout(template="plotly_white", height=350)
    return fig


def bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, color_col: str | None = None):
    if color_col:
        fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=title)
    else:
        fig = px.bar(df, x=x_col, y=y_col, title=title)
    fig.update_layout(template="plotly_white", height=350)
    return fig


def scatter_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str, color_col: str = "region"):
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=title, size=y_col)
    fig.update_layout(template="plotly_white", height=350)
    return fig
