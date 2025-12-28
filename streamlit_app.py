import streamlit as st

# ======= NORMES ECG PÉDIATRIQUES =======
def normes_ecg(age):
    if age < 1: return {"FC_min":100,"FC_max":160,"PR_max":120,"QRS_max":80,"QTc_max":460}
    elif age<3: return {"FC_min":90,"FC_max":150,"PR_max":130,"QRS_max":80,"QTc_max":460}
    elif age<6: return {"FC_min":80,"FC_max":140,"PR_max":140,"QRS_max":90,"QTc_max":460}
    elif age<12: return {"FC_min":70,"FC_max":120,"PR_max":160,"QRS_max":100,"QTc_max":460}
    else: return {"FC_min":60,"FC_max":100,"PR_max":180,"QRS_max":110,"QTc_max":450}

# ======= ANALYSE ECG =======
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

# ======= HYPERTROPHIE & DILATATION =======
def score_hvg(r_v6,s_v1,axe,repolarisation=False):
    score=0
    if r_v6>=35: score+=2
    if s_v1>=20: score+=1
    if axe<-30: score+=1
    if repolarisation: score+=2
    return score

def score_hvd(r_v1,s_v6,axe):
    score=0
    if r_v1>=20: score+=2
    if s_v6>=15: score+=1
    if axe>120: score+=2
    return score

def interpretation_hvg(score):
    if score<=1: return "Pas d’argument ECG pour une HVG"
    elif score<=3: return "HVG possible – à confirmer par échocardiographie"
    else: return "HVG probable – corrélation échographique recommandée"

def interpretation_hvd(score):
    if score<=1: return "Pas d’argument ECG pour une HVD"
    elif score<=3: return "HVD possible – à confirmer par échocardiographie"
    else: return "HVD probable – corrélation échographique recommandée"

def interpretation_dilatation(vg,vd):
    conclusions=[]
    if vg: conclusions.append("Dilatation VG possible")
    if vd: conclusions.append("Dilatation VD possible")
    if not conclusions: conclusions.append("Pas de dilatation ventriculaire")
    return conclusions

# ======= INTERFACE STREAMLIT =======
st.title("ECG Pédiatrique – Version Pro")
st.write("Entrez les paramètres ECG pour obtenir l'analyse complète")

# Paramètres ECG
age=st.number_input("Âge (années)",min_value=0,max_value=18,value=6)
fc=st.number_input("Fréquence cardiaque (bpm)",value=105)
pr=st.number_input("PR (ms)",value=70)
qrs=st.number_input("QRS (ms)",value=80)
qt=st.number_input("QT (ms)",value=300)
axe_qrs=st.number_input("Axe QRS (°)",value=62)

# Ondes ventriculaires
r_v6=st.number_input("Onde R V6 (mm)",value=20)
s_v1=st.number_input("Onde S V1 (mm)",value=15)
r_v1=st.number_input("Onde R V1 (mm)",value=10)
s_v6=st.number_input("Onde S V6 (mm)",value=10)
repolarisation=st.checkbox("Anomalies de repolarisation associées")

# Calcul QTc
rr=60/fc
qtc_bazett=qt/(rr**0.5)
qtc_fridericia=qt/(rr**(1/3))

st.write(f"QTc Bazett : {qtc_bazett:.1f} ms")
st.write(f"QTc Fridericia : {qtc_fridericia:.1f} ms")

st.subheader("Alerte QTc")
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
hvg_score=score_hvg(r_v6,s_v1,axe_qrs,repolarisation)
hvd_score=score_hvd(r_v1,s_v6,axe_qrs)
st.write("•",interpretation_hvg(hvg_score))
st.write("•",interpretation_hvd(hvd_score))

# Dilatation automatique à partir de cases écho
dilat_vg=st.checkbox("Dilatation VG (clinique / écho)")
dilat_vd=st.checkbox("Dilatation VD (clinique / écho)")
for d in interpretation_dilatation(dilat_vg,dilat_vd): st.write("•",d)

# Conclusion synthétique
st.subheader("Conclusion automatique")
conclusion=f"{analyse_rythme(fc,age)}, {analyse_bav(pr,age)}, {analyse_qrs(qrs,age)}. "
conclusion+=f"HVG: {interpretation_hvg(hvg_score)}, HVD: {interpretation_hvd(hvd_score)}. "
conclusion+=f"Dilatation: {', '.join(interpretation_dilatation(dilat_vg,dilat_vd))}. "
conclusion+=f"QTc Bazett: {qtc_bazett:.0f} ms ({alerte_qtc(qtc_bazett)})."
st.info(conclusion)
