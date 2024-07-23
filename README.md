# XML-to-WP-v.2

este programa extrae el contenido de un xml y lo convierte a un csv para luego poder importarlo al WordPress

el esquema actual que tiene que tener el xml es el siguiente

`

<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Agenda>
	<Evento-Principal>
		<Evento-Principal-Titulo></Evento-Principal-Titulo>
		<Evento-Principal-Dia-inicio></Evento-Principal-Dia-inicio>
		<Evento-Principal-Dia-fin></Evento-Principal-Dia-fin>
		<Evento-Principal-Hora></Evento-Principal-Hora>
		<Evento-Principal-Lugar></Evento-Principal-Lugar>
		<Evento-Principal-Descripcion></Evento-Principal-Descripcion>
		<Evento-Principal-info-extra></Evento-Principal-info-extra>
		<Evento-Principal-Programa>
			<Sub-evento>
				<Sub-evento-Dia></Sub-evento-Dia>
				<Sub-evento-Titulo></Sub-evento-Titulo>
				<Sub-evento-Hora></Sub-evento-Hora>
				<Sub-evento-descripcion></Sub-evento-descripcion>
				<Sub-evento-info-extra></Sub-evento-info-extra>
				<Sub-evento-lugar></Sub-evento-lugar>
				<Sub-evento-actividades>
					<actividad>
						<actividad-hora></actividad-hora>
						<actividad-titulo></actividad-titulo>
						<actividad-lugar></actividad-lugar>
						<actividad-descipcion></actividad-descipcion>
						<actividad-info-extra></actividad-info-extra>
					</actividad>
				</Sub-evento-actividades>
			</Sub-evento>
		</Evento-Principal-Programa>
		<Evento-comarca></Evento-comarca>
		<Evento-tipo></Evento-tipo>
		<Evento-categoria></Evento-categoria>
	</Evento-Principal>
</Agenda>
`'''`

Los campos del post en Wordpress para su importación son los siguiente

    # CAMPOS GENERALES
    post_title
    post_content
    post_excerpt
    featured_image

    # TERMINOS Y CATEGORIAS
    comarca-del-evento
    tipo-de-evento
    categoria-eventos

    # CAMPOS JETENGINE
    evento_fecha
    evento_fecha__end_date
    evento_fecha__config
    evento_hora
    evento_lugar

    # SUB EVENTOS (estos van con | )
    sub_evento_titulo
    sub_evento_descripcion
    sub_evento_fecha_inicio
    sub_evento_fecha_fin
    sub_evento_hora
    sub_evento_lugar
    sub_evento_actividades
    sub_evento_imagen

    # ACTIVIDADES en html
    actividad_hora
    actividad_titulo
    actividad_lugar
    actividad_descripcion
