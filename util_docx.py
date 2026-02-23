"""
Generador de documentos DOCX para reportes de incidentes.
Utiliza python-docx para crear un documento profesional.
"""
import os
from datetime import datetime
try:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    Document = None

def _get_downloads_folder():
    """Retorna la ruta de la carpeta Descargas del usuario en Windows."""
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def generar_reporte_docx(reporte: dict, save_path: str = None) -> str | None:
    """
    Recibe un diccionario con los datos del reporte y genera un archivo DOCX 
    en la carpeta de Descargas del usuario.
    Devuelve la ruta absoluta del archivo generado o None si falla.
    """
    if Document is None:
        print("Error: python-docx no está instalado.")
        return None

    try:
        doc = Document()

        # Configuración de estilos globales (opcional)
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)

        # -- Encabezado Principal --
        header = doc.add_paragraph()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        runner = header.add_run("SISTEMA DE BRIGADAS AMBIENTALES\n")
        runner.bold = True
        runner.font.size = Pt(16)
        runner.font.color.rgb = RGBColor(0x05, 0x96, 0x69) # Verde primario
        
        runner_sub = header.add_run("REPORTE OFICIAL DE INCIDENTE")
        runner_sub.bold = True
        runner_sub.font.size = Pt(14)
        
        doc.add_paragraph("_" * 70).alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_paragraph() # Espacio

        # -- Información Principal --
        p_info = doc.add_paragraph()
        p_info.add_run("ID Reporte: ").bold = True
        p_info.add_run(f"#{reporte.get('id', 'N/A')}\n")
        
        p_info.add_run("Fecha del Reporte: ").bold = True
        # Formatear fecha
        fecha = reporte.get('fecha')
        fecha_str = fecha.strftime("%d/%m/%Y %H:%M") if hasattr(fecha, 'strftime') else str(fecha)
        p_info.add_run(f"{fecha_str}\n")
        
        p_info.add_run("Brigada Asignada: ").bold = True
        p_info.add_run(f"{reporte.get('brigada', 'N/A')}\n")

        p_info.add_run("Estado Actual: ").bold = True
        p_estado = p_info.add_run(f"{reporte.get('estado', 'N/A')}")
        if reporte.get('estado') == 'Resuelto':
            p_estado.font.color.rgb = RGBColor(0x10, 0xb9, 0x81)
        elif reporte.get('estado') == 'En Proceso':
            p_estado.font.color.rgb = RGBColor(0xf5, 0x9e, 0x0b)
        else:
            p_estado.font.color.rgb = RGBColor(0xef, 0x44, 0x44)

        doc.add_paragraph() # Espacio

        # -- Detalles del Incidente --
        doc.add_heading('Detalles del Incidente', level=2)
        
        p_det = doc.add_paragraph()
        p_det.add_run("Título: ").bold = True
        p_det.add_run(f"{reporte.get('titulo', 'N/A')}\n")
        
        p_det.add_run("Nivel de Prioridad: ").bold = True
        p_prio = p_det.add_run(f"{reporte.get('prioridad', 'N/A')}\n")
        if "Alta" in reporte.get('prioridad', ''):
            p_prio.font.color.rgb = RGBColor(0xef, 0x44, 0x44) # Rojo
            
        p_det.add_run("Ubicación: ").bold = True
        p_det.add_run(f"{reporte.get('ubicacion', 'N/A')}\n")

        # -- Descripción --
        doc.add_heading('Descripción de los Hechos', level=2)
        p_desc = doc.add_paragraph(reporte.get('descripcion', 'Sin descripción.'))
        p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        doc.add_paragraph()
        doc.add_paragraph("_" * 70).alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Firma
        doc.add_paragraph()
        doc.add_paragraph()
        p_firma = doc.add_paragraph("_____________________________\nFirma del Responsable / Coordinador")
        p_firma.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Pie de página
        footer = doc.add_paragraph(f"\nDocumento generado automáticamente el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}")
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.runs[0].font.size = Pt(8)
        footer.runs[0].font.color.rgb = RGBColor(0x6b, 0x72, 0x80)

        # -- Guardar Archivo --
        # Usar la ruta explícita o seguir con la vieja lógica de Downloads
        if not save_path:
            filename = f"Reporte_Incidente_{reporte.get('id', 'X')}_{datetime.now().strftime('%Y%m%d')}.docx"
            save_path = os.path.join(_get_downloads_folder(), filename)
            
            counter = 1
            while os.path.exists(save_path):
                filename = f"Reporte_Incidente_{reporte.get('id', 'X')}_{datetime.now().strftime('%Y%m%d')}_{counter}.docx"
                save_path = os.path.join(_get_downloads_folder(), filename)
                counter += 1

        doc.save(save_path)
        return save_path

    except Exception as e:
        print(f"Error generando DOCX: {e}")
        return None
