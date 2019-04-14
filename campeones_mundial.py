import pandas as pd
import matplotlib.pyplot as plt
from numpy import round

# leer data
partidos_fifa = pd.read_csv(
    "https://raw.githubusercontent.com/cienciadedatos/datos-de-miercoles/master/datos/2019/2019-04-10/partidos.txt", sep="\t")

# Dejar sólo dígitos
partidos_fifa.partido_orden = partidos_fifa.partido_orden.str.extract('(\d+)')

# Crear columna con ganador partido
partidos_fifa["ganador_partido"] = partidos_fifa.apply(
    lambda x: x['equipo_1'] if x['equipo_1_final'] >= x['equipo_2_final']
    else x['equipo_2'], axis=1)

# Crear columna con goles del ganador
partidos_fifa["ganador_goles"] = partidos_fifa.apply(
    lambda x: x['equipo_1_final'] if x['equipo_1_final'] >= x['equipo_2_final']
    else x['equipo_2_final'], axis=1)

# Agrupar por año y hallar los últimos
campeones_fifa = partidos_fifa.groupby("anio").last()
campeones_fifa = campeones_fifa.loc[:, ["ganador_partido"]]
campeones_fifa.rename(
    columns={"ganador_partido": "ganador_mundial"}, inplace=True)

# Left join
partidos_fifa = pd.merge(partidos_fifa, campeones_fifa, how="left", on="anio")
partidos_fifa = partidos_fifa[partidos_fifa["ganador_partido"]
                              == partidos_fifa["ganador_mundial"]]
campeones_goles = partidos_fifa.loc[:, [
    'anio', 'ganador_goles', 'ganador_mundial']]
# Sumar goles
campeones_goles = campeones_goles.groupby(["anio", "ganador_mundial"]).sum()

# Gráfico
plt.style.use(['ggplot'])
plt.scatter(campeones_goles.index.get_level_values(
    'anio'), campeones_goles['ganador_goles'], color='k')
plt.plot(campeones_goles.index.get_level_values('anio'),
         campeones_goles['ganador_goles'], linestyle='solid', color='k')
plt.axhline(
    y=round(campeones_goles["ganador_goles"].mean(), 1), linestyle="--", color='r')
plt.show()
