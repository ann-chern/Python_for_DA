import streamlit as st

st.markdown('Автор: Анна Чернова')
st.write("# Добро пожаловать на главную страницу Streamlit project! 👋")

#st.sidebar.title("Разделы")
st.sidebar.success("Выберите раздел выше.")


st.markdown("В ходе проекта было необходимо исследовать наличие глобального потепления или похолодания на основе имеющегося набора данных (см. раздел 📊 Links and data)")
if st.button("📊 Links and data"):
    st.switch_page("pages/2_📊_Links_and_data.py")

st.markdown(
        """
        
        **👈 Выберите вкладку слева** чтобы увидеть разделы исследования в данном проекте

    """
    )
