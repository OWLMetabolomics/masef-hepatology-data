#!/usr/bin/env python
# coding: utf-8

import pandas as pd

data = pd.read_csv('../data/masef-hepatology-data.csv')


data.head(10)


data.Biopsy.value_counts()


data_derivation = \
pd.DataFrame({
    'Biopsy': data.loc[data.Cohort == 'Derivation', 'Biopsy'],
'MASEF': ['Not at-risk MASH' if x <= 0.330 else 'At-risk MASH' for x in data.loc[data.Cohort == 'Derivation', 'OWLiver at-risk MASH Score']]})

data_validation = \
pd.DataFrame({
    'Biopsy': data.loc[data.Cohort == 'Validation', 'Biopsy'],
'MASEF': ['Not at-risk MASH' if x <= 0.330 else 'At-risk MASH' for x in data.loc[data.Cohort == 'Validation', 'OWLiver at-risk MASH Score']]})


pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True)


sensitivity = (pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[0,0] / \
               pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[2,0])

print(f"Sensitivity: {sensitivity:.3f}")


specificity = (pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[1,1] / \
               pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[2,1])

print(f"Specificity: {specificity:.3f}")


ppv = (pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[0,0] / \
               pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[0,2])

print(f"PPV: {ppv:.3f}")



npv = (pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[1,1] / \
               pd.crosstab(data_derivation.MASEF, data_derivation.Biopsy, margins = True).iloc[1,2])

print(f"NPV: {npv:.3f}")


pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True)



sensitivity = (pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[0,0] / \
               pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[2,0])

print(f"Sensitivity: {sensitivity:.3f}")



specificity = (pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[1,1] / \
               pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[2,1])

print(f"Specificity: {specificity:.3f}")


ppv = (pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[0,0] / \
               pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[0,2])

print(f"PPV: {ppv:.3f}")

npv = (pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[1,1] / \
               pd.crosstab(data_validation.MASEF, data_validation.Biopsy, margins = True).iloc[1,2])

print(f"NPV: {npv:.3f}")

from sklearn.metrics import roc_curve, roc_auc_score

auc_d = \
roc_auc_score(y_true = [0 if x == 'Not at-risk MASH' else 1 for x in data.loc[data.Cohort == 'Derivation', 'Biopsy']],
          y_score = data.loc[data.Cohort == 'Derivation', 'OWLiver at-risk MASH Score'])

print(f"AUC: {auc_d:.2f}")

auc_v = \
roc_auc_score(y_true = [0 if x == 'Not at-risk MASH' else 1 for x in data.loc[data.Cohort == 'Validation', 'Biopsy']],
          y_score = data.loc[data.Cohort == 'Validation', 'OWLiver at-risk MASH Score'])
print(f"AUC: {auc_v:.2f}")

fpr_d, tpr_d, thresholds = \
roc_curve(y_true = [0 if x == 'Not at-risk MASH' else 1 for x in data.loc[data.Cohort == 'Derivation', 'Biopsy']],
          y_score = data.loc[data.Cohort == 'Derivation', 'OWLiver at-risk MASH Score'])
fpr_v, tpr_v, thresholds = \
roc_curve(y_true = [0 if x == 'Not at-risk MASH' else 1 for x in data.loc[data.Cohort == 'Validation', 'Biopsy']],
          y_score = data.loc[data.Cohort == 'Validation', 'OWLiver at-risk MASH Score'])

import matplotlib.pyplot as plt

fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (6,6))

ax.plot(fpr_d, tpr_d, linewidth = 3, label = f"Derivation Cohort, AUC: {auc_d:.2f}")
ax.plot(fpr_v, tpr_v, linewidth = 3, label = f"Validation Cohort, AUC: {auc_v:.2f}")
ax.grid(axis = 'both', linestyle = ':')

ax.set_xlabel(r'False Positive Rate (FPR)', fontsize = 12)
ax.set_ylabel(r'True Positive Rate (TPR)', fontsize = 12)

ax.legend()
plt.show()

