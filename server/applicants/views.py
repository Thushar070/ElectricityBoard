import pandas as pd
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Applicant

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_csv(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file uploaded"})

    df = pd.read_csv(file)

    for _, row in df.iterrows():
        Applicant.objects.create(
            name=row['name'],
            phone=row['phone'],
            address=row['address'],
            meter_type=row['meter_type'],
            status=row['status']
        )

    return Response({"message": "CSV Uploaded"})
@api_view(['GET'])
def get_applicants(request):
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))
    size = 2

    data = Applicant.objects.filter(name__icontains=q)
    total = data.count()

    data = data[(page-1)*size : page*size].values()

    return Response({
        "total": total,
        "page": page,
        "data": list(data)
    })
@api_view(['PUT'])
def update_applicant(request, id):
    a = Applicant.objects.get(id=id)
    a.name = request.data['name']
    a.phone = request.data['phone']
    a.address = request.data['address']
    a.meter_type = request.data['meter_type']
    a.status = request.data['status']
    a.save()
    return Response({"message":"Updated"})

from django.db.models import Count

@api_view(['GET'])
def status_chart(request):
    data = Applicant.objects.values("status").annotate(count=Count("id"))
    return Response(list(data))
from django.contrib.auth import authenticate

@api_view(['POST'])
def login_api(request):
    user = authenticate(
        username=request.data['username'],
        password=request.data['password']
    )
    if user:
        return Response({"ok": True})
    return Response({"ok": False})
