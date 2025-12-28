import streamlit as st

# ========= NORMES ECG PÉDIATRIQUES =========

def normes_ecg_pediatriques(age):
    if age < 1:
        return {"FC_min": 100, "FC_max": 160, "PR_max": 120, "QRS_max": 80, "QTc_max": 460}
    elif age < 3:
        return {"FC_min": 90, "FC_max": 150, "PR_max": 130, "QRS_max": 80, "QTc_max": 460}
    elif age < 6:
        return {"FC_min": 80, "FC_max": 140, "PR_max": 140, "QRS_max": 90, "QTc_max": 460}
    elif age < 12:
        return {"FC_min": 70, "FC_max": 120, "PR_max": 160, "QRS_max": 100, "QTc_max": 460}
    else:
        return {"FC_min": 60, "FC_max": 100, "PR_max": 180, "QRS_max": 110, "QTc_max": 450}

# ========= ANALYSE DU RYTHME =========

def analyse_rythme(fc, age):
    normes = normes_ecg_pediatriques(age)
    if fc < normes["FC_min"]:
        return "Rythme sinusal lent (bradycardie)"
    elif fc > normes["FC_max"]:
        return "Rythme sinusal rapide (tachycardie)"
    else:
        return "Rythme sinusal normal"

# ========= ANALYSE BAV =========

def analyse_bav(pr, age):
    normes = normes_ecg_pediatriques(age)
    if pr <= normes["PR_max"]:
        return "Conduction auriculo-ventriculaire normale"
    else:
        return "Bloc auriculo-ventriculaire du 1er degré (PR allongé pour l’âge)"

# ========= ANALYSE QRS =========

def analyse_qrs(qrs, age):
    normes = normes_ecg_pediatriques(age)
    if qrs <= normes["QRS_max"]:
        return "Durée du QRS normale"
    elif qrs <= 110:
        return "Retard de conduction intraventriculaire"
    else:
        return "Bloc de branche suspect"

# ========= QTc =========

def interpretation_qtc(qtc):
    if qtc < 440:
        return "QTc normal"
    elif qtc < 460:
        return "QTc limite"
    elif qtc < 500:
        return "QTc prolongé"
    else:
        return "QTc sévèrement prolongé (haut risque rythmique)"

def alerte_qtc(qtc):
    if qtc >= 500:
        return "⚠️ QTc très prolongé – risque rythmique majeur"
    elif qtc >= 460:
        return "⚠️ QTc prolongé – surveillance cardiologique recommandée"
    elif qtc >= 440:
        return "QTc limite"
    else:
        return "QTc normal"

# ========= INTERPRÉTATION GLOBALE =========

def interpretation_ecg(age, fc, pr, qrs, qtc):
    conclusions = []
    conclusions.append(analyse_rythme(fc, age))
    conclusions.append(analyse_bav(pr, age))
    conclusions.append(analyse_qrs(qrs, age))
    conclusions.append(interpretation_qtc(qtc))
    return conclusions

# ========= HYPERTROPHIE =========

def score_hvg(r_v6, s_v1, axe_qrs, repolarisation=False):
    score = 0
    if r_v6 >= 35:
        score += 2
    if s_v1 >= 20:
        score += 1
    if axe_qrs < -30:
        score += 1
    if repolarisation:
        score += 2
    return score

def interpretation_hvg(score):
    if score <= 1:
        return "Pas d’argument ECG pour une HVG"
    elif score <= 3:
        return "HVG possible – à confronter à l’échocardiographie"
    else:
        return "HVG probable – corrélation échographique recommandée"

def score_hvd(r_v1, s_v6, axe_qrs):
    score = 0
    if r_v1 >= 20:
        score += 2
    if s_v6 >= 15:
        score += 1
    if axe_qrs > 120:
        score += 2
    return score

def interpretation_hvd(score):
    if score <= 1:
        return "Pas d’argument ECG pour une HVD"
    elif score <= 3:
        return "HVD possible – à confronter à l’échocardiographie"
    else:
        return "HVD probable – corrélation échographique recommandée"

# ========= DILATATION =========

def interpretation_dilatation(vg, vd):
    conclusions = []
    if vg:
        conclusions.append("Aspect compatible avec une dilatation ventriculaire gauche")
    if vd:
        conclusions.append("Aspect compatible avec une dilatation ventriculaire droite")
    if not conclusions:
        conclusions.append("Pas d’argument pour une dilatation ventriculaire")
    return conclusions

# ========= INTERFACE STREAMLIT =========

st.title("ECG Pédiatrique – Version Pro")
st.write("Interprétation ECG pédiatrique automatisée – niveau expert")

age = st.number_input("Âge (années)", min_value=0, max_value=18, value=6)
fc = st.number_input("Fréquence cardiaque (bpm)", value=105)
pr = st.number_input("PR (ms)", value=120)
qrs = st.number_input("QRS (ms)", value=80)
qt = st.number_input("QT (ms)", value=320)
axe_qrs = st.number_input("Axe QRS (°)", value=60)

# ========= CALCUL QTc (CORRIGÉ) =========

