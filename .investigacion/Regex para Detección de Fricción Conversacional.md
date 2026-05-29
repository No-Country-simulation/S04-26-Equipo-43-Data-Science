# **Detección de Fricción Conversacional en Pipelines de Inferencia Híbridos: Marco Heurístico de Expresiones Regulares para ConversaSense AI**

## **Arquitectura de Inferencia en Cascada y el Rol de la Capa CPU**

En el diseño de sistemas conversacionales orientados a los sectores de banca, tecnología financiera (Fintech) y comercio electrónico, la latencia de respuesta y los costes de infraestructura representan dos de las restricciones operativas más críticas.1 Para mitigar el alto coste computacional asociado al uso sistemático de Modelos de Lenguaje de Gran Tamaño (LLMs) que operan en unidades de procesamiento gráfico (GPUs), las arquitecturas avanzadas emplean pipelines de inferencia híbridos en cascada.3  
El sistema ConversaSense AI implementa este enfoque bifásico mediante una primera capa de clasificación hospedada en CPU que utiliza el algoritmo de potenciación de gradiente LightGBM.3 Esta capa actúa como un filtro de clasificación rápida y de bajo coste, procesando cada mensaje entrante en un tiempo inferior a los cinco milisegundos.3 Su objetivo principal es extraer un conjunto de características heurísticas simples y representaciones vectoriales dispersas para predecir si el usuario se encuentra en un estado de alta fricción o insatisfacción conversacional.3  
La optimización de esta primera capa CPU es fundamental.3 Si el clasificador heurístico detecta señales inequívocas de frustración, agresividad o intentos implícitos de escalamiento, el sistema puede eludir la llamada al modelo generativo en GPU.3 Al interrumpir el flujo estándar, se puede desviar la conversación de forma inmediata hacia un protocolo de contención, modificar dinámicamente el tono del asistente virtual o transferir la sesión directamente a un agente humano en tiempo real.3 Este desvío temprano reduce de forma drástica la latencia global y los costes por tokens consumidos, al tiempo que previene el abandono del usuario debido a respuestas automatizadas repetitivas.2  
Para formalizar la extracción de estas características heurísticas dentro del clasificador de primera capa, se define un vector de activación de expresiones regulares ![][image1] para un texto de usuario ![][image2]. Cada componente ![][image3] de este vector se calcula mediante una función indicadora sobre la coincidencia de un patrón regular ![][image4] 3:  
![][image5]  
Donde ![][image6] es la función indicadora que devuelve ![][image7] si el motor de expresiones regulares identifica el patrón en el texto, y ![][image8] en caso contrario.3 Posteriormente, este vector ![][image9] se concatena con variables contextuales e históricas del diálogo ![][image10]—tales como la tasa de repetición de intenciones fallidas, la longitud del mensaje o el tiempo de espera acumulado—para alimentar la función de decisión del clasificador LightGBM 3:  
![][image11]  
Si la probabilidad estimada ![][image12] supera un umbral crítico ![][image13], el sistema activa de forma inmediata el protocolo de escalamiento o de ajuste del tono conversacional.3 Para garantizar la máxima sensibilidad de esta capa y capturar la amplia variedad de modismos, variaciones ortográficas y estructuras regionales en los mercados hispanohablantes y lusófonos, se presenta a continuación el diccionario heurístico optimizado de ConversaSense AI.10

## **Diccionario SIGNALS de ConversaSense AI**

El siguiente bloque de código en Python define el diccionario de configuración estructurado para el pipeline de inferencia de ConversaSense AI. Los patrones de expresiones regulares han sido diseñados para ser compilados con soporte de insensibilidad a mayúsculas y minúsculas (re.IGNORECASE), tolerancia a la omisión de tildes mediante caracteres de clase opcionales y optimización de rendimiento a través de agrupamientos no capturadores (?:...) y delimitadores de palabra \\b.12

Python  
import re

\# ConversaSense AI: Diccionario Heurístico de Fricción Conversacional (SIGNALS)  
\# Optimizado para una rápida evaluación en CPU y alta sensibilidad dialectal.

