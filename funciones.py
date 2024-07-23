import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timedelta

def process_files(file_paths, csv_path):
    csv_columns = [
        "post_title", "post_content", "post_excerpt", "featured_image",
        "comarca-del-evento", "tipo-de-evento", "categoria-eventos",
        "evento_fecha", "evento_fecha__end_date", "evento_fecha__config",
        "evento_hora", "evento_lugar",
        "sub_evento_titulo", "sub_evento_descripcion", "sub_evento_fecha_inicio",
        "sub_evento_fecha_fin", "sub_evento_hora", "sub_evento_lugar",
        "sub_evento_actividades", "sub_evento_imagen", "post_status"
    ]

    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()

        for file_path in file_paths:
            tree = ET.parse(file_path)
            root = tree.getroot()
            csv_data = parse_xml(root)
            writer.writerow(csv_data)

def parse_xml(root):
    csv_data = {}

    evento_principal = root.find("Evento-Principal")
    csv_data["post_title"] = get_text(evento_principal, "Evento-Principal-Titulo")
    csv_data["post_content"] = get_text(evento_principal, "Evento-Principal-Descripcion")
    csv_data["post_excerpt"] = get_text(evento_principal, "Evento-Principal-Descripcion-corta")
    csv_data["featured_image"] = ""

    csv_data["comarca-del-evento"] = get_text(evento_principal, "Evento-comarca")
    csv_data["tipo-de-evento"] = get_text(evento_principal, "Evento-tipo")
    csv_data["categoria-eventos"] = get_text(evento_principal, "Evento-categoria")

    evento_dia_inicio = get_text(evento_principal, "Evento-Principal-Dia-inicio")
    evento_dia_fin = get_text(evento_principal, "Evento-Principal-Dia-fin")
    evento_hora = get_text(evento_principal, "Evento-Principal-Hora")
    evento_lugar = get_text(evento_principal, "Evento-Principal-Lugar")

    if evento_dia_inicio and evento_dia_fin:
        csv_data["evento_fecha"] = generate_event_dates(evento_dia_inicio, evento_dia_fin)
        csv_data["evento_fecha__end_date"] = convert_to_timestamp(evento_dia_fin)
        csv_data["evento_fecha__config"] = generate_event_config(evento_dia_inicio, evento_dia_fin)
    else:
        csv_data["evento_fecha"] = ""
        csv_data["evento_fecha__end_date"] = ""
        csv_data["evento_fecha__config"] = ""

    csv_data["evento_hora"] = evento_hora
    csv_data["evento_lugar"] = evento_lugar

    sub_eventos = evento_principal.findall(".//Sub-evento")
    sub_evento_fields = {
        "sub_evento_titulo": [],
        "sub_evento_descripcion": [],
        "sub_evento_fecha_inicio": [],
        "sub_evento_fecha_fin": [],
        "sub_evento_hora": [],
        "sub_evento_lugar": [],
        "sub_evento_actividades": []
    }

    actividades_html = ""
    for sub_evento in sub_eventos:
        sub_evento_fields["sub_evento_titulo"].append(get_text(sub_evento, "Sub-evento-Titulo"))
        sub_evento_fields["sub_evento_descripcion"].append(get_text(sub_evento, "Sub-evento-descripcion"))
        sub_evento_fields["sub_evento_fecha_inicio"].append(get_text(sub_evento, "Sub-evento-Dia"))
        sub_evento_fields["sub_evento_fecha_fin"].append(get_text(sub_evento, "Sub-evento-Dia"))
        sub_evento_fields["sub_evento_hora"].append(get_text(sub_evento, "Sub-evento-Hora"))
        sub_evento_fields["sub_evento_lugar"].append(get_text(sub_evento, "Sub-evento-lugar"))

        actividades = sub_evento.findall(".//actividad")
        for actividad in actividades:
            actividad_fields = {
                "hora_actividad": get_text(actividad, "actividad-hora"),
                "titulo_actividad": get_text(actividad, "actividad-titulo"),
                "lugar_actividad": get_text(actividad, "actividad-lugar"),
                "descripcion_actividad": get_text(actividad, "actividad-descipcion"),
                "info_extra_actividad": get_text(actividad, "actividad-info-extra")
            }
            # Check if any activity fields have values
            if any(actividad_fields.values()):
                actividad_html = '<div class="Actividad">'
                for field, value in actividad_fields.items():
                    if value:  # Only include the field if it has a value
                        actividad_html += f'<div class="{field}">{value}</div>'
                actividad_html += '</div>'
                actividades_html += actividad_html

    for key in sub_evento_fields:
        sub_evento_fields[key] = [item if item is not None else "" for item in sub_evento_fields[key]]
        csv_data[key] = "|".join(sub_evento_fields[key])

    csv_data["sub_evento_actividades"] = actividades_html

    csv_data["post_status"] = "pending"

    return csv_data

def get_text(parent, tag):
    if parent is not None:
        element = parent.find(tag)
        return element.text if element is not None else ""
    return ""

def generate_event_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    date_list = [start + timedelta(days=x) for x in range((end - start).days + 1)]
    return "|".join([str(int(date.timestamp())) for date in date_list])

def convert_to_timestamp(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return str(int(date.timestamp()))

def generate_event_config(start_date, end_date):
    config = {
        "date": start_date,
        "is_end_date": "1",
        "end_date": end_date,
        "is_recurring": "1",
        "recurring": "daily",
        "recurring_period": "1",
        "end": "on_date",
        "end_after_date": end_date
    }
    return '{"date":"%s","is_end_date":"1","end_date":"%s","is_recurring":"1","recurring":"daily","recurring_period":"1","end":"on_date","end_after_date":"%s"}' % (
        start_date, end_date, end_date
    )
