import pygame


def sensor_table(surface, values:list, pos:tuple, spacing:tuple, serialMode:bool = False):
    xpos = pos[0] + spacing[0]*0.3
    ypos = pos[1] 
    font = pygame.font.SysFont("Arial", 16)

    # Columna de Cabecera: MAGNETICO, ACCELEROMETRO, GIROSCOPIO, LUZ, PROXIMIDAD, TEMPERATURA, HUMEDAD, PRESION ATMOSFERICA, RESPUESTA IMPULSO AUDIO
    sensor_list = ["MAG", "ACC", "GYR", "LIG", "PRO", "TEM", "HUM", "ATM", "IRE"]
    for i in range(len(sensor_list)):
        sensor = font.render(str(sensor_list[i]),True,(200,200,200) )
        surface.blit( sensor, (pos[0], ypos + spacing[1]*(i+1)) )

    
    # Columnas de datos
    i = 1
    for sensor in values: #g.sensorDataList
        # Cabecera
        sensorName = font.render("RAW_"+str(i),True,(200,200,200) )
        surface.blit( sensorName, (xpos, ypos) )
        ypos += spacing[1]

        if serialMode:
            # Sensor values
            for value in sensor:
                pytext = font.render( value,True,(255,255,255) )
                surface.blit( pytext, (xpos, ypos) )
                ypos += spacing[1]
        else:
            for key, value in sensor.getSensorData().items(): # returns a dict (key, value)
                if not (key == 'uuid' or key == 'gest'):
                    if not value == None:
                        pytext = str(value).replace('\x00','')
                        pytext = font.render( pytext,True,(255,255,255) )
                    else:
                        pytext = font.render( str("NaN"),True,(255,255,255) )
                    surface.blit( pytext, (xpos, ypos) )
                    ypos += spacing[1]
        xpos += spacing[0]
        ypos = pos[1]
        i += 1