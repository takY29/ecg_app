import streamlit as st

st.title("Test ECG Pédiatrique")
st.write("Si tu vois ça, Streamlit fonctionne correctement.")

age = st.number_input("Âge de l'enfant (années)", min_value=0, max_value=18, value=5)
fc = st.number_input("Fréquence cardiaque (bpm)", min_value=30, max_value=250, value=100)

st.write(f"Âge : {age} ans")
st.write(f"Fréquence cardiaque : {fc} bpm")

if st.button("Test"):
    st.success("Tout fonctionne ! 🎉")
