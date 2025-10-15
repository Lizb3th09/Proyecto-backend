# TITULO DEL DESIGN DOC

Análisis de Panaderías en Ensenada

Link: [](#)

Author(s): Rosa Lizbeth Barcenas Mancilla

Status: [Draft]

Ultima actualización: 2025-10-14

## Contenido

- Goals
- Non-Goals
- Background
- Overview
- Detailed Design
  - Solucion 1
    - Frontend
    - Backend
  - Solucion 2
    - Frontend
    - Backend
- Consideraciones
- Métricas

## Links

## Objetivo

Analizar panaderías en Ensenada para ver dónde hay muchas, dónde hay pocas y qué panaderías necesitan mejorar su presencia en internet.

## Goals

- Ver cuántas panaderías hay en cada zona de Ensenada.
- Detectar zonas con demasiadas panaderías o con pocas.
- Saber qué panaderías no tienen web o redes sociales.
- Mostrar las panaderias en graficas o talves una grafica.

## Non-Goals

- No se analizará saturación de zonas.
- No se harán recomendaciones sobre dónde abrir nuevas panaderías.
- No se crearán planes de marketing.
- No se harán comparaciones entre zonas o sectores económicos.
- No se optimizara rutas o negocios.
- No se ofrecerán servicios de creación de páginas web o chatbots.
- No se procesarán datos fuera de lo que aparece en la lista de panaderías.

## Background

Se cuenta con una lista de panaderías en Ensenada con su ubicación, tamaño (micro, pequeña, mediana) y si tienen web o redes sociales.

## Overview

El proyecto mostrará:

- Cuántas panaderías hay en cada zona.
- Zonas saturadas o con baja oferta.
- Panaderías sin presencia digital.

## Detailed Design

## Solution 1

### Frontend

Tabla simple con nombre, zona, tamaño y presencia digital.

### Backend

- Base de datos o lista con información de panaderías.
- Funciones simples para contar panaderías por zona y detectar falta de web.

## Consideraciones

- Los datos pueden estar incompletos.
- No se considerarán panaderías que no estén en la lista.

## Métricas

- Número de panaderías por zona.
- Zonas saturadas o con poca oferta.
- Porcentaje de panaderías sin web o redes sociales.
