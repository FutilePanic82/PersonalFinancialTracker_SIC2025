"""
classifier.py — SVM + DistilBERT real-time concept classifier.

The .pkl files were trained with DistilBERT embeddings (SVM3.py), so we keep
the same tokenizer/model here to ensure consistency.
"""
from __future__ import annotations

import logging
import os

import joblib
import numpy as np
import torch
from transformers import DistilBertTokenizer, DistilBertModel

logger = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(__file__)
_SVM_PATH = os.path.join(_BASE, "modelo_svm_entrenado.pkl")
_PCA_PATH = os.path.join(_BASE, "pca_entrenado.pkl")
_LE_PATH  = os.path.join(_BASE, "le_entrenado.pkl")

# ── Device ─────────────────────────────────────────────────────────────────────
_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Load models once at import-time ────────────────────────────────────────────
logger.info("Loading DistilBERT tokenizer and model …")
_tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
_bert      = DistilBertModel.from_pretrained("distilbert-base-uncased").to(_DEVICE)
_bert.eval()

logger.info("Loading SVM / PCA / LabelEncoder …")
_svm = joblib.load(_SVM_PATH)
_pca = joblib.load(_PCA_PATH)
_le  = joblib.load(_LE_PATH)

logger.info("Classifier ready ✓")


def _embed(text: str) -> np.ndarray:
    """Return the [CLS] DistilBERT embedding for *text*."""
    inputs = _tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128,
    ).to(_DEVICE)
    with torch.no_grad():
        outputs = _bert(**inputs)
    return outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()


def clasificar(concepto: str) -> str:
    """
    Classify *concepto* (a short description of an expense/income)
    and return its category label.
    Falls back to 'Otros' on any error.
    """
    try:
        emb = _embed(concepto)
        emb_pca = _pca.transform([emb])
        pred = _svm.predict(emb_pca)
        return str(_le.inverse_transform(pred)[0])
    except Exception as exc:
        logger.warning("Classification failed for '%s': %s", concepto, exc)
        return "Otros"
