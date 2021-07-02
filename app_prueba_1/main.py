import os
import time
import geopy
import geopy.geocoders

from geopy.geocoders import Nominatim
from geopy import distance


class LocationResources():
    """ Ubicacion de recursos de una empresa """

    count = 0
    distance_menor = 30
    location_pkgs = []
    cant_pkgs = {}

    geopy.geocoders.options.default_user_agent = 'app_prueba_1'
    DEFAULT_SENTINEL = geopy.geocoders.options.default_timeout = 4
    geolocator = Nominatim()

    # Identificar el punto donde esta ubicada la empresa
    address_siata = "Carrera 48A Poblado, Medellin, Antioquia"
    # Obtenemos direccion completa
    _location_business = geolocator.geocode(address_siata)
    

    def _long_lat(self, location_current, location_dest):
        """ obtenemos longitud y latitud para medir distancia entre dos puntos """

        long_lat_current = (location_current.latitude, location_current.longitude)
        long_lat_dest    = (location_dest.latitude, location_dest.longitude)

        return (long_lat_current, long_lat_dest)


    def find_vehicles(self, pickup_pkg=False):
        """ Vehiculos con los que cuenta la empresa y los lugares donde estan """

        vehicles_business = [
            {
            "brand" : "Toyota",
            "plate" : "XDF234",
            "current_location" : "La Milagrosa, Medellín, Antioquia",
            },
            {
            "brand" : "Mercedez Benz",
            "plate" : "89RTY",
            "current_location" : "Los colores, Medellín, Antioquia",
            },
            {
            "brand" : "Chevrolet",
            "plate" : "067EFL",
            "current_location" : "Carrera 48A Poblado, Medellin, Antioquia",
            },
            {
            "brand" : "Mustang",
            "plate" : "TYH440",
            "current_location" : "Laureles, Medellin, Antioquia",
            },
            {
            "brand" : "Audi",
            "plate" : "TRK779",
            "current_location" : "San Antonio, Medellin, Antioquia",
            },
            {
            "brand" : "Chevrolet v2",
            "plate" : "YTU000",
            "current_location" : "Castilla, Medellin, Antioquia",
            },
            {
            "brand" : "Volvo",
            "plate" : "KMZ441",
            "current_location" : "Guarne, Medellin, Antioquia",
            },
        ]
        
        if pickup_pkg:
            return vehicles_business
        
        def _function():
            
            print("=======================================")
            print("Vehiculos disponibles:\n")

            for vehicle in vehicles_business:
                print(f"* {vehicle['brand']}, placa: {vehicle['plate']}")

        flag = True

        # Buscamos donde se encuentra un vehiculo
        while flag:
            exists_veh = False # para validar que exista el vehiculo
            
            _function()

            chossen_option = input("""
=======================================
Escoja una opción:

1) Verificar ubicación de un vehiculo
99) Atrás

Ingrese el número de la opción: """)



            if chossen_option == "1":
                continue_flag = True
                count_calls_function = 0
                
                while continue_flag:
                    if count_calls_function == 0:
                        pass
                    else:
                        _function()

                    print("=============================================================")
                        
                    plate_number = input("\n¿Cuál es la placa del vehiculo a ubicar?: ").upper()

                    if plate_number == "99":
                        self.main_menu()

                    for vehicle in vehicles_business:
                        if vehicle["plate"] == plate_number:
                            exists_veh = True
                            print("\nMarca del vehiculo:", vehicle["brand"])

                            location_veh = self.geolocator.geocode(vehicle["current_location"])
                            distance_veh_bussines = self._long_lat(location_veh, self._location_business)
                            distance_kms_business = distance.distance(distance_veh_bussines[0], distance_veh_bussines[1]).km

                            print(f"\nEl vehiculo se encuentra ubicado en: {location_veh}")

                            if int(distance_kms_business) == 0:
                                print("\nEl vehiculo está en la empresa")
                            else:
                                print(f"\nEl vehiculo está a {distance_kms_business:.2f} kilometros de la empresa")

                            ask_go_out = input("\n¿Desea verificar otro vehiculo? Y/n: ")
                            if ask_go_out in ("Y", "y"):
                                count_calls_function +=1
                                os.system("cls")
                                pass
                            else:
                                continue_flag = False
                                self.main_menu()

                    if not exists_veh:
                        print("\n\nLa placa que ha sido ingresada no coincide con los vehiculos con los que actualmente cuenta la empresa")
                        time.sleep(4)

                    os.system("cls")

            elif chossen_option == "99":
                flag = False
                self.main_menu()
            
            else:
                os.system("cls")

    # Busqueda del personal de la empresa
    def find_staff(self, pickup_pkg=False):
        staffs = [
            {
                "nombres": "Juana De Arco",
                "edad"   : 20,
                "direccion" : "Cataluña, Medellín, Antioquia",
                "telefono" : "3220990099" 
            },
            {
                "nombres": "Armin Arlert",
                "edad"   : 19,
                "direccion" : "Caicedo, Medellín, Antioquia",
                "telefono" : "3125990349" 
            },
            {
                "nombres": "Darwin Hernan",
                "edad"   : 27,
                "direccion" : "Santa Elena, Medellín, Antioquia",
                "telefono" : "3000556054" 
            },
            {
                "nombres": "Mikasa Ackerman",
                "edad"   : 19,
                "direccion" : "La Alpujarra, Medellín, Antioquia",
                "telefono" : "3078965032" 
            },
            {
                "nombres": "Eren Geager",
                "edad"   : 19,
                "direccion" : "El Estadio, Medellín, Antioquia",
                "telefono" : "3078965032" 
            },
            {
                "nombres": "Diego Díaz",
                "edad"   : 23,
                "direccion" : "San Cristobal, Medellín, Antioquia",
                "telefono" : "3078965032" 
            },
        ]

        if pickup_pkg:
            return staffs
            
        flag = True

        while flag:
            found_staff = False

            print("Personal a cargo:")

            for objects in staffs:
                for key, value in objects.items():
                    if key == "nombres":
                        print(' - ', value)

            print("\n99) Volver")
            
            answer_name = input("\nEscribe el nombre completo del personal que ubicaras: ").lower()

            if answer_name == "99":
                self.main_menu()

            for staff in staffs:
                # Tomamos las vocales con acento y los transformamo a vocales sin acento
                transliterar_entry_name = answer_name.maketrans('ÁÉÍÓÚáéíóú', 'AEIOUaeiou')
                name_entry_check = answer_name.translate(transliterar_entry_name).lower()
                
                transliterar_name = staff['nombres'].maketrans('ÁÉÍÓÚáéíóú', 'AEIOUaeiou')
                name_check = staff['nombres'].translate(transliterar_name).lower()

                if name_entry_check == name_check:
                    found_staff = True
                    location_current = self.geolocator.geocode(staff['direccion'])
                    distance_staff = self._long_lat(location_current, self._location_business)

                    print(f"\nEl empleado {staff['nombres']} se encuentra en: \n{location_current}, a {distance.distance(distance_staff[0], distance_staff[1]).km:.2f} kilometros del la empresa")

            if not found_staff:
                print("\nEl empleado ingresado no existe o copio mal el nombre.")

            pregunta_salir = input("\n¿Desea buscar otro empleado? Y/n: ")
            if pregunta_salir in ("Y", "y"):
                os.system("cls")
                pass
            else:
                flag = False
                self.main_menu()

    def find_this_staff_vehicle(self, option):
        """ Aquí hubicamos el personal o vehiculo más cercano a recojer un paquete """

        print("=============================================================")
        number_ubication_pkg = input("\nIngrese el número del paquete a recojer y mostraremos personal más cercano a el: ")
        location_pkg = ""
        name_staff_vehicle = ""
        location_staff_vehicle = ""
        staff_or_vehicle_found = []
        no_exist_pkg = True

        if number_ubication_pkg.isnumeric():
            # obtenemos la ubicacion de paquete
            for locations in range(len(self.location_pkgs)):
                for key, value in self.location_pkgs[locations].items():
                    if key == int(number_ubication_pkg):
                        location_pkg = value
                        no_exist_pkg = False
        
        else:
            print("\nIngrese el número que aparece al final de la ubicación del paquete.")
            time.sleep(5)
            os.system("cls")

        if no_exist_pkg:
            print("\nEl número de paquete elegido no existe, por favor verifique el número al final de cada orden de paquete.")
            time.sleep(5)
            return True

        if option == "1":
            # Obtenemos los vehiculos que tenenemos disponibles en la empresa
            staff_or_vehicle_found = self.find_vehicles(pickup_pkg=True)
            
        elif option == "2":
            # Obtenemos el personal que tenenemos disponible en la empresa  
            staff_or_vehicle_found = self.find_staff(pickup_pkg=True)
            
        for staff_or_vehicle in staff_or_vehicle_found:
        
            if option == "1":
                location_curretn_staff_or_vehicle = self.geolocator.geocode(staff_or_vehicle['current_location'], timeout=self.DEFAULT_SENTINEL)
            
            elif option == "2":
                location_curretn_staff_or_vehicle = self.geolocator.geocode(staff_or_vehicle['direccion'], timeout=self.DEFAULT_SENTINEL)
            
            # Obtenemos la distancia entre el personal o vehiculo y el paquete
            distance_pkg_staff_or_vehicle = self._long_lat(location_curretn_staff_or_vehicle, location_pkg)
            distance_obtained = round(distance.distance(distance_pkg_staff_or_vehicle[0], distance_pkg_staff_or_vehicle[1]).km, 2)

            # Buscamos el personal o vehiculo más cercano al paquete
            if distance_obtained <= self.distance_menor:
                self.distance_menor = distance_obtained
                if option == "1":
                    name_staff_vehicle = staff_or_vehicle['brand']
                    location_staff_vehicle = staff_or_vehicle['current_location']
                if option == "2":
                    name_staff_vehicle = staff_or_vehicle['nombres']
                    location_staff_vehicle = staff_or_vehicle['direccion']

        print(f"\nEl personal mas cercano es: {name_staff_vehicle}, y esta a {self.distance_menor} kilometros del punto de recogida del paquete\n")

        input("Preciona Enter para continuar")

        self.distance_menor = 30
        os.system("cls")
    
    # Busqueda de paquetes
    def find_pkgs(self):
        # Lugares donde se van a recojer paquetes
        pkgs_location = ["Aranjuez, Medellín, Antioquia", "Jardin Botanico, Medellín, Antioquia", "Moravia, Medellin, Antioquia", "Aranjuez, Medellín, Antioquia", "Hospital Consejo de Medellin, Medellín, Antioquia", "La Ceja, Antioquia", "Marinilla, Antioquia"]

        for pkg in range(len(pkgs_location)):
            direction_exist = False 

            # Obtenemos direccion completa
            direccion = self.geolocator.geocode(pkgs_location[pkg], timeout=self.DEFAULT_SENTINEL)

            if self.cant_pkgs:
                for value in self.cant_pkgs.values():
                    if value == direccion: # Verificamos que la direccion a ingresar no exista ya
                        direction_exist = True
                        break
            
            if not direction_exist:
                self.count += 1
                self.cant_pkgs[self.count] = direccion
            
        self.location_pkgs.append(self.cant_pkgs)

        flag = True

        while flag:
            
            print("=============================================\n")
            print("*********** Paquetes por recoger ************\n")
            print("=============================================\n")

            for locations in range(len(self.location_pkgs)):
                for key, value in self.location_pkgs[locations].items():
                    distance_business = self._long_lat(value, self._location_business)
                    print(f"La ubicación donde se recoje el paquete es: {value}; \n\nEstá a: {distance.distance(distance_business[0], distance_business[1]).km:.2f} kilometros de distancia de la empresa. \n\n(*IMPORTANTE) Número para ubicar el paquete: {key}", end="\n\n")
                    print("=============================================================")

            chossen_option = input("""
Elija una de las opciones a continuación:

    1) Buscar vehiculos cerca
    2) Buscar personal cerca
    99) Atrás

Ingrese el número de lo que desea hacer: """)

            if chossen_option == "1":
                pkg_exist = self.find_this_staff_vehicle(chossen_option)
                if pkg_exist:
                    continue

            elif chossen_option == "2":
                pkg_exist = self.find_this_staff_vehicle(chossen_option)
                if pkg_exist:
                    continue

            elif chossen_option == "99":
                flag = False
                self.main_menu()


    def main_menu(self):
            """ Menú con las opciones principales """
            
            os.system("cls")
            answer = input(""" 
Elija la opción que se adecue a lo que desea hacer:

    1) Ubicar direccion de recibo de un paquete
    2) Ubicar un vehiculo
    3) Ubicar personal
    4) Salir

Ingresa el número que identifica lo que deseas hacer: """)

            while answer not in("1", "2", "3", "4"):
                answer = input("Ingresa solo 1, 2, 3, 4 según la acción: ")

            os.system("cls")

            # Ubicacion de paquete
            if answer == "1":
                self.find_pkgs()

            # Ubicacion de vehiculo
            elif answer == "2":
                self.find_vehicles()

            # Ubicar personal
            elif answer == "3":
               self.find_staff()

            elif answer == "4":
                print("""
=================
**             **
** HASTA LUEGO **
**     :)      **
=================""")
                time.sleep(3)
                os.system("cls")
                exit()


if __name__ == "__main__":
    location_resources = LocationResources()

    try:
        location_resources.main_menu()
    except KeyboardInterrupt as ex:
        print("\nCierre forzoso de CTRL + C")
        exit()