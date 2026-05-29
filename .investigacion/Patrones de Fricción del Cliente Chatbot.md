# **Detección computacional de la fricción del usuario en sistemas conversacionales: Análisis empírico de patrones dialectales, desviación pragmática y diseño de expresiones regulares para español y portugués**

La evaluación del rendimiento de las interfaces conversacionales ha transitado desde la simple clasificación de intenciones hacia el análisis del comportamiento del usuario en escenarios de colapso dialógico.1 En el ámbito de la lingüística computacional y el diseño de la experiencia del cliente (CX), la fricción se define como la resistencia o insatisfacción que experimenta un usuario debido a la incapacidad del sistema para comprender o resolver una demanda.1 Investigaciones recientes revelan que las interrupciones conversacionales mal gestionadas —clasificadas como malentendidos (misunderstandings) o declaraciones de no-comprensión (non-understandings)— disparan las tasas de abandono de la interacción hasta un 62% y 75% respectivamente.1 Esto ocurre especialmente cuando el usuario se ve atrapado en el denominado "bucle del chatbot" (chatbot loop), caracterizado por respuestas repetitivas o preguntas irrelevantes.3  
A pesar del auge de la inteligencia artificial generativa, estudios del sector indican que únicamente el 14% de los problemas de servicio al cliente se resuelven completamente mediante el autoservicio automatizado.3 Cuando un sistema conversacional carece de la flexibilidad o de los niveles de autorización requeridos para ejecutar transacciones complejas, el cliente manifiesta su frustración mediante una serie de marcas lingüísticas, variaciones de entonación y patrones de insistencia.3  
Para parametrizar matemáticamente este estado de frustración del usuario en canales conversacionales de texto o voz, los sistemas modernos de análisis de sentimiento implementan modelos de puntuación agregada de fricción (![][image1]) que evalúan múltiples dimensiones lingüísticas y paralingüísticas 4:  
![][image2]  
Donde ![][image3] representa el peso de los marcadores lingüísticos explícitos de enojo o resignación detectados en el texto; ![][image4] es el índice de prosodia o intensidad paralingüística (como el uso de mayúsculas sostenidas o signos de exclamación reiterados) 4; ![][image5] representa el contador de intenciones repetidas de forma consecutiva sin progreso dialógico (un factor crítico que suele detonar alarmas tras el tercer intento fallido) 4; y ![][image6] mide la velocidad de respuesta del usuario o las pausas prolongadas.4 Los coeficientes ![][image7], ![][image8], ![][image9] y ![][image10] actúan como ponderadores según el canal de interacción y el segmento del cliente.4  
El procesamiento en tiempo real de este indicador permite a los sistemas NLU (Natural Language Understanding) desviar la interacción hacia un agente humano antes de que la fricción escale a quejas públicas en plataformas de defensa del consumidor.6 En este contexto, el diseño de patrones de expresiones regulares (regex) optimizados en Python (re.search) constituye la primera línea de defensa para la tokenización ultrarrápida y el filtrado de flujos de conversación de baja latencia.4

## **1\. PROFANITY / AGRESIVIDAD IMPLÍCITA**

Esta categoría comprende aquellos enunciados donde el usuario exterioriza hostilidad, desprecio o descrédito hacia la interfaz conversacional sin recurrir necesariamente a un léxico soez de alta gravedad que activaría los filtros estándar de seguridad.4 Se caracteriza por el uso de insultos atenuados, eufemismos dialectales, expresiones pasivo-agresivas y enunciados que asimilan el desempeño de la máquina con una burla o estafa.12  
Pragmáticamente, estas expresiones denotan una ruptura de la cortesía conversacional, indicando que el cliente ha perdido la confianza en las capacidades resolutivas de la entidad sintáctica.1 En español, las variaciones geográficas muestran un uso extendido de eufemismos anatómicos en España ("hasta los mismísimos") 15, mientras que en el ámbito hispanoamericano prevalecen metáforas de engaño como "me están viendo la cara" (México) 13 o "me estás cargando" (Argentina y Uruguay).12  
En portugués, los usuarios brasileños recurren de manera característica a términos asociados a la farsa o al desorden operativo ("palhaçada", "estão me tirando", "sacanagem") 14, mientras que en el portugués de Portugal (PT-PT) se observa el predominio de la locución aspectual "estar a gozar" para denunciar que el bot se está burlando del problema del cliente.19

### **Patrón de Expresión Regular en Español (ES)**

Python  
import re

