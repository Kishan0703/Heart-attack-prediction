import streamlit as st
import pandas as pd
import xgboost
import numpy as np
import re


@st.cache_resource
def load_model(path: str = "xgb_model.bin"):
    try:
        model = xgboost.Booster()
        model.load_model(path)
        return model
    except Exception as e:
        return e


st.set_page_config(page_title="Heart Attack Prediction", layout="centered")

st.title("Heart Attack Prediction")

st.markdown(
    """
    <style>
    .main .block-container { max-width: 900px; padding: 2rem 2rem 4rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("Use the form below to enter patient clinical parameters and get a prediction.")

# Sidebar: examples and info
st.sidebar.header("Examples & Info")
examples = {
    "Low risk example": {
        "age": 45,
        "sex": 1,
        "cp": 0,
        "trtbps": 120,
        "chol": 180,
        "fbs": 0,
        "restecg": 0,
        "thalachh": 150,
        "exng": 0,
        "oldpeak": 0.0,
        "slp": 2,
        "caa": 0,
        "thall": 2,
    },
    "High risk example": {
        "age": 64,
        "sex": 1,
        "cp": 3,
        "trtbps": 160,
        "chol": 300,
        "fbs": 1,
        "restecg": 1,
        "thalachh": 120,
        "exng": 1,
        "oldpeak": 3.0,
        "slp": 0,
        "caa": 2,
        "thall": 3,
    },
}

selected_example = st.sidebar.selectbox("Load example patient", options=[None] + list(examples.keys()))

# Load model (cached)
model = load_model()
if isinstance(model, Exception):
    st.error(f"Failed to load model: {model}")

def _extract_int_from_label(x, default: int = 0) -> int:
    """Extract an integer inside parentheses from a label like 'Normal (0)'."""
    if isinstance(x, int):
        return x
    s = str(x)
    m = re.search(r"\((\d+)\)", s)
    if m:
        return int(m.group(1))
    # fallback: find any digits
    digits = "".join(ch for ch in s if ch.isdigit())
    return int(digits) if digits else default


with st.form("predict_form"):
    st.subheader("Patient parameters")
    # use defaults from example if available
    defaults = examples[selected_example] if selected_example else {}

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=defaults.get("age", 50), step=1)
        sex_label = st.selectbox("Sex", ("Male", "Female"), index=0 if defaults.get("sex", 1) == 1 else 1)
        sex = 1 if sex_label == "Male" else 0
        cp = st.selectbox("Chest pain type",
                          ("Asymptomatic (0)", "Atypical angina (1)", "Non-anginal pain (2)", "Typical angina (3)"),
                          index=defaults.get("cp", 0))
        # map cp label to int (e.g. 'Typical angina (3)' -> 3)
        cp_val = _extract_int_from_label(cp, default=defaults.get("cp", 0))
    with col2:
        trtbps = st.number_input("Resting blood pressure (mm Hg)", min_value=50, max_value=300, value=defaults.get("trtbps", 120), step=1)
        chol = st.number_input("Cholesterol (mg/dl)", min_value=50, max_value=600, value=defaults.get("chol", 200), step=1)
        fbs_label = st.selectbox("Fasting blood sugar > 120 mg/dl", ("No", "Yes"), index=1 if defaults.get("fbs", 0) == 1 else 0)
        fbs = 1 if fbs_label == "Yes" else 0

    col3, col4 = st.columns(2)
    with col3:
        restecg = st.selectbox("Resting ECG result",
                               ("Normal (0)", "ST-T abnormality (1)", "Left ventricular hypertrophy (2)"),
                               index=defaults.get("restecg", 0))
        thalachh = st.number_input("Max heart rate achieved", min_value=60, max_value=250, value=defaults.get("thalachh", 140), step=1)
    with col4:
        exng_label = st.selectbox("Exercise induced angina", ("No", "Yes"), index=1 if defaults.get("exng", 0) == 1 else 0)
        exng = 1 if exng_label == "Yes" else 0
        oldpeak = st.number_input("Oldpeak (ST depression)", min_value=0.0, max_value=10.0, value=defaults.get("oldpeak", 1.0), step=0.1)

    slp = _extract_int_from_label(st.selectbox("Slope of peak exercise ST segment", ("Downsloping (0)", "Flat (1)", "Upsloping (2)"), index=defaults.get("slp", 1)), default=defaults.get("slp", 1))
    caa = st.selectbox("Number of major vessels (0-3)", (0, 1, 2, 3), index=defaults.get("caa", 0))
    thall_label = st.selectbox("Thalassemia",
                         ("NULL/Unknown (0)", "Fixed defect (1)", "Normal (2)", "Reversible defect (3)"),
                         index=defaults.get("thall", 2))
    thall = _extract_int_from_label(thall_label, default=defaults.get("thall", 2))

    submit = st.form_submit_button("Predict")

    # map selected indices to numeric values expected by the model
    # Prepare DataFrame for model using keys the saved model expects
    # The original model expects: ['thall','caa','cp','oldpeak','exng','chol','thalachh']
    data_1 = pd.DataFrame({
        "thall": [int(thall)],
        "caa": [caa],
        "cp": [int(cp_val)],
        "oldpeak": [oldpeak],
        "exng": [exng],
        "chol": [chol],
        "thalachh": [thalachh],
    })

    if submit:
        if isinstance(model, Exception):
            st.error("Model not loaded. Fix model file or environment.")
        else:
            try:
                dtest = xgboost.DMatrix(data_1)
                pred_prob = model.predict(dtest)
                # model.predict returns an array
                prob_no_attack = float(pred_prob[0]) if hasattr(pred_prob, "__len__") else float(pred_prob)
                # Based on this project's labeling, the model's positive class represents 'no heart disease'
                # so probability of heart attack = 1 - prob_no_attack
                prob_attack = 1.0 - prob_no_attack

                threshold = 0.5

                # show both probabilities
                cols = st.columns(2)
                cols[0].metric("Prob (no heart attack)", f"{prob_no_attack:.3f}")
                cols[1].metric("Prob (heart attack)", f"{prob_attack:.3f}")

                # visual risk bar (percent)
                risk_pct = int(prob_attack * 100)
                st.progress(risk_pct)

                if prob_attack >= threshold:
                    st.error("Patient has risk of Heart Attack")
                else:
                    st.success("Patient has low risk of Heart Attack")

                # Save the last input in session state so we can use widgets outside the form
                st.session_state['last_input_json'] = data_1.to_json(orient="records")
                st.session_state['last_input_record'] = data_1.to_dict(orient="records")[0]
            except Exception as e:
                st.exception(e)

# After the form: show saved input summary and download button (download buttons cannot live inside forms)
if 'last_input_json' in st.session_state:
    with st.expander("Input summary"):
        st.json(st.session_state['last_input_record'])
        st.download_button("Download input as JSON", st.session_state['last_input_json'], file_name="input.json", mime="application/json")

# Sidebar action: clear last saved input/result
if st.sidebar.button("Clear last result"):
    if 'last_input_json' in st.session_state:
        del st.session_state['last_input_json']
    if 'last_input_record' in st.session_state:
        del st.session_state['last_input_record']

