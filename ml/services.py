ensemble = None


def get_ensemble():
    """
        Повертає singleton екземпляр EnsemblePredictor для прогнозування.

        Реалізує патерн Singleton для ефективного використання пам'яті.
        При першому виклику завантажує ML моделі з диску та зберігає їх
        в глобальній змінній. При наступних викликах повертає вже
        завантажений екземпляр без повторного читання файлів.

        Returns:
            EnsemblePredictor: Ініціалізований екземпляр предиктора з
                завантаженими ML моделями

        Note:
            - Перший виклик може зайняти час через завантаження моделей
            - Наступні виклики повертають результат миттєво
            - Моделі завантажуються з шляхів MODEL_WITH_CH та MODEL_WITHOUT_CH

        Example:
            >>> predictor = get_ensemble()
            >>> result = predictor.predict(data, method="mode1")
    """
    global ensemble
    if ensemble is None:
        from ml.prediction import EnsemblePredictor, MODEL_WITH_CH, MODEL_WITHOUT_CH

        ensemble = EnsemblePredictor(MODEL_WITH_CH, MODEL_WITHOUT_CH)
    return ensemble
