VLANNum = int(input("Cual es el número de VLAN? ")) 
if VLANNum >= 1 and VLANNum <= 1005: 
    print("Este es un VLAN es Rango Normal.") 
elif VLANNum >=1006 and VLANNum <= 4096: 
    print("Este es una VLAN es Rango Extendo") 
else: 
    print("Esta VLAN no es de Rango Normal ni Extendido.")