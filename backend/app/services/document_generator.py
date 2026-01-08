"""
Document Generation Service for Legal Documents
"""

from typing import Dict, Any, Optional
from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from jinja2 import Template


# Document templates
DOCUMENT_TEMPLATES = {
    "carta-reclamo": {
        "name": "Carta de Reclamo Simple",
        "template": """
Lima, {{ fecha }}

Señores
{{ empresa }}
Presente.-

ASUNTO: RECLAMO POR {{ motivo | upper }}

De mi consideración:

Yo, {{ nombreCompleto }}, identificado(a) con DNI N° {{ dni }}, con domicilio en {{ direccion }}, me dirijo a ustedes para presentar el siguiente reclamo:

HECHOS:
{{ hechos }}

PETICIÓN:
{{ peticion }}

Por lo expuesto, solicito se atienda mi reclamo en el plazo establecido por ley, caso contrario, me veré en la necesidad de presentar mi queja ante INDECOPI.

Atentamente,

_________________________
{{ nombreCompleto }}
DNI: {{ dni }}
"""
    },
    "carta-notarial": {
        "name": "Carta Notarial de Intimación",
        "template": """
CARTA NOTARIAL

Lima, {{ fecha }}

Señor(a)
{{ destinatario }}
{{ direccionDestinatario }}
Presente.-

Por medio de la presente, yo, {{ nombreCompleto }}, identificado(a) con DNI N° {{ dni }}, con domicilio en {{ direccion }}, me dirijo a usted para INTIMARLO a cumplir con lo siguiente:

ANTECEDENTES:
{{ hechos }}

{% if monto %}
MONTO ADEUDADO: S/. {{ monto }}
{% endif %}

REQUERIMIENTO:
Por lo expuesto, le REQUIERO cumplir con la obligación pendiente en un plazo máximo de {{ plazo }} días calendario, contados desde la recepción de la presente carta.

De no cumplir con lo requerido, me veré en la obligación de iniciar las acciones legales correspondientes, lo que generará mayores gastos y costas que serán de su cargo.

Sin otro particular, me suscribo.

Atentamente,

_________________________
{{ nombreCompleto }}
DNI: {{ dni }}
"""
    },
    "contrato-alquiler": {
        "name": "Contrato de Alquiler de Vivienda",
        "template": """
CONTRATO DE ARRENDAMIENTO DE BIEN INMUEBLE

Conste por el presente documento, el contrato de arrendamiento que celebran:

EL ARRENDADOR: {{ arrendador }}, identificado con DNI N° {{ dniArrendador }}

EL ARRENDATARIO: {{ arrendatario }}, identificado con DNI N° {{ dniArrendatario }}

En los términos y condiciones siguientes:

PRIMERO: DEL INMUEBLE
El ARRENDADOR es propietario del inmueble ubicado en {{ direccionInmueble }}, el cual da en arrendamiento al ARRENDATARIO.

SEGUNDO: DEL PLAZO
El presente contrato tiene una duración de {{ duracion }} meses, iniciando el {{ fechaInicio }}.

TERCERO: DE LA RENTA
El monto de la renta mensual es de S/. {{ montoRenta }} ({{ montoRentaLetras }} Soles), que el ARRENDATARIO pagará el primer día de cada mes.

CUARTO: DE LA GARANTÍA
El ARRENDATARIO entrega la suma equivalente a {{ garantia }} meses de renta como garantía.

QUINTO: OBLIGACIONES DEL ARRENDATARIO
a) Pagar puntualmente la renta
b) Mantener el inmueble en buen estado
c) No subarrendar el inmueble
d) Usar el inmueble solo para vivienda

SEXTO: CAUSALES DE RESOLUCIÓN
El contrato podrá resolverse por:
a) Falta de pago de dos meses consecutivos
b) Destinar el inmueble a uso diferente
c) Subarrendar sin autorización

Firmado en Lima, a los {{ dia }} días del mes de {{ mes }} de {{ anio }}.

_________________________          _________________________
ARRENDADOR                         ARRENDATARIO
DNI: {{ dniArrendador }}           DNI: {{ dniArrendatario }}
"""
    },
}


def format_date_spanish(date: datetime) -> Dict[str, str]:
    """Format date components in Spanish"""
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    return {
        "dia": str(date.day),
        "mes": meses[date.month - 1],
        "anio": str(date.year),
        "fecha": date.strftime("%d de ") + meses[date.month - 1] + date.strftime(" de %Y")
    }


def number_to_words(number: int) -> str:
    """Convert number to Spanish words (simplified)"""
    # Simplified implementation
    units = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
    teens = ["diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve"]
    tens = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
    hundreds = ["", "cien", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]
    
    if number < 10:
        return units[number]
    elif number < 20:
        return teens[number - 10]
    elif number < 100:
        if number % 10 == 0:
            return tens[number // 10]
        return f"{tens[number // 10]} y {units[number % 10]}"
    elif number < 1000:
        if number == 100:
            return "cien"
        if number % 100 == 0:
            return hundreds[number // 100]
        return f"{hundreds[number // 100]} {number_to_words(number % 100)}"
    else:
        return str(number)


def generate_document_content(template_id: str, data: Dict[str, Any]) -> str:
    """Generate document content from template and data"""
    template_info = DOCUMENT_TEMPLATES.get(template_id)
    if not template_info:
        raise ValueError(f"Template not found: {template_id}")
    
    # Add date information
    now = datetime.now()
    data.update(format_date_spanish(now))
    
    # Add number to words for monetary amounts
    if "montoRenta" in data and data["montoRenta"]:
        try:
            monto = int(float(data["montoRenta"]))
            data["montoRentaLetras"] = number_to_words(monto)
        except:
            data["montoRentaLetras"] = data["montoRenta"]
    
    # Render template
    template = Template(template_info["template"])
    content = template.render(**data)
    
    return content


def generate_pdf(content: str, title: str) -> BytesIO:
    """Generate a PDF document from content"""
    buffer = BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=1*inch,
        leftMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=20,
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16,
    )
    
    right_style = ParagraphStyle(
        'RightAligned',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_RIGHT,
    )
    
    # Build document
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # Process content
    paragraphs = content.strip().split('\n\n')
    for para in paragraphs:
        if para.strip():
            # Handle special formatting
            lines = para.strip().split('\n')
            for line in lines:
                if line.strip():
                    story.append(Paragraph(line.strip(), body_style))
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer


async def generate_legal_document(
    template_id: str,
    data: Dict[str, str],
    add_watermark: bool = False
) -> tuple[BytesIO, str]:
    """
    Generate a legal document.
    
    Returns:
        - pdf_buffer: BytesIO containing the PDF
        - preview_content: Text content for preview
    """
    template_info = DOCUMENT_TEMPLATES.get(template_id)
    if not template_info:
        raise ValueError(f"Template not found: {template_id}")
    
    # Generate content
    content = generate_document_content(template_id, data)
    
    # Generate PDF
    pdf_buffer = generate_pdf(content, template_info["name"])
    
    return pdf_buffer, content


def get_available_templates() -> list:
    """Get list of available document templates"""
    return [
        {
            "id": template_id,
            "name": info["name"],
        }
        for template_id, info in DOCUMENT_TEMPLATES.items()
    ]

