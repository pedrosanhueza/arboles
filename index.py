import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.markdown('''
<ol>
<li>What is the distribution of net worth among billionaires?</li>
<li>What is the distribution of age among billionaires?</li>
<li>Is there a correlation between age and net worth?</li>
<li>What are the most common industries among billionaires?</li>
</ol>
''',unsafe_allow_html=True)