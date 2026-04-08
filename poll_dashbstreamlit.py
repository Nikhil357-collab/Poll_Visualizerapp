import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
df = pd.read_csv('cleaned_poll_data.csv')
st.title("Poll Results Visualizer")

# Sidebar filters
st.sidebar.header("Filter Responses")
selected_tool = st.sidebar.multiselect("Select Preferred Tool(s):", df['Preferred Tool'].unique(), default=df['Preferred Tool'].unique())
filtered_df = df[df['Preferred Tool'].isin(selected_tool)]

# File Upload
# =============================
uploaded_file = st.file_uploader("Upload Feedback Data CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

# Show dataset preview
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)
# Bar chart - Preferred Tools
st.subheader("Tool Preference")
tool_counts = filtered_df['Preferred Tool'].value_counts()
st.bar_chart(tool_counts)
# Line plot - Submissions Over Time
st.subheader("Responses Over Time")
df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
daily = df.groupby('Date').size()
st.line_chart(daily)
# Word Cloud - Feedback
st.subheader("Feedback Word Cloud")
text = ' '.join(filtered_df['Feedback'].dropna().astype(str))
if text:
    wordcloud = WordCloud(width=800, height=400, background_color='black').generate(text)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)
else:
    st.write("No feedback available to generate word cloud.")


