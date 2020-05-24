import time
import inspect
from typing import Dict, Callable, Optional

import streamlit as st
import pandas as pd
import numpy as np


def do_stuff(fn: Optional[Callable] = None) -> None:
    for percent_complete in range(100):
        time.sleep(0.05)
        if fn is not None:
            fn(percent_complete + 1)
        # my_bar.progress()
    # fn()


def show_progress() -> None:
    st.header("Show progress of longer operations")

    st.write("Source code of time consuming task:")
    st.code(inspect.getsource(do_stuff))

    st.subheader("Spinner")
    with st.echo():
        if st.button("Start Spinner"):
            with st.spinner("Waiting for it to be done"):
                do_stuff()

    st.markdown('-' * 6)

    st.subheader("Progress bar")

    with st.echo():
        my_bar = st.progress(0)
        if st.button("Start Progress"):
            do_stuff(my_bar.progress)


def show_messages() -> None:
    st.header("Message types")
    with st.echo():
        st.info("This is just some information")
    with st.echo():
        st.success("This is a **success** message")
    with st.echo():
        st.warning("This is a _warning_ message")
    with st.echo():
        st.error("This is an __error__ message")
    with st.echo():
        st.exception("This is an error message")
        st.exception(RuntimeError("This is a runtime error"))


def show_utilities() -> None:
    st.header("Utility functions")

    st.subheader("Show help for an object")
    with st.echo():
        if st.button("Show help"):
            st.help(pd.DataFrame)

    st.markdown('-' * 6)

    st.subheader("Placeholder")
    with st.echo():
        placeholder = st.empty()
        st.info("This message was created **after** the placeholder!")
        choice = st.radio("Option", [None, 'markdown', 'dataframe'])

        if choice == "markdown":
            placeholder.markdown("This was written at a later point in time :wave:")
        elif choice == "dataframe":
            placeholder.dataframe(pd.DataFrame(np.random.randint(0, 100, size=(5, 4)), columns=list('ABCD')))

    st.markdown('-' * 6)

    st.subheader("Get and set options")

    st.write("""Show and change options for streamlit.  
    Available options can be viewed by entering `streamlit config show` in the terminal.  
    Option key has structure `section.optionName`.
    """)

    st.code("""
    ...
    [server]
    ...
    # Max size, in megabytes, for files uploaded with the file_uploader.
    # Default: 200
    maxUploadSize = 200
    ...
    """)

    with st.echo():
        up_size = st.get_option("server.maxUploadSize")
        st.write(f"Maximum upload size upload size is `{up_size} MB`")

    st.write("""
    #### Updating client settings 
    Changing config options currently works ony for client options, i.e.:
    * client.caching
    * client.displayEnabled
    """)


def get_sections() -> Dict[str, Callable]:
    return {
        "Show messages": show_messages,
        "Show progress": show_progress,
        "Show utilities": show_utilities
    }


def main():
    # TODO: notfications
    # TODO: progress
    # TODO: gimmicks like balloons
    if st.button("Perform slow task"):
        show_progress()
