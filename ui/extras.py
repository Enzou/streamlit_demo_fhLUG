from typing import Dict, Callable

import streamlit as st


def show_sessionstate() -> None:
    st.header("Session state")

    st.markdown("""Two workarounds are available to maintain state:  
    1. `session_state.py`: getter function to retrieve reference to `SessionState` instance  
    2. `st_state_patch.py`: adds `State`, `GlobalState` and `SessionState` classes to streamlit reference.  
    
    """)
    st.write("This example uses the `st_state_patch.py` solution:")

    with st.echo():
        import ui.session_state.st_state_patch

        s = st.State(is_global=False)

        if "is_authenticated" not in s or not s.is_authenticated:
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")

            if st.button("Authenticate"):
                s.is_authenticated = do_authentication()
                if s.is_authenticated:
                    s.username = user
                    s.password = pwd
                    st.success(f"{s.username} successfully authenticated!")
                else:
                    st.error(f"Failed to authenticate as {s.username}")
        else:
            st.write(f"> Authenticated as `{s.username}`")

            if st.button("Logout"):
                s.is_authenticated = False
                s.username = s.password = None


def do_authentication() -> True:
    # Just a dummy function for the demonstration of cli mode
    return True


def show_script_mode() -> None:
    st.header("Use as a regular script")

    st.markdown("It is important to set proper default for all selection controls, "
                "as there is no interactivity supported out of the box")

    with st.echo():
        lab = st.selectbox("Choose your Lab", ["Linz", "Hagenberg", "Barcelona", "Detroit", "Gdansk"], index=1)
        st.write("> :bell: Place debugger here to check correct default option")

    st.subheader("Deal with tricky widgets")
    st.write("Actions triggered by buttons need extra treatment :unamused:")
    with st.echo():
        script_mode = not st._is_running_with_streamlit

        if script_mode or st.button("Click me"):
            st.balloons()
            do_authentication()


def show_components() -> None:
    st.header("Demonstrate use of a custom component")

    st.markdown("A component is just a collection of streamlit widgets and custom functions."
                "To use a custom components simply import it and call the required function")

    st.write("This project has the following folder structure:")
    st.text("""
        .
        ├── app.py
        ├── data
        │   ├── external
        │   └── raw
        │       ├── data_1.csv
                ...
        │       └── web_1.json
        ...
        ├── ui
        │   ├── basics.py
        │   ├── components
        │   │   └── data_selector.py
        │   ├── extras.py
        │   ├── interactive.py
        ...  
    """)
    
    with st.echo():
        import ui.components.data_selector as file_selector

        file_selector.select_file("raw", st, [".csv", ".json"])

    st.markdown('-'*6)
    st.write("Help for the custom component is available via `st.help`")
    with st.echo():
        st.help(file_selector.select_file)


def show_layouts() -> None:
    st.header("Custom layouts are possible")

    st.markdown("""With quite some effort
    The used code is shamelessly copied from [Layout Experiments](https://raw.githubusercontent.com/MarcSkovMadsen/awesome-streamlit/master/gallery/layout_experiments/app.py) 
    Author is [Marc Skov Madsen](https://datamodelsanalytics.com/)
    """)

    st.markdown('-'*6)
    with st.echo():
        import src.layout_experiment as layout
        layout.main()


def get_sections() -> Dict[str, Callable]:
    return {
        "Script Mode": show_script_mode,
        "Session State": show_sessionstate,
        "Components": show_components,
        "Show Custom Layouts": show_layouts,
    }

