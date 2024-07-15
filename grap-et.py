import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "83e79107-bd87-410c-be1e-76556cfd037c"  ### Reemplaza con tu clave API

def geocoding(location, key):
    while location == "":
        location = input("Ingresa la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200:
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
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("Geocoding API URL for " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location

    return json_status, lat, lng, new_loc

while True:
    print("\n")
    print("Bienvenido al asistente de viajes DRY7122!")
    print("\n")
    print("A continuación, deberás elegir el tipo de vehículo que utilizarás, y luego seleccionar la ubicación de partida y la ubicación de destino.")
    input("Presione ENTER para continuar...")
    print("\n")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de Vehiculos disponibles para elegir:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile=["car", "bike", "foot"]
    vehicle = input("Ingresa un perfil de Vehiculo: ")
    if vehicle.lower() == "s":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else: 
        vehicle = "car"
        print("Perfil de Vehiculo no valido. se utilizará el perfil 'car'.")

    loc1 = input("Ciudad de Origen:(Presiona 's' para Salir.) ")
    if loc1.lower() == 's':
        break
    orig = geocoding(loc1, key)
    print(orig)

    loc2 = input("Ciudad de Destino:(Presiona 's' para Salir.) ")
    if loc2.lower() == 's':
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Routing API Status: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.61
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)

            print("Distancia de Viaje: {0:.1f} miles / {1:.1f} km".format(miles, km))
            print("Duración de viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance/1000, distance/1000/1.61))
                print("=============================================")
            choice = input("Presione ENTER para continuar o 's' para salir: ")
            if choice.lower() == 's':
                break 
        else:
            print("Error message: " + paths_data["message"])
            print("*************************************************")

print("\n")
print("¡Gracias por usar el asistente de viajes DRY7122!")
print("\n")