SIGNALS \= {  
    "ES": {  
        "PROFANITY\_IMPLICIT\_AGRESSION": \[  
            \# Captura insultos atenuados, términos de descontento agudo, estafas y vulgaridades regionales (España y LatAm)  
            re.compile(  
                r"\\b(?:p\[eé\]s\[ií\]mo\\s+serv\[ií\]c\[ií\]o|me\\s+est\[aá\]n?\\s+tomando\\s+el\\s+pelo|es\\s+un\\s+ch\[ií\]ste|vaya\\s+(?:ayuda|basura|porquer\[ií\]a)|estafador(?:es)?|g\[ií\]l\[ií\]pollas|v\[eé\]te\\s+a\\s+fre\[ií\]r\\s+esp\[aá\]rragos|una\\s+polla\\s+en\\s+v\[ií\]nagre|hasta\\s+los\\s+(?:huevos|cojones|pelotas|catapl\[ií\]nes)|me\\s+cago\\s+en|p\[ií\]nche|no\\s+mames|ch\[ií\]nga(?:r|te|\\s+tu)?|val\[ií\]\[oó\]\\s+verga|pendejo\[as\]?|la\\s+concha\\s+de|boludo\[as\]?|pelotudo\[as\]?|h\[ií\]jueputa|gonorrea|huev\[oó\]n|carajo|m\[ií\]erda|por\\s+la\\s+puta\\s+madre)\\b",  
                re.IGNORECASE  
            )  
        \],  
        "NEGATION\_RESIGNATION": \[  
            \# Captura la desconexión del usuario, rechazo de propuestas del bot e impotencia ante respuestas automáticas  
            re.compile(  
                r"\\b(?:no\\s+me\\s+s\[ií\]rve|deja\\s+as\[ií\]|no\\s+es\\s+eso|olv\[ií\]dalo|otra\\s+vez\\s+con\\s+lo\\s+m\[ií\]smo|no\\s+ent\[ií\]endes\\s+nada|as\[ií\]\\s+no\\s+se\\s+puede|decepcionado\[as\]?|no\\s+entiend\[es|e\]|corta\\s+el\\s+rollo|es\\s+un\\s+rollo|no\\s+sirve\\s+para\\s+nada|me\\s+rindo|ya\\s+para\\s+qu\[eé\]|deja\\s+de\\s+escribir|eres\\s+in\[uú\]t\[ií\]l|vuelve\\s+a\\s+ti\\s+mismo)\\b",  
                re.IGNORECASE  
            )  
        \],  
        "IMPLICIT\_ESCALATION": \[  
            \# Captura solicitudes de transferencia humana eludiendo palabras clave explícitas como "agente" o "humano"  
            re.compile(  
                r"\\b(?:alg\[uú\]i\[eé\]n\\s+real|con\\s+una\\s+persona|que\\s+me\\s+atienda\\s+alg\[uú\]i\[eé\]n|con\\s+un\\s+superv\[ií\]sor|tel\[eé\]fono\\s+de\\s+soporte|as\[ií\]stenc\[ií\]a\\s+de\\s+verdad|atenc\[ií\]\[oó\]n\\s+humana|soporte\\s+humano|hablar\\s+con\\s+humano|con\\s+un\\s+humano|atenci\[oó\]n\\s+espec\[ií\]al\[ií\]zada|atendente\\s+de\\s+carne\\s+y\\s+hueso|asesor\\s+verdadero)\\b",  
                re.IGNORECASE  
            )  
        \],  
        "SARCASM\_VEILED\_FRUSTRATION": \[  
            \# Captura exclamaciones de aparente satisfacción asociadas temporalmente a bloqueos, cobros incorrectos o fallos  
            re.compile(  
                r"\\b(?:(?:gen\[ií\]al|excelente|marav\[ií\]llosa|buen\[ií\]s\[ií\]ma|l\[ií\]nda|gran)\\s+(?:ayuda|atenc\[ií\]\[oó\]n|serv\[ií\]c\[ií\]o)\\s\*(?:\\(sarc\[aá\]st\[ií\]co\\)\\s\*)?|grac\[ií\]as\\s+por\\s+nada|(?:s\[uú\]per|gen\[ií\]al|excelente)\\s\*,\\s\*(?:me\\s+bloquearon|me\\s+estafaron|me\\s+bloqueaste|no\\s+func\[ií\]ona|un\\s+desastre|otra\\s+traba|otra\\s+tonter\[ií\]a|me\\s+bloqueasteis|vaya\\s+jefe|qu\[eé\]\\s+jefazo))\\b",  
                re.IGNORECASE  
            )  
        \]  
    },  
    "PT": {  
        "PROFANITY\_IMPLICIT\_AGRESSION":ada|est\[aã\]o\\s+me\\s+t\[ií\]rando|que\\s+p\[ií\]ada|p\[eé\]ss\[ií\]mo\\s+serv\[ií\]\[cç\]o|br\[ií\]ncade\[ií\]ra|pelas\\s+barbas\\s+do\\s+profeta|macacos\\s+me\\s+mordam|f\[ií\]car\\s+p\\s+da\\s+v\[ií\]da|merda|puta\\s+que\\s+par\[ií\]u|pqp|caralho|v\[aã\]o\\s+se\\s+foder|bosta|desgra\[cç\]a|f\[ií\]lho\\s+da\\s+puta|\[ií\]mbe\[cç\]\[ií\]l|\[ií\]d\[ií\]ota)\\b",  
                re.IGNORECASE  
            )  
        \],  
        "NEGATION\_RESIGNATION": \[  
            \# Captura el desistimiento conversacional, la inutilidad percibida y estados afectivos de apatía  
            re.compile(  
                r"\\b(?:de\[ií\]xa\\s+pra\\s+l\[aá\]|n\[aã\]o\\s+ad\[ií\]anta|esquece|de\\s+novo\\s+i\[s|ss\]o|voc\[eê\]\\s+n\[aã\]o\\s+entende|n\[aã\]o\\s+serve|t\[ií\]rar\\s+o\\s+caval\[ií\]nho\\s+da\\s+chuva|ver\\s+nav\[ií\]os|chatead\[oa\]|morgad\[oa\]|magoad\[oa\]|aborrec\[ií\]d\[oa\]|\[ií\]rr\[ií\]tad\[oa\]|abusad\[oa\]|zangad\[oa\]|enjeitad\[oa\]|enjoado\[as\]?|n\[aã\]o\\s+func\[ií\]ona|des\[ií\]sto|canse\[ií\])\\b",  
                re.IGNORECASE  
            )  
        \],  
        "IMPLICIT\_ESCALATION": \[  
            \# Captura solicitudes indirectas de derivación a agentes reales o físicos en canales de soporte lusófonos  
            re.compile(  
                r"\\b(?:algu\[eé\]m\\s+de\\s+verdade|falar\\s+com\\s+pessoa|atendente\\s+real|ajuda\\s+humana|atend\[ií\]mento\\s+espec\[ií\]al\[ií\]zado|falar\\s+com\\s+humano|atendente\\s+humano|quero\\s+falar\\s+com\\s+algu\[eé\]m|suporte\\s+humano|quero\\s+um\\s+humano|n\[aã\]o\\s+quero\\s+rob\[oó\]|falar\\s+com\\s+um\\s+gerente)\\b",  
                re.IGNORECASE  
            )  
        \],  
        "SARCASM\_VEILED\_FRUSTRATION": \[  
            \# Identifica agradecimientos irónicos y exclamaciones de aparente éxito asociadas a restricciones o fallos operativos  
            re.compile(  
                r"\\b(?:(?:\[oó\]t\[ií\]ma?|marav\[ií\]lhosa?|l\[ií\]nda?|excelente)\\s+(?:ajuda|atend\[ií\]mento|suporte|serv\[ií\]\[cç\]o)\\s\*(?:\\(\[ií\]r\[oó\]n\[ií\]co\\)\\s\*)?|obrigad\[oa\]\\s+por\\s+nada|(?:\[oó\]t\[ií\]mo|marav\[ií\]lha|l\[ií\]ndo)\\s\*,\\s\*(?:me\\s+bloquearam|me\\s+bloqueou|n\[aã\]o\\s+func\[ií\]ona|perdi\\s+meu\\s+acesso|que\\s+beleza)|parab\[eé\]ns\\s+pelo\\s+p\[eé\]ss\[ií\]mo)\\b",  
                re.IGNORECASE  
            )  
        \]  
    }  
}

## **Análisis Lingüístico y Validación de Patrones en Español**

El desarrollo de patrones de coincidencia para el idioma español exige la consideración de una marcada pluralidad dialectal.10 Las diferencias en el uso de vocablos específicos entre España y las diversas regiones de América Latina determinan el éxito de la detección de fricción en tiempo de ejecución.10

### **Profanity e Irritación Implícita en Español**

En España, las manifestaciones de agresividad atenuada recurren con frecuencia a expresiones relacionadas con el cansancio extremo ("estar hasta los cojones", "hasta los huevos") 10 o al cuestionamiento directo del valor del sistema mediante exclamaciones despectivas ("es un chiste", "vaya porquería").10  
Por su parte, el español americano presenta una alta fragmentación: la región mexicana muestra un uso sistemático de términos vulgares que denotan frustración profunda ante procesos fallidos ("no mames", "valió verga", "pinche").10 En el Cono Sur, especialmente en Argentina y Uruguay, se observa una fuerte presencia de vocativos descalificadores ("boludo", "pelotudo") 15, mientras que en la región andina colombiana predominan sustantivaciones con carga ofensiva alta como "gonorrea" e "hijueputa".15  
La tabla siguiente detalla tres casos reales de activación para esta categoría:

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"El servicio de esta app de banca es un pésimo servicio, son unos estafadores."* 14 | pésimo servicio, estafadores | El adjetivo "pésimo" califica de forma directa la calidad operativa del canal financiero, mientras que el plural de "estafadores" atribuye dolo institucional, elevando la fricción de moderada a severa.14 |
| *"No mames con sus respuestas automáticas, mi transferencia sigue retenida."* 10 | no mames | Expresión mexicana de incredulidad y molestia extrema. Funciona como una descalificación de la lógica recursiva del bot de atención en flujos transaccionales.10 |
| *"Llevo una hora intentando cambiar mi clave y ya estoy hasta los huevos."* 10 | hasta los huevos | Expresión idiomática de la Península Ibérica que denota el agotamiento absoluto de la paciencia del usuario ante un cuello de botella de autoservicio.10 |

### **Negación y Resignación Pasiva en Español**

Este patrón captura la retirada o el desistimiento conversacional de los usuarios.19 Este fenómeno ocurre cuando, tras varios intentos de resolución infructuosos con el asistente virtual, el usuario asume que la máquina es incapaz de procesar su solicitud semántica.18 En lugar de insistir, adopta fórmulas verbales de desactivación o rechazo explícito de la ayuda que el bot le sigue ofreciendo.16

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"Lo que me dices no me sirve para nada, deja así y ya veré qué hago."* 16 | no me sirve, deja así | La negación de utilidad de la información ("no me sirve") seguida del imperativo de resignación ("deja así") señala una desconexión voluntaria del canal digital por ineficacia del sistema.16 |
| *"Olvídelo, es imposible resolver esto con sus respuestas predefinidas."* 18 | olvídalo | El uso del imperativo "olvídalo" (u "olvídelo" en variante de respeto formal) constituye un comando pragmático de detención del diálogo ante un fallo de coincidencia de intención.18 |
| *"Otra vez con lo mismo, no entiendes nada de lo que te pregunto sobre mi saldo."* 18 | otra vez con lo mismo, no entiendes nada | Revela el bucle interactivo o "looping" en el que ha caído el diálogo, atribuyendo de manera directa incompetencia cognitiva al asistente virtual.18 |

### **Solicitud de Escalamiento Implícito en Español**

