import streamlit as st

# ====== NORMES ECG PÉDIATRIQUES ======
def normes_ecg(age):
    if age < 1:
        return {"FC_min":100,"FC_max":160,"PR_min":80,"PR_max":120,"QRS_max":80,"QTc_max":460}
    elif age < 3:
        return {"FC_min":90,"FC_max":150,"PR_min":90,"PR_max":130,"QRS_max":80,"QTc_max":460}
    elif age < 6:
        return {"FC_min":80,"FC_max":140,"PR_min":100,"PR_max":140,"QRS_max":90,"QTc_max":460}
    elif age < 12:
        return {"FC_min":70,"FC_max":120,"PR_min":110,"PR_max":160,"QRS_max":100,"QTc_max":460}
    else:
        return {"FC_min":60,"FC_max":100,"PR_min":120,"PR_max":160,"QRS_max":100,"QTc_max":440}


# ====== ANALYSE ECG ======

def analyse_rythme(fc, age):
    normes = normes_ecg(age)
    if fc < normes["FC_min"]:
        return "Bradycardie pour l’âge"
    elif fc > normes["FC_max"]:
        return "Tachycardie pour l’âge"
    else:
        return "Fréquence cardiaque adaptée à l’âge"


def analyse_bav(pr, age):
    normes = normes_ecg(age)
    if pr < normes["PR_min"]:
        return "PR court pour l’âge"
    elif pr <= normes["PR_max"]:
        return "Conduction auriculo-ventriculaire normale"
    else:
        return "Bloc auriculo-ventriculaire du 1er degré (PR allongé pour l’âge)"


def analyse_qrs(qrs, age):
    normes = normes_ecg(age)
    if qrs <= normes["QRS_max"]:
        return "Durée du QRS normale pour l’âge"
    elif qrs <= normes["QRS_max"] + 20:
        return "Retard de conduction intraventriculaire"
    else:
        return "Bloc de branche suspect"


def interpretation_qtc(qtc, age):
    normes = normes_ecg(age)
    if qtc <= normes["QTc_max"]:
        return "QTc normal pour l’âge"
    elif qtc <= normes["QTc_max"] + 20:
        return "QTc limite"
    elif qtc < 500:
        return "QTc prolongé"
    else:
        return "QTc sévèrement prolongé"


def alerte_qtc(qtc):
    if qtc >= 500:
        return "⚠️ QTc très prolongé – risque de torsades de pointes"
    elif qtc >= 460:
        return "⚠️ QTc prolongé – surveillance cardiologique"
    else:
        return "QTc sans alerte immédiate"


# ====== MICROVOLTAGE ======
def analyse_microvoltage(qrs_membres=None, qrs_precordiales=None):
    if qrs_membres is None and qrs_precordiales is None:
        return "Microvoltage non analysable"
    if (qrs_membres is not None and qrs_membres < 5) or \
       (qrs_precordiales is not None and qrs_precordiales < 10):
        return "Microvoltage électrique suspect"
    else:
        return "Amplitude des QRS conservée"


# ====== SUSPICION WPW (PR + QRS UNIQUEMENT) ======
def suspicion_wpw(pr, qrs, age):
    normes = normes_ecg(age)
    if pr < normes["PR_min"] and qrs > normes["QRS_max"]:
        return "Suspicion de pré-excitation ventriculaire (WPW à discuter)"
    elif pr < normes["PR_min"]:
        return "PR court isolé – pré-excitation non confirmée"
    else:
        return "Pas d’argument ECG pour une pré-excitation"


# ====== HYPERTROPHIE & DILATATION ======
def score_hvg(r_v5_s_v1_mm):
    if r_v5_s_v1_mm >= 27:
        return "HVG probable"
    elif r_v5_s_v1_mm >= 23:
        return "HVG possible"
    else:
        return "Pas d’argument ECG pour HVG"


def score_hvd(r_v1_s_v6_mm, axe_qrs):
    if r_v1_s_v6_mm >= 25 or axe_qrs > 120:
        return "HVD probable"
    elif r_v1_s_v6_mm >= 20:
        return "HVD possible"
    else:
        return "Pas d’argument ECG pour HVD"


def interpretation_dilatation(vg, vd):
    conclusions = []
    if vg:
        conclusions.append("Dilatation VG possible")
    if vd:
        conclusions.append("Dilatation VD possible")
    if not conclusions:
        conclusions.append("Pas de dilatation ventriculaire")
    return conclusions


# ====== INTERFACE STREAMLIT ======
st.title("ECG Pédiatrique – Version Pro")

age = st.number_input("Âge (années)", 0, 18, 6)
fc = st.number_input("Fréquence cardiaque (bpm)", value=105)
pr = st.number_input("PR (ms)", value=72)
qrs = st.number_input("QRS (ms)", value=75)
qt = st.number_input("QT (ms)", value=307)
axe_qrs = st.number_input("Axe QRS (°)", value=62)

# Voltages
r_v6 = st.number_input("R V6 (mm)", value=17)
s_v1 = st.number_input("S V1 (mm)", value=12)
r_v1 = st.number_input("R V1 (mm)", value=3)
s_v6 = st.number_input("S V6 (mm)", value=2)

qrs_membres = st.number_input("Amplitude QRS dérivations membres (mm)", value=8)
qrs_precordiales = st.number_input("Amplitude QRS précordiales (mm)", value=15)

# QTc
rr = 60 / fc
qtc_bazett = qt / (rr ** 0.5)
st.write(f"QTc Bazett : {qtc_bazett:.1f} ms")

# Analyse ECG
st.subheader("Analyse ECG automatique")
st.write("•", analyse_rythme(fc, age))
st.write("•", analyse_bav(pr, age))
st.write("•", analyse_qrs(qrs, age))
st.write("•", interpretation_qtc(qtc_bazett, age))
st.write("•", suspicion_wpw(pr, qrs, age))
st.write("•", analyse_microvoltage(qrs_membres, qrs_precordiales))

# Morphologie ventriculaire
st.subheader("Morphologie ventriculaire")
st.write("•", score_hvg(r_v6 + s_v1))
st.write("•", score_hvd(r_v1 + s_v6, axe_qrs))

# Dilatation
dilat_vg = st.checkbox("Dilatation VG")
dilat_vd = st.checkbox("Dilatation VD")
for d in interpretation_dilatation(dilat_vg, dilat_vd):
    st.write("•", d)