qt_sec = qt / 1000
rr = 60 / fc

qtc_bazett = qt_sec / (rr ** 0.5) * 1000
qtc_fridericia = qt_sec / (rr ** (1/3)) * 1000

st.write(f"QTc Bazett : {qtc_bazett:.1f} ms")
st.write(f"QTc Fridericia : {qtc_fridericia:.1f} ms")

st.subheader("Alerte QTc")
if qtc_bazett >= 460:
    st.warning(alerte_qtc(qtc_bazett))
else:
    st.success(alerte_qtc(qtc_bazett))

# ========= CONCLUSION ECG =========

st.subheader("Analyse ECG automatique")
resultats = interpretation_ecg(age, fc, pr, qrs, qtc_bazett)
for r in resultats:
    st.write("•", r)

# ========= MORPHOLOGIE VENTRICULAIRE =========

st.subheader("Morphologie ventriculaire")

r_v6 = st.number_input("Onde R en V6 (mm)", value=20)
s_v1 = st.number_input("Onde S en V1 (mm)", value=15)
r_v1 = st.number_input("Onde R en V1 (mm)", value=10)
s_v6 = st.number_input("Onde S en V6 (mm)", value=10)

repolarisation = st.checkbox("Anomalies de repolarisation associées")

hvg_score = score_hvg(r_v6, s_v1, axe_qrs, repolarisation)
hvd_score = score_hvd(r_v1, s_v6, axe_qrs)

st.write("•", interpretation_hvg(hvg_score))
st.write("•", interpretation_hvd(hvd_score))

dilat_vg = st.checkbox("Dilatation VG (clinique / écho)")
dilat_vd = st.checkbox("Dilatation VD (clinique / écho)")

for d in interpretation_dilatation(dilat_vg, dilat_vd):
    st.write("•", d)

        score += 1
    if axe_qrs < -30:
        score += 1
    if repolarisation:
        score += 2
    return score


def interpretation_hvg(score):
    if score <= 1:
        return "Pas d’argument électrocardiographique pour une HVG"
    elif score <= 3:
        return "HVG possible (faible probabilité)"
    else:
        return "HVG probable (arguments électrocardiographiques présents)"


def score_hvd(r_v1, s_v6, axe_qrs):
    score = 0
    if r_v1 >= 20:
        score += 2
    if s_v6 >= 15:
        score += 1
    if axe_qrs > 120:
        score += 2
    return score


def interpretation_hvd(score):
    if score <= 1:
        return "Pas d’argument électrocardiographique pour une HVD"
    elif score <= 3:
        return "HVD possible (faible probabilité)"
    else:
        return "HVD probable (arguments électrocardiographiques présents)"


def interpretation_dilatation(vg, vd):
    conclusions = []
    if vg:
        conclusions.append("Aspect compatible avec une dilatation ventriculaire gauche")
    if vd:
        conclusions.append("Aspect compatible avec une dilatation ventriculaire droite")
    if not conclusions:
        conclusions.append("Pas d’argument pour une dilatation ventriculaire")
    return conclusions
# ========= INTERFACE STREAMLIT =========

st.title("ECG Pédiatrique – Version Pro")
st.write("Remplissez les paramètres ECG pour obtenir une interprétation clinique avancée.")

age = st.number_input("Âge (années)", min_value=0, max_value=18, value=6)
fc = st.number_input("Fréquence cardiaque (bpm)", value=105)
pr = st.number_input("PR (ms)", value=72)
qrs = st.number_input("QRS (ms)", value=75)
qt = st.number_input("QT (ms)", value=307)
axe_qrs = st.number_input("Axe QRS (°)", value=62)

# QTc
qtc_bazett = qt / ((60 / fc) ** 0.5)
qtc_fridericia = qt / ((60 / fc) ** (1/3))

st.write(f"QTc Bazett : {qtc_bazett:.1f} ms")
st.write(f"QTc Fridericia : {qtc_fridericia:.1f} ms")

st.subheader("Analyse ECG automatique")
resultats = interpretation_ecg(age, fc, pr, qrs, qtc_bazett)
for r in resultats:
    st.write("•", r)

# ========= MORPHOLOGIE VENTRICULAIRE =========

st.subheader("Morphologie ventriculaire")

r_v6 = st.number_input("Onde R en V6 (mm)", value=20)
s_v1 = st.number_input("Onde S en V1 (mm)", value=15)
r_v1 = st.number_input("Onde R en V1 (mm)", value=10)
s_v6 = st.number_input("Onde S en V6 (mm)", value=10)

repolarisation = st.checkbox("Anomalies de repolarisation associées")

hvg_score = score_hvg(r_v6, s_v1, axe_qrs, repolarisation)
hvd_score = score_hvd(r_v1, s_v6, axe_qrs)

st.write("•", interpretation_hvg(hvg_score))
st.write("•", interpretation_hvd(hvd_score))

dilat_vg = st.checkbox("Dilatation VG (clinique / écho)")
dilat_vd = st.checkbox("Dilatation VD (clinique / écho)")

for d in interpretation_dilatation(dilat_vg, dilat_vd):
    st.write("•", d)
