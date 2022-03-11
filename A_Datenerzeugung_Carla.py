#!/usr/bin/env python   
  
# ==============================================================================
# -- Basis-Code ---------------------------------------------------------
# ==============================================================================

import glob
import os
import sys
import random
import time
import numpy as np
import pandas as pd


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % ( # "%d.%d-%s" -> Version von Python (muss 3.7 sein)
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla # ist zwar gelb unterstrichen, wird aber nach dem Block hier drüber erkannt


# Ausgeben der Lidar-Messungen und abspeichern der Messdaten als ply- (Meshlab) und txt-Dateien 
def lidar_data_received(lidar_data):
   print(lidar_data)


# Speicherort - Datensatz statisch
#------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#   lidar_data.save_to_disk('data/lidar_data/Datensatz/Dynamisch/Fahrzeug/55_meter/%01d.ply' % lidar_data.frame_number) 
#   lidar_data.save_to_disk('data/lidar_data/Datensatz/Dynamisch/Fahrzeug/55_meter/%01d.txt' % lidar_data.frame_number)
   
# Speicherort - Datensatz dynamisch
#------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------
   lidar_data.save_to_disk('data/lidar_data/Datensatz/onePixel/TEST/%01d.ply' % lidar_data.frame_number) #Neu_Channels150_PPS200k
   lidar_data.save_to_disk('data/lidar_data/Datensatz/onePixel/TEST/%01d.txt' % lidar_data.frame_number)





actor_list = [] # Leere List zum sammeln aller erzeugten Aktoren, damit das löschen am Ende bequemer ist


try: # Versuchen die Verbindung zum Server herzustellen, etc.

    # ==============================================================================
    # -- Verbindung zum Server herstellen ------------------------------------------
    # ==============================================================================

    client = carla.Client("localhost", 2000) # Port 2000 ausgewählt für die Verbindung Server <=> Client
    client.set_timeout(3.0) # Timeout von xx Sekunden - Innerhalb dieser Zeit muss eine Verbindung entstanden sein
    world = client.get_world() # World ist die Umgebung und enthält die Funktionen um aus dem Blueprint einen Actor zu machen



    # ==============================================================================
    # -- Actoren erstellen ---------------------------------------------------------
    # ==============================================================================

    # ==========================
    # - Messfahrzeug erstellen - 
    # ==========================

    # Auswählen des Fahrzeugs aus der blueprint library # Das Messfahrzeug ist das Fahrzeug, an dem der LiDAR-Sensor befestigt wird
    blueprint_library = world.get_blueprint_library() # Enthält die Attribute aller Actors
    bp = blueprint_library.filter("model3")[0] # Auto Erstellen, "[0]" = das erste Fahrzeug, dass "model3" enthält nehmen
    print(bp)


    # ======================================
    # - Messfahrzeug korrekt positionieren - 
    # ======================================

    # +++++++++++ y=-315 = 40 Meter zur Wand +++++++++++ #
    # +++++++++++ y=-310 = 45 Meter zur Wand +++++++++++ #
    # +++++++++++ y=-305 = 50 Meter zur Wand +++++++++++ #
    # +++++++++++ 1.Szenario: x=110, y=5, z=0.5 / y=0.77 für Mittelinsel +++++++++++ #
    # +++++++++++ 2.Szenario: x=-235, y=-305, z=0.5 +++++++++++ #

    #spawn_point = random.choice(world.get_map().get_spawn_points()) # Das Auto soll an einem beliebig-möglichen Ort erzeugt werden # "get_spawn_points()" sind die möglichen Erstellungspunkte für Actoren der aktuellen Karte
    spawn_point = carla.Transform(carla.Location(x=-235, y=-295, z=0.5), carla.Rotation(pitch=0, yaw=-90, roll=0)) # Konkreter selbst festgelegter spawn point  # Rotation: Attribute für Ausrichtung des Fahrzeugs
    vehicle = world.spawn_actor(bp, spawn_point) # Erzeugen des Fahrzeugs

    #vehicle.set_autopilot(True) # Erstelltes Fahrzeug soll autonom fahren
    vehicle.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0)) # Geschwindigkeit und Lenkwinkel selber festlegen # "steer=0.0" = Auto fährt geradeaus

    actor_list.append(vehicle) # Jeden erstellten Aktor in die "actor_list" hinzufügen, um hinterher bequem alle Aktoren auf einmal entfernen zu können




    # ================================
    # - Szenariofahrzeug 1 erstellen - 
    # ================================
    blueprint_library = world.get_blueprint_library() # Enthält die Attribute aller Actors
    bp2 = blueprint_library.filter("Vehicle")[0] # CarlaCola# Auto Erstellen, "[0]" = das erste Fahrzeug, dass "xxx" enthält nehmen
    print(bp2)

    # +++++++++++ 2.Szenario: x=-234, y=-349, z=0.5 +++++++++++ #

    # y=-338.6 = 40 Meter zum Sensor 
    #------------------------------------------------------------------------------------------------------------------------
    spawn_point = random.choice(world.get_map().get_spawn_points()) # Das Auto soll an einem beliebig-möglichen Ort erzeugt werden # "get_spawn_points()" sind die möglichen Erstellungspunkte für Actoren der aktuellen Karte
    spawn_point_2 = carla.Transform(carla.Location(x=-235, y=-338.6, z=0.5), carla.Rotation(pitch=0, yaw=-180, roll=0)) # Konkreter spawn point
    vehicle_2 = world.spawn_actor(bp2, spawn_point_2) # Sagen was wo erzeugt werden soll
    vehicle_2.apply_control(carla.VehicleControl(throttle=0.0, steer=0.0)) # Um das Auto selber zu steuern "steer=0.0" = Auto fährt geradeaus
    #-------------------------------------------------------------------------------------------------------------------------
    actor_list.append(vehicle_2)



    # ==============================
    # - Szenarioperson 1 erstellen - 
    # ==============================
    blueprint_library = world.get_blueprint_library() # Enthält die Attribute aller Actors
    bp3 = blueprint_library.filter("Walker")[0] # Auto Erstellen, "[0]" = das erste Fahrzeug, dass "model3" enthält nehmen
    print(bp3)

    # walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
    # print(walker_controller_bp)

    # +++++++++++ y=-326 = Szenarioperson ist 18 Meter vom Sensor entfernt +++++++++++ #
    # +++++++++++ 2.Szenario: x=-237, y=-326, z=0.5 +++++++++++ #

    # 1.1 weniger bei der y-Angabe entspricht dem gleichen Wert wie beim Szenariofahrzeug, warsch. wegen der Breite des Objektes
    # y=-315.7 = 18 Meter zum Sensor 
    #------------------------------------------------------------------------------------------------------------------------
    spawn_point = random.choice(world.get_map().get_spawn_points()) # Das Auto soll an einem beliebig-möglichen Ort erzeugt werden # "get_spawn_points()" sind die möglichen Erstellungspunkte für Actoren der aktuellen Karte
    spawn_point_3 = carla.Transform(carla.Location(x=-237.5, y=-317.7, z=0.5), carla.Rotation(pitch=0, yaw=0, roll=0)) 
    walker = world.spawn_actor(bp3, spawn_point_3) 

    # control = carla.WalkerControl()
    # control.speed = 0
    # control.direction.y = 0
    # control.direction.x = 0
    # control.direction.z = 0
    # # Quelle: https://www.gitmemory.com/issue/carla-simulator/carla/1461/478069651

    # walker.apply_control(control)

    # #------------------------------------------------------------------------------------------------------------------------
    actor_list.append(walker) 






    # ==============================================================================
    # -- Sensor erstellen ---------------------------------------------------------
    # ==============================================================================
    
    lidar_bp = blueprint_library.find('sensor.lidar.ray_cast')

    # Einstellen der verschiedenen Attribute
    lidar_bp.set_attribute('upper_fov', '15')
    lidar_bp.set_attribute('lower_fov', '-15')
    lidar_bp.set_attribute('horizontal_fov', '30')
    #lidar_bp.set_attribute('rotation_frequency','10')
    lidar_bp.set_attribute('range', '70')
    lidar_bp.set_attribute('atmosphere_attenuation_rate', '0') # Afection of the atmosphere on the laser intensity
    lidar_bp.set_attribute('channels', '150') # Number of Lasers Lasern  # Default = 32
    lidar_bp.set_attribute('points_per_second', '200000') # Points generated by all lasers per second # Default = 56000

 
    # Den Sensor an der gewünschten Position am Messfahrzeug befestigen
    # Mit den eingestellten Werten (x=2.5, z=0.7) befindet sich der Sensor vorne an der Front des Fahrzeugs
    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7)) # "carla.Location" ist die relative Lage des Sensors zum Auto 
    sensor = world.spawn_actor(lidar_bp, spawn_point, attach_to=vehicle) # "attach_to=vehicle" um zu sagen, dass der Sensor am Messfahrzeug befestigt werden soll

    actor_list.append(sensor) 



    # ==============================================================================
    # -- Messungen mit dem Sensor durchführen --------------------------------------
    # ==============================================================================

    #camera.listen(lambda image: image.save_to_disk('output/%06d.png' % image.frame)) # Speichern der Daten
    sensor.listen(lambda data: lidar_data_received(data))



    time.sleep(60) # xx Sekunden bevor das Fahrzeug wieder zerstört wird


finally: # Am Ende wieder alles "aufräumen"
    for actor in actor_list:
        actor.destroy()
    print("Alles aufgeräumt!")



