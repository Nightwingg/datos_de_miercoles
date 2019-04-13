rm(list = ls())

library(dplyr)
library(magrittr)
library(ggplot2)
extrafont::loadfonts(device = "win")

# Import Data
partidos_fifa_copa_mundial_procesado <-
  readr::read_delim(
    "https://raw.githubusercontent.com/cienciadedatos/datos-de-miercoles/master/datos/2019/2019-04-10/partidos.txt",
    delim = "\t"
  )

# Encontrar campeón y año respectivo

campeones_mundial <- partidos_fifa_copa_mundial_procesado %>%
  mutate(partido_orden = as.numeric(stringr::str_extract(partido_orden, "[[:digit:]]+"))) %>% # Dejar sólo los números
  group_by(anio) %>%
  mutate(
    ganador_partido = ifelse(equipo_1_final >= equipo_2_final , equipo_1, equipo_2),
    ganador_goles = ifelse(
      equipo_1_final >= equipo_2_final ,
      equipo_1_final  ,
      equipo_2_final
    ),
    ganador_mundial = ganador_partido[n()]
  ) %>%
  filter(ganador_partido == ganador_mundial) %>%
  ungroup() %>%
  group_by(anio, ganador_mundial) %>%
  summarise(goles = sum(ganador_goles))

# Gráfico

windowsFonts(Roboto = windowsFont("Roboto Medium"))

ggplot(data = campeones_mundial, aes(x = anio, y = goles, label = ganador_mundial)) +
  geom_point() +
  geom_line() +
  geom_segment(
    aes(
      x = min(anio) - 1,
      xend = max(anio) + 1,
      y = mean(campeones_mundial$goles),
      yend = mean(campeones_mundial$goles)
    ),
    linetype = "dashed",
    color = "red"
  ) +
  annotate(
    "text",
    x = 2018,
    y = mean(campeones_mundial$goles),
    label = round(mean(campeones_mundial$goles), 1),
    hjust = -0.55,
    size = 5,
    color = "red",
    fontface = 2
  ) +
  labs(
    x = "Año",
    y = "Número de Goles",
    title = "Distribución de Goles del país ganador del Mundial",
    subtitle = "Por mundial, el equipo ganador marca aproximadamente unos 15 goles",
    caption = "Fuente: Datos De Miércoles"
  ) +
  theme_minimal() +
  theme(text = element_text(size = 16, family = "Roboto Medium")) +
  scale_x_continuous(
    limits = c(min(campeones_mundial$anio) - 1, y = max(campeones_mundial$anio) +
                 5),
    expand = c(0, 2),
    breaks = seq(
      min(campeones_mundial$anio),
      max(campeones_mundial$anio) + 2,
      by = 4
    )
  )

ggsave(
  "campeones_gol.png",
  dpi = 600,
  height = 6,
  width = 12
)
