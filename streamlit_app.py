import streamlit as st

# ======= TITRE =======
st.title("ECG Pédiatrique – Version Pro")
st.write("Remplissez les paramètres ECG pour obtenir la conclusion clinique avancée.")

# ======= CHAMPS D'ENTRÉE =======
age = st.number_input("Âge (années)", min_value=0, max_value=18, value=5)
fc = st.number_input("Fréquence cardiaque (bpm)", min_value=30, max_value=250, value=100)
pr = st.number_input("PR (ms)", min_value=60, max_value=300, value=120)
qrs = st.number_input("QRS (ms)", min_value=40, max_value=200, value=80)
qt = st.number_input("QT (ms)", min_value=200, max_value=600, value=400)
axe_qrs = st.number_input("Axe QRS (°)", min_value=-90, max_value=180, value=60)

# Conduction
bav1 = st.checkbox("BAV 1er degré")
bav2 = st.checkbox("BAV 2e degré")
bav3 = st.checkbox("BAV 3e degré")

# Hypertrophie/dilatation ventriculaire
hvg = st.selectbox("HVG suspectée ?", ["Non", "Modérée", "Sévère"])
hvd = st.selectbox("HVD suspectée ?", ["Non", "Modérée", "Sévère"])
dil_vg = st.selectbox("Dilatation VG ?", ["Non", "Oui"])
dil_vd = st.selectbox("Dilatation VD ?", ["Non", "Oui"])

# ======= CALCUL QTc =======
if fc != 0:
    qtc_bazett = qt / ((60/fc)**0.5)
    qtc_fridericia = qt / ((60/fc)**(1/3))
else:
    qtc_bazett = qt
    qtc_fridericia = qt

qtc_bazett = round(qtc_bazett, 1)
qtc_fridericia = round(qtc_fridericia, 1)

# ======= ALERTES ET MESSAGES =======
alerte = "Normal"
messages = []

# QTc critique
if qtc_bazett > 500 or qtc_fridericia > 500:
    alerte = "Urgent"
    messages.append("QTc très long : risque torsade de pointe")

# BAV
if bav2 or bav3:
    alerte = "Urgent"
    messages.append("BAV 2e ou 3e degré détecté")
elif bav1:
    if alerte != "Urgent":
        alerte = "Attention"
        messages.append("BAV 1er degré détecté")

# HVG/HVD
for vent, val, label in [(hvg, "HVG", hvg), (hvd, "HVD", hvd)]:
    if vent == "Sévère":
        alerte = "Urgent"
        messages.append(f"{label} sévère")
    elif vent == "Modérée" and alerte != "Urgent":
        alerte = "Attention"
        messages.append(f"{label} modérée")

# Dilatation ventriculaire
if dil_vg == "Oui" or dil_vd == "Oui":
    if alerte != "Urgent":
        alerte = "Attention"
    if dil_vg == "Oui":
        messages.append("Dilatation VG détectée")
    if dil_vd == "Oui":
        messages.append("Dilatation VD détectée")

# ======= AFFICHAGE =======
st.write(f"**QTc Bazett :** {qtc_bazett} ms")
st.write(f"**QTc Fridericia :** {qtc_fridericia} ms")
st.write(f"**Alerte :** {alerte}")

# Conclusion courte
if alerte == "Normal":
    conclusion = "ECG dans les limites normales."
elif alerte == "Attention":
    conclusion = "ECG anormal, surveiller et confirmer selon contexte clinique."
else:
    conclusion = "ECG critique, nécessite avis urgent."

st.success(f"**Conclusion :** {conclusion}")

# Messages détaillés
if messages:
    st.warning("Messages cliniques :")
    for msg in messages:
        st.write(f"- {msg}")

# ======= BOUTON RÉSUMÉ =======
if st.button("Afficher résumé complet"):
    st.write("Résumé ECG pédiatrique :")
    st.write(f"- Âge : {age} ans")
    st.write(f"- FC : {fc} bpm")
    st.write(f"- PR : {pr} ms")
    st.write(f"- QRS : {qrs} ms")
    st.write(f"- QT : {qt} ms")
    st.write(f"- QTc Bazett : {qtc_bazett} ms")
    st.write(f"- QTc Fridericia : {qtc_fridericia} ms")
    st.write(f"- Axe QRS : {axe_qrs}°")
    st.write(f"- BAV 1er : {'Oui' if bav1 else 'Non'}")
    st.write(f"- BAV 2e : {'Oui' if bav2 else 'Non'}")
    st.write(f"- BAV 3e : {'Oui' if bav3 else 'Non'}")
    st.write(f"- HVG : {hvg}")
    st.write(f"- HVD : {hvd}")
    st.write(f"- Dilatation VG : {dil_vg}")
    st.write(f"- Dilatation VD : {dil_vd}")
