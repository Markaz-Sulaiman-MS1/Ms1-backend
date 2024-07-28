from rest_framework.views import APIView, Response


# Create your views here.
class HealthCheckAPI(APIView):
    def get(self, request):
        return Response({"status": 200})
