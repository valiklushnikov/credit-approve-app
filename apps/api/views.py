from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


from . import serializers
from apps.credits.models import PredictionConfig
from ml.services import get_ensemble


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_predict(request):
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
