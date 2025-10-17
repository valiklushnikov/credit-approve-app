from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from . import serializers
from apps.credits.models import PredictionConfig
from ml.services import get_ensemble


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_predict(request):
    """
        API ендпоінт для отримання прогнозу схвалення кредитної заявки.

        Приймає дані заявки, валідує їх відповідно до активного режиму
        прогнозування (з кредитною історією або без) та повертає результат
        прогнозування ML моделі.

        Режими роботи:
            - mode1: Прогнозування з урахуванням кредитної історії
            - mode2: Прогнозування без урахування кредитної історії

        Args:
            request (Request): HTTP запит з даними заявки у форматі JSON

        Returns:
            Response: JSON відповідь з результатом або помилками валідації
                - 200 OK: {"prediction": <boolean або int>}
                - 400 BAD REQUEST: {"field_name": ["error message"]}

        Example:
            Request (mode1):
                POST /api/predict/
                {
                    "gender": "Male",
                    "married": "Yes",
                    "dependents": 2,
                    "education": "Graduate",
                    "self_employed": "No",
                    "applicant_income": 5000.00,
                    "coapplicant_income": 2000.00,
                    "loan_amount": 150000.00,
                    "loan_amount_term": 360,
                    "credit_history": "Yes",
                    "property_area": "Urban"
                }

            Response:
                {
                    "prediction": 1
                }
    """
    predict_mode = PredictionConfig.objects.get(id=1)

    if predict_mode.active_mode == "mode2":
        data = request.data.copy()
        data.pop("credit_history", None)
        serializer = serializers.UserInfoWithoutCreditHistorySerializer(data=data)
    else:
        serializer = serializers.UserInfoWithCreditHistorySerializer(data=request.data)

    if serializer.is_valid():
        predict = get_ensemble().predict(serializer.validated_data, predict_mode.active_mode)
        return Response({"prediction": predict}, status.HTTP_200_OK)

    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
