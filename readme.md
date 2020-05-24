# Streamlit Demo Application

This application was created to show capabilities of [Streamlit](http://streamlit.io/) at the time of writing (`version 0.57`).
All the explained functions and features are spread across several pages, each divided into several sections.



## Structure

The entry point for the application is `app.py`. This script is executed by `streamlit`.
In the folder `ui` is all the code related to `streamlit`.
Each page has its own file with a self-descriptive name.
All pages are imported into `app.py` from where they are accessed.

The pages are:
 - `basics.py`: Explanation of basic elements, like widgets to:
    - display text 
    - display tabular data
    - display multimedia content
 - `interactive.py`: Overview of interactive controls:
    - general (i.e. button and checkbox)
    - selection widgets
    - text input 
    - numeric inputs
    - misc widgets (i.e. date/time selector and file uploader)
 - `utility.py`: Utility features
    - show different kind of messages 
    - displaying progress and dealing with long running processes  
    - other utility functions like showing help, placeholder and streamlit options
 - `visualization.py`: showcase of support for different visualization libraries
    - basic usage of most common charting libraries
    - more specific cases like maps, 3D data and graphs  
 - `intermediate.py`: covers more complex but still essential functions
    - caching, basic usage of the core function of streamlit
    - advanced caching covers ways to fine tune caching
    - dynamic updating is supported by adding data at a later point to certain streamlit widgets
 - `extras.py`: Undocumented features are either not yet officially supported or just tips and tricks from experience
    - Script mode refers to a streamlit app being run as a regular python script. With this the application can be debugged with well known tools and IDEs
    - with session state can data be stored across multiple interactions and navigation between pages
    - as all is just standard python, individual widgets can be combined and reused in the form of custom components
    - layout is also possible, but not trivial or very practical (code just shows experiments from another user)
 


## Installation

1. Clone this repository
2. _optional:_ create virtual environment
3. install `streamlit` and dependencies
4. run application


```shell
# clone repository
git clone https://github.com/Enzou/streamlit_demo_fhLUG

# navigate to clone repository
cd streamlit-demo

# create and use virtual environment
python -m venv ./venv
source ./venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run demo application
streamlit run app.py
```
