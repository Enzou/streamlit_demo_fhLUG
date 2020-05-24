from typing import Dict, Callable
import streamlit as st
import pandas as pd


def show_general_widgets() -> None:
    st.header("General widgets")
    st.subheader("Checkbox")
    with st.echo():
        feature_flag = st.checkbox("Enable feature flag?")
        st.write(f"Feature is `{'enabled' if feature_flag else 'disabled'}`")

    st.markdown("------")

    st.subheader("Button")
    with st.echo():
        if st.button("celebrate"):
            st.balloons()


def show_selection_widgets() -> None:
    st.header("Selection widgets")
    st.subheader("Radio buttons")
    with st.echo():
        option = st.radio("Choose wisely:", ["Blue Pill", "Red Pill"], index=1)
        st.write(f"You chose: {option}")

    st.markdown("------")
    st.subheader("Selectbox")
    with st.echo():
        option = st.selectbox("Choose wisely:", ["Blue Pill", "Red Pill"], index=1)
        st.write(f"You chose: {option}")

    st.markdown("------")
    st.subheader("Multiselect")
    with st.echo():
        tags = st.multiselect("Streamlit is", ["awesome", "lit", "fancy", "boring"], default=["awesome"])
        st.write(f"You will chose: {tags}")


def show_text_widgets() -> None:
    st.header("Text input widgets")
    st.subheader("Text input")
    with st.echo():
        name = st.text_input("What is your name?", value="-")
        st.write(f"Hello, {name} :wave:")

    st.write("This widget can also be used to enter secrets:")
    with st.echo():
        secret = st.text_input("What is your name?", type="password")
        st.write(f"I know your secret: _{secret}_")

    st.markdown("------")

    st.subheader("Text area")
    with st.echo():
        name = st.text_area("Please enter text to analyzer", value="1st line\n2nd line\n3rd line")


def show_misc_widgets() -> None:
    st.header("Misc widgets")
    st.subheader("Date input")
    with st.echo():
        date = st.date_input("What day is today?")
        st.write(f"Today is {date}")

    st.markdown("------")
    st.subheader("Time input")
    with st.echo():
        time = st.time_input("What time is it?")
        st.write(f"Currently it is {time}")

    st.markdown("------")
    st.subheader("File Uploader")
    st.write("This widget is useful for deployed ML apps hosted on a remote server. "
             "Default limit of uploaded file is 200MB, but the limit can be adjusted using `server.maxUploadSize`")
    with st.echo():
        csv = st.file_uploader("Please choose a CSV file", type="csv", encoding="utf-8")
        if csv is not None:
            df = pd.read_csv(csv)
            st.write(df)


def show_numeric_widgets() -> None:
    st.header("Numeric widgets")
    st.subheader("Slider")
    with st.echo():
        score = st.slider("How awesome is streamlit?",
                          min_value=0., max_value=10., value=5.,
                          step=0.5, format="%.1f")

    st.write(f"_Note: the type of the (min/max/.) value and step must be of the same type, i.e. mixing float and int leads to an error_")
    st.write("-"*6)

    st.subheader("Number input")
    with st.echo():
        st.number_input("How awesome is streamlit?",
                        min_value=0., max_value=10., value=5.,
                        step=0.5, format="%.1f")
    st.write(f"_Note: the type of the (min/max/.) value and step must be of the same type, i.e. mixing float and int leads to an error_")


def get_sections() -> Dict[str, Callable]:
    return {
        "Show general widgets": show_general_widgets,
        "Show selection widgets": show_selection_widgets,
        "Show text widgets": show_text_widgets,
        "Show numeric widgets": show_numeric_widgets,
        "Show misc widgets": show_misc_widgets,
    }

