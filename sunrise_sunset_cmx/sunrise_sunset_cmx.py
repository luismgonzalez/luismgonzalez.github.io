import requests
from datetime import datetime, timedelta, timezone

LAT = 19.4326   # CDMX
LON = -99.1332

def obtener_datos(dt):
    """Consulta sunrise/sunset para una fecha específica."""
    url = f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LON}&date={dt.strftime('%Y-%m-%d')}&formatted=0"
    r = requests.get(url)
    data = r.json()['results']
    sunrise = datetime.fromisoformat(data['sunrise'])
    sunset = datetime.fromisoformat(data['sunset'])
    return sunrise, sunset

def evento_ics(uid, fecha_inicio, titulo):
    """Crea un evento ICS."""
    inicio = fecha_inicio.strftime("%Y%m%dT%H%M%SZ")
    fin = (fecha_inicio + timedelta(minutes=1)).strftime("%Y%m%dT%H%M%SZ")  # evento corto
    return f"""
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{inicio}
DTSTART:{inicio}
DTEND:{fin}
SUMMARY:{titulo}
END:VEVENT
""".strip()

def generar_ics():
    hoy = datetime.now().date()
    dias = 365  # 1 año de eventos

    eventos = []

    for i in range(dias):
        fecha = hoy + timedelta(days=i)
        sunrise, sunset = obtener_datos(fecha)

        eventos.append(
            evento_ics(
                uid=f"sunrise-{fecha}",
                fecha_inicio=sunrise.astimezone(timezone.utc),
                titulo="Sunrise CMX"
            )
        )

        eventos.append(
            evento_ics(
                uid=f"sunset-{fecha}",
                fecha_inicio=sunset.astimezone(timezone.utc),
                titulo="Sunset CMX"
            )
        )

    ics = "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Sun Calendar//MX//EN\n" + "\n".join(eventos) + "\nEND:VCALENDAR"

    with open("sunrise_sunset_cmx.ics", "w") as f:
        f.write(ics)

    print("Archivo ICS generado: sunrise_sunset_cdmx.ics")

if __name__ == "__main__":
    generar_ics()