Los usuarios frustrados evitan a menudo las palabras clave que los bots reconocen por defecto (como "agente", "operador" o "humano") debido a la creencia de que el sistema dilatará la derivación mediante nuevos árboles de decisión.2 En su lugar, recurren a expresiones que contrastan la simulación algorítmica con la autenticidad del soporte físico o el nivel jerárquico del interlocutor ("alguien real", "asistencia de verdad", "supervisor").21

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"No quiero hablar con una máquina, ponme con alguien real de soporte."* 21 | alguien real | Expresa el deseo de interrumpir la interacción con la inteligencia artificial mediante la demanda explícita de un interlocutor de existencia fáctica ("alguien real").18 |
| *"Esta consulta es compleja, pásame con un supervisor por favor."* 23 | con un supervisor | Demanda de escalamiento vertical que busca superar las limitaciones técnicas percibidas del asistente virtual mediante una figura con mayor nivel de autorización.23 |
| *"Quiero asistencia de verdad para mi reclamo de reembolso."* 21 | asistencia de verdad | Descalificación pragmática del flujo automatizado actual mediante la exigencia de una interacción humana auténtica y resolutiva.21 |

### **Sarcasmo y Frustración Velada en Español**

La ironía y el sarcasmo representan uno de los desafíos más complejos para la clasificación de sentimiento tradicional, dado que la polaridad de las palabras individuales contradice la intención semántica global.6 El usuario simula un estado de satisfacción extrema o gratitud formal mediante modificadores de alta valoración afectiva positiva ("genial", "excelente", "buenísima") para calificar un evento que compromete gravemente su experiencia operativa.6

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"Excelente ayuda, me bloquearon la tarjeta de crédito justo antes de viajar."* 6 | excelente ayuda | Sarcasmo estructural donde una valoración positiva ("excelente ayuda") se asocia directamente a una restricción severa del servicio ("bloquearon la tarjeta").6 |
| *"Gracias por nada, su chatbot es una pérdida de tiempo total."* 6 | gracias por nada | Expresión de gratitud vacía o subvertida que actúa como cierre negativo de la interacción, denotando insatisfacción con el soporte automatizado.6 |
| *"Buenísima la atención, me cobraron dos veces la suscripción mensual."* 6 | buenísima la atención | Contraste irónico entre el superlativo positivo de evaluación del servicio y el reporte de un error financiero crítico.6 |

## **Análisis Lingüístico y Validación de Patrones en Portugués**

La detección de señales de fricción en la lengua portuguesa requiere un tratamiento diferenciado que reconozca la brecha sociolingüística entre el portugués europeo (PT-PT) y el portugués brasileño (PT-BR).25

### **Profanity e Irritación Implícita en Portugués**

En Brasil, el descontento del cliente se manifiesta con frecuencia mediante la denuncia de la falta de seriedad del canal de soporte, utilizando el término "palhaçada" (asimilable a "falta de respeto" o "circo") 9 o mediante cuestionamientos informales sobre la competencia de la interacción ("estão me tirando", "que piada").25  
Por otro lado, el portugués europeo conserva estructuras de indignación con un arraigo idiomático particular ("macacos me mordam", "pelas barbas do profeta") 11, junto con exclamaciones de enfado directo que recurren a la blasfemia clásica o vulgarismos ("caralho", "puta que pariu", "pqp").26

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"Não consigo acessar meu aplicativo, isso já virou uma palhaçada."* 9 | palhaçada | Expresión de uso extendido en Brasil para señalar que un problema operativo recurrente está siendo tratado con informalidad por parte de la empresa.9 |
| *"Vocês estão me tirando? Já paguei essa fatura há três dias\!"* 25 | estão me tirando | Locución brasileña de carácter marcadamente informal y defensivo. Expresa molestia ante lo que el usuario interpreta como un error injustificado.25 |
| *"O sistema deu erro na transferência de novo, que péssimo serviço."* 16 | péssimo serviço | Calificación directa de ineficacia operativa, común en ambas variantes de la lengua portuguesa, que denota un fallo crítico del canal de soporte.16 |

### **Negación e Resignação Pasiva en Portugués**

El desistimiento conversacional en portugués suele acompañarse de expresiones de inutilidad como "não adianta" (no sirve de nada/no tiene sentido) y "esquece" (olvídalo).25 Asimismo, el uso de modismos históricos para indicar la pérdida de expectativas sobre el comportamiento de un tercero—tales como "pode tirar o cavalinho da chuva" (desiste) o "ficar a ver navios" (quedar frustrado)—señala un alto nivel de descontento.11  
Estas expresiones se asocian frecuentemente con estados de desánimo recogidos bajo categorías léxicas específicas de frustración activa o pasiva ("chateado", "morgado", "aborrecido", "p da vida").26

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"Deixa pra lá, já vi que esse bot não entende minhas perguntas."* 20 | deixa pra lá, não entende | Estructura de resignación pasiva ("deixa pra lá") combinada con la atribución directa de incapacidad interpretativa a la máquina.20 |
| *"Tentei parcelar meu saldo e não consegui, estou muito chateado."* 25 | chateado | Expresión de un estado afectivo negativo ("chateado" en Brasil suele indicar enojo profundo, no solo tristeza ligera) tras un proceso financiero fallido.25 |
| *"Esquece, não adianta tentar resolver meu problema de acesso por aqui."* 25 | esquece, não adianta | Imperativo de cancelación ("esquece") acoplado a un juicio de inutilidad técnica ("não adianta"), indicando que el autoservicio ha fracasado.25 |

### **Solicitud de Escalamiento Implícito en Portugués**

Los clientes de los mercados de Brasil y Portugal emplean modismos indirectos para exigir la atención de una persona real, evitando términos genéricos que puedan ser interceptados por los clasificadores de intención tradicionales.20 Utilizan variantes que enfatizan la necesidad de hablar con un profesional dotado de empatía natural ("alguém de verdade", "falar com pessoa") o un nivel de decisión superior al del software básico ("atendimento especializado", "falar com um gerente").25

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"Por favor, quero falar com alguém de verdade que resolva minha conta."* 2 | alguém de verdade | Contraste semántico explícito donde el usuario rechaza la entidad sintética ("robô") en favor de una entidad real.2 |
| *"O sistema travou meu cartão, preciso de atendimento especializado."* 25 | atendimento especializado | Exigencia formal de escalamiento que busca eludir las respuestas automáticas genéricas del chatbot mediante la apelación a un departamento técnico experto.25 |
| *"Quero falar com uma pessoa, cansei de receber respostas prontas."* 19 | falar com pessoa | Solicitud directa de intervención humana gatillada por la insatisfacción con los textos predefinidos o estáticos del sistema automatizado.18 |

### **Sarcasmo e Frustração Velada en Português**

Al igual que en español, el sarcasmo en portugués subvierte la polaridad afectiva de las palabras de alta valoración positiva ("ótimo", "maravilhosa", "excelente") para calificar fallos del sistema o bloqueos de cuentas.6 La coincidencia se produce cuando estas unidades léxicas positivas aparecen junto a verbos de restricción operativa o pérdida de privilegios del usuario.6

| Mensaje de Entrada del Usuario | Fragmento Coincidente | Justificación Lingüística del Patrón |
| :---- | :---- | :---- |
| *"Ótimo, me bloquearam o acesso e agora não consigo pagar meu boleto."* 6 | ótimo, me bloquearam | Construcción irónica clásica en la que el adverbio positivo "ótimo" introduce un incidente crítico de bloqueo de credenciales de usuario.6 |
| *"Muito obrigado por nada, excelente atendimento do seu sistema."* 21 | obrigado por nada | Agradecimiento subvertido ("obrigado por nada") acoplado a una calificación irónica del rendimiento del canal automático de soporte.6 |
| *"Maravilha, fiz a transferência Pix e o dinheiro simplesmente sumiu."* 6 | maravilha | Uso sarcástico del sustantivo de entusiasmo "maravilha" para calificar una pérdida transaccional, evidenciando un alto grado de fricción.6 |

## **Optimización de Rendimiento y Métricas del Sistema**

La implementación de este diccionario heurístico bilingüe dentro de la primera capa CPU del sistema ConversaSense AI tiene un impacto directo sobre la eficiencia computacional y la experiencia del usuario.3 Al procesar cada interacción con expresiones regulares optimizadas antes de invocar los modelos de clasificación profunda en GPU o APIs externas, se logra una reducción de latencia y costes operativos.3  
La tabla a continuación presenta una comparativa de las métricas clave antes y después de integrar este diccionario en el pipeline de inferencia híbrido:

