
# Heart Attack Analysis Prediction



## Introduction

Heart disease is a major health concern worldwide, accounting for a significant number of deaths each year. Early detection and prevention are crucial in managing this condition. Machine learning models offer a promising approach to predicting the likelihood of heart attacks based on clinical parameters. In this study, we have developed a classification model to predict whether a patient is at risk of experiencing a heart attack based on their clinical parameters.

## Problem Statement

The aim of this study is to develop a reliable classification model that can predict the likelihood of a patient experiencing a heart attack based on their clinical parameters. By accurately identifying individuals at risk, healthcare providers can intervene early with targeted interventions and lifestyle modifications to reduce the risk of heart disease and improve patient outcomes.

**Code flow**

        * Data processing
        * EDA
        * Feature Engineering
        * Scaling and Normalization
        * Model Selection and Evaluation
        * Test the model
        * Deploying the model

**Data**

Input the below information to check whether the patient has risk of heart attack or not

Age : Age of the patient

Sex: The person’s sex (1 = male, 0 = female)


cp: chest pain type

— Value 0: asymptomatic

— Value 1: atypical angina

— Value 2: non-anginal pain

— Value 3: typical angina


trestbps: The person’s resting blood pressure (mm Hg on admission to the hospital)

chol: The person’s cholesterol measurement in mg/dl

fbs: The person’s fasting blood sugar (> 120 mg/dl, 1 = true; 0 = false)

restecg: resting electrocardiographic results

— Value 0: showing probable or definite left ventricular hypertrophy by Estes’ criteria

— Value 1: normal

— Value 2: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)

thalach: The person’s maximum heart rate achieved

exang: Exercise induced angina (1 = yes; 0 = no)

oldpeak: ST depression induced by exercise relative to rest (‘ST’ relates to positions on the ECG plot. See more here)

slope: the slope of the peak exercise ST segment — 0: downsloping; 1: flat; 2: upsloping

ca: The number of major vessels (0–3)

thal: A blood disorder called thalassemia 

Value 0: NULL (dropped from the dataset previously

Value 1: fixed defect (no blood flow in some part of the heart)

Value 2: normal blood flow

Value 3: reversible defect (a blood flow is observed but it is not normal)

target: Heart disease (1 = no, 0= yes)


## Things implemented

- Exploratory Data Analysis
- Finding **Mutual information** with the target feature
- Applying **Decision tree classification, Random forest classifiaction and XGB classification** algorithms with different feature parameters and picking up the best model based on AUC score and accuracy
- Used **Matplotlib and Seaborn Heatmap** for visualization
  
## Deploying model

* Implemented the model in **Streamlit**.
* XGB Model will predict whether a patient is at risk of experiencing a heart attack based on their clinical parameters.

## Things to try it out next!
* Applying crossvalidation concepts in model training
* Applying Pipeline concepts in model training
# Heart Attack Analysis & Prediction

This repository contains a Streamlit app that predicts the likelihood of a heart attack based on clinical parameters. The project includes a trained XGBoost model and a Streamlit frontend (`heart.py`).

## Quick summary

- Streamlit app: `heart.py`
- Model files: `xgb_model.bin` (legacy binary) and `finalized_model_classification.sav` (pickle)
- Frontend: Streamlit — improved layout, examples, probability display, and download of inputs.

## Quick start (local)

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
streamlit run heart.py
```

4. Open http://localhost:8501 in your browser.

## Notes about XGBoost and the model file

- The included `xgb_model.bin` is in XGBoost's legacy binary format. Newer XGBoost releases (3.x) removed that format. To keep the repo runnable out of the box the project currently pins `xgboost==1.7.6` in `requirements.txt`.
- Recommended long-term: convert `xgb_model.bin` to JSON or UBJ and then upgrade to latest `xgboost`. See the `Converting` section below.

## Convert legacy model to JSON (optional)

Use an environment with `xgboost==1.7.6` to convert the model:

```python
import xgboost
bst = xgboost.Booster()
bst.load_model('xgb_model.bin')
bst.save_model('xgb_model.json')
```

Then test loading the JSON model with the newer XGBoost API.

## Deploying to Streamlit Community Cloud

Streamlit Cloud requires the app code to be hosted in a GitHub repository. Steps:

1. Create a GitHub repo and push this project (see `deploy.sh` and `DEPLOY.md` included in this repo for helpers).
2. Go to https://share.streamlit.io → New app → select your GitHub repo and branch → set the app file path to `heart.py` → deploy.

If you prefer other hosts (Render, Railway, Fly, Heroku), you can containerize or use their git-based deploy flows.

## What changed in the Streamlit UI

- Inputs grouped in a two-column form
- Sidebar examples to quickly load low/high risk samples
- Cached model loader
- Clear results and download input JSON
- Probability metrics: shows both `Prob (no heart attack)` and `Prob (heart attack)` and a visual risk bar

## Next steps I can help with

- Convert the model to JSON and upgrade `xgboost` to latest stable release.
- Migrate the frontend to React + FastAPI and provide Dockerfiles + deployment manifests.
- Add unit tests and CI that deploys to Streamlit Cloud on push.

---

If you'd like me to push this repo to GitHub and create the Streamlit deployment for you, tell me your GitHub username and I'll run the helper script (requires `gh` CLI and authentication).

