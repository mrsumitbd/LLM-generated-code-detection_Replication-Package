import os
import json
from django.http import JsonResponse
from django.conf import settings
from .models import Cluster

def secrets(request, cluster_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        cluster = Cluster.objects.get(id=cluster_id)
    except Cluster.DoesNotExist:
        return JsonResponse({'error': 'Cluster not found'}, status=404)

    secrets_file = os.path.join(settings.BASE_DIR, 'secrets', f'{cluster.name}.json')
    if not os.path.exists(secrets_file):
        return JsonResponse({'error': 'Secrets file not found'}, status=404)

    with open(secrets_file, 'r') as f:
        secrets_data = json.load(f)

    return JsonResponse(secrets_data)