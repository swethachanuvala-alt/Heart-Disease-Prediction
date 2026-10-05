"""Cached loaders so the CSV and the model are only read once per session."""
import streamlit as st

from . import ml


@st.cache_data(show_spinner=False)
def get_data():
    return ml.load_dataset()


@st.cache_resource(show_spinner=False)
def get_artifacts():
    """(scaler, model, source) — source is 'saved' or 'retrained'."""
    return ml.load_or_train(get_data())


@st.cache_data(show_spinner=False)
def get_metrics():
    scaler, model, _ = get_artifacts()
    return ml.evaluate(scaler, model, get_data())
