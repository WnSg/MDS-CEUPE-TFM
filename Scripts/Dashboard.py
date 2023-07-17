## Importar librerias
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import plotly.offline as pyo 

## Crear aplicacion de Dash para cargar el Layout
app = dash.Dash()
#Definimos la cadena con el token de la cuenta de mapbox
mapbox_access_token = "pk.eyJ1Ijoid25zZyIsImEiOiJjbGliOTQ2NGwwOWw0M2V0NzVveWc0OWRoIn0.ENqvqKKlrZerjSufywTKfg"


## Paso 1. Cargar los Datos
df_Totales = pd.read_excel("../resultados/df_Totales.xlsx")
df_Totales2 = pd.read_excel("../resultados/df_Totales.xlsx")
df_TotalesByDepto = pd.read_excel("../resultados/df_TotalesByDepto.xlsx")
df_Tabla = pd.read_excel("../resultados/df_Tabla.xlsx")
df_GroupByEdades = pd.read_excel("../resultados/df_GroupByEdades.xlsx")
df_Mapa = pd.read_excel("../resultados/df_mapa.xlsx")



## Pas 2. Creacion de  Graficos
#Grafico 1 Incidencia de Casos
data_IncidenciByAnio = [go.Bar(x=df_Totales["año"],y=df_Totales["Tasa_100mil"],marker={"color":"#2E7DA1"})]
layout_IncidenciaByAnio = go.Layout(title="Incidencia de Casos por Año", #font=dict(size=16),
                   yaxis=dict(title="Tasa x 100,000 Habitantes"),
                   xaxis=dict(title="Años")                   
                   )
fig_IncidenciaByAnio = go.Figure(data=data_IncidenciByAnio, layout=layout_IncidenciaByAnio)

## Grafico 2 % de Positividad
df_Totales2['Positividad%'] = df_Totales2['POSITIVO'] / df_Totales2['Total_Muestras']
data_Positividad = [go.Bar(x=df_Totales2["año"],y=df_Totales2["Positividad%"],marker={"color":"#38BCB0"})]
layout_Positividad = go.Layout(title="% Positividad por Año", #font=dict(size=16),
                   yaxis=dict(title=" % de Positividad", tickformat=".0%"),
                   xaxis=dict(title="Años")                   
                   )
fig_PositividadByAnio = go.Figure(data=data_Positividad, layout=layout_Positividad)

