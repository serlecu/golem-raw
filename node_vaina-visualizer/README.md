# VAINAS & DASHBOARD

'displayplacer' sctript has to be instlled for 'golem_autorun' to be able to fix the screen changing.
A copy v1.4.0 is kept in this repo, but the original might be found at https://github.com/jakehilborn/displayplacer.
 Following the instuctions, after download (brew is not an option due to an updated Xcode version) it has to be renamed to 'displyplacer' (if it is not its current name), granted execution permits with 'sudo chmod +x displyplacer', and moved to '/etc/'.

### Power-On routine
1. Plug in everything.
1. Turn on the projector and the screen.
2. Wait for the screen home-menu to load and set the right HDMI source (wher the computer is connected).
3. Turn on the computer and wait for the desktop to load.
4. In case the log-in screen shows up, input the credentials provided in the manual.

### Rutina de inicio

1. Force double disply setup: 
   ```
   /etc/displayplacer "id:5CEC9623-FB47-232A-34FD-A7D4190EF5A9 res:3840x2160 hz:30 color_depth:4 enabled:true scaling:off origin:(0,0) degree:0" "id:71BA247B-2026-6ACA-9E09-3CAC2D3F0E0B res:1280x1024 hz:75 color_depth:4 enabled:true scaling:off origin:(3840,0) degree:0"
   ``` 
2. Wait for some seconds (3).
3. Run the shell script that launches the python program:
   ```
   sh /Users/golem/Desktop/golem-node-screen/node_vaina-visualizer/runVisualizer.sh
   ```

4. (The python program is executed by the shell script):
   ```
   /usr/local/bin/python3 /Users/golem/Desktop/golem-node-screen/node_vaina-visualizer/main.py
   ```

### Diagrama de flujo 
```mermaid  
---
title: Dashboard
---
flowchart TB

%% HILO PRINCIPAL %%
start1(("START"))
end1(("END"))
A["Lanzar hilo de Audio"]
B["Abrir Serial"]
C["Iniciar GUI"]
D["Lanzar hilo Serial"]
E["Leer Eventos Pygame"]
F["Dibujar GUI Pantalla TV"]
G["Dibujar GUI Pantalla Proyector"]
H["Actualizar cronómetros"]

start1 --> A --> B --> C --> D --> E
E -->|ninguno| F --> G --> H --> E
E -->|ESC| end1

%% HILO AUDIO %%
s2(["START (hilo Audio)"])
e2(["END (hilo Audio)"])

s2 --> e2

```

```mermaid
flowchart TB

%% HILO SERIAL %%
start3(["START (hilo Serial)"])

%% findPorts()
a3a["Detectar puertos"]
a3b["Actualizar lista de nuevos puertos"]
start3 --> a3a --> a3b --> b3

%% openSerial()
b3{"¿Detectado dispositivo VAINA?"}
b3a{"¿Estaba/n conectado/s antes?"}
b3b{"¿Estaba/n conectado/s antes?"}
c3a["Conectar Puerto/s"]
c3b["Desconectar Puerto/s"]
d3["Actualizar lista de puertos actuales"]
b3 -->|S| b3a -->|N| c3a --> d3
          b3a -->|S| d3
b3 -->|N| b3b -->|S| c3b --> d3
          b3b -->|N| d3
d3 --> serialCronoA

%% readSerial ( leer mensaje)
serialCronoA["¿ha pasado el crono. de Serial?"]
serialCronoB["Poner crono. de Serial a 0"]

e3["¿Puerto VAINA1 conectado?"]
f3a["Leer Serial hasta salto de línea"]
f3b["¿Mensaje válido?"]
g3a["Extraer mensaje integro"]
g3b["Aislar cabecera"]
g3c[" Aislar dato y extaer tipo"]

serialCronoA --> serialCronoB --> e3 --> f3a --> f3b
f3b -->|S| g3a --> g3b --> g3c --> i3
f3b -->|N| serialCronoC


%% readSerial ( almacenar mensaje )
%%h3["¿Mensaje Nuevo?"]
i3["Guardar Valor en variable según Cabecera"]

%%h3 -->|S| i3
%%h3 -->|N| serialCronoC
i3 --> serialCronoC


serialCronoC["Actualizar crono. de Serial"]
serialCronoC --> a3a


%%end3(["END (hilo Serial)"])



```