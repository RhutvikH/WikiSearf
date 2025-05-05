import streamlit as st
from main import main


st.title("WikiSearf")

query: str = st.text_input("Perform a search: ", value="Search here")
main_docs, num_docs = main(query)

for idx, i in enumerate(main_docs):
    if idx == num_docs:
        st.write("---")
        # st.write(" ")
        st.warning("The rest of the results might not be what you're looking for.")
    st.write("---")
    st.subheader(i[1])
    st.markdown(f"*Description:* {i[3]}")
    # st.write(f"*Url:* {i[3]}")
    st.link_button(label=f"{i[1]} Wiki", url=i[2])
    # st.page_link.
    st.write(" ")
    
    print(num_docs)