## Grafico 3 Incidencia por Departamento
## Ordenar el Data Frame
df_TotalesByDepto = df_TotalesByDepto.sort_values(by="Tasa_100mil",ascending=False)
## Calcular tasa promedio
x0 = df_TotalesByDepto["Departamento"].iloc[0]            # La primera
x1 = df_TotalesByDepto["Departamento"].iloc[-1]           # La última
xm = df_TotalesByDepto["Departamento"].iloc[len(df_TotalesByDepto)//2]   # La del medio
mean_tasa = np.mean(df_TotalesByDepto["Tasa_100mil"])
data_IncidenciaByDepto = [go.Bar(x=df_TotalesByDepto["Departamento"],y=df_TotalesByDepto["Tasa_100mil"],marker={"color":"#2E7DA1"})]
layout_IncidenciaByDepto = go.Layout(title="Incidencia de Casos por Departamento", height=520, #font=dict(size=14),
                   yaxis=dict(title="Tasa x 100,000 Habitantes")
                   #xaxis=dict(title="Departamentos")                   
                   )
fig_IncidenciaByDepto = go.Figure(data=data_IncidenciaByDepto, layout=layout_IncidenciaByDepto)
fig_IncidenciaByDepto.add_shape(type="line",
    x0=x0, y0=mean_tasa, x1=x1, y1=mean_tasa,
    line=dict(color="Red",width=3))

fig_IncidenciaByDepto.add_annotation(x=xm, y=mean_tasa,
            text='Tasa Promedio Nacional',
            showarrow=False,
            yshift=10)


## Grafico 4 Piramide Poblacional
women_bins = df_GroupByEdades['-MUJER']
men_bins = df_GroupByEdades['HOMBRE']
y = df_GroupByEdades['RangoEdad']
layout_PiramidePoblacion = go.Layout(yaxis=go.layout.YAxis(title='Grupos de Edad'),
                   xaxis=go.layout.XAxis(
                       range=[-50000, 50000],
                       tickvals=[-50000, -25000, -10000, 0, 10000, 25000, 50000],
                       ticktext=[50000, 25000, 10000, 0, 10000, 25000, 50000],
                       title='TOTAL'),
                   title="Pirámide Poblacional por Rango de Edades", height=500,
                   barmode='overlay',
                   bargap=0.1)
data_PiramidePoblacion = [go.Bar(y=y,
               x=men_bins,
               orientation='h',
               name='HOMBRES',
               text=men_bins.astype('int'),
               hoverinfo='x',
               marker=dict(color='#2E7DA1')
               ),
        go.Bar(y=y,
               x=women_bins,
               orientation='h',
               name='MUJERES',
               text=-1 * women_bins.astype('int'),
               hoverinfo='text',
               marker=dict(color='#CD6155')
               )]

fig_PiramidePoblacion = go.Figure(data=data_PiramidePoblacion, layout=layout_PiramidePoblacion)

## Grafico 5 Serie Temporal
x0 = df_Tabla["Fecha"].iloc[0]            # La primera
x1 = df_Tabla["Fecha"].iloc[-1]           # La última
xm = df_Tabla["Fecha"].iloc[len(df_Tabla)//2]   # La del medio
mean_positividad = np.mean(df_Tabla["Positividad%"])
data_SerieTemporal = [go.Line(x=df_Tabla["Fecha"],y=df_Tabla["Positividad%"],marker={"color":"#38BCB0"})]
layout_SerieTemporal = go.Layout(title="% Positividad por Mes y Año", height=550, #font=dict(size=18),
                   yaxis=dict(title=" % de Positividad", tickformat=".0%"),
                   xaxis=dict(title="FECHA (Mes / Año)")                   
                   )
fig_SerieTemporal = go.Figure(data=data_SerieTemporal, layout=layout_SerieTemporal)
fig_SerieTemporal.add_shape(type="line",
    x0=x0, y0=mean_positividad, x1=x1, y1=mean_positividad,
    line=dict(color="Red",width=3)
 )
fig_SerieTemporal.add_annotation(x=xm, y=mean_positividad,
            text='Promedio Nacional de Positividad',
            showarrow=False,
            yshift=10)


# Mapa
#Creamos directamente la figura, obviamos data puesto que directamente lo definimos como el primer argumento de Figure
fig_Mapa = go.Figure(go.Scattermapbox(
        lon = df_Mapa['Longitud'], #Seleccionamos nuestra columna con la coordenada longitud
        lat = df_Mapa['Latitud'], #Seleccionamos nuestra columna con la coordenada latitud
        mode='markers', text=df_Mapa['Tasa_100mil'], 
        marker=go.scattermapbox.Marker(
            size=df_Mapa["Tasa_100mil"]/40, #Indicamos que el tamaño dependa del tráfico promedio de peatones y escalamos entre 10 para no inundar el mapa
            color=df_Mapa["Tasa_100mil"] #Indicamos que el color dependa del tráfico promedio de peatones (podemos usar otra variable)
        )
    ))

#Actualizamos la propiedad "layout" de la figura
fig_Mapa.update_layout(height=800,title="Mapa de Tasa de Incidencia x 100,000 Habitantes",
    autosize=True,
    hovermode='closest', #muestra el dato más cercano al mover el cursor por el gráfico
    mapbox=dict(
        accesstoken=mapbox_access_token,
        center=dict(
            lat=14.754, #coordenadas del centro de nuestro mapa inicial
            lon=-86.429 #coordenadas del centro de nuestro mapa inicial
        ),
        pitch=0,
        zoom=7 #zoom inicial del mapa
    ),
)



##Paso 3. Deficinico del Layout HTML conteniendo el div global del Dashboard
app.layout = html.Div([
                    html.Div([
                        html.H1(children='Sala de Situación - Vigilancia Epidemiológica (SSVE) - HONDURAS', 
                                style={'textAlign':'center','fontFamily':'Sans-serif'})                                
                         ]),
                    
                    # Div Grafico Incidencia By Año
                    html.Div([
                    dcc.Graph(id='barplot_Incidencia_HN',figure=fig_IncidenciaByAnio)
                    ],style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),

                    # Div Grafico %positividad By Año
                    html.Div([
                    dcc.Graph(id='barplot_Positividad_HN', figure=fig_PositividadByAnio)
                    ],style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),

                    # Div Tabla Resumen Nacional By Año
                    html.Div([
                        html.H3(children='Tabla de Frecuencias por Año', 
                                style={'textAlign':'center','fontFamily':'Sans-serif'}) ,
                        dash.dash_table.DataTable(id='dt_Frecuencias_HN',
                                              data=df_Totales.to_dict('records'),
                                              columns=[{"name":i,"id":i} for i in df_Totales.columns[1:8]],
                                              style_table={'marginTop':'10px','fontSize':'16px'},
                                              style_header={'backgroundColor': 'rgb(46, 125, 161)','color': 'white','fontWeight':'bold'},
                                              style_data={'backgroundColor': 'rgb(225, 237, 245)','color': 'black' })
                    ],style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),

                    # Div Grafico Incidencia By Departamentos
                    html.Div([
                    dcc.Graph(id='barplot_Incidencia_HNByDepto',figure=fig_IncidenciaByDepto)
                    ],style={'width': '60%', 'float': 'left', 'display': 'inline-block'}),

                    # Div Grafico Piramide Poblacional
                    html.Div([                    
                    dcc.Graph(id='barplot_Piramide_Poblacion',figure=fig_PiramidePoblacion)
                    ],style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),

                    # Div Grafico Seria Temporal
                    html.Div([                    
                    dcc.Graph(id='lineplot_Piramide_Poblacion',figure=fig_SerieTemporal)
                    ],style={'width': '100%', 'float': 'center', 'display': 'inline-block'}),

                     # Div Mapa
                    html.Div([
                    dcc.Graph(id='mapa_ventas', figure=fig_Mapa)
                    ],style={'width': '100%'})

]
)




## Ejecutar Dashboard
if __name__ == "__main__":
    app.run_server()
