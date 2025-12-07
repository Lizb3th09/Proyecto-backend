import pandas as pd
from flask import Flask, request, jsonify, render_template
import math

# --- CONFIG ---
CSV_FILE = 'data/db-ens-RL(Gimnasios).csv'

# Coordenadas aproximadas que delimitan Ensenada
LAT_MIN = 31.7
LAT_MAX = 31.9
LON_MIN = -116.8
LON_MAX = -116.5

app = Flask(__name__)
df_maestro = pd.DataFrame()

def load_master_dataframe():
    global df_maestro
    try:
        df = pd.read_csv(CSV_FILE, encoding='latin1')

        # Limpiar coordenadas inválidas
        df = df[(df['latitud'].notna()) & (df['longitud'].notna())]

        # Resetear índice
        df_maestro = df.reset_index(drop=True)
        print(f"✅ DataFrame cargado. Total de gimnasios: {len(df_maestro)}")
        print("Servidor corriendo en http://localhost:5000")
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {CSV_FILE}")
    except Exception as e:
        print(f"❌ Error cargando CSV: {e}")

@app.route('/')
def index():
    return render_template('index.html')

# --- ENDPOINT PARA EL MAPA: SOLO GIMNASIOS EN ENSENADA ---
@app.route('/api/datos_negocios', methods=['GET'])
def api_datos_negocios():
    global df_maestro
    if df_maestro.empty:
        return jsonify({"error": "Datos no cargados"}), 500

    # Filtrar por coordenadas de Ensenada
    df_ensenada = df_maestro[
        (df_maestro['latitud'] >= LAT_MIN) &
        (df_maestro['latitud'] <= LAT_MAX) &
        (df_maestro['longitud'] >= LON_MIN) &
        (df_maestro['longitud'] <= LON_MAX)
    ]

    columnas_salida = ['nom_estab', 'latitud', 'longitud', 'telefono', 'correoelec', 'web']
    datos_respuesta = df_ensenada[columnas_salida].astype(object).where(pd.notnull(df_ensenada[columnas_salida]), None)

    return jsonify(datos_respuesta.to_dict(orient='records')), 200

# --- ENDPOINTS GENERALES ---
@app.route('/excel/negocio/gimnasios', methods=['GET'])
def obtener_gimnasios():
    global df_maestro
    if df_maestro.empty:
        return jsonify({"error": "Datos no cargados"}), 500

    columnas_salida = ['nom_estab', 'latitud', 'longitud', 'telefono', 'correoelec', 'web']
    datos_respuesta = df_maestro[columnas_salida].astype(object).where(pd.notnull(df_maestro[columnas_salida]), None)
    return jsonify(datos_respuesta.to_dict(orient='records')), 200

@app.route('/excel/negocio/ubicacion', methods=['GET'])
def gimnasios_por_ubicacion():
    global df_maestro
    if df_maestro.empty:
        return jsonify({"error": "Datos no cargados"}), 500

    try:
        lat = float(request.args.get('latitud'))
        lon = float(request.args.get('longitud'))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros de latitud y longitud inválidos o faltantes"}), 400

    delta = 0.01
    df_filtrado = df_maestro[
        (df_maestro['latitud'] >= lat - delta) &
        (df_maestro['latitud'] <= lat + delta) &
        (df_maestro['longitud'] >= lon - delta) &
        (df_maestro['longitud'] <= lon + delta)
    ]

    cantidad = len(df_filtrado)

    return jsonify({
        "latitud": lat,
        "longitud": lon,
        "radio_grados": delta,
        "cantidad_gimnasios": cantidad
    }), 200

