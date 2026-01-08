"""
Script para preparar los datos legales peruanos
Ejecutar: python -m scripts.prepare_legal_data
"""

import json
from pathlib import Path

# Base de conocimiento legal peruana
# En producción, esto vendría del scraping de SPIJ, Congreso, etc.
LEGAL_DATA = [
    # ═══════════════════════════════════════════════════════════════
    # CÓDIGO CIVIL - PERSONAS
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "cc-art-1",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 1",
        "titulo": "Sujeto de derecho",
        "texto": "La persona humana es sujeto de derecho desde su nacimiento. La vida humana comienza con la concepción. El concebido es sujeto de derecho para todo cuanto le favorece. La atribución de derechos patrimoniales está condicionada a que nazca vivo.",
        "libro": "Derecho de las Personas",
        "categoria": "civil"
    },
    
    # ═══════════════════════════════════════════════════════════════
    # CÓDIGO CIVIL - FAMILIA (ALIMENTOS)
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "cc-art-472",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 472",
        "titulo": "Definición de alimentos",
        "texto": "Se entiende por alimentos lo que es indispensable para el sustento, habitación, vestido, educación, instrucción y capacitación para el trabajo, asistencia médica y psicológica y recreación, según la situación y posibilidades de la familia. También los gastos del embarazo de la madre desde la concepción hasta la etapa de postparto.",
        "libro": "Derecho de Familia",
        "categoria": "familia"
    },
    {
        "id": "cc-art-474",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 474",
        "titulo": "Obligación recíproca de alimentos",
        "texto": "Se deben alimentos recíprocamente: 1. Los cónyuges. 2. Los ascendientes y descendientes. 3. Los hermanos.",
        "libro": "Derecho de Familia",
        "categoria": "familia"
    },
    {
        "id": "cc-art-481",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 481",
        "titulo": "Criterios para fijar alimentos",
        "texto": "Los alimentos se regulan por el juez en proporción a las necesidades de quien los pide y a las posibilidades del que debe darlos, atendiendo además a las circunstancias personales de ambos, especialmente a las obligaciones a que se halle sujeto el deudor. No es necesario investigar rigurosamente el monto de los ingresos del que debe prestar los alimentos.",
        "libro": "Derecho de Familia",
        "categoria": "familia"
    },
    {
        "id": "cc-art-483",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 483",
        "titulo": "Exoneración de alimentos",
        "texto": "El obligado a prestar alimentos puede pedir que se le exonere si disminuyen sus ingresos, de modo que no pueda atenderlos sin poner en peligro su propia subsistencia, o si ha desaparecido en el alimentista el estado de necesidad. Tratándose de hijos menores, a quienes el padre o la madre estuviese pasando una pensión alimenticia por resolución judicial, esta deja de regir al llegar aquellos a la mayoría de edad.",
        "libro": "Derecho de Familia",
        "categoria": "familia"
    },
    {
        "id": "cc-art-424",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 424",
        "titulo": "Subsistencia de alimentos a hijos mayores",
        "texto": "Subsiste la obligación de proveer al sostenimiento de los hijos e hijas solteros mayores de dieciocho años que estén siguiendo con éxito estudios de una profesión u oficio hasta los 28 años de edad; y de los hijos e hijas solteros que no se encuentren en aptitud de atender a su subsistencia por causas de incapacidad física o mental debidamente comprobadas.",
        "libro": "Derecho de Familia",
        "categoria": "familia"
    },
    
    # ═══════════════════════════════════════════════════════════════
    # CÓDIGO CIVIL - CONTRATOS
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "cc-art-1351",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 1351",
        "titulo": "Noción de contrato",
        "texto": "El contrato es el acuerdo de dos o más partes para crear, regular, modificar o extinguir una relación jurídica patrimonial.",
        "libro": "Fuentes de las Obligaciones",
        "categoria": "civil"
    },
    {
        "id": "cc-art-1361",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 1361",
        "titulo": "Obligatoriedad del contrato",
        "texto": "Los contratos son obligatorios en cuanto se haya expresado en ellos. Se presume que la declaración expresada en el contrato responde a la voluntad común de las partes y quien niegue esa coincidencia debe probarla.",
        "libro": "Fuentes de las Obligaciones",
        "categoria": "civil"
    },
    {
        "id": "cc-art-1666",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 1666",
        "titulo": "Definición de arrendamiento",
        "texto": "Por el arrendamiento el arrendador se obliga a ceder temporalmente al arrendatario el uso de un bien por cierta renta convenida.",
        "libro": "Fuentes de las Obligaciones",
        "categoria": "civil"
    },
    {
        "id": "cc-art-1678",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 1678",
        "titulo": "Obligaciones del arrendador",
        "texto": "El arrendador está obligado a entregar al arrendatario el bien arrendado con todos sus accesorios, en el plazo, lugar y estado convenidos. Si no se indica en el contrato el tiempo ni el lugar de la entrega, debe realizarse inmediatamente donde se celebró, salvo que por costumbre deba efectuarse en otro lugar o época.",
        "libro": "Fuentes de las Obligaciones",
        "categoria": "civil"
    },
    {
        "id": "cc-art-1681",
        "ley": "Código Civil Peruano",
        "numero_ley": "Decreto Legislativo 295",
        "articulo": "Artículo 1681",
        "titulo": "Obligaciones del arrendatario",
        "texto": "El arrendatario está obligado: 1. A recibir el bien, cuidarlo diligentemente y usarlo para el destino que se le concedió en el contrato o al que pueda presumirse de las circunstancias. 2. A pagar puntualmente la renta en el plazo y lugar convenidos y, a falta de convenio, cada mes, en su domicilio. 3. A pagar puntualmente los servicios públicos suministrados en beneficio del bien, con sujeción a las normas que los regulan. 4. A dar aviso inmediato al arrendador de cualquier usurpación, perturbación o imposición de servidumbre que se intente contra el bien. 5. A permitir al arrendador que inspeccione por causa justificada el bien, previo aviso de siete días, y a hacer las reparaciones que le correspondan conforme a la ley o al contrato. 6. A no hacer uso imprudente del bien o contrario al orden público o a las buenas costumbres. 7. A no introducir cambios ni modificaciones en el bien, sin asentimiento del arrendador. 8. A no subarrendar el bien, total o parcialmente, ni ceder el contrato, sin asentimiento escrito del arrendador. 9. A devolver el bien al arrendador al vencerse el plazo del contrato en el estado en que lo recibió, sin más deterioro que el de su uso ordinario. 10. A cumplir las demás obligaciones que establezca la ley o el contrato.",
        "libro": "Fuentes de las Obligaciones",
        "categoria": "civil"
    },
    
    # ═══════════════════════════════════════════════════════════════
    # DERECHO LABORAL
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "lab-ds003-art4",
        "ley": "Ley de Productividad y Competitividad Laboral",
        "numero_ley": "D.S. 003-97-TR",
        "articulo": "Artículo 4",
        "titulo": "Contrato de trabajo",
        "texto": "En toda prestación personal de servicios remunerados y subordinados, se presume la existencia de un contrato de trabajo a plazo indeterminado. El contrato individual de trabajo puede celebrarse libremente por tiempo indeterminado o sujeto a modalidad. El primero podrá celebrarse en forma verbal o escrita y el segundo en los casos y con los requisitos que la presente Ley establece.",
        "libro": "Del Contrato de Trabajo",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds003-art10",
        "ley": "Ley de Productividad y Competitividad Laboral",
        "numero_ley": "D.S. 003-97-TR",
        "articulo": "Artículo 10",
        "titulo": "Período de prueba",
        "texto": "El período de prueba es de tres meses, a cuyo término el trabajador alcanza derecho a la protección contra el despido arbitrario. Las partes pueden pactar un término mayor en caso las labores requieran de un período de capacitación o adaptación o que por su naturaleza o grado de responsabilidad tal prolongación pueda resultar justificada. La ampliación del período de prueba debe constar por escrito y no podrá exceder, en conjunto con el período inicial, de seis meses en el caso de trabajadores calificados o de confianza y de un año en el caso de personal de dirección.",
        "libro": "Del Contrato de Trabajo",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds003-art16",
        "ley": "Ley de Productividad y Competitividad Laboral",
        "numero_ley": "D.S. 003-97-TR",
        "articulo": "Artículo 16",
        "titulo": "Causas de extinción del contrato",
        "texto": "Son causas de extinción del contrato de trabajo: a) El fallecimiento del trabajador o del empleador si es persona natural; b) La renuncia o retiro voluntario del trabajador; c) La terminación de la obra o servicio, el cumplimiento de la condición resolutoria y el vencimiento del plazo en los contratos legalmente celebrados bajo modalidad; d) El mutuo disenso entre trabajador y empleador; e) La invalidez absoluta permanente; f) La jubilación; g) El despido, en los casos y forma permitidos por la Ley; h) La terminación de la relación laboral por causa objetiva, en los casos y forma permitidos por la presente Ley.",
        "libro": "Extinción del Contrato de Trabajo",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds003-art22",
        "ley": "Ley de Productividad y Competitividad Laboral",
        "numero_ley": "D.S. 003-97-TR",
        "articulo": "Artículo 22",
        "titulo": "Despido justificado",
        "texto": "Para el despido de un trabajador sujeto a régimen de la actividad privada, que labore cuatro o más horas diarias para un mismo empleador, es indispensable la existencia de causa justa contemplada en la ley y debidamente comprobada. La causa justa puede estar relacionada con la capacidad o con la conducta del trabajador. La demostración de la causa corresponde al empleador dentro del proceso judicial que el trabajador pudiera interponer para impugnar su despido.",
        "libro": "Extinción del Contrato de Trabajo",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds003-art34",
        "ley": "Ley de Productividad y Competitividad Laboral",
        "numero_ley": "D.S. 003-97-TR",
        "articulo": "Artículo 34",
        "titulo": "Despido arbitrario",
        "texto": "El despido del trabajador fundado en causas relacionadas con su conducta o su capacidad no da lugar a indemnización. Si el despido es arbitrario por no haberse expresado causa o no poderse demostrar ésta en juicio, el trabajador tiene derecho al pago de la indemnización establecida en el Artículo 38, como única reparación por el daño sufrido. Podrá demandar simultáneamente el pago de cualquier otro derecho o beneficio social pendiente.",
        "libro": "Extinción del Contrato de Trabajo",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds003-art38",
        "ley": "Ley de Productividad y Competitividad Laboral",
        "numero_ley": "D.S. 003-97-TR",
        "articulo": "Artículo 38",
        "titulo": "Indemnización por despido arbitrario",
        "texto": "La indemnización por despido arbitrario es equivalente a una remuneración y media ordinaria mensual por cada año completo de servicios con un máximo de doce (12) remuneraciones. Las fracciones de año se abonan por dozavos y treintavos, según corresponda. Su abono procede superado el período de prueba.",
        "libro": "Extinción del Contrato de Trabajo",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds001-art1",
        "ley": "Ley de Compensación por Tiempo de Servicios",
        "numero_ley": "D.S. 001-97-TR",
        "articulo": "Artículo 1",
        "titulo": "Naturaleza de la CTS",
        "texto": "La compensación por tiempo de servicios tiene la calidad de beneficio social de previsión de las contingencias que origina el cese en el trabajo y de promoción del trabajador y su familia.",
        "libro": "Disposiciones Generales",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds001-art2",
        "ley": "Ley de Compensación por Tiempo de Servicios",
        "numero_ley": "D.S. 001-97-TR",
        "articulo": "Artículo 2",
        "titulo": "Trabajadores comprendidos",
        "texto": "La compensación por tiempo de servicios se devenga desde el primer mes de iniciado el vínculo laboral; cumplido este requisito toda fracción se computa por treintavos. La CTS se deposita semestralmente en la institución elegida por el trabajador. Efectuado el depósito queda cumplida y pagada la obligación, sin perjuicio de los reintegros que deban efectuarse en caso de depósito insuficiente o que resultare diminuto.",
        "libro": "Disposiciones Generales",
        "categoria": "laboral"
    },
    {
        "id": "lab-ds001-art21",
        "ley": "Ley de Compensación por Tiempo de Servicios",
        "numero_ley": "D.S. 001-97-TR",
        "articulo": "Artículo 21",
        "titulo": "Remuneración computable para CTS",
        "texto": "Son remuneración computable la remuneración básica y todas las cantidades que regularmente perciba el trabajador, en dinero o en especie como contraprestación de su labor, cualquiera sea la denominación que se les dé, siempre que sean de su libre disposición. Se incluye en este concepto el valor de la alimentación principal cuando es proporcionada en especie por el empleador y se excluyen los conceptos contemplados en los Artículos 19 y 20 de esta Ley.",
        "libro": "Remuneración Computable",
        "categoria": "laboral"
    },
    {
        "id": "lab-dl713-art10",
        "ley": "Ley de Descansos Remunerados",
        "numero_ley": "D.L. 713",
        "articulo": "Artículo 10",
        "titulo": "Duración de vacaciones",
        "texto": "El trabajador tiene derecho a treinta días calendario de descanso vacacional por cada año completo de servicios.",
        "libro": "Vacaciones Anuales",
        "categoria": "laboral"
    },
    {
        "id": "lab-dl713-art23",
        "ley": "Ley de Descansos Remunerados",
        "numero_ley": "D.L. 713",
        "articulo": "Artículo 23",
        "titulo": "Triple remuneración vacacional",
        "texto": "Los trabajadores, en caso de no disfrutar del descanso vacacional dentro del año siguiente a aquél en el que adquieren el derecho, percibirán lo siguiente: a) Una remuneración por el trabajo realizado; b) Una remuneración por el descanso vacacional adquirido y no gozado; y, c) Una indemnización equivalente a una remuneración por no haber disfrutado del descanso. Esta indemnización no está sujeta a pago o retención de ninguna aportación, contribución o tributo.",
        "libro": "Vacaciones Anuales",
        "categoria": "laboral"
    },
    
    # ═══════════════════════════════════════════════════════════════
    # CÓDIGO DEL CONSUMIDOR
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "cons-ley29571-art1",
        "ley": "Código de Protección y Defensa del Consumidor",
        "numero_ley": "Ley 29571",
        "articulo": "Artículo 1",
        "titulo": "Derechos de los consumidores",
        "texto": "1.1 En los términos establecidos por el presente Código, los consumidores tienen los siguientes derechos: a) Derecho a una protección eficaz respecto de los productos y servicios que, en condiciones normales o previsibles, representen riesgo o peligro para la vida, salud e integridad física. b) Derecho a acceder a información oportuna, suficiente, veraz y fácilmente accesible, relevante para tomar una decisión o realizar una elección de consumo que se ajuste a sus intereses, así como para efectuar un uso o consumo adecuado de los productos o servicios. c) Derecho a la protección de sus intereses económicos y en particular contra las cláusulas abusivas, métodos comerciales coercitivos, cualquier otra práctica análoga e información interesadamente equívoca sobre los productos o servicios. d) Derecho a un trato justo y equitativo en toda transacción comercial y a no ser discriminados por motivo de origen, raza, sexo, idioma, religión, opinión, condición económica o de cualquier otra índole. e) Derecho a la reparación o reposición del producto, a una nueva ejecución del servicio, o en los casos previstos en el presente Código, a la devolución de la cantidad pagada, según las circunstancias. f) Derecho a elegir libremente entre productos y servicios idóneos y de calidad, conforme a la normativa pertinente, que se ofrezcan en el mercado y a ser informados por el proveedor sobre los que cuenta. g) A la protección de sus derechos mediante procedimientos eficaces, céleres o ágiles, con formalidades mínimas, gratuitos o no costosos, según sea el caso, para la atención de sus reclamos o denuncias ante las autoridades competentes.",
        "libro": "Derechos de los Consumidores",
        "categoria": "consumidor"
    },
    {
        "id": "cons-ley29571-art18",
        "ley": "Código de Protección y Defensa del Consumidor",
        "numero_ley": "Ley 29571",
        "articulo": "Artículo 18",
        "titulo": "Idoneidad",
        "texto": "Se entiende por idoneidad la correspondencia entre lo que un consumidor espera y lo que efectivamente recibe, en función a lo que se le hubiera ofrecido, la publicidad e información transmitida, las condiciones y circunstancias de la transacción, las características y naturaleza del producto o servicio, el precio, entre otros factores, atendiendo a las circunstancias del caso. La idoneidad es evaluada en función a la propia naturaleza del producto o servicio y a su aptitud para satisfacer la finalidad para la cual ha sido puesto en el mercado.",
        "libro": "Protección del Consumidor",
        "categoria": "consumidor"
    },
    {
        "id": "cons-ley29571-art19",
        "ley": "Código de Protección y Defensa del Consumidor",
        "numero_ley": "Ley 29571",
        "articulo": "Artículo 19",
        "titulo": "Obligación de los proveedores",
        "texto": "El proveedor responde por la idoneidad y calidad de los productos y servicios ofrecidos; por la autenticidad de las marcas y leyendas que exhiben sus productos o del signo que respalda al prestador del servicio, por la falta de conformidad entre la publicidad comercial de los productos y servicios y éstos, así como por el contenido y la vida útil del producto indicado en el envase, en lo que corresponda.",
        "libro": "Protección del Consumidor",
        "categoria": "consumidor"
    },
    {
        "id": "cons-ley29571-art97",
        "ley": "Código de Protección y Defensa del Consumidor",
        "numero_ley": "Ley 29571",
        "articulo": "Artículo 97",
        "titulo": "Derechos de los consumidores frente a productos defectuosos",
        "texto": "Los consumidores tienen derecho, en los términos establecidos por el presente Código, a la reparación o reposición del producto, a una nueva ejecución del servicio, o a la devolución de la cantidad pagada, según las circunstancias, sin perjuicio de la indemnización por los daños y perjuicios ocasionados.",
        "libro": "Responsabilidad del Proveedor",
        "categoria": "consumidor"
    },
    {
        "id": "cons-ley29571-art150",
        "ley": "Código de Protección y Defensa del Consumidor",
        "numero_ley": "Ley 29571",
        "articulo": "Artículo 150",
        "titulo": "Libro de reclamaciones",
        "texto": "Los establecimientos comerciales deben contar con un libro de reclamaciones, en forma física o virtual. El reglamento establece las condiciones, los supuestos y las demás especificaciones para el cumplimiento de esta obligación. Los consumidores pueden exigir la entrega del libro de reclamaciones para formular su queja o reclamo respecto de los productos o servicios ofertados. Los establecimientos comerciales tienen la obligación de remitir al Indecopi la documentación correspondiente al libro de reclamaciones cuando éste sea requerido. En los procedimientos sancionadores, el proveedor debe acreditar que atendió o contestó el reclamo en un plazo máximo de treinta (30) días calendario.",
        "libro": "Procedimientos",
        "categoria": "consumidor"
    },
    
    # ═══════════════════════════════════════════════════════════════
    # TRÁNSITO
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "trans-ds016-art295",
        "ley": "Reglamento Nacional de Tránsito",
        "numero_ley": "D.S. 016-2009-MTC",
        "articulo": "Artículo 295",
        "titulo": "Impugnación de papeletas",
        "texto": "El presunto infractor podrá interponer recurso de reconsideración dentro de los siete (7) días hábiles de notificado, ante la autoridad que impuso la sanción. También podrá interponer recurso de apelación ante el superior jerárquico dentro de los quince (15) días hábiles de notificada la resolución que resuelve el recurso de reconsideración o de notificada la papeleta si no interpuso reconsideración. La interposición de cualquiera de los recursos administrativos no suspende la ejecución de la sanción, salvo que se presente garantía conforme a ley.",
        "libro": "Procedimiento Sancionador",
        "categoria": "transito"
    },
    {
        "id": "trans-ds016-art313",
        "ley": "Reglamento Nacional de Tránsito",
        "numero_ley": "D.S. 016-2009-MTC",
        "articulo": "Artículo 313",
        "titulo": "Clasificación de infracciones",
        "texto": "Las infracciones de tránsito se clasifican en: a) Muy graves (M); b) Graves (G); c) Leves (L). Las sanciones se aplican de acuerdo a la clasificación de la infracción cometida, siguiendo la escala establecida en el presente Reglamento.",
        "libro": "Infracciones y Sanciones",
        "categoria": "transito"
    },
    
    # ═══════════════════════════════════════════════════════════════
    # EMPRESAS
    # ═══════════════════════════════════════════════════════════════
    {
        "id": "emp-ley26887-art1",
        "ley": "Ley General de Sociedades",
        "numero_ley": "Ley 26887",
        "articulo": "Artículo 1",
        "titulo": "La Sociedad",
        "texto": "Quienes constituyen la Sociedad convienen en aportar bienes o servicios para el ejercicio en común de actividades económicas.",
        "libro": "Reglas Aplicables a todas las Sociedades",
        "categoria": "empresas"
    },
    {
        "id": "emp-ley26887-art51",
        "ley": "Ley General de Sociedades",
        "numero_ley": "Ley 26887",
        "articulo": "Artículo 51",
        "titulo": "Capital y acciones",
        "texto": "En la sociedad anónima el capital está representado por acciones nominativas y se integra por aportes de los accionistas, quienes no responden personalmente de las deudas sociales. No se admite el aporte de servicios en la sociedad anónima.",
        "libro": "Sociedad Anónima",
        "categoria": "empresas"
    },
    {
        "id": "emp-ley26887-art234",
        "ley": "Ley General de Sociedades",
        "numero_ley": "Ley 26887",
        "articulo": "Artículo 234",
        "titulo": "Sociedad Anónima Cerrada",
        "texto": "La sociedad anónima puede sujetarse al régimen de la sociedad anónima cerrada cuando tiene no más de veinte accionistas y no tiene acciones inscritas en el Registro Público del Mercado de Valores. No se puede solicitar la inscripción en dicho registro de las acciones de una sociedad anónima cerrada.",
        "libro": "Sociedad Anónima Cerrada",
        "categoria": "empresas"
    },
    {
        "id": "emp-ley21621-art1",
        "ley": "Ley de la Empresa Individual de Responsabilidad Limitada",
        "numero_ley": "D.L. 21621",
        "articulo": "Artículo 1",
        "titulo": "Definición de EIRL",
        "texto": "La Empresa Individual de Responsabilidad Limitada es una persona jurídica de derecho privado, constituida por voluntad unipersonal, con patrimonio propio distinto al de su Titular, que se constituye para el desarrollo exclusivo de actividades económicas de Pequeña Empresa, al amparo del Decreto Ley Nº 21435.",
        "libro": "Disposiciones Generales",
        "categoria": "empresas"
    },
    {
        "id": "emp-ley21621-art3",
        "ley": "Ley de la Empresa Individual de Responsabilidad Limitada",
        "numero_ley": "D.L. 21621",
        "articulo": "Artículo 3",
        "titulo": "Responsabilidad limitada",
        "texto": "La responsabilidad de la Empresa está limitada a su patrimonio. El Titular de la Empresa no responde personalmente por las obligaciones de ésta, salvo lo dispuesto en el artículo 41º de esta Ley.",
        "libro": "Disposiciones Generales",
        "categoria": "empresas"
    },
]


def save_legal_data():
    """Guarda los datos legales en formato JSON"""
    import os
    
    # Crear directorio data si no existe
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "legal_knowledge.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(LEGAL_DATA, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Guardados {len(LEGAL_DATA)} artículos en {output_file}")
    
    # Mostrar resumen por categoría
    categorias = {}
    for item in LEGAL_DATA:
        cat = item["categoria"]
        categorias[cat] = categorias.get(cat, 0) + 1
    
    print("\n📊 Resumen por categoría:")
    for cat, count in sorted(categorias.items()):
        print(f"   - {cat}: {count} artículos")
    
    return output_file


if __name__ == "__main__":
    save_legal_data()

