from collections import OrderedDict
from typing import Tuple, Optional

import argparse
import streamlit as st

import ui.intermediate
import ui.basics
import ui.interactive
import ui.visualization
import ui.utility
import ui.extras


PAGES = OrderedDict({
    "Basic Elements": ui.basics,
    "Interactivity": ui.interactive,
    "Utility Features": ui.utility,
    "Visualization": ui.visualization,
    "Intermediate Features": ui.intermediate,
    "Undocumented Features": ui.extras
})


def main(target_section: Optional[str]) -> None:
    st.sidebar.title("Topics")
    pages = list(PAGES.keys())

    if target_section is not None:
        initial_page, initial_section = target_section.split('/')
    else:
        initial_page = initial_section = None

    page_idx = pages.index(initial_page) if initial_page is not None else 0
    sel_page = st.sidebar.radio("", pages, index=page_idx)
    st.sidebar.markdown('-'*6)

    page = PAGES[sel_page]

    st.image(
        "https://aws1.discourse-cdn.com/standard10/uploads/streamlit/original/2X/7/7cbf2ca198cd15eaaeb2e177a37b2c1c8c9a6e33.png",
        use_column_width=True)
    st.title(sel_page)
    st.sidebar.header("Section")

    # display sections available in selected page
    section_map = page.get_sections()
    sections = list(section_map.keys())
    section_idx = sections.index(initial_section) if initial_section is not None else 0
    section = st.sidebar.radio("", options=sections, index=section_idx)
    section_map[section]()  # call function set in the get_section() function on each page
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrate capabilities of Streamlit")
    parser.add_argument('--section', dest="section", default=None, help='Path to the desired section (default: None)')
    args = parser.parse_args()

    default_selection = args.section
    main(default_selection)
