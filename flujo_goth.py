import pandas as pd
import numpy as np

cambio_lealtades = pd.read_csv(
    "https://raw.githubusercontent.com/cienciadedatos/datos-de-miercoles/master/datos/2019/2019-04-17/cambio_lealtades.csv")

melt_array = cambio_lealtades.columns.drop(["origen", "episodios", "nombre"])
cambio_lealtades = cambio_lealtades.drop(["origen", "episodios"], axis=1)\
    .melt(id_vars="nombre", value_vars=melt_array)\
    .drop_duplicates()\
    .copy()\


cambio_lealtades = cambio_lealtades[np.logical_and(
    cambio_lealtades["value"] != "Muerto/a",
    ~cambio_lealtades["nombre"].str.contains("uncredited"))].copy()

cambio_lealtades.rename(
    columns={"value": "lealtad", "nombre": "temporada"}, inplace=True)

mayores_lealtades = cambio_lealtades.groupby("lealtad")\
    .count()\
    .sort_values("variable", ascending=False)\
    .iloc[1: 9, :]\
    .index


in_lealtades = list(map(lambda x: x in mayores_lealtades,
                        cambio_lealtades["lealtad"]))
cambio_lealtades = cambio_lealtades[in_lealtades].copy()

print(cambio_lealtades)