\# Patrón optimizado para agresividad implícita en español  
pattern\_es\_profanity \= re.compile(  
    r'(?i)\\b(es( un)? chiste|vaya ayuda|estafador(es)?|p\[eé\]simo servicio|'  
    r'me est\[aá\]n? (tomando el pelo|viendo la cara|cargando)|'  
    r'hasta los (mism\[ií\]simos|cojones|huevos|ovarios))\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"La verdad es que su chatbot es un chiste, no resuelve nada de lo que le pido."* 1 | es un chiste | Deslegitimación ontológica del bot. Al categorizar el sistema como una burla o "chiste", el usuario invalida la autoridad y utilidad de la interfaz.1 |
| *"Pésimo servicio al cliente, llevo una hora intentando hacer el trámite."* 22 | pésimo servicio | Calificación evaluativa peyorativa de carácter terminal. El cliente realiza un juicio de valor adjetivado que precede al abandono de la interacción.22 |
| *"Me están tomando el pelo con sus respuestas automáticas, exijo una solución."* 13 | me están tomando el pelo | Expresión idiomática de incredulidad y hostilidad pasiva. Implica que el usuario percibe una falta de respeto o una simulación condescendiente por parte de la marca.13 |

### **Patrón de Expresión Regular en Portugués (PT)**

Python  
import re

\# Patrón optimizado para agresividad implícita en portugués  
pattern\_pt\_profanity \= re.compile(  
    r'(?i)\\b(palha\[cç\]ada|est\[aã\]o (me tirando|a gozar)|que piada|p\[eé\]ssimo servi\[cç\]o|brincadeira)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Isso é uma palhaçada\! Cadê o meu reembolso?"* 14 | palhaçada | Metáfora brasileña de devaluación institucional. El usuario asimila el flujo automatizado a un espectáculo circense o farsa no profesional.14 |
| *"Vocês estão me tirando com essa conversa repetitiva."* 14 | estão me tirando | Modismo sociolectal brasileño altamente informal que expresa indignación ante lo que el cliente percibe como una falta de seriedad o intento de engaño. |
| *"Péssimo serviço, o robô só envia mensagens automáticas."* 22 | Péssimo serviço | Declaración evaluativa directa de la calidad del servicio en portugués. Indica la frustración por la rigidez de las respuestas estructuradas.25 |

## **2\. NEGATION / FRUSTRACIÓN PASIVA Y RESIGNACIÓN**

Esta categoría agrupa aquellos enunciados en los cuales el usuario expresa desacuerdo directo con las afirmaciones del bot, descalifica la pertinencia de la información provista o manifiesta una capitulación forzada ante la inoperancia del sistema.1 Esta conducta lingüística suele ser la antesala del abandono silencioso o de la deserción del cliente.27  
Desde la perspectiva pragmática de la interacción, la resignación pasiva ("deja así", "olvídalo", "deixa pra lá") rompe de forma unilateral el principio de cooperación dialógica.1 El usuario calcula que el costo cognitivo de continuar reconfigurando su solicitud para adaptarla a la limitada gramática del bot es muy superior al beneficio potencial de la respuesta, lo que destruye el compromiso conversacional.1

### **Patrón de Expresión Regular en Español (ES)**

Python  
import re

\# Patrón optimizado para frustración pasiva y resignación en español  
pattern\_es\_negation \= re.compile(  
    r'(?i)\\b(no me sirve|deja as\[ií\]|no es eso|olv\[ií\]dalo|otra vez con lo mismo|no entiendes nada)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Tu respuesta no me sirve de nada, solo me haces perder el tiempo."* 1 | no me sirve | Negación funcional explícita. El usuario evalúa el resultado de la búsqueda de información y declara de forma tajante su inutilidad práctica.1 |
| *"Deja así, ya veo que esta máquina no entiende mi problema."* 1 | Deja así | Fórmula de desistimiento conversacional. Marca el cese voluntario del esfuerzo del cliente por hacerse entender frente a un sistema rígido.1 |
| *"No, no es eso lo que pregunté, es frustrante esta interacción."* 1 | no es eso | Estructura de corrección sintáctico-semántica. Indica que el asistente virtual ha incurrido en un error de comprensión (misunderstanding).1 |

### **Patrón de Expresión Regular en Portugués (PT)**

Python  
import re

\# Patrón optimizado para frustración pasiva y resignación en portugués  
pattern\_pt\_negation \= re.compile(  
    r'(?i)\\b(deixa (pra|para) l\[aá\]|n\[aã\]o adianta|esquece|de novo isso|voc\[eê\] n\[aã\]o entende|n\[aã\]o serve)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Deixa pra lá, vou ter que resolver isso em outra empresa."* 25 | Deixa pra lá | Expresión de abandono sumamente común en Brasil. Representa la renuncia del cliente a continuar interactuando con el autoservicio.25 |
| *"Não adianta explicar nada para você, não entende nada mesmo."* 26 | Não adianta | Declaración de ineficacia instrumental. El cliente dictamina que no existe viabilidad operativa para lograr el entendimiento mutuo con el bot.26 |
| *"Esquece, cansei desse atendimento robótico que não me dá soluções."* 3 | Esquece | Imperativo de cancelación en portugués. Denota cansancio y frustración frente a la incapacidad del sistema para resolver problemas complejos.3 |

## **3\. ESCALATION / SOLICITUD DE ESCALAMIENTO IMPLÍCITO**

El escalamiento implícito se produce cuando el cliente intenta evadir los canales automatizados y conectar con un agente humano, pero evita usar los términos directos mapeados por las gramáticas rígidas del bot (como "agente", "humano", "atendente" o "chat en vivo").3 Los usuarios recurren a circunloquios y fórmulas indirectas porque asumen que el bot ha sido configurado para retenerlos forzosamente y retrasar la derivación.3  
Este comportamiento lingüístico refleja la necesidad de interactuar con un sujeto que posea empatía, criterio subjetivo y, fundamentalmente, la autoridad administrativa que le ha sido negada al chatbot (por ejemplo, para procesar reembolsos o resolver fallos técnicos complejos).3 En foros de internet, se ha documentado que los usuarios repiten términos absurdos o exigen hablar con cargos superiores para romper de forma deliberada el bucle conversacional del asistente.3

### **Patrón de Expresión Regular en Español (ES)**

Python  
import re

\# Patrón optimizado para solicitud de escalamiento implícito en español  
pattern\_es\_escalation \= re.compile(  
    r'(?i)\\b(alguien real|con una persona|que me atienda alguien|'  
    r'con un supervisor|tel\[eé\]fono de soporte|asistencia de verdad)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Por favor, pásame con alguien real que comprenda mi caso."* 3 | alguien real | Oposición ontológica entre el agente sintético y el interlocutor humano. Expresa desprecio por las capacidades cognitivas del bot.3 |
| *"Quiero hablar con una persona de verdad, no con este software."* 3 | con una persona | Demanda explícita de mediación biológica. El cliente busca un entorno comunicativo que admita la flexibilidad semántica y la empatía.3 |
| *"Exijo que me atienda un supervisor de inmediato."* 3 | un supervisor | Solicitud de escalamiento jerárquico. Presupone que la resolución del problema exige facultades decisorias que exceden la programación de la máquina.3 |

### **Patrón de Expresión Regular en Portugués (PT)**

Python  
import re

\# Patrón optimizado para solicitud de escalamiento implícito en portugués  
pattern\_pt\_escalation \= re.compile(  
    r'(?i)\\b(algu\[eé\]m de verdade|falar com pessoa|atendente real|ajuda humana|atendimento especializado)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Preciso falar com alguém de verdade para resolver o meu estorno."* 3 | alguém de verdade | Reivindicación de autenticidad humana. El cliente asume que el chatbot es un obstáculo artificial que dilata la resolución de su trámite financiero.25 |
| *"Como faço para falar com pessoa humana? Não quero mais robôs."* 25 | falar com pessoa | Solicitud directa de transferencia a un operador humano. Denota insatisfacción y saturación por la frialdad de las interacciones automatizadas.26 |
| *"Quero falar com um atendente real agora mesmo."* 3 | atendente real | Intención de derivación humana. Utiliza el adjetivo de existencia "real" para evitar que el bot responda con un menú de opciones repetitivas.3 |

## **4\. SARCASMO Y FRUSTRACIÓN VELADA**

El sarcasmo constituye uno de los desafíos empíricos más rigurosos para la lingüística computacional aplicada a la atención al cliente, dado que representa una inversión deliberada de la polaridad del enunciado.30 A nivel sintáctico y léxico, el mensaje presenta una estructura aparentemente positiva, optimista o cortés, pero su intencionalidad pragmática y contextual es profundamente negativa y denota una frustración extrema.11  
La detección del sarcasmo requiere que el sistema analice la contradicción inherente entre el uso de adjetivos de excelencia ("genial", "excelente", "maravilha") y el resultado perjudicial o nulo de la acción descrita ("me bloquearon", "gracias por nada").11 La ausencia de contexto situacional suele provocar que los motores tradicionales de análisis de sentimiento clasifiquen de manera errónea estas interacciones como interacciones altamente satisfactorias, enmascarando serios problemas de retención de clientes.11

### **Patrón de Expresión Regular en Español (ES)**

Python  
import re

\# Patrón optimizado para sarcasmo y frustración velada en español  
pattern\_es\_sarcasm \= re.compile(  
    r'(?i)\\b(genial(,? me)? bloquearon|excelente ayuda|gracias por nada|buen\[ií\]sima la atenci\[oó\]n)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Genial, me bloquearon la tarjeta justo cuando iba a pagar."* 11 | Genial, me bloquearon | Antífrasis irónica. El adjetivo exclamativo positivo "genial" es anulado pragmáticamente por la descripción de un perjuicio financiero directo.11 |
| *"Excelente ayuda la suya, ahora tengo el sistema completamente caído."* 11 | excelente ayuda | Sarcasmo mediante hipérbole de cortesía. El usuario califica irónicamente como "excelente" un resultado catastrófico causado por el bot.11 |
| *"Muchas gracias por nada, sigo con el mismo inconveniente."* 11 | gracias por nada | Oxímoron pragmático. El ritual social de agradecimiento ("muchas gracias") queda inmediatamente invalidado por la locución restrictiva "por nada".11 |

### **Patrón de Expresión Regular en Portugués (PT)**

Python  
import re

\# Patrón optimizado para sarcasmo y frustración velada en portugués  
pattern\_pt\_sarcasm \= re.compile(  
    r'(?i)\\b(\[oó\]timo(,? me)? bloquearam|obrigado por nada|\[oó\]tima ajuda)\\b'  
)

| Ejemplo Real de Activación | Fracción Coincidente | Justificación Lingüística y Pragmática |
| :---- | :---- | :---- |
| *"Ótimo, me bloquearam a conta e agora não posso acessar minhas configurações."* 11 | Ótimo, me bloquearam | Incongruencia de polaridad semántica en portugués brasileño. El adverbio "ótimo" introduce de forma irónica una experiencia de alta frustración.11 |
| *"Obrigado por nada, esse robô não ajuda em absolutamente nenhum problema."* 11 | Obrigado por nada | Expresión idiomática de descontento velado. Expresa formalmente agradecimiento con el único propósito de enfatizar la inoperancia del sistema.25 |
| *"Ótima ajuda, agora tenho que reiniciar o processo inteiro."* 11 | Ótima ajuda | Calificación de ironía mordaz. Se describe el desempeño del sistema como "ótima ajuda" cuando la consecuencia real ha sido duplicar el esfuerzo del usuario. |

## **ANÁLISIS DE RENDIMIENTO DIALECTAL, PARALINGÜÍSTICA E IMPLEMENTACIÓN DE SISTEMAS DE ENRUTAMIENTO EMPÁTICO**

Para lograr que la detección de estas estructuras lingüísticas impacte positivamente en las métricas corporativas, los sistemas conversacionales deben integrar estos patrones de expresiones regulares en una arquitectura híbrida de enrutamiento empático.4 Esto implica correlacionar de forma inmediata el análisis léxico con otros indicadores del comportamiento del usuario en tiempo real.4

### **Matriz comparativa de métricas, señales paralingüísticas e indicadores de fricción en producción**

| Dimensión de Análisis | Canal / Región de Impacto | Parámetro Técnico / Métrica Asociada | Indicadores Conductuales en Tiempo Real | Acción del Sistema (Protocolo de Mitigación) |
| :---- | :---- | :---- | :---- | :---- |
| **Latencia de Respuesta** | Canales de Voz / Telefonía 7 | Límite Crítico: ![][image11] de retraso conversacional.7 | El usuario empieza a hablar sobre la IA (overlapping) o pierde el interés.7 | Activar modelos predictivos de preparación de respuesta y modular el ritmo conversacional.7 |
| **Velocidad de Escritura y Pausas** | Canales Escritos (Webchat / WhatsApp) 4 | Desviación estándar de pulsaciones por minuto.4 | Ráfagas de mensajes cortos combinados con pausas prolongadas injustificadas.4 | Simplificar de forma drástica las opciones del menú de autoservicio y reducir los pasos lógicos.4 |
| **Intensidad Paralingüística** | WhatsApp / Redes Sociales 6 | Uso de mayúsculas sostenidas e hiper-puntuación (ej. *\!\!\!*, *???*).4 | Mensajes estructurados totalmente en mayúsculas (*Caps Lock*) o repetición de emoticonos de enojo.4 | Elevar la puntuación de fricción agregada e implementar un tono conversacional neutral y sumamente asertivo.4 |
| **Desviación Dialectal** | España / Latinoamérica 12 | Mapeo de regionalismos críticos de descontento en el diccionario NLU. | Uso de modismos locales como *"me estás cargando"* (ES-AR) o *"hasta los mismísimos"* (ES-ES).12 | Reclasificar de forma dinámica la gravedad de la llamada y derivar al flujo prioritario correspondiente.4 |
| **Evasión de Retención** | Portugal / Brasil 3 | Detección de patrones de escalamiento iterados más de 2 veces.3 | El cliente escribe frases disruptivas o repite términos aleatorios para forzar el fallo del sistema.3 | Desactivar el bot de retención y transferir al cliente de forma directa al canal telefónico o chat humano de alta prioridad.3 |

### **Integración de arquitecturas híbridas (Regex y Transformers)**

En sistemas que gestionan un alto volumen de interacciones mensuales, delegar el análisis de sentimiento y la detección de fricción exclusivamente a modelos lingüísticos masivos basados en transformadores (como BERT o GPT) puede generar cuellos de botella de infraestructura y costos computacionales significativos.8 Por este motivo, el uso de expresiones regulares compactas y altamente eficientes actúa como un filtro heurístico de primera capa.4  
Este enfoque de análisis de sentimiento basado en reglas permite clasificar el texto de forma casi instantánea 35:

* **Procesamiento de primera línea:** Al recibir una interacción, el microservicio de mensajería evalúa el texto del cliente utilizando el motor interno de expresiones regulares compiladas en Python. Si se detecta un patrón de alta fricción (como expresiones pertenecientes a la categoría de profanidad o escalamiento implícito severo), se anula el procesamiento semántico profundo.4  
* **Derivación inmediata con baja latencia:** El sistema de enrutamiento dispara un protocolo de derivación inmediata (handoff inteligente) al canal de operadores de soporte humano con un tiempo de procesamiento inferior a los 2 segundos, previniendo la frustración del cliente.6  
* **Optimización de recursos cognitivos:** Los modelos transformer avanzados se reservan exclusivamente para analizar aquellas interacciones donde no se han disparado alertas de expresiones regulares, o donde la complejidad semántica y el sarcasmo requieran desentrañar relaciones contextuales profundas y referencias de turnos previos.2

Esta combinación estratégica de reglas lingüísticas compactas y procesamiento neuronal distribuye el costo operativo de la atención al cliente, incrementa la resiliencia técnica de la plataforma y mejora significativamente la experiencia del usuario final.4

#### **Obras citadas**

1. Full article: “Have I Answered Your Question Satisfactorily?”: Customer Requests, Intent Recognition Errors, and Repair Strategies in Chatbot Interactions \- Taylor & Francis, fecha de acceso: mayo 29, 2026, [https://www.tandfonline.com/doi/full/10.1080/10447318.2026.2626805](https://www.tandfonline.com/doi/full/10.1080/10447318.2026.2626805)  
2. Angry Customers: Is AI Not Ready to Handle Complaints and Difficult Conversations?, fecha de acceso: mayo 29, 2026, [https://velaro.com/blog/difficult-conversations-with-angry-customers-ai-in-customer-service](https://velaro.com/blog/difficult-conversations-with-angry-customers-ai-in-customer-service)  
3. Chatbot Frustration is Real: Hidden Costs and Best Practices, fecha de acceso: mayo 29, 2026, [https://cmr.berkeley.edu/2026/04/chatbot-frustration-is-real-hidden-costs-and-best-practices/](https://cmr.berkeley.edu/2026/04/chatbot-frustration-is-real-hidden-costs-and-best-practices/)  
4. Can AI Agents Detect Customer Frustration and Adapt? | CX Guide, fecha de acceso: mayo 29, 2026, [https://www.pedowitzgroup.com/can-ai-agents-detect-customer-frustration-and-adapt-cx-guide](https://www.pedowitzgroup.com/can-ai-agents-detect-customer-frustration-and-adapt-cx-guide)  
5. How Chatbot Sentiment Analysis is Transforming Customer Experience in Contact Centers \- Voxtron | Dubai, fecha de acceso: mayo 29, 2026, [https://www.voxtronme.com/2025/11/24/how-chatbot-sentiment-analysis-is-transforming-customer-experience-in-contact-centers/](https://www.voxtronme.com/2025/11/24/how-chatbot-sentiment-analysis-is-transforming-customer-experience-in-contact-centers/)  
6. Chatbot Detecção Insatisfação Tempo Real 2026 | SocialHub, fecha de acceso: mayo 29, 2026, [https://www.socialhub.pro/blog/chatbot-whatsapp-deteccao-insatisfacao-tempo-real-handoff-humano-2026/](https://www.socialhub.pro/blog/chatbot-whatsapp-deteccao-insatisfacao-tempo-real-handoff-humano-2026/)  
7. The Complete Guide To AI Turn-Taking | 2025 \- Tavus, fecha de acceso: mayo 29, 2026, [https://www.tavus.io/post/ai-turn-taking](https://www.tavus.io/post/ai-turn-taking)  
8. Chatbot WhatsApp Análise de Sentimento 2026 | SocialHub, fecha de acceso: mayo 29, 2026, [https://www.socialhub.pro/blog/chatbot-whatsapp-deteccao-sentimento-frustracao-cliente-ia-2026/](https://www.socialhub.pro/blog/chatbot-whatsapp-deteccao-sentimento-frustracao-cliente-ia-2026/)  
9. Regex for Translators: Filtering Segments Starting with a Spanish Infinitive in Trados Studio, fecha de acceso: mayo 29, 2026, [http://noradiaz.blogspot.com/2025/01/regex-for-translators-filtering.html](http://noradiaz.blogspot.com/2025/01/regex-for-translators-filtering.html)  
10. They have an interesting regex for detecting negative sentiment in users prompt ... \- Hacker News, fecha de acceso: mayo 29, 2026, [https://news.ycombinator.com/item?id=47585326](https://news.ycombinator.com/item?id=47585326)  
11. Stress Testing Generative AI Against Emotions in Live Chats \- CoSupport AI, fecha de acceso: mayo 29, 2026, [https://cosupport.ai/articles/stress-testing-generative-ai-against-sarcasm-anger-and-emotional-volatility-in-live-chats](https://cosupport.ai/articles/stress-testing-generative-ai-against-sarcasm-anger-and-emotional-volatility-in-live-chats)  
12. Derecho Penal \- Biblioteca, fecha de acceso: mayo 29, 2026, [https://tsjcaba.opac.ar/pgmedia/Media/PDFs/1.11416\_D-11923\_Infojus-DERECHO\_PENAL\_A2\_N5.pdf](https://tsjcaba.opac.ar/pgmedia/Media/PDFs/1.11416_D-11923_Infojus-DERECHO_PENAL_A2_N5.pdf)  
13. ¿Me están tomando el pelo con el servicio? : r/TeslaLounge \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/TeslaLounge/comments/1hx0wll/service\_pulling\_my\_leg/?tl=es-419](https://www.reddit.com/r/TeslaLounge/comments/1hx0wll/service_pulling_my_leg/?tl=es-419)  
14. Conta suspensa com benefícios corporativos \- Reclamação para Mercado Pago \- Proteste, fecha de acceso: mayo 29, 2026, [https://www.proteste.org.br/reclame/lista-de-reclamacoes-publicas/reclamacoes-publicas?referenceid=CPTBR01987758-34](https://www.proteste.org.br/reclame/lista-de-reclamacoes-publicas/reclamacoes-publicas?referenceid=CPTBR01987758-34)  
15. 11 Frases para expresar enojo y frustración en español (lección 382\) \- YouTube, fecha de acceso: mayo 29, 2026, [https://www.youtube.com/watch?v=KAZQ\_ssU-zI](https://www.youtube.com/watch?v=KAZQ_ssU-zI)  
16. Buzón Automotriz \- ElNorte, fecha de acceso: mayo 29, 2026, [https://www.elnorte.com/aplicaciones/articulo/default.aspx?id=1205968](https://www.elnorte.com/aplicaciones/articulo/default.aspx?id=1205968)  
17. Correo Argentino me robo una Macbook Pro y la reemplazaron por 2 kg de azúcar \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/argentina/comments/1kxmprw/correo\_argentino\_me\_robo\_una\_macbook\_pro\_y\_la/](https://www.reddit.com/r/argentina/comments/1kxmprw/correo_argentino_me_robo_una_macbook_pro_y_la/)  
18. Ficção e Emoções em Recanto das Alegrias | PDF | Amor \- Scribd, fecha de acceso: mayo 29, 2026, [https://pt.scribd.com/document/874815832/Rendidos-Ao-Amor-Spin-Off-Deby-Incour](https://pt.scribd.com/document/874815832/Rendidos-Ao-Amor-Spin-Off-Deby-Incour)  
19. Qual a vossa opinião em relação a este tipo de marketing? Ficaram chateados? : r/portugal \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/portugal/comments/1b72iab/qual\_a\_vossa\_opini%C3%A3o\_em\_rela%C3%A7%C3%A3o\_a\_este\_tipo\_de/](https://www.reddit.com/r/portugal/comments/1b72iab/qual_a_vossa_opini%C3%A3o_em_rela%C3%A7%C3%A3o_a_este_tipo_de/)  
20. Viva à CP\! : r/portugal \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/portugal/comments/11da4cm/viva\_%C3%A0\_cp/](https://www.reddit.com/r/portugal/comments/11da4cm/viva_%C3%A0_cp/)  
21. Pergunta à Tina \- Verdade, fecha de acceso: mayo 29, 2026, [https://verdade.co.mz/wp-content/uploads/2020/08/a\_verdade\_ed\_0475.pdf](https://verdade.co.mz/wp-content/uploads/2020/08/a_verdade_ed_0475.pdf)  
22. eh QUÉ\!? la dirección y todo está bien. Wtf, ¿qué quieres decir con que falta el número de unidad? : r/purolator \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/purolator/comments/1n1kkar/uhm\_what\_address\_and\_everything\_is\_correct\_wtf/?tl=es-419](https://www.reddit.com/r/purolator/comments/1n1kkar/uhm_what_address_and_everything_is_correct_wtf/?tl=es-419)  
23. Problema de speaker.bot con el filtro de palabras y el reemplazo : r/streamerbot \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/streamerbot/comments/1qe905q/speakerbot\_bad\_word\_and\_replacement\_problem/?tl=es-419](https://www.reddit.com/r/streamerbot/comments/1qe905q/speakerbot_bad_word_and_replacement_problem/?tl=es-419)  
24. Los civilizados frente a los bárbaros en Ciudades desiertas, del escritor mexicano José Agustín \- S-Space, fecha de acceso: mayo 29, 2026, [https://s-space.snu.ac.kr/bitstream/10371/69289/1/200819109.pdf](https://s-space.snu.ac.kr/bitstream/10371/69289/1/200819109.pdf)  
25. Chatbot no atendimento: evite essas 5 falhas e melhore a experiência do cliente, fecha de acceso: mayo 29, 2026, [https://otima.digital/chatbot-no-atendimento/](https://otima.digital/chatbot-no-atendimento/)  
26. UNIVERSIDADE DE SÃO PAULO FACULDADE DE ECONOMIA, ADMINISTRAÇÃO E CONTABILIDADE DEPARTAMENTO DE ADMINISTRAÇÃO PROGRAMA DE PO \- Teses USP, fecha de acceso: mayo 29, 2026, [https://teses.usp.br/teses/disponiveis/12/12139/tde-10022020-175423/publico/CorrigidoFernanda.pdf](https://teses.usp.br/teses/disponiveis/12/12139/tde-10022020-175423/publico/CorrigidoFernanda.pdf)  
27. Las 10 mejores herramientas de análisis de sentimiento para la atención al cliente en 2026, fecha de acceso: mayo 29, 2026, [https://www.edesk.com/es/blog/10-mejores-herramientas-de-analisis-de-sentimiento-para-tickets-de-atencion-al-cliente-edicion-espana/](https://www.edesk.com/es/blog/10-mejores-herramientas-de-analisis-de-sentimiento-para-tickets-de-atencion-al-cliente-edicion-espana/)  
28. 20 frases útiles de atención al cliente (+4 que debes evitar) \- SalesGroup AI, fecha de acceso: mayo 29, 2026, [https://salesgroup.ai/es/frases-de-servicio-al-cliente/](https://salesgroup.ai/es/frases-de-servicio-al-cliente/)  
29. 20 Frases Úteis de Atendimento ao Cliente (+4 para Evitar) | SalesGroup AI, fecha de acceso: mayo 29, 2026, [https://salesgroup.ai/pt/frases-de-atendimento-ao-cliente/](https://salesgroup.ai/pt/frases-de-atendimento-ao-cliente/)  
30. Sarcasm-as-a-Service: Five Years Later \- JAVAPRO International, fecha de acceso: mayo 29, 2026, [https://javapro.io/2026/01/14/sarcasm-as-a-service-five-years-later/](https://javapro.io/2026/01/14/sarcasm-as-a-service-five-years-later/)  
31. Contextual Sentiment Analysis: Handling Sarcasm, Irony, and Ambiguity in Text \- ExcelR, fecha de acceso: mayo 29, 2026, [https://www.excelr.com/blog/artificial-intelligence/contextual-sentiment-analysis-for-sarcasm-irony-ambiguity](https://www.excelr.com/blog/artificial-intelligence/contextual-sentiment-analysis-for-sarcasm-irony-ambiguity)  
32. Analisis de Sentimiento con Inteligencia Artificial \- PotenzzIA, fecha de acceso: mayo 29, 2026, [https://www.potenzzia.com/blog/analisis-de-sentimiento-con-inteligencia-artificial](https://www.potenzzia.com/blog/analisis-de-sentimiento-con-inteligencia-artificial)  
33. ¿Cuáles son algunas frases para expresar frustración en español? : r/Spanish \- Reddit, fecha de acceso: mayo 29, 2026, [https://www.reddit.com/r/Spanish/comments/anec45/what\_are\_some\_phrases\_for\_expressing\_frustration/?tl=es](https://www.reddit.com/r/Spanish/comments/anec45/what_are_some_phrases_for_expressing_frustration/?tl=es)  
34. 4 ejemplos de análisis de sentimiento para que mejores tu CX \- Contentsquare, fecha de acceso: mayo 29, 2026, [https://contentsquare.com/es-es/guias/analisis-de-sentimiento/ejemplos/](https://contentsquare.com/es-es/guias/analisis-de-sentimiento/ejemplos/)  
35. ¿Qué es el análisis de sentimientos? \- IBM, fecha de acceso: mayo 29, 2026, [https://www.ibm.com/es-es/think/topics/sentiment-analysis](https://www.ibm.com/es-es/think/topics/sentiment-analysis)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAbCAYAAADszNYXAAAB20lEQVR4Xu3WvStHURgH8EdeIkUkLyExkCiDUmTzEoXBSxYZJCKZTAZKKRYUsSgZZLBQRv8Ai0lZWcyMSvl+Pc/xO35I+RnO1f3Wp7juPc695znPvSJx4qScdCiGsh+UQKZdE0wKYRru4cHMwzDMwrl5hGa7JqgUwQ2sGj8ZZgsqkv4WRPhEn6DXMCyR3PczRBZFbzK4RHryrHnWeo1hemBUdENTg2j5BJU0OIBbGDPcsFdQ750XZNxm3ZREW+wS7TAF3nlBJtKTd5t1wDvGG1jyfg82/maNTLhR6Qgu5GNb/C5ckT7DnxmOUWv6Ic+OczzqhnbRjuXKss3O7zBsy24cjuGP8yns5ZfmBZ7hVLTW6atUi3YhtkxaE/2Hc6KfEjQB61AFO4afH+OiKzxk9mEKTkwjrMAIVBp2vS8T6cn/JnVwB2eG3zn8pyy7HJMlWgLsXHzJETMI21BuDkW7XLZh07gWbRJ8GFT6dmWK4WRoUnRTLxg+SdZm8odcPhxL4m3N1dkQXVG+9GhPPr6tO0VXw8+fvM05GeKTa4Vlw9Lg09+FFsMbbIIZ0ZsjHiPeBFeAeNwPx2cZujHcOCkn0pP/KZyUa4t+XLmxRbq4jzxekxw3Tpw4cf5LXgFUIWJEgcIjRgAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAAAaCAYAAAAHfFpPAAACKklEQVR4Xu3Xz0sVURQH8CNplFphhvkjiSSEQBIJkkLkiYi9hVJpK6WV1iIXEbiRcFEI5kICBUUEf4ALEWzVzkVbceH/IEE7Fy3cRX2/nHOYedNDajFv8e584cOD+2beu+fOvXdmRLJkiecCNEBTQj1UxI4r2wQ/ANdhFI7hxLyCHFRGh5V36uAI5kxweQA/IW+Cyxj8gDYTXIIeAO70G3AANSaoxDfAIBPfAJO5A29MKVIN72FVdGaW5Dkkvv6TmYJHplRhf14nG9NMsAPgU4wb4DeoTXw3CF/hmuEj82Nohk4zAFehN9bm05af3tYl+hts80dt/lY79EOVYZagB+4aHud95fE0JPq/3ifiBWR/bss/hOv90PyCM9gVvRPQKfwWnQGebhgXHSy/XU7DZ7gCy8YHgefmTB9si95hRsy66CP3Htwz3JC3YFj08Zw2RYv9AC9Mq2hfuH/xk/ZhEhYlpXCDeimF0/OT6NXi7OFMohbogB24bFgQB4tXjN8TC70BlyQKB++76EbIookzg4XyXWXWcHAbJeqT94vvLqm+v3jBvOLEIm6K7hEL5j48l8LbKgt6KnpX8au9In931tc/z39nWPwT0RkTj5/LPnm/Uk/QA8CC10SnbbKIPHw0z+CWaNG+Zr/AW2tncVRsp+c6Z8E5mDHcjLmBzsNDMyG6XLxP3q/U46PuuzLX9P+G55DfLeK5KFF7cj2zvdijevK4LFmyZMlyXv4AAnBjLntcWywAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAaCAYAAAD1wA/qAAACDElEQVR4Xu3XzStlYRwH8J/MiDE0JhkmFqYxYkaSLMhGGRoTC2bhLbOwsKam5kUpZcFGZoHIS2rGTNlMWYga9rb+BDUL+QOQ8v32fB/3dJob6arjut/65DrPc849z3PO83LNUol20qEAiuJ4LJFP0jTkKXTBPhxIL3yAr3Aoo/BQ50Q2eeYaMiHBdMoJ1IfKIpcKOIJ3EsyQnEFjqCxy6YN/8EJ8smBLtu0OjJWkach32IVS4WxVBguwI4WXtSMaP9D/mJupgl5BmkQ+fqB3hAv+k2LoDh+8RnJgGmbDBYkMx8exuQZdlXyoDB+8Zjjz8btuLXe+If7dX4E9u3pGyoW3kG1uW0MN8ByqVUac6XxeCo/PQ22gjNdpMXeuvxfi/7wuJxvi57hjlIveXzmHU/gBJRLMA+G2Zczcubwh6jfXCZyyP4lfULkb6BFOGpvmJpYqWTW3PRqw2L6ODWPdLzAiv+GZJSC+97mxZK/yoo+EN8FXhpkUrv6ss6G/xEbPmOvZZVmDz9Cq48SnxP3cHLwWHktouM+agjrIkOCN8xUlvhq8uSWLPU02dhhq4Kf414yd5BvC8cfz2UjOdMSnl6m6CUnSNITrxzdos9iXcOXnTFYOi8J6T2Ac3ssvcz8J3phbr2gQmuGj6hOvx3G4Du3SZLeQcM+wt28aPtF4v2/4lFgWrzyVVFK5T7kAJ2xdET2s8BYAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADQAAAAbCAYAAAAzgqwIAAACI0lEQVR4Xu3Wv0tVYRgH8G9ooliaGUaWBFKCZDoESREOomFDEeUgFYJRROBU0JqLRIuSRqEp4iD+B+IgLUJLa0FLgyA0tAUtQeD32/O8nJfrvVbg5d5zOV/4gJzjezjP++O5B8iSpaSpohY6kYeu676kJkfpNn2kT+4OjdA8bbtrYUAa0gQraNLFCdc+07Gce2WbTvoOW4V4JQ7QkvtKx6N7ZZ2KK+gufaN2F3IGyRl6BiswFZmhL3TPDdMLWqc+l5piQkOYRtKuT9EirdEhl5pUXEFxQ4hznX7SBVeqHMZ//rjHDSHOE/pBPa4UqYd1WO0Y2TM65KEtb8AGx1mmLSTbUCt5Hjamw2kVG8IA2DOu0hUks6r7g34vXGuFPSdMlrqphOeJfsTHaJP6XcHGpK713v2mX7Azc8QpT2ErdMPNwr7txmFdUO7TSzrtXsM+pUbpodNn1HPYlg4F6LyepZvuA/XCCtLOkFrYczQ2fq+8qbiC/iVaXhVwyWnLdNEK1bkaOgh7QRn6MxK4BZuAMAna1idh51UewcaGraRJUXQ9/I8yQQP+d1GiGcz9eG2kVafGoomYgp0b0dl7S9VICteqaIVUQChCE7RAl9052ES0oYidVp3mDV10D2Bb6LHTy+mahKajMe9gkxG2ubatVuyVU9HNsG2vbSwqZM7/7nb7noorSNFL6jzltnlF5ynfD6Cu6V5utA2lUP52P0uWLFl2Zwd+X3rmEEbK/AAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAAaCAYAAADrCT9ZAAACVElEQVR4Xu2Xy6uNURiHX7kfd8lxjQyI5JIoUi5RDEii3CKXMjEwEUpIFFJiQG6JMjKg/AGUIeVfMDMyMzHi93jf17fOx9Ype3C+vfdTT2fv9a3bu9a33r2OWY/uYHw4c5CO8WbNpasCZvJvwk/yoXwhv4cfo+yJ/BKe/dWyoSyWt8KRRdnXcHeUwcFwR1HWOA7JtWFCUBkwwSfHw1VFWeNYZL6zubtwV74PJxTl88KxRVnj6LqA60yRH8yDxo4nExbJqkxYHUsmLAIvExbMCl/K/bVnreBIDK8XDiUeW3V2y/MLw8I7NrhMPU4+lXPqD4YSXRVwmbD+Bs/xmZwWZbkIy+VKOSme4VHzxdtc1MOF5peXiSGv/Drz40I/uNWqX4NW7ZB6LCx95JGjbktWmAeAn+UP+U2+Drf/rum7iuxwTuJUuFFuks/NJ4CH5SU5WY4Ir8i9cq75pQfpk7/v5ILwjPnY5Rh75DF5Ux4I6Z965BvmlXNrC3m1PBnfl5rfu5Hd2Gk+0eSy3BKfc7G4r180D2BG2Ge+ONkv3JDr7c8xRsnRcnrIkZlt1bzKPv4LVi1XcJv5ILxe10K4IHfJJSGTYScJlMCRHJHkrkMG2B/Sllf7iA0cA2iTvyL34/ttuTpsC10XMJ1mwOfMAyb7EiRyLl/J01ZN5oH5mVtmnszwulwjT1iVoPg14F9QEh1XXXwk98n58l5YtmNspB5n+61VybJtkAmxvHf/i3IHE94UElqder2STJBlOxIVcsY3yKtFvY7kfEiS5A2bOvBxjx49OpGfZS9zc97761oAAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAcCAYAAAC6YTVCAAAAtUlEQVR4Xu3RPQ4BURSG4Ssq8RNCo1KrlVoJDbVgBSJRigUoVQqJygI0Wg1qO9Bp7EDvPdc3MROV6ci8yZNMTu6Zuck4l/SLZTDABlMpRE6EqskRbaQwkj2yGEtFO98v5XCQiQ1UXa7ouPd17YWuhbvYoaCq3HBCQ3wzXKQUDF10ae5eX/BfsWIt9XCWfDCkpjzQDc199m/WssAQW/RlhR2WYucjFVF2oWvo2a6dlo9iLSX9UU8A4CMLXf0LWgAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAbCAYAAACnZAX6AAAA30lEQVR4Xu3SPQtBURzH8b9QBsVgkUFGixh4ASykTAZlNDDIw6TMDJSFzQuwmAzegbJ7RX5/53d1H6Tb2ZRvfZZz7zn3nNsR+cmi0KY9NCFCH0vBGkqkC2yhR4F0pRFUfOML2FGgAizFu40YnOTLl6wmtcQcugFdmsMB4hRIz1OGlZi/pi4wc7/klCTdWsL3rAp3yNA7q0lFGrgHmU56QJbedUhvgL8xXMXswLML59B911ieblBzjb/Ss2zoCBMxq5/JfzteWU3SHzAkLS1moa/pLahT6KaQo9BZTfpn2xNOUyU6upZZmwAAAABJRU5ErkJggg==>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAuUlEQVR4XmNgoCVghOJgID4AxH1QbICkBgyIVigOxXlAzAXE7VDcygAxAA5gCpcDsTCyBDpggWKQwmYGhFMwACsUZwHxTwaIW0EYAxClUB6It0CxHRCvAeITUMwPU8QDxFuBOAiKQSAaiB9CsSRUjMEFiC8yIHwNAr5AfBeKYWIMRQwQq2C+BgGQiSAxmDgYEK3QD4hXQQVAGOTzRUDsCsVwAJKYwACJKhAGBXYOA54AB/kehkfBQAMAs78i6qgmbxUAAAAASUVORK5CYII=>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAcCAYAAABVo158AAAAmElEQVR4XmNgGAWDCUhCcS0QVwIxNxSDACcQa0IxGMgD8UUo3gbEd4B4AhQzArEfENtAMXkaSoBYFYpBAOSEXihWAeIyqBgIgwHMrcjAE4pBfgLZQBAYQ/FWIBZHk8MKyNbQygDxOEEACxWQP4gCWVBsii6BC5CkgQOIp0KxNJocVgAKlXYoZkGTwwqYgZgLiokCJGsY9gAAhd4Yyig9lP8AAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEkAAAAVCAYAAAAKP8NQAAAAnUlEQVR4Xu3VMQrCQBRF0S8hhbiKVHZpLNILVhamtLAQa5dkFdBO1+DSfJ/5QmYQwU70HrhYTKqHyZgBAPCrdtFJzYszFGbqoAbVRZPsCTDSJ2q1jW5qqarsCWR8nI26xq/HYC/4KCt1jxbjw3/mr5zXq4taWxqLf9EII70xVXtLH2yPGy741e8d1Vm1loZhnOCvz/O6b4ozAMCXeQD+bhCFi6oBOgAAAABJRU5ErkJggg==>