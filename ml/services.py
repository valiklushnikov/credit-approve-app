ensemble = None


def get_ensemble():
    global ensemble
    if ensemble is None:
        from ml.prediction import EnsemblePredictor, MODEL_WITH_CH, MODEL_WITHOUT_CH

        ensemble = EnsemblePredictor(MODEL_WITH_CH, MODEL_WITHOUT_CH)
    return ensemble
