from dataclasses import dataclass
from typing import Dict, Callable, Collection, List

import time
import copy
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


def show_basic_caching() -> None:
    st.header("Improve performance by caching")
    # TODO: load big file
    #       max size
    #       cache complex object -> custom hash function
    #
    st.write("""Caching is the core mechanic of streamlit to allow for an acceptable UX:  
    Simply decorate a function with `st.cache`""")

    use_cache = st.checkbox("Use caching?")

    st.write("Used function for loading the data:")
    load_data = _with_cache() if use_cache else _without_caching()
    st.write("Load and inspect the downloaded dataset")

    # simple caching
    with st.echo():
        base_url = "https://raw.githubusercontent.com/vega/vega-datasets/master/data/"

        src = st.selectbox("Vega Dataset:", ["gapminder.json", "jobs.json", "flights-20k.json"])
        df = load_data(base_url+src)
        # n = st.slider("Show first n entries:", min_value=0, max_value=len(df), value=10, step=1000)
        st.dataframe(df.head(100))

    st.subheader("Not just dataframes can be cached")
    with st.echo():
        create_chart = st.cache(_create_chart, allow_output_mutation=True) if use_cache else _create_chart
        chart = create_chart(df)
        st.altair_chart(chart, use_container_width=True)

    st.info("**Hint**: Data is cached across sessions!")


def _create_chart(df: pd.DataFrame) -> alt.Chart:
    x_col = "year" if 'year' in df.columns else 'date'
    val_col = df.select_dtypes([np.number]).columns[-1]
    cat_col = df.select_dtypes([np.object]).columns[0]
    chart = alt.Chart(df).mark_line().encode(
        x=f"{x_col}:T",
        y=val_col,
        color=cat_col,
        tooltip=[x_col, val_col, cat_col]
    )
    return chart


def show_advanced_caching() -> None:
    st.header("Fine grained control")
    st.subheader("Under the Hood")
    st.markdown(""" Information used for detecting changes in cache:   
    
    1. The input parameters that you called the function with
    2. The value of any external variable used in the function
    3. The body of the function
    4. The body of any function used inside the cached function
    """)
    # pythons LRU cache uses only input parameters (see: https://docs.python.org/3/library/functools.html#functools.lru_cache)

    st.subheader("Cache custom objects")
    
    if st.checkbox("Show error message"):
        st.image("https://aws1.discourse-cdn.com/standard10/uploads/streamlit/optimized/2X/8/8e43b6b1b88db7d0759adfe163ac1ebe09fcd3f8_2_690x401.png")

    with st.echo():
        @dataclass()
        class MyObject:
            value: int = 0
            __hash__ = None

            def __repr__(self):
                return f"MyObject={self.value}"

        @st.cache(suppress_st_warning=True)
        def load_data(n: int = 10) -> List[MyObject]:
            st.warning("Cache miss!")
            return [MyObject(np.random.randint(0, 100)) for _ in range(n)]

    st.write(f"Representation of MyObject: `{MyObject()}`")

    st.markdown('-'*6)
    st.subheader("Selective caching of specific types")

    with st.echo():
        hash_fns = {'default': 'default', 'hash': hash, 'id': id, 'None': lambda _: None}
        fn = st.radio("Hashing function", list(hash_fns.keys()))

        cached_load_data = st.cache(load_data, hash_funcs={MyObject: hash_fns[fn]}) \
            if fn != "default" else st.cache(load_data)

        n = st.slider("Number of objects", min_value=1, max_value=10, key=1)
        data = cached_load_data(n)
        st.text(data)

    st.markdown('-'*6)

    st.subheader("Limit cache")
    st.markdown("""
    Two mechanics to limit caching:
    - **max_entries**: limit number of cached entries (oldest will be removed first)
    - **ttl**: limit lifetime of entry (in seconds)""")
    with st.echo():
        @st.cache(ttl=5, max_entries=100, suppress_st_warning=True)
        def load_data(num_entries: int = 10) -> List[MyObject]:
            st.warning("cache miss!")
            return [MyObject(np.random.randint(0, 100)) for _ in range(num_entries)]

        n = st.slider("Number of objects", min_value=1, max_value=10)
        data = load_data(n)
        st.text(data)


def _without_caching() -> Callable:
    with st.echo():
        def load_data(src: str) -> pd.DataFrame:
            df = pd.read_json(src)
            time.sleep(2)
            return df

    return load_data


def _with_cache() -> Callable:
    with st.echo():
        @st.cache
        def load_data(src: str) -> pd.DataFrame:
            df = pd.read_json(src)
            time.sleep(2)
            return df
    return load_data


def _gen_data() -> Collection:
    pass


def _cont_update_chart() -> None:
    st.subheader("Update chart")
    np.random.seed(42)

    with st.echo():
        data = np.random.randn(10, 2)

        add_data = st.checkbox("Continuously update chart")
        chart = st.line_chart(data)

        while add_data:
            chart.add_rows(np.random.randn(1, 2))
            time.sleep(0.5)


def _update_dataframe() -> None:
    with st.echo():
        df = pd.DataFrame(np.random.randn(10, 2), columns=['A', 'B'])
        table = st.dataframe(df)

        add_data = st.checkbox("Continuously add data")
        while add_data:
            table.add_rows(np.random.randn(1, 2))
            time.sleep(0.5)


def show_dynamic_updating() -> None:
    st.header("Dynamically update content")
    st.write("Uses `DeltaGenerator` under the hood.")

    _cont_update_chart()
    _update_dataframe()


def get_sections() -> Dict[str, Callable]:
    return {
        "Caching": show_basic_caching,
        "Advanced Caching": show_advanced_caching,
        "Dynamic updating": show_dynamic_updating
    }
