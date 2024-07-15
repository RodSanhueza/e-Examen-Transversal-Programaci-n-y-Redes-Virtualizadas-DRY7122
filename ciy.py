import requests 
import urllib.parse 
 
route_url = "https://graphhopper.com/api/1/route?" 
loc1 = "Santiago, Chile" 
loc2 = "Ovalle, Chile" 
key = "83e79107-bd87-410c-be1e-76556cfd037c"  ## Reemplaza con tu clave API 

def geocoding(location, key): 
    while location == "": 
        location = input("Ingresa la ubicación nuevamente: ") 
    geocode_url = "https://graphhopper.com/api/1/geocode?"  
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key}) 
    
    replydata = requests.get(url) 
    json_data = replydata.json() 
    json_status = replydata.status_code 

    if json_status == 200 and len(json_data["hits"]) != 0: 
        json_data = requests.get(url).json() 
        lat = json_data["hits"][0]["point"]["lat"] 
        lng = json_data["hits"][0]["point"]["lng"] 
        name = json_data["hits"][0]["name"] 
        value = json_data["hits"][0]["osm_value"] 

        if "country" in json_data["hits"][0]: 
            country = json_data["hits"][0]["country"] 
        else: 
            country = "" 
         
        if "state" in json_data["hits"][0]: 
            state = json_data["hits"][0]["state"] 
        else: 
            state = "" 
         
        if len(state) != 0 and len(country) != 0: 
            new_loc = name + ", " + state + ", " + country 
        elif len(state) != 0: 
            new_loc = name + ", " + state 
        else: 
            new_loc = name 

        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url) 
    else: 
        lat = "null" 
        lng = "null" 
        new_loc = location
        if json_status != 200: 
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc 

while True: 
    print("\n+++++++++++++++++++++++++++++++++++++++++++++") 
    print("Perfiles de vehículos disponibles en Graphhopper:") 
    print("+++++++++++++++++++++++++++++++++++++++++++++") 
    print("coche, bicicleta, pie") 
    print("+++++++++++++++++++++++++++++++++++++++++++++") 
    profile = ["coche", "bicicleta", "pie"] 
    vehicle = input("Introduce un perfil de vehículo de la lista anterior: ") 
    if vehicle == "salir" or vehicle == "s": 
        break 
    elif vehicle in profile: 
        vehicle = vehicle 
    else:  
        vehicle = "coche" 
        print("No se ingresó un perfil de vehículo válido. Usando el perfil de coche.")
    loc1 = input("Ubicación de inicio: ") 
    if loc1 == "salir" or loc1 == "s": 
        break 
    orig = geocoding(loc1, key) 
    print(orig)
    loc2 = input("Destino: ")         
    if loc2 == "salir" or loc2 == "s": 
        break 
    dest = geocoding(loc2, key) 
    print(dest)
    print("=================================================") 
    if orig[0] == 200 and dest[0] == 200: 
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2]) 
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2]) 
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code 
        paths_data = requests.get(paths_url).json() 
        print("Estado de la API de Rutas: " + str(paths_status) + "\nURL de la API de Rutas:\n" + paths_url)
        print("=================================================") 
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)  
        print("=================================================") 
        if paths_status == 200: 
            millas = (paths_data["paths"][0]["distance"]) / 1000 / 1.61 
            km = (paths_data["paths"][0]["distance"]) / 1000 
            combustible = int(km) / 10
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60) 
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60) 
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60) 
            print("Distancia recorrida: {0:.1f} millas / {1:.1f} km".format(millas, km)) 
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec)) 
            print("Combustible: " + str(combustible) + " litros")
            print("=================================================") 
            for each in range(len(paths_data["paths"][0]["instructions"])): 
                path = paths_data["paths"][0]["instructions"][each]["text"] 
                distance = paths_data["paths"][0]["instructions"][each]["distance"] 
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(path, distance / 1000, distance / 1000 / 1.61)) 
            print("=================================================") 
        else: 
            print("Mensaje de error: " + paths_data["message"]) 
            print("*************************************************") 