@app.route('/excel/negocio/contacto', methods=['GET'])
def gimnasios_con_contacto():
    global df_maestro
    if df_maestro.empty:
        return jsonify({"error": "Datos no cargados"}), 500

    telefono = request.args.get('telefono')
    correoelec = request.args.get('correoelec')
    paginweb = request.args.get('paginweb')

    if not correoelec:
        return jsonify({"error": "Parámetro correoelec es requerido"}), 400

    df_filtrado = df_maestro[
        df_maestro['correoelec'].str.contains(correoelec, case=False, na=False)
    ]

    if telefono:
        df_filtrado = df_filtrado[
            df_filtrado['telefono'].str.contains(telefono, case=False, na=False)
        ]

    if paginweb:
        df_filtrado = df_filtrado[
            df_filtrado['web'].str.contains(paginweb, case=False, na=False)
        ]

    columnas_salida = ['nom_estab', 'latitud', 'longitud', 'telefono', 'correoelec', 'web']
    datos_respuesta = df_filtrado[columnas_salida].astype(object).where(pd.notnull(df_filtrado[columnas_salida]), None)

    return jsonify(datos_respuesta.to_dict(orient='records')), 200

@app.route('/excel/negocio/saturacion', methods=['GET'])
def gimnasios_por_saturacion():
    global df_maestro
    if df_maestro.empty:
        return jsonify({"error": "Datos no cargados"}), 500

    try:
        radio = float(request.args.get('radio'))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetro radio inválido o faltante"}), 400

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    counts = []
    coords = df_maestro[['latitud', 'longitud']].values
    for lat1, lon1 in coords:
        count = sum(
            1 for lat2, lon2 in coords if haversine(lat1, lon1, lat2, lon2) <= radio
        )
        counts.append(count)

    df_maestro['gimnasios_cercanos'] = counts

    poco = df_maestro['gimnasios_cercanos'].quantile(0.25)
    mucho = df_maestro['gimnasios_cercanos'].quantile(0.75)

    def saturacion_label(x):
        if x <= poco:
            return 'poco'
        elif x >= mucho:
            return 'mucho'
        else:
            return 'medio'

    df_maestro['saturacion'] = df_maestro['gimnasios_cercanos'].apply(saturacion_label)

    columnas_salida = ['nom_estab', 'latitud', 'longitud', 'telefono', 'correoelec', 'web', 'gimnasios_cercanos', 'saturacion']
    datos_respuesta = df_maestro[columnas_salida].astype(object).where(pd.notnull(df_maestro[columnas_salida]), None)

    return jsonify(datos_respuesta.to_dict(orient='records')), 200

# --- ENDPOINT NUEVO PARA FILTROS ---
@app.route('/api/filtro', methods=['GET'])
def filtro_gimnasios():
    global df_maestro
    if df_maestro.empty:
        return jsonify({"error": "Datos no cargados"}), 500

    tipo = request.args.get('tipo')  # correo, telefono, web, saturacion_poco, saturacion_mucho

    df_filtrado = df_maestro.copy()

    if tipo == 'correo':
        df_filtrado = df_filtrado[df_filtrado['correoelec'].notna() & (df_filtrado['correoelec'] != '')]
    elif tipo == 'telefono':
        df_filtrado = df_filtrado[df_filtrado['telefono'].notna() & (df_filtrado['telefono'] != '')]
    elif tipo == 'web':
        df_filtrado = df_filtrado[df_filtrado['web'].notna() & (df_filtrado['web'] != '')]
    elif tipo == 'saturacion_mucho':
        if 'saturacion' not in df_filtrado.columns:
            return jsonify({"error": "Calcula saturación primero usando /excel/negocio/saturacion"}), 400
        df_filtrado = df_filtrado[df_filtrado['saturacion'] == 'mucho']
    elif tipo == 'saturacion_poco':
        if 'saturacion' not in df_filtrado.columns:
            return jsonify({"error": "Calcula saturación primero usando /excel/negocio/saturacion"}), 400
        df_filtrado = df_filtrado[df_filtrado['saturacion'] == 'poco']
    else:
        return jsonify({"error": "Tipo de filtro inválido"}), 400

    columnas_salida = ['nom_estab', 'latitud', 'longitud', 'telefono', 'correoelec', 'web', 'saturacion']
    datos_respuesta = df_filtrado[columnas_salida].astype(object).where(pd.notnull(df_filtrado[columnas_salida]), None)

    return jsonify(datos_respuesta.to_dict(orient='records')), 200

if __name__ == '__main__':
    load_master_dataframe()
    app.run(debug=True)
