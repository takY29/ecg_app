import streamlit as st
# ========= MOTEUR ECG PÉDIATRIQUE – ÉTAPE 1 =========

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


def analyse_bav(pr, fc, age):
    normes = normes_ecg_pediatriques(age)
    if pr <= normes["PR_max"]:
        return "Conduction auriculo-ventriculaire normale"
    if fc < normes["FC_min"]:
        return "BAV du 1er degré probablement fonctionnel (vagal)"
    return "BAV du 1er degré"


def analyse_qrs(qrs, age):
    normes = normes_ecg_pediatriques(age)
    if qrs <= normes["QRS_max"]:
        return "Durée du QRS normale"
    if qrs < 120:
        return "Retard de conduction intraventriculaire"
    return "Bloc de branche suspect"


def interpretation_qtc(qtc):
    if qtc < 440:
        return "QTc normal"
    elif qtc < 460:
        return "QTc limite"
    elif qtc < 500:
        return "QTc allongé"
    else:
        return "QTc sévèrement allongé (haut risque rythmique)"


def interpretation_ecg(age, fc, pr, qrs, qtc):
    conclusions = []
    normes = normes_ecg_pediatriques(age)

    if fc < normes["FC_min"]:
        conclusions.append("Bradycardie")
    elif fc > normes["FC_max"]:
        conclusions.append("Tachycardie")
    else:
        conclusions.append("Fréquence cardiaque adaptée à l’âge")

    conclusions.append(analyse_bav(pr, fc, age))
    conclusions.append(analyse_qrs(qrs, age))
    conclusions.append(interpretation_qtc(qtc))

    return conclusions