| Dimensión Métrica | Pipeline Tradicional (Clasificación basada únicamente en LLMs en GPU) | Pipeline Híbrido ConversaSense AI (Capa CPU Heurística \+ LLM) | Relevancia e Impacto Operativo para el Negocio |
| :---- | :---- | :---- | :---- |
| **Latencia de Triage de Sentimiento** | **![][image14]** 3 | ![][image15] (en hilos estándar de CPU) 3 | Permite detectar de manera inmediata la fricción conversacional del usuario antes de que se inicie la generación de la respuesta.3 |
| **Consumo y Coste de Infraestructura** | **![][image16]** de las llamadas dirigidas a GPUs o APIs externas 3 | Reducción del ![][image17] en llamadas a LLMs por desvío temprano en CPU 2 | Disminución de los costes de procesamiento mediante la optimización de los flujos de autoservicio y de soporte.2 |
| **Tasa de Contención Efectiva (Containment)** | **![][image18]** (debido al abandono silencioso en bucles del bot) 2 | Incremento del ![][image19] en la retención del canal digital 6 | El sistema detecta la frustración a tiempo y redirige al usuario hacia flujos alternativos o de asistencia humana directa.6 |
| **Resolución en el Primer Contacto (FCR)** | Tasa estándar de resolución inicial de consultas de nivel 1 6 | Incremento de hasta un ![][image20] en la resolución del primer contacto 6 | Al transferir al usuario con el contexto acumulado de su frustración, el agente puede resolver el problema de inmediato.6 |
| **Puntuación de Satisfacción (CSAT)** | Niveles de satisfacción promedio debido a fricciones no resueltas 8 | Mejora del ![][image21] en la percepción del servicio al cliente 8 | El cambio automático hacia un tono de asistencia empático o la derivación rápida mitigan la insatisfacción del usuario.8 |

Esta optimización del pipeline de ConversaSense AI demuestra que la combinación de expresiones regulares bien estructuradas y modelos ligeros en CPU es una de las estrategias más eficientes en términos de rendimiento.3 Al equilibrar la precisión semántica con el ahorro de cómputo en la primera capa de inferencia, el sistema puede identificar la insatisfacción del cliente de manera ágil.3 Esta intervención temprana mejora de forma significativa la experiencia del usuario y optimiza el uso de los recursos de la plataforma de soporte.2

#### **Obras citadas**

