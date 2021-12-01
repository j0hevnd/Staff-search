import os
import time
import json
import csv
import geopy
import ssl

import geopy.geocoders
from geopy import distance
from geopy.exc import GeocoderTimedOut
# from geopy.geocoders import Nominatim


class LocationResources():
    """Package delivery management"""

    # Range of delivery and collection of packages
    less_distance = 30
    _ctx = ssl.create_default_context()
    _ctx.check_hostname = False
    _ctx.verify_mode = ssl.CERT_NONE
    geopy.geocoders.options.default_ssl_context = _ctx

    geopy.geocoders.options.default_user_agent = 'app_prueba_1'
    DEFAULT_SENTINEL = geopy.geocoders.options.default_timeout = 5
    geolocator = geopy.geocoders.Nominatim(scheme='http')
    
    def __init__(self, address_company="Carrera 48A Poblado, Medellin, Antioquia"):
        """LocationResources constructor

        Args:
            address_company (str, optional): Shipping company location. 
            Defaults to "Carrera 48A Poblado, Medellin, Antioquia".
        """
        self.count = 0
        self.cant_pkgs = {}
        self.address_company = address_company
        
        
    def get_location(self, adrress):
        """ Solve a geolocation from a given string.
        Args:
            adrress (str): Location

        Returns:
            [class 'geopy.location.Location']: Geopy type instance to improve location usage
        """
        try:
            return self.geolocator.geocode(adrress, timeout=self.DEFAULT_SENTINEL)
        except GeocoderTimedOut as e:
            print(f"Error ocurrido por: {e}")
            # raise
    

    def _long_lat(self, location_current, location_dest):
        """We obtain longitude and latitude for to mesure the distance beetwen two points 

        Args:
            location_current ([geopy.location.Location]): Geopy type geolocation
            location_dest ([geopy.location.Location]): Geopy type geolocation

        Returns:
            [tuple]: Information with the latitude and longitude of the given arguments  
        """
        long_lat_current = (location_current.latitude, location_current.longitude)
        long_lat_dest    = (location_dest.latitude, location_dest.longitude)
        return (long_lat_current, long_lat_dest)


    def find_vehicles(self, pickup_pkg=False):
        """ Vehicles that the company has and places where they are

        Args:
            pickup_pkg (bool, optional): Define if only vehicles are returned. 
            Defaults to False.

        Returns: None
        """
        # Call the vehicles archive
        vehicles_company = json.loads(open('vehicles.json', encoding='utf8').read())
        
        if pickup_pkg: return vehicles_company
        
        def _view_vehicles():
            """
            View of company vehicles
            Return: None
            """
            print(f"{'':=>40s}\nVehiculos disponibles:\n")
            [print(f"* {vehicle['brand']}, placa: {vehicle['plate']}") for vehicle in vehicles_company]
                

        flag = True

        # Search where a vehicle located
        while flag:
            _view_vehicles()
            chossen_option = input(f"""
{'':=>40s}
Escoja una opción:

1) Verificar ubicación de un vehículo
99) Atrás

Ingrese el número de la opción: """)

            if chossen_option == "1":
                continue_flag = True
                count_calls_function = 0
                
                while continue_flag:
                    exists_veh = False # Validate that the exist vehicle
                    if count_calls_function == 0: pass
                    else:
                        _view_vehicles()
                        print(f"{'':=>40s}")
                        print("\n99) Atrás")

                    print(f"{'':=>40s}")
                    
                    plate_number = input("\n¿Cuál es la placa del vehículo a ubicar?: ").upper()

                    if plate_number == "99":
                        self.main_menu()

                    for vehicle in vehicles_company:
                        if vehicle["plate"] == plate_number:
                            exists_veh = True
                            print("\nMarca del vehiculo:", vehicle["brand"])

                            location_veh = self.get_location(vehicle["current_location"])
                            distance_veh_company = self._long_lat(location_veh, self.get_location(self.address_company))
                            distance_kms_company = distance.distance(distance_veh_company[0], distance_veh_company[1]).km

                            print(f"\nEl vehículo se encuentra ubicado en: {location_veh}")

                            if int(distance_kms_company) == 0: print("\nEl vehiculo está en la empresa")
                            else: print(f"\nEl vehiculo está a {distance_kms_company:.2f} kilometros de la empresa")

                            get_out = input("\n¿Desea verificar otro vehículo? Y/n: ")
                            if get_out in ("Y", "y"):
                                count_calls_function = 1
                                os.system("cls")
                            else:
                                continue_flag = False
                                self.main_menu()

                    if not exists_veh:
                        print("\n\nLa placa que ha sido ingresada no coincide con los vehiculos con los que actualmente cuenta la empresa")
                    #     time.sleep(4)

                    # os.system("cls")

            elif chossen_option == "99":
                flag = False
                self.main_menu()
            
            else:
                os.system("cls")


    def find_staff(self, pickup_pkg=False):
        """ Personnel with which the company has and places where they are 
        
        Args:
            pickup_pkg (bool, optional): Define if only personnel are returned.
            Defaults to False.

        Returns: None
        """
        # Call the personnel archive
        staffs = json.loads(open('staff.json', encoding='utf8').read())
        
        if pickup_pkg:
            return staffs
            
        # Displays the name of the staff
        print(f"{'':=>40s}\nPersonal a cargo:\n")
        [print(' - ', objects['name']) for objects in staffs]
        print(f"\n{'':=>40s}\n99) Volver")

        def _find_staff():
            """
            Search an employee
            Return: None
            """
            found_staff = False
            answer_name = input("\nEscribe el nombre completo del personal que ubicaras: ").lower()

            if answer_name == "99":
                self.main_menu()

            # Takes accented vowels and transforms them into unstressed vowels
            transliterar_entry_name = answer_name.maketrans('ÁÉÍÓÚáéíóú', 'AEIOUaeiou')
            name_entry_check = answer_name.translate(transliterar_entry_name).lower()
            
            for staff in staffs:    
                transliterar_name = staff['name'].maketrans('ÁÉÍÓÚáéíóú', 'AEIOUaeiou')
                name_check = staff['name'].translate(transliterar_name).lower()

                if name_entry_check == name_check:
                    found_staff = True
                    location_current = self.get_location(staff['current_location'])
                    distance_staff = self._long_lat(location_current, self.get_location(self.address_company))
                    break
            
            if not found_staff:
                print("\nEl empleado ingresado no existe, o copió mal el nombre.")
                return None
            
            return answer_name, location_current, distance_staff

        flag = True
        
        while flag:
            
            staff_location_distance = _find_staff()
            
            if staff_location_distance:
                print(f"\nEl empleado {staff_location_distance[0]} se encuentra en: \n{staff_location_distance[1]}.\nEstá a {distance.distance(staff_location_distance[2][0], staff_location_distance[2][1]).km:.2f} kilometros del la empresa")

            get_out = input("\n¿Desea buscar otro empleado? Y/n: ")
            if get_out in ("Y", "y"): continue
            else:
                flag = False
                self.main_menu()
                

    def _find_this_staff_vehicle(self, option):
        """We locate personnel or vehicle closest to a package

        Args:
            option ([int], 1, 2): Defines whether to search for a staff or a vehicle
        """

        location_pkg = ""
        name_staff_vehicle = ""
        # staff_or_vehicle_found = []
        no_exist_pkg = True
        
        print(f"{'':=>50s}")
        number_location_pkg = input("\nIngrese el número de orden del paquete a recojer y mostraremos personal más cercano a el, o 99 para salir: ")
        
        while no_exist_pkg:
            if number_location_pkg == "99":
                return
            
            if not number_location_pkg.isnumeric():
                number_location_pkg = input("\nSolo ingrese el número de orden que aparece al final de la ubicación del paquete, o 99 para salir: ")
                time.sleep(4)
                continue
            
            else:
                # We get the location of a package
                for key, value in self.cant_pkgs.items():
                    if key == int(number_location_pkg):
                        location_pkg = value
                        no_exist_pkg = False
                        break

                if no_exist_pkg:
                    print("\nEl número de orden no existe, por favor verifique que sea correcto.")
                    number_location_pkg = input("Número de orden: ")

        if option == "1":
            # Vehicles that we have available in the company
            staff_or_vehicle_found = self.find_vehicles(pickup_pkg=True)
            
        elif option == "2":
            # Personnel that we have available in the company 
            staff_or_vehicle_found = self.find_staff(pickup_pkg=True)
            
        for staff_or_vehicle in staff_or_vehicle_found:
            location_curretn_staff_or_vehicle = self.get_location(staff_or_vehicle['current_location'])
            # Distance between staff or vehicle and package
            distance_pkg_staff_or_vehicle = self._long_lat(location_curretn_staff_or_vehicle, location_pkg)
            distance_obtained = round(distance.distance(distance_pkg_staff_or_vehicle[0], distance_pkg_staff_or_vehicle[1]).km, 2)

            # Find the closest personnel or vehicle to the package
            if distance_obtained <= self.less_distance:
                self.less_distance = distance_obtained
                if option == "1": name_staff_vehicle = staff_or_vehicle['brand']
                elif option == "2": name_staff_vehicle = staff_or_vehicle['name']

        print(f"\nEl personal mas cercano es: {name_staff_vehicle}, y esta a {self.less_distance} kilometros del punto de recogida del paquete\n")

        self.less_distance = 30
        input("Preciona Enter para continuar")
    
    
    def _chossen_option(self):
        '''Menu of options'''
        return input("""
Elija una de las opciones a continuación:

    1) Buscar vehículos cerca
    2) Buscar personal cerca
    99) Atrás

Ingrese el número de lo que desea hacer: """)
    

    def _find_pkgs(self):
        """
        Show packages to pick up and menu of options
        Returns: None
        """
        # File with the addresses where packages are collected
        with open('direcciones_pkg.csv', 'rt', encoding= 'utf8') as pkgs:
            pkgs_location = csv.reader(pkgs)
        
            for locations in pkgs_location:
                locations_dirt = ','.join(locations)
                
                direction = self.get_location(locations_dirt)
                
                # Verify that the address to enter is not repeated
                if direction in self.cant_pkgs.values(): continue
                
                self.count += 1
                self.cant_pkgs[self.count] = direction
   
        print(f"{'':=>50s}\n")
        print(f"{' Paquetes por recoger ':*^50}\n")
        print(f"{'':=>50s}\n")

        for key, value in self.cant_pkgs.items():
            distance_business = self._long_lat(value, self.get_location(self.address_company))
            print(f"La ubicación donde se recoje el paquete es: {value}; \n\nEstá a: {distance.distance(distance_business[0], distance_business[1]).km:.2f} kilometros de distancia de la empresa. \n\n(*IMPORTANTE) Número de orden del paquete: {key}", end="\n\n")
            print(f"{'':=>50s}")
        
        flag = True
        while flag:
                
            chossen_option = self._chossen_option()
            
            if chossen_option == "1":
                self._find_this_staff_vehicle(chossen_option)
                continue

            elif chossen_option == "2":
                self._find_this_staff_vehicle(chossen_option)
                continue

            elif chossen_option == "99":
                flag = False
                self.main_menu()

            else:
                print("\nSolo ingrese una de las opciones que se muestran")
                time.sleep(2)


    def main_menu(self):
            """ 
            Menú con las opciones principales 
            Return: None
            """
            os.system("cls")
            
            answer = input(""" 
Elija la opción para lo que desea hacer:

    1) Ubicar dirección de recibo de un paquete
    2) Ubicar un vehículo
    3) Ubicar personal
    4) Salir

Ingresa el número que identifica lo que deseas hacer: """)

            while answer not in("1", "2", "3", "4"):
                answer = input("Ingresa solo 1, 2, 3, 4 según la acción: ")

            os.system("cls")

            # Ubicacion de paquete
            if answer == "1": self._find_pkgs()

            # Ubicacion de vehiculo
            elif answer == "2": self.find_vehicles()

            # Ubicar personal
            elif answer == "3": self.find_staff()

            elif answer == "4":
                print("""
==================
** See you soon **
**      :)      **
==================""")
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