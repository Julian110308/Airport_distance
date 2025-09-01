from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests

#Vsita principal que muestra el formulario
def airport_distance_view(request):
    return render(request, 'airport_distance.html')

@csrf_exempt # Desactivar CSRF para simplificar las pruebas (no recomendado en producción)

# Vista para calcular la distancia entre dos aeropuertos
def calculate_distance(request):
    if request.method == 'POST':
        try:
            #Obtener datos del formulario
            aeropuerto_origen = request.POST.get('aeropuerto_origen', '').strip().upper()
            aeropuerto_destino = request.POST.get('aeropuerto_destino', '').strip().upper()
            
            #Validar que los campos no esten vacios
            if not aeropuerto_origen or not aeropuerto_destino:
                return JsonResponse({
                    'success': False,
                    'error': 'Debe ingresar ambos códigos de aeropuerto.'
                })
            
            #Validar que los códigos de aeropuerto tengan 3 caracteres
            if len(aeropuerto_origen) != 3 or len(aeropuerto_destino) != 3:
                return JsonResponse({
                    'success': False,
                    'error': 'Los códigos IATA deben tener exactamente 3 caracteres.'
                })
            
            #Validar que los códigos de aeropuerto no sean iguales
            if aeropuerto_origen == aeropuerto_destino:
                return JsonResponse({
                    'success': False,
                    'error': 'Los códigos de aeropuerto no pueden ser iguales.'
                })
            
            #Url de la API para obtener datos del aeropuerto
            base_url = 'https://airportgap.com/api/airports'
            
            #Datos para el POST request
            airports_data = {
                'from': aeropuerto_origen,
                'to': aeropuerto_destino
            }
            
            #Realizar la petición POST a la API
            response_post = requests.post(f'{base_url}/distance', json=airports_data, timeout=10)
            
            if response_post.status_code == 200:
                datos = response_post.json()
                
                #Extraer informacion de la respuesta
                result_data = {
                    'success': True,
                    'codigo': datos['data']['id'],
                    'aeropuerto_origen':{
                        'nombre': datos['data']['attributes']['from_airport']['name'],
                        'ciudad': datos['data']['attributes']['from_airport']['city'],
                        'pais': datos['data']['attributes']['from_airport']['country'],
                        'codigo': aeropuerto_origen
                    },
                    'aeropuerto_destino':{
                        'nombre': datos['data']['attributes']['to_airport']['name'],
                        'ciudad': datos['data']['attributes']['to_airport']['city'],
                        'pais': datos['data']['attributes']['to_airport']['country'],
                        'codigo': aeropuerto_destino
                    },
                    'distancia_km': datos['data']['attributes']['kilometers'],
                    'distancia_millas': datos['data']['attributes']['miles'],
                    'distancia_millas_nauticas': datos['data']['attributes']['nautical_miles']
                }
                return JsonResponse(result_data)