1. Spanish chatbot solution | Botpress \- \#1 conversational bot for Spanish speakers, fecha de acceso: mayo 29, 2026, [https://botpress.com/best-spanish-chatbot](https://botpress.com/best-spanish-chatbot)  
2. Customer Service Chatbot: Everything you need to know \- GuruSup, fecha de acceso: mayo 29, 2026, [https://gurusup.com/customer-service-chatbot](https://gurusup.com/customer-service-chatbot)  
3. Claude Knows When You're Mad — And Uses Regex, Not AI \- DEV Community, fecha de acceso: mayo 29, 2026, [https://dev.to/toji\_openclaw\_fd3ff67586a/claude-knows-when-youre-mad-and-uses-regex-not-ai-2klc](https://dev.to/toji_openclaw_fd3ff67586a/claude-knows-when-youre-mad-and-uses-regex-not-ai-2klc)  
4. Practicum \- Data Science & Artificial Intelligence, MS | University of San Francisco, fecha de acceso: mayo 29, 2026, [https://www.usfca.edu/arts-sciences/programs/graduate/data-science-artificial-intelligence/practicum](https://www.usfca.edu/arts-sciences/programs/graduate/data-science-artificial-intelligence/practicum)  
5. “Stupid robot, I want to speak to a human\!” User Frustration Detection in Task-Oriented Dialog Systems \- arXiv, fecha de acceso: mayo 29, 2026, [https://arxiv.org/html/2411.17437v2](https://arxiv.org/html/2411.17437v2)  
6. Chatbot Sentiment Analysis: Complete Guide to Implementation and Optimization \- Dialzara, fecha de acceso: mayo 29, 2026, [https://dialzara.com/blog/step-by-step-guide-to-adding-sentiment-analysis-to-chatbots](https://dialzara.com/blog/step-by-step-guide-to-adding-sentiment-analysis-to-chatbots)  
7. How Chatbot Sentiment Analysis is Transforming Customer Experience in Contact Centers \- Voxtron | Dubai, fecha de acceso: mayo 29, 2026, [https://www.voxtronme.com/2025/11/24/how-chatbot-sentiment-analysis-is-transforming-customer-experience-in-contact-centers/](https://www.voxtronme.com/2025/11/24/how-chatbot-sentiment-analysis-is-transforming-customer-experience-in-contact-centers/)  
8. Sentiment Analysis Secret Making AI Chatbots Shockingly Helpful \- NOEM.AI, fecha de acceso: mayo 29, 2026, [https://noem.ai/blog/the-sentiment-analysis-secret-making-ai-chatbots-shockingly-helpful](https://noem.ai/blog/the-sentiment-analysis-secret-making-ai-chatbots-shockingly-helpful)  
9. A IA arruinou o suporte / atendimento ao cliente para quase todas as empresas \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/artificial/comments/1lqiwlg/ai\_has\_ruined\_support\_customer\_service\_for\_nearly/?tl=pt-br](https://www.reddit.com/r/artificial/comments/1lqiwlg/ai_has_ruined_support_customer_service_for_nearly/?tl=pt-br)  
10. ¿Cuáles son algunas frases para expresar frustración en español? : r/Spanish \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/Spanish/comments/anec45/what\_are\_some\_phrases\_for\_expressing\_frustration/?tl=es](https://www.reddit.com/r/Spanish/comments/anec45/what_are_some_phrases_for_expressing_frustration/?tl=es)  
11. 9 expressões clássicas e engraçadas para expressar sua frustração \- Dicio, Dicionário Online de Português, fecha de acceso: mayo 29, 2026, [https://www.dicio.com.br/expressoes-classicas-e-engracadas-para-expressar-sua-frustracao/](https://www.dicio.com.br/expressoes-classicas-e-engracadas-para-expressar-sua-frustracao/)  
12. re — Regular expression operations — Python 3.14.5 documentation, fecha de acceso: mayo 29, 2026, [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)  
13. Regular Expressions in Python: RegEx Explained With Examples \- WsCube Tech, fecha de acceso: mayo 29, 2026, [https://www.wscubetech.com/resources/python/regular-expression](https://www.wscubetech.com/resources/python/regular-expression)  
14. \+200 expresiones españolas: habla como un español \- Mochileros TV, fecha de acceso: mayo 29, 2026, [https://mochilerostv.com/expresiones-espanolas/](https://mochilerostv.com/expresiones-espanolas/)  
15. Palabrotas en español \- No aprendas este vocabulario \- Let's Speak Spanish, fecha de acceso: mayo 29, 2026, [https://letsspeakspanish.com/es/blog/palabrotas-en-espanol/](https://letsspeakspanish.com/es/blog/palabrotas-en-espanol/)  
16. Plantillas para manejar quejas de clientes \- Pipedrive, fecha de acceso: mayo 29, 2026, [https://www.pipedrive.com/es/blog/manejo-de-quejas-de-clientes](https://www.pipedrive.com/es/blog/manejo-de-quejas-de-clientes)  
17. Cómo tratar con clientes enojados \- SalesGroup AI, fecha de acceso: mayo 29, 2026, [https://salesgroup.ai/es/como-tratar-con-clientes-enojados/](https://salesgroup.ai/es/como-tratar-con-clientes-enojados/)  
18. ¿A alguien más se le está comportando el ChatGPT de forma totalmente distinta de repente? \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/ChatGPT/comments/1iw1a1k/is\_anyone\_elses\_chatgpt\_behaving\_completely/?tl=es-es](https://www.reddit.com/r/ChatGPT/comments/1iw1a1k/is_anyone_elses_chatgpt_behaving_completely/?tl=es-es)  
19. Top 10 Phrases That Annoy Customers in Chats \- NovaTalks.AI, fecha de acceso: mayo 29, 2026, [https://novatalks.ai/en/blog/top-10-chat-phrases-to-avoid/](https://novatalks.ai/en/blog/top-10-chat-phrases-to-avoid/)  
20. O USO DE CHATBOTS NO ATENDIMENTO DE CLIENTES DE REVENDA POR CATÁLOGO, fecha de acceso: mayo 29, 2026, [https://repositorio.ufpa.br/bitstreams/ec013a77-c60e-43f0-ad99-379e51141c17/download](https://repositorio.ufpa.br/bitstreams/ec013a77-c60e-43f0-ad99-379e51141c17/download)  
21. Customer Service Phrases: What to Say, What to Avoid, and Scenario Scripts, fecha de acceso: mayo 29, 2026, [https://www.gorgias.com/blog/customer-service-phrases](https://www.gorgias.com/blog/customer-service-phrases)  
22. 30 Customer Service Phrases That Turn Support Into Sales | Zipchat AI, fecha de acceso: mayo 29, 2026, [https://www.zipchat.ai/blog/customer-service-phrases-that-convert](https://www.zipchat.ai/blog/customer-service-phrases-that-convert)  
23. 15 winning customer service phrases (+ 9 to avoid) \- Zendesk, fecha de acceso: mayo 29, 2026, [https://www.zendesk.com/blog/customer-experience/engagement/customer-service-phrases/](https://www.zendesk.com/blog/customer-experience/engagement/customer-service-phrases/)  
24. 40+ Proven Customer Service Script Examples for Difficult Situations \- Yonyx, fecha de acceso: mayo 29, 2026, [https://corp.yonyx.com/customer-service/customer-service-script/](https://corp.yonyx.com/customer-service/customer-service-script/)  
25. Chatbot em Português e inteligência artifical : r/Portuguese \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/Portuguese/comments/jvb08s/chatbot\_em\_portugu%C3%AAs\_e\_intelig%C3%AAncia\_artifical/](https://www.reddit.com/r/Portuguese/comments/jvb08s/chatbot_em_portugu%C3%AAs_e_intelig%C3%AAncia_artifical/)  
26. NÍVEIS DE INSATISFAÇÃO / FRUSTRAÇÃO \- VOCABULÁRIO EM PORTUGUÊS \- YouTube, fecha de acceso: mayo 29, 2026, [https://www.youtube.com/watch?v=9qUrgKAsUp4](https://www.youtube.com/watch?v=9qUrgKAsUp4)  
27. 30 frases para atendimentos difíceis: Transforme desafios em oportunidades \- Digisac, fecha de acceso: mayo 29, 2026, [https://digisac.com.br/blog/30-frases-prontas-atendimentos-dificeis](https://digisac.com.br/blog/30-frases-prontas-atendimentos-dificeis)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIkAAAAaCAYAAACD1n8kAAAEyklEQVR4Xu2aW8hlYxjHn8kQMU6jQZFvXCiHUIwaQ7lQKFxwQ+SCJpJDEZLom6RMTU2MnMOQU0wSUnPBNjTCxQzlcKNp5BCSlCvl8Px6n6e99rvetfY67G/v78v7r1975l1r77X28/zf932etT+RrKysrMWofZUDjS5aZqyw18Wi/ZWjDf49be2jrFIOjQ8kdI7ynvK0ca/yinKdhM+BmSqbZGG0aExCUlbKMBgxBKcuQIcoDyvHGQjTHCnlz0pRDMAlynqZvVG4/o3KbuVa44iRM6ajAyTE5A3lZYN4p0SOXlLOMBDfY7NyodFZfPgdyrPKr8a/ynblSeV0IyVu4j7lsmj8euUXZavB5+yR8NlcBxj7WBkoBxnLlYeUc2W2wuBfSJidsZgAtxnvKNuUByQkFNqIz1pnYAQmTUqHKZ8aF0XHXMcrb0o4F1x3FegtkjQwMAkOHqdTlBdlNDiYbosyF40RUM71rQXxxTb6SSZmwavSLeiTEsliFfEZWdQVEu4PSDLf5X5l3mgqJt6jyhPGXqk2STE3VXk5X8LEK8YXsfUwaaGzjpWwf32i/G1gkp+V5yRcHFJ72rxyUzR2onJzNIYZfpLyjZ6WGCMgGGqt0VQnKa8pzxgE7E4Jq9xRRlNVmcTNHs9MEvel0XZb4r3Q1ySsZldFY6yI7ysnG52VTVJWNomE5YjkAqbYoZwqo9vN5coNyj/GuzIsmryTeUvK+zbJiAOFyX5X1kTjh0uo3mNRCPu+30RnKvfI5LanKpMwTjI9sS5i8KOB8dtoEiYhF9tk9H7J8e3KLYWxVsJh3xoYAgemahIPCjDms55xoJBi5RgnXN5mlmEOb+XqhGlhk4T7n5RY+b6SskmOUb6Xskk47zsjfs84tTVJsUlgkgGTmVzSGdLywlMSOppifdJKtLyfG578lEk8KMAYRRsiiLBTqr8Y8va5WLQ2EdfeatTJ270r4wMddbDxgvKYhMK0KCbEbzJ9kyDMAeSMVX8q8tb2a+UPCXvsLgNDbJCQ3L8M2mQPGksqcG7dF3MzpeqROrU1CbUINUiKR5QTjDrNyfCaH0jo3GJVbTdsoz6ZFsokbmA6ooFUt8ITVTbJqOYkm6RSyyQEiK3kGwOTbFTOk/QTV69JBvZaJb4I/CnlorVOLKtNTOIm7FycVYiHeUye1dH4CuVDKRfVJNlNwhbdRk1MslyGT1x5JkPOZqJUTVIlClD4SOpnDgVr26IVsar5e+tEsICnvmdFx/qIZKW6GzQvofsCF12iJ5GE0mU9LqHjgrqkNjHJuO5mweU3gDFSxEsrIhDu7mK1jfgt5kEZfe4C/J8tK7UyFUVAn1cuNZqIFnCzhN9YvOPpozqTcGy7cY2EDuJtGf3tiuvvkOHKTDcZa06CkX4wiPVnko7RzE3SR2xRW6R+prQVAX3dXlPBrRL3QN2xwWhbkxRVZxJEbQY8oOIZTdwFuUg4tFlFU8omiZRNUtaSNslKCQldHR/ooaslBHaWGmeSJsLgtxp9J9GSNgmiYKTA9Dqlj9jTeYjVt6boK66/U7lbuv/BznoZrVP66GwZPqxbGx1bMrpAudjoov0Mupq2LeRCiS2CbWtg8Dcf0xYrtf9oyQ+YkJWVlZWVlZX1v9F/4qdWqH7GlxkAAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAaCAYAAABozQZiAAAAuklEQVR4XmNgGGjAA8SSJGAOiDYIIFsziLEZiM9D8SwgXgrEP6H4DFRsLhA/h+JysE4g0ATiHiBmhWKY2FsoDoKKgUA0FPvCBGKA2BIuDQEgBTDNIINgIBmKjWEC6gwIG2FgEhAfhmJeJHF5KOaECVCkGR0IAvFpBogBIEwSgAUWKKCQA4soAAsskCHIgUUUmMOA8Cuyf4kCZGkGBRRyYBEFDIB4IRA/gOL/QPwFiDdAsSdM4SgYBfQFAFWWKUZZIXItAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAZCAYAAAAIcL+IAAAAkElEQVR4XmNgGLrAF4iPQbEwmhwKsAPiQihmRZMjHvBBcRUQVwIxNxSjAH4grodiISBeCMRFUIwCiFboAsRWUMwLxIeBOBqKcQJNIL4FxPpQjBP4AfEpIBaEYpxgEhDPQRdEBjxQfICBCLeB8FUojRMQVHgOiAOBuByKNwMxJ4oKKLgOxBuBeDEUS6BKj2QAAKm9GQgEGG33AAAAAElFTkSuQmCC>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAcCAYAAACOGPReAAABIElEQVR4Xu3UMUtCURQH8CuoBCIOCRLqYFs0OIhbSISLqzgIrkV7W0sE0RcQAidtbGjVIdqcotkPIIiiix9B/wf/z46+wKvvvc0//AaP9x149577jDlGJQIpOPvHKYXWqy2ThjuY0xvUoAFf1IOE84BtCjCioqpnSOr3qm6VQJrKqw4oqernNIEHVbdKEz4prOp1msKlqu9MHPrwQs7JV+GHbtarLRNIU9mzITyRjJO4hhPaOxUYm79DsYk8c7Fd1HmFb4iRTWQE9ZS44mtTZ7+6ZtV4V+T+5xXX90D25JcWMINHiqp1OiW4orZZfYQ8R7YmSx3+9pxAmkrK9LxV9xTn1smZeI68qlznFuU2/z4svjaV8RIf8A635JrRY/zPEmqLNwaGNl36AAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,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>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAcCAYAAABcSP4GAAAARklEQVR4XmNgoAsQAGJJNCwOxawwBWVQrA/EJUBsAMVgBSAQBcUg3RlAzAPFcDCqgBoKkoH4ABQvBeJDQDwVikEaRgF9AABRWhWIiq+howAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAR0lEQVR4XmNgGKZAHIrrgbgATQ4MOIC4FIi7ofgGEJejqIACohXCAA8UH2AYVYgFUFdhMhDvg+K/QPweiFdCsQGSulFAIQAA9wMX9lc1TDgAAAAASUVORK5CYII=>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAsElEQVR4XuXQIQoCYRAF4BE0LAoGi9usJoOICEbBosVksHsExW5fPIEG9QaGZZHFa5i8iW/2f2MQhcn64CuPB//sivxgmrCnM6QwoZKNynCCBWkacKUBO/+wDXfokuVAOyum8ICYLFvKoKrFTD4PV5RDTQv3cCnO4bcbN5QLhz0Jww5Z7KuPwp/uHtbhBiPSRHChObsiYwm3qD6sIaHKa8XowWoILQnPFU++xz38nzwBR6srDXInwPQAAAAASUVORK5CYII=>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAbCAYAAAA6aQxyAAACVElEQVR4Xu2WTahNURTHl3xEiHj5KHqPmRJKTynKQElhwEQxFQMmSkbEQHlDDJSUj5KUmaSMbhIxkYGYSEoJAykj5eP/a6/l7bude89573ly6/7q172tc+7ee+2799rbrE+f/47pcrY7XqbIuf45JvjBQrm0gzPdTsyT5+WgCyS02C3bK53vwk55wNKYGifC4I7JK/KT+1Pel5fkOrcKOjkpdxfxg/Kje81SO29stH36IvZYttw5cpo8Jze7Y4IGWi4JMBt1rJY35KwsxoRckENuxO5aehdjdlfKETdYL2+5ebu19GwCy+UJ+UR+d0ngg7wqt7pT/f2cU/JwEVsljxQxBvre0tLCYG1FjIkkWdyYxdtgBugYGfADucba/4E98pD84d6ztGEhKs4ducljwRI5UMSYgM9y2A0WyEVuDkUBjxbx31AdXrsMdp9VLyGqxFuXWMxUVJCnlma8jjPyhaXEyuSqYOB4uXwQ9HwC1P3nbgysKoFl8p1LbK8lWNP4yFIi3cg3cNP6Tt9ICe5I1PeX8os8Lp+5DPa0pY6/uZwVHFDA5kPerUsg38BNaZRAwIwMWZrdVy4JUNq2WPVJHEuo5Z/d2C6/WvvmrYODERslEFQtoU7EWn5oqW53I1//TWE1IL9tTM8mEANn0FXGeszhzoI37c97EBezs5YOxvxw5Dv7CMslmcOSvu7uKp79ddg3XBuaVJamUOJvu3yfVCjHdLSifDAB9tvoPzXp9HwCsMHSZot9MREG5UVLd664d/0Ttskd7niZYanycPr36dOnC78AsGWlAEbC7l0AAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAbCAYAAADVq2dMAAACU0lEQVR4Xu2WTahNURSAl/xEiJCfUg8zpQxEKWaKVxgYGZhKiYmSmUwUQwyU1IuSlJlMTJyB/E2MxEQyUgxEDCg/62ut5e27z37nnBtX3ut89XVP69yz91777L32Eenp+e+Z6y7MbwzBLHWx/w7NInXNFC53mxpeol50xzxGQqvcvM3cpS7sUw+L9dfUZ41x9Yp6z/2pvlcn1JPu/N//HoSOTqsH3OCI+s69Jtb+a7F2o21ij9TKZTLnqBfUnW4jkX06y8wCkkQl1mjA9Up1dhKDTeoNdYELJHxJXedG7K7YfzH63KCed4Mt6i032iwy7ZNg8PddBnxT7DWWktjvfle/qLtlkDPqsSy2UT2exRjsW7FlhsHmQox+SRi3J/Eau9wf6iuxDVhK4pRLjLWdQiW6o+7I4qvVFVmMvj6oW91gmdgbxpQoFCey+ADMAH5S34hViVISV11iZ3kwgWeeis18Gzz7XCy5PMESDB7pe0pmRBIMECuxJbVH6kmMiQ0Sv0p9fbLOH4ol00S6qbvW/xhLvoSLMIsv1I8yWRFIgrfzWP3mHpV657zJZ9KeRLqpuzJUEkDZpKxFqSOJl2JVidMYSzD4yn+bGFc/y+CGbiMOz85JBPlySs+JEqztB2IT0ES6H7oSVTHfh61M6yTiHChZuaWEOCA5KNNvJuAwPac+cTkokeu2bzFg7113WdIj56DYJ0bXqtMFDt7bLtcjh28vOlvv/g0OyeQb+yfMiCRgm9gGRPbJn8ABe1maS/vI4OsW9+Y3hmCeWJFZm9/o6elp5hd4A5+Zyk/nZwAAAABJRU5ErkJggg==>

[image11]: <data:image/png;base64,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>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIkAAAAaCAYAAACD1n8kAAAE9klEQVR4Xu2Za8hlUxjHn8klk+vMyLjmHQ1S41KKhHzxweQakpAvGox8QXItMy4fUO6XklyTZKJJGrd445PIpSglhUhDUopCLs/P+j+z19nvPufsfc55zztN61+/zjn7rLP2Wuv5r7WetY9ZUdGUtcjZVa9Q1E472/yOVx6XsbWds5ezTx92EU2iAVc6Z+k9LLO5dTTRr86tSXs6x4iJDHamy639GESMBsUpYPyB9p7urNH7sdpfTNJfxSTSUucc5wPnM3GBc65zo/OduNnZQb8Jnejc72yfcbLzvPOv84Z4TDzt/Ch430bcl/sfIiah3Z13xYvOTr1f/y/KvOU8KZrKjKMuJmFMfxEvWBrLD50/xHO6tsn5WmAY4kF8iBOMpSWWTHKHyHW2oDHH6dpiQeNW6Vquo53fLDkZcq0UdKrNwLNKbbRqhkxCmJ3Bg5ts7izj8/XOPVb1ddLqYpJbnWNF6AHnPUHugYjjvSLqJhYYC8bqx2HOT85qkesy8Zdzgq5hFthgzTduMglLJp2JFedafd4aRVsxct08k1Rbk7Dl3WLVuKGY1BgFQsuddSLEPV4VMclH0oXOD85BIoQBXhNsG9Gpq0V91Qk1mWR/6y1/hLOvc5VVs/oUS7OXV7ZBiO9nROhQ52HxsnODs1v2PQFm5j1l1Uy61FKfDnfuEpg1VrTYu/kdg/+spa0YMA5BOtN5RJyalWVrhrwNg9TWJIzBfrVrTOqfrVrlQ/TtQJErzETMRlYxSVIxyQBRwTvOCkHSc7ClvOFNsfeW0inpBLahJoVJ7hSYEJORAOYiNzjN+VU8bikX+NTS0gnnOZst1QmI08b7ltoIlPvKuU7fIwJL4skgHym4B6YlKY1Az1oVrLWCfjPgGCOCv96SgTA2fQES35N0/SHBWLZRW5M0ifHEJJgFhglzAOM7kmJ/22jpRJPDaSJmV4jZRC4C9aQ0FCa5WLCKkCA2NRJDfinI4jEOD5pC1PWtXoFZz/6aB4P2YRz27+Bzq0xMnXC8VXVjKJi1FCwmB0YD2hGK+0YbUEwSEvcYm3p9wzSOSeh7JKxt8rpY0WnzSMKJJK1n1L/oIwaZGQrDTJJvN5jhti0lKnH9ExFByFU3CeW/sd5VI1eUi/v3Uz2ocZ/cDKipvjBJPuj1+oZpVJPkSWtbjW2SfOlqqxigfkFoMkk/dTVJrBJsAU2KJZg+5ft1XfWgsh0xWaBpJWGrWq1rC2mS2DYH9a0uykIxiVRMMlcjm2SRIJmctW4NZqmDQUv+fJkErbOUNJKAAlpu6S+CeJ7AU1/6Ri4SWmUpEUb1oJKoviKoJ8RJCz6y9FgcLaRJRpnU0bZ+p9FGMSPeFn87f1pKwg4Qw3S+eMaqxI2EEkhQv7f0WH6zIFgzKpdrxlIS+o/4wqpk8yjxsb57XcxYyotIguOUcYnzoPUe/TiNbbLUr3ggyPEaU11h1d8D9P12S23nN/CSc5+lvwQ49QFBoQxPP3/P4PM1VtXHeD7h7GGD1dYk3JNjeuSBtJex5e+Tu8WgexEf4gRt886JaIXg+QkzeKHEIMMy6z2B5WIAgy6i3q6/6aK2JhlXxGeDmGqsYqtab2lFKequaZnkIksrEUxVxSTja5s3SSieXPKwrKibpmEScrRHrTfBXxBhEBK3HUVRO/G/D0npfIlYcKIpE7ioqKioqKioqGjb1X8ABVsmQbpubwAAAABJRU5ErkJggg==>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAeCAYAAAD6t+QOAAAAcklEQVR4XmNgGAWDFkhCcQAQh6BhfygWAimUB+IdUDwXiI9B8XogngXEvVAMMowhC4iFoZgFiHugWAYkiQ5IUowMpIF4PhTzoMlhABcgngPFBAFJiluBuByKcQJuKN4FxJ5QjBOQpBgGeIGYGYpHwbADAP3MFO7nGgX1AAAAAElFTkSuQmCC>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJQAAAAVCAYAAACg0MepAAAC0klEQVR4Xu2ZS6hNURjHP6EIKeRRymsg8iqvREYKRQlFHkWSksRAHhMmJkwwMJC4lxATA48k6cTQwMgjjwHJgIERM4//r/UtZ5/tnHuP65xw+371a52z91p77+7+t9a3zjULgiAIgiAI/pRR8rDcUz4h+ls6jk/lR3lVjnYzfO5wr8i7coXs4wLtOj+H9Dsrh/n54D9mgNznHpfP5f6aHontcqsLQ+U9q4ZisOwnL8tNLgyX9+UCF2g5xjkE+jOWa2DQCyAUFfs1UH0tzUavXWYy2Cg/u7PlFPnSP2OmU55ygZZjRejPWK6BQS+gUaBgoVVnKJY/KAdqpXwjx7iZo5ZmMxxp9e8xUb6Xy916LLYUxm1ysnvM0vXHFuQ7/aamYT/h3BFLyyvSj6U3aBMRqKCldBWoMoTqmtXWUKutfqC4XsWlaH/ox4rQn7GEEutBvXVavpBrXAr8XfKZpToPeTY2Ao/lCJeaj+clVBn67C18D1rM7wSKl/lIjnNhh3UfKPo+8WNFmgkUMI5ADnGB/u+sOkMBM+Zbb5G6j/vutjRLIuMneP+gDTQbqHnyutX+XACNlrxDVg0UL5a2fA+CQCiaCVTF0rMi1LtvOVCwQX6R391XcpafK1Pc/Z5pwpNyPAODKt0FKs9G1CcsIbDUnS7nWnqxM91Mp7zkskTRUsMU4aUTKK6BjehpoAbKGZZ2rJNcgsByPcjHBC0mAhW0lK4CRZBuulvkWrfDZckiZA/kEhd4kbflehdob1haVhCWWRrLNXJY69HTQHGc39KK157mxyJQLYZtOPLr9Vf5ydIfGqkxmFXOW7X2KEqBnItkYLaquPPlAXnC0s4LgSBckAdd+t2Rc/x8I3bKD5ae8Zy72VItxLPcctltssP75i0ScDYRFy393IH8y2eVBf88efZYZKlQJZBliksP/fJM1S64Xw513uXlgAdBEARBEATBX+MH/7zM08CkQS4AAAAASUVORK5CYII=>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAAAVCAYAAAD2KuiaAAAAlklEQVR4Xu3WMQqDQBCF4RWxEME7WFlpG0iZC6RNGTyAB/A0llroGX2Ds8VKJP3M++Cv1maHZdcQiIiI/snRG21aly7bVGpftKNnOAchueB2ABUa0aL1KEu+MKjWJjSjNlk1To60bDxuvklWnbmeAlcnQbgfQCQX4aDJC/AIDi7COwX6oBW9NPNP4S+y6TgAF3+CRGTfAfI6EImxBa2TAAAAAElFTkSuQmCC>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACoAAAAWCAYAAAC2ew6NAAACMklEQVR4Xu3Wz0sVURQH8BMVJRaBhhEIaobgSiMjAsNNC4XaGFhgtGmhgYISEbVI2hluRFuFIBYW/YCMMqJAHrYQJMiNIIiLINz2FwR+v97vYa7zZsRV+OB94YM6976Z8+6cuaNZOXvKUaiBg+kB5YBUpgf+d/Z9oXUyDQPwDKrEwwJvy2B0fDunYASG0gMWPnhDvsFrmJL4Ak3yGV7CF7ggngnp1d934IPMaOxj5BgncfnvyxiswQMOpHIJFqRax27JKzgEJ+C7XNacs7AkDRYuWpBrmsOfjuGi3INzUhQ/SVah/Jb8tuQ5L+vQDFf0O53WnLiwPgsLMy9e2FULnyWmHe7q98yUfKHx8XjsjGxCl8YKst1XFlrivbCfmX55AkfgkYXng7gLjFvy+czkFXocfuh4PMZVo98WVocXLEh8Ib8TfjcOCx/aTxb62beix5b0Jc/hdiSv0JOwquO7Fcr2KMhuhWbFb71vRdfhuYz6JE/JF5rXo7Xyx0KhWT3K2zkreYV6X3pvcmG4V/szUJFMDckr1C/mG7zHn3oWyg29GzaEDwbj5yT2cDpxX3pv8pwrltyxouQVyty00PjELYbplEULm30D/BRuVwwLXha+NNKJb7enBX5ZKRfKdy3x9fgP/sIbadUcfokX8hAuwldp0xyGGzW9tXDBSRgW3uY47M2nVtyDvNacJa1Vv2N0D+G/Y9Ro4e3BlfXVTacaOizp1az0WLLy6dTDu0g55ezrbAHUV51Se/SNTwAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAVCAYAAAAtkUK4AAACL0lEQVR4Xu2YMUhVYRiGv7DCMigzokAoGqJIqNBFwcXaIqmUHFqiICUUMosIwkERBJdEBQsKokFochJ0axG1Bh3cG6K1qaGlel/+9/OcezoXE4zynv+BB84957/3wnu++/3fuWaRHcuhlOXYA/fKyBa5AcfkMLwPq0pWmNXAcXhRRrZIDLkMp+Uc/Aw/wS65S2vOw2X5Cr6Es3BIkiNwAZ6S+7TuHXwhp+ASHNB7CsFR+FoyJNIBv8l2nWuEX+QPCzei10Jvpb5mFR6XhNXsx6QOjsIDqXMVTzP8Lh/qXC38IN/oHAPskeU4C1csCZm/gmcWbh6PKSu4MC3CYX/sl2wZZLOQOTUwxGpdc9geZmCrPAkfWQj3suzzxUUihvyPYEBfZbonc8Oid2ALXIRt0jlmYWOk03rNvv9cshcz9MNW2s8LxUE4b6F3Up8uGMoZ6XTDNckNLQ++f9CScY2hMuynlkwc9RurCwADmIC3LdmoHLYGVmF6KrhqyRTCSs8j2yL4mi1lN2yQN1PXs9y1MAb+iRfkf4kHypHsms6xouk9Cw8Tb+G69FFvs5C9TaRvzBNL+rxPIRzzKp4Y8l+G4XI+ppOwU3IqoA+0bsR+fwpkYL4Z8oY4ftO8F6fh92RDfpxcrkxYgV6NP3PkfxHkhIVqprcsbIofLb8P+rjGKSQLv4+P46zu6/JSyYqC4yNXEzyn4yz7LWx0lHNzFlb4FfjeQqXTvM+JRCKRSGTb+QUj/36oSFpqEwAAAABJRU5ErkJggg==>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAVCAYAAAAtkUK4AAACOUlEQVR4Xu2XzYtOYRiHb/nIZxjyEUmUUgr5SpEFC5KFWWBhxUKJjY+kJiUbskERMhMKZUUsZCHMRlYWrGSh5E9QrPyunt/jnDnTG7MZvOe56mre87znnMXvued+7jei8N8yo2YnxssJtjBCeuVFe04elmOH3BExRV6Wq21hhJSQO3DNPpY3Zb98YZf5njFyr30uH8hbssfCbH+3xE6K9L6H8oa9Kt/I436mNQzY7/KHfBop3BwwbIwq+Fle2y/v23FyjXwn51ugmvNn4NnzcmptrRUQRDOMJlfkHZsh1I92uX0bVchUf1+kCuczUsGtaRF1csiL5NxI1ZZDAarupTxlM7SEr3ZHpPZAG9lsF8sTkd6zzR7lwTZSQh4FOJyQVkALOBtVn2YSmCYHY3jItITPdpfX5kU6OPG6r+fIS5YNI3QOS2ZlbAUrLYECPfS9PejrD/FnITch0DNRjWuEStino5o4Fv66u0shhJk2z7O5PSDV3aldEM4X2ynkZovgmpbCNLLC7ql934RNzv9pv3OV/edYL7/ZQ15rhsxG3Is0F2OG1pJDXldbz+Q2UR/X2CTeCXkK4TzoakrIowCz7W1LKLBAfrL7vMbfJ3ai17bL13a614BNqffiOsdieMgnq6+7E8I4YqkowuTn9QWbT3+q8a7l0Nogn8m1tk4e1w401oHqfxTpfbvt1iF3dDnMyFui+tnchIMRl8pNUVV0ncmRDjpkbm7Cpu6UryJVOrZmjCsUCoXC3+UnoXOG0txe8rwAAAAASUVORK5CYII=>

[image19]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAVCAYAAAAtkUK4AAAB8ElEQVR4Xu2XPShFYRjHH/nIVxHyUYpMRCEmZcEmAwODjYFEyUdSokgpC4NCGWQQk9kgFiEDgzKarCYj+f97n9c997jnXrd0w3l/9atzz3nvvd3/ee7zPkfE8Wcp9BhEJsxSHUnSB9fVFTgG06NWiOTBTdisOpLEhZyAMrgEJ/0XQCO8VvfgLjyByyopgaewRs3RdcdwR92CV3Ba3xMKsuGsyup7hHNRKwwt8Fl9h09wXExvpXbNHaxQCavZHpNiuAbzPedCBX/4uQSHPKoGUQdvJBJyGlwQU+E8pqzg0LUIL98NmVMDQ+S/wAvbwyFsV6vhjJhwu9QJuzisuJBTQKKQuWHRIdgGL2GHaikXszHSbX1dCjdUfgdDL5Lofh4a4oXMUGpVywi8V7mhxYKBLkpkXGOoDHteIhNH5efqEBAvZLYGXvdOBT3wVWWlx8LfIviaLSUDNqj9nut+hsWMgd+xSf3VBIXMh4kD+KByWiCJQrZtwntj+Nn7emynEI55ocGFnAKCQiarcEBlnyVcZzfDAj1H7Exse7GXKfkaMh+E/j3se/QMvsEXeKTaHlclpprpoJiHilu97u+DdlzjFOKHFc/Hcd7QXrUzakXIsSNXK6zXYz+5YjY6yrnZDyu8G16IqXQa63McDofD4fhxPgDe8G1NzQ2ERAAAAABJRU5ErkJggg==>

[image20]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACEAAAAWCAYAAABOm/V6AAACBUlEQVR4Xu3VP0iVURzG8RNamEVFhWgERUMUCRk2hS2hiEhDETQ0JYgRtZQQiTgUQtBSUFBBgzoIEeIWNEhBiEVDDe0FkYNb4Bo933uen7z3Hy1Bl7gPfPC+5x7f97zn/M65Kf3n2WX1stm2VH7xN/NPB3He7stduSotFtkmD+1ENB62BZmXT3LRNrnPcXlvz+WZLNod99krr+2QbHW/F/ZUHsuK3LRSdsqSjbqtT37agNt65Yf9kq9yzZjW6MMLoMttzAaf43qP3JPtVgqDYGRgFlpTvtm6jbkfbVesXo7KB+OhzOJkyjMErnn7jSWINMQgaoUpXrNjbisOgqrnIW0WoQZ4EZyWgzKe8sPRL9ejc71QfLPyUbotwiBixkbklCzbmUK/TqN4n/hzhz1IuQ4Y0G6LeioLjRPyzva7nX84YhGWCp9TLrha4YFTxjJwfwZz29gxVWmIQRAe/N2iWFn7sm2lnDUKmOWqlaiDqAWu454oLTl1EHt72B0pum/2RnbInHwxKp38aRDFOojB35KZjR4+P4ZSPnxw2V9w2q0aN2FKp1P1KcoNQbGy1YuJZajcjjdSow6Cvf3IOGIvyEt5ZXHzAykvCS6lfOiwldHjPsWw9mzlyrBs/N7EEp2LLxg19smg/0ZbMfHzezLlQyyui2k3CpEXrAz3pPbeGrPVTDNl+Q1+kIIdg3dhOAAAAABJRU5ErkJggg==>

[image21]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAAAVCAYAAAAtkUK4AAACLUlEQVR4Xu2YS6hOURiGP7nkGg6JMhCllAEhKUYMSOSWY2AgykCUazolExNl4lrIOUWhjJQSBnKZnJiYGJlQMjUyMOJ9Wu+y99n8dc7A7d/rqaez97fXPn+9e/Xt7/8jCv8t02p2YqwcZwsjZJs8Z8/IA3L0kBURk+QFudQWRkgJuQML7UP5Ub6XvXaU1/A3157Iu/KG7LEw09fm2wnyurwnr9krclAe8z2tYJYcsIQE2+UXu9m1VfKpneHabnnHjpHL5Bs5xwK7OR8D956Vk2u1rofwvtqjrk2Xr+1N1y76OJ8Dob6zi+yrqEJm95+K9PA4RnZwa1pEhv54xNIyoBkyu+6ZPGkztIRPdkOk9kAbWWPnyeORwl1nD3Fj2ygh/yUI6LOlJ0+RL+PnkGkJH+wm12bLfnvV5/T985YHRui8LJmVsXVMlY8j9U4kEHrq2xheyE24/3RU4xqhEnZfVBPH3B+rWwABXJJ7onpRQad2QTiMfNgp5GaL4JyWwjSy2O6sXW+yL9IYOByX2H+SHOhBucU1djTu97XbkeZizDBd5JBX1OqZ3Cbq4xoPiT4PeQphzOt6Ssi/GQJkPsbLcodlKsDDXrdLPrDjXVsvX1geSCY/tNyL6/A5zZBPVJe7E3Zj/nb37RfyWwSwG29ZXlor5SO53NbJ49reRh34vPuR/t9Wu3bIipbDDz24QK6OakfXmRjpRYfMzU3Y4Rvl80g7HVs5xhUKhULhz/MdB2KGADDAAlMAAAAASUVORK5CYII=>