import streamlit as st

# ====== NORMES ECG PÉDIATRIQUES ======
def normes_ecg(age):
    if age < 1: return {"FC_min":100,"FC_max":160,"PR_max":120,"QRS_max":80,"QTc_max":460}
    elif age<3: return {"FC_min":90,"FC_max":150,"PR_max":130,"QRS_max":80,"QTc_max":460}
    elif age<6: return {"FC_min":80,"FC_max":140,"PR_max":140,"QRS_max":90,"QTc_max":460}
    elif age<12: return {"FC_min":70,"FC_max":120,"PR_max":160,"QRS_max":100,"QTc_max":460}
    else: return {"FC_min":60,"FC_max":100,"PR_max":180,"QRS_max":110,"QTc_max":450}

# ====== ANALYSE ECG ======
def analyse_rythme(fc, age):
    normes=normes_ecg(age)
    if fc<normes["FC_min"]: return "Bradycardie"
    elif fc>normes["FC_max"]: return "Tachycardie"
    else: return "Fréquence cardiaque adaptée à l’âge"

def analyse_bav(pr, age):
    normes=normes_ecg(age)
    if pr <= normes["PR_max"]: return "Conduction auriculo-ventriculaire normale"
    elif pr <= normes["PR_max"]+20: return "BAV 1er degré (fonctionnel possible)"
    else: return "BAV 1er degré suspect – contrôle recommandé"

def analyse_qrs(qrs, age):
    normes=normes_ecg(age)
    if qrs<=normes["QRS_max"]: return "Durée du QRS normale"
    elif qrs<=120: return "Retard de conduction intraventriculaire"
    else: return "Bloc de branche suspect"

def interpretation_qtc(qtc):
    if qtc<440: return "QTc normal"
    elif qtc<460: return "QTc limite"
    elif qtc<500: return "QTc prolongé"
    else: return "QTc sévèrement prolongé"

def alerte_qtc(qtc):
    if qtc>=500: return "⚠️ QTc très prolongé – risque torsade de pointes"
    elif qtc>=460: return "⚠️ QTc prolongé – surveillance cardiologique"
    else: return "QTc normal"

# ====== HYPERTROPHIE & DILATATION ======
def score_hvg(r_v5_s_v1_mm):
    if r_v5_s_v1_mm >= 27: return "HVG probable"
    elif r_v5_s_v1_mm >= 23: return "HVG possible"
    else: return "Pas d’argument ECG pour HVG"

def score_hvd(r_v1_s_v6_mm, axe_qrs):
    if r_v1_s_v6_mm >= 25 or axe_qrs > 120: return "HVD probable"
    elif r_v1_s_v6_mm >= 20: return "HVD possible"
    else: return "Pas d’argument ECG pour HVD"

def interpretation_dilatation(vg, vd):
    conclusions=[]
    if vg: conclusions.append("Dilatation VG possible")
    if vd: conclusions.append("Dilatation VD possible")
    if not conclusions: conclusions.append("Pas de dilatation ventriculaire")
    return conclusions

# ====== INTERFACE STREAMLIT ======
st.title("ECG Pédiatrique – Version Pro")
st.write("Entrez les paramètres ECG pour obtenir l'analyse complète")

# Paramètres ECG
age=st.number_input("Âge (années)",min_value=0,max_value=18,value=6)
fc=st.number_input("Fréquence cardiaque (bpm)",value=105)
pr=st.number_input("PR (ms)",value=72)
qrs=st.number_input("QRS (ms)",value=75)
qt=st.number_input("QT (ms)",value=307)
axe_qrs=st.number_input("Axe QRS (°)",value=62)

# Ondes ventriculaires
r_v6=st.number_input("R V6 (mm)",value=17)
s_v1=st.number_input("S V1 (mm)",value=12)
r_v1=st.number_input("R V1 (mm)",value=3)
s_v6=st.number_input("S V6 (mm)",value=2)
repolarisation=st.checkbox("Anomalies de repolarisation associées")

# Calcul QTc
rr=60/fc
qtc_bazett=qt/(rr**0.5)
qtc_fridericia=qt/(rr**(1/3))
st.write(f"QTc Bazett : {qtc_bazett:.1f} ms")
st.write(f"QTc Fridericia : {qtc_fridericia:.1f} ms")

# Alerte QTc
if qtc_bazett>=460: st.warning(alerte_qtc(qtc_bazett))
else: st.success(alerte_qtc(qtc_bazett))

# Analyse ECG
st.subheader("Analyse ECG automatique")
conclusions_ecg=[]
conclusions_ecg.append(analyse_rythme(fc,age))
conclusions_ecg.append(analyse_bav(pr,age))
conclusions_ecg.append(analyse_qrs(qrs,age))
conclusions_ecg.append(interpretation_qtc(qtc_bazett))
for r in conclusions_ecg: st.write("•",r)

# Morphologie ventriculaire
st.subheader("Morphologie ventriculaire")
r_v5_s_v1=r_v6+s_v1
r_v1_s_v6=r_v1+s_v6

st.write("•",score_hvg(r_v5_s_v1))
st.write("•",score_hvd(r_v1_s_v6,axe_qrs))

# Dilatation (manuel ou écho)
dilat_vg=st.checkbox("Dilatation VG (clinique / écho)")
dilat_vd=st.checkbox("Dilatation VD (clinique / écho)")
for d in interpretation_dilatation(dilat_vg,dilat_vd): st.write("•",d)

# Conclusion synthétique avec sources visibles
sources = "- Davignon 1980\n- Rijnbeek 2001\n- Redline 2020\n- Bazett 1920"
conclusion = f"**Analyse ECG**:\n"
conclusion += f"- {analyse_rythme(fc,age)}\n"
conclusion += f"- {analyse_bav(pr,age)}\n"
conclusion += f"- {analyse_qrs(qrs,age)}\n"
conclusion += f"- HVG: {score_hvg(r_v5_s_v1)}, HVD: {score_hvd(r_v1_s_v6,axe_qrs)}\n"
conclusion += f"- Dilatation: {', '.join(interpretation_dilatation(dilat_vg,dilat_vd))}\n"
conclusion += f"- QTc Bazett: {qtc_bazett:.0f} ms ({alerte_qtc(qtc_bazett)})\n\n"
conclusion += "**Sources :**\n" + sources

st.markdown(conclusion)
