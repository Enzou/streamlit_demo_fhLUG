from typing import Dict, Callable

import streamlit as st
import numpy as np
import pandas as pd


def show_charts() -> None:
    st.header("Plotting options")

    # st.write("_Note: All plots use the `iris dataset` from [seaborns data repository](https://github.com/mwaskom/seaborn-data/blob/master/iris.csv)_")
    # iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

    st.subheader("Simple charts")
    st.write("""Simple functions to create `line`/`bar` or `area` charts. 
    This is a simple wrapper around _altair_ plots.  
    Provided data can be any of `pandas dataframe`, `numpy array`, `iterable`, `dict`. 
    
    > This is just syntax-sugar around st.altair_chart.   
    > The main difference is this command uses the data’s own column and indices to figure out the chart’s spec.   
    > As a result this is easier to use for many “just plot this” scenarios, while being less customizable.
    """)

    np.random.seed(42)
    df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    st.dataframe(df)

    with st.echo():
        plot_types = {"bar": st.bar_chart, "line": st.line_chart, "area": st.area_chart}
        plot_type = st.selectbox("Select plot type:", list(plot_types), index=0)
        plot_types[plot_type](df, use_container_width=True)

    st.write('-' * 6)
    st.subheader("Pyplot (Matplotlib)")

    with st.echo():
        import matplotlib.pyplot as plt
        plt.plot(df['a'], df['b'])
        plt.title("Abstract (science) art")
        st.pyplot()

    st.write('-' * 6)
    st.subheader("Altair / Vega-lite")

    st.write("A detailed documentation can be found on [Altair](https://altair-viz.github.io/) homepage")
    with st.echo():
        import altair as alt
        chart = alt.Chart(df).mark_circle().encode(
            x='a',
            y='b',
            size='c',
            color='c',
            tooltip=['a', 'b', 'c']
        )
        st.altair_chart(chart)

    st.write('-' * 6)
    st.subheader("Bokeh")
    st.write("A detailed documentation can be found on [Bokeh](https://docs.bokeh.org/en/latest/index.html) homepage")
    with st.echo():
        from bokeh.plotting import figure
        p = figure(
            title='simple line example',
            x_axis_label='a',
            y_axis_label='b')
        p.line(df['a'], df['b'], legend='Trend', line_width=2)

        st.bokeh_chart(p, use_container_width=True)

    st.write('-' * 6)
    st.subheader("Plotly")
    st.write("A detailed documentation can be found on [Plotly](https://plotly.com/python/) homepage")
    with st.echo():
        import plotly.express as px
        fig = px.scatter(df, x="a", y="b")
        st.plotly_chart(fig)


def show_maps_and_graphs() -> None:
    st.header("3D maps and graphs")

    lat, long = 48.30, 14.2958

    st.write("Data used for the geographic visualizations")
    df = pd.DataFrame(
        np.random.randn(1000, 2) / [60, 60] + [lat, long],
        columns=['lat', 'lon'])
    st.dataframe(df)

    st.write('-' * 6)
    st.subheader("Maps")

    zoom_lvl = st.slider("Zoom level: ", min_value=-1, max_value=20)
    if zoom_lvl == -1:
        zoom_lvl = None
    st.write("Zoom level is integer taken from [Open Streetmap](https://wiki.openstreetmap.org/wiki/Zoom_levels)")

    with st.echo():
        st.map(df, zoom=zoom_lvl)

    st.write('-' * 6)
    st.subheader("pydeck / DeckGL")
    st.write(
        "This supports 3D maps, point clouds, and more! More info about PyDeck at [deckgl](https://deckgl.readthedocs.io/en/latest/).")
    with st.echo():
        import pydeck as pdk

        st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=long,
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'HexagonLayer',
                    data=df,
                    get_position='[lon, lat]',
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=df,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))

    st.write('-' * 6)
    st.subheader("Graphviz")
    st.write("A detailed documentation about Graphviz cound be found [here](https://graphviz.readthedocs.io/en/stable/index.html)")
    with st.echo():
        import graphviz
        graph = graphviz.Digraph()
        graph.attr(rankdir='LR')
        graph.edge('Domain Controller', 'Server 1')
        graph.edge('Domain Controller', 'Server 2')
        graph.edge('Server 1', 'Database')
        graph.edge('Server 1', 'Client 1')
        graph.edge('Server 2', 'Client 1')

        st.graphviz_chart(graph)

    st.write("The use of the graphviz library is not mandatory, a graph as string in dot notation works just as fine")

    with st.echo():
        dot_format = """digraph {
            tbl [
            shape=plaintext
            label=<
            <table border='0' cellborder='1' color='blue' cellspacing='0'>
                <tr><td>foo</td><td>bar</td><td>baz</td></tr>
                <tr><td cellpadding='4'>
                    <table color='orange' cellspacing='0'>
                        <tr><td>one  </td><td>two  </td><td>three</td></tr>
                        <tr><td>four </td><td>five </td><td>six  </td></tr>
                        <tr><td>seven</td><td>eight</td><td>nine </td></tr>
                    </table>
                </td>
                <td colspan='2' rowspan='2'>
                    <table color='pink' border='0' cellborder='1' cellpadding='10' cellspacing='0'>
                        <tr><td>eins</td><td>zwei</td><td rowspan='2'>drei<br/>sechs</td></tr>
                        <tr><td>vier</td><td>fünf</td>                             </tr>
                    </table>
                </td> 
                </tr>
                <tr><td>abc</td></tr>
            </table>
            >];}
        """
        st.graphviz_chart(dot_format)


def get_sections() -> Dict[str, Callable]:
    return {
        "Show charts": show_charts,
        "Show maps and graphs": show_maps_and_graphs
    }
