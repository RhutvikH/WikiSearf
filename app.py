import streamlit as st
from main import main


st.title("WikiSearf")

query: str = st.text_input("Perform a search: ")
stuff=main(query)

for i in stuff:
    st.subheader(i[1])
    st.markdown(f"*Description:* {i[2]}")
    st.write(f"*Url:* {i[3]}")
    st.write(" ")