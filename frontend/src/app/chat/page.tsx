'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Send,
  Plus,
  MessageSquare,
  Briefcase,
  ShoppingCart,
  Users,
  FileText,
  Car,
  Building,
  ThumbsUp,
  ThumbsDown,
  Copy,
  Check,
  Sparkles,
  Scale,
  ChevronRight,
  History,
  CreditCard,
  Menu,
  Loader2,
  AlertTriangle,
  BookOpen,
  Paperclip,
  Gavel,
  X
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Sheet, SheetContent } from '@/components/ui/sheet';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import ReactMarkdown from 'react-markdown';
import { LEGAL_CATEGORIES } from '@/lib/constants';
import { sendChatMessage, sendDemoMessage, uploadUserDocument } from '@/lib/api';
import { Message, LegalSource, LegalCategory } from '@/types';

const categoryIcons: Record<string, React.ElementType> = {
  laboral: Briefcase,
  consumidor: ShoppingCart,
  familia: Users,
  civil: FileText,
  transito: Car,
  empresas: Building,
  general: MessageSquare,
};

// Mock conversations for demo
const mockConversations = [
  { id: '1', title: 'Consulta sobre despido laboral', category: 'laboral' as LegalCategory, date: new Date() },
  { id: '2', title: 'Reclamo a Indecopi', category: 'consumidor' as LegalCategory, date: new Date(Date.now() - 86400000) },
  { id: '3', title: 'Pensión alimenticia', category: 'familia' as LegalCategory, date: new Date(Date.now() - 172800000) },
];

// Demo welcome message
const welcomeMessage: Message = {
  id: 'welcome',
  conversationId: 'new',
  role: 'assistant',
  content: `¡Hola! 👋 Soy **LegalBot**, tu asistente legal inteligente.

Estoy aquí para ayudarte con cualquier duda legal que tengas. Puedo orientarte sobre:

- 💼 **Derecho Laboral** - Despidos, liquidaciones, CTS, vacaciones
- 🛒 **Derecho del Consumidor** - Reclamos Indecopi, devoluciones
- 👨‍👩‍👧 **Derecho de Familia** - Pensión alimenticia, divorcios, tenencia
- 📝 **Derecho Civil** - Contratos, deudas, alquileres
- 🚗 **Derecho de Tránsito** - Papeletas, licencias
- 🏢 **Constitución de Empresas** - SAC, EIRL, RUC

**Escríbeme tu consulta o simplemente salúdame** 😊

Puedes preguntarme cualquier cosa, desde un simple "hola" hasta consultas legales complejas.`,
  createdAt: new Date(),
};

// Demo responses for different types of queries
const getDemoResponse = (query: string): { content: string; sources?: LegalSource[] } => {
  const queryLower = query.toLowerCase().trim();

  // Greetings
  if (queryLower.match(/^(hola|hey|hi|buenos días|buenas tardes|buenas noches|buenas|qué tal|como estas|cómo estás|saludos)/)) {
    return {
      content: `¡Hola! 😊 ¡Qué gusto saludarte!

Soy LegalBot, tu asistente legal. Estoy aquí para ayudarte con cualquier duda sobre leyes peruanas.

**¿En qué puedo orientarte hoy?** Puedes preguntarme sobre:
- Problemas laborales (despidos, liquidaciones, CTS)
- Reclamos como consumidor
- Temas de familia (pensión, divorcios)
- Contratos y documentos legales
- Y mucho más...

**Cuéntame, ¿qué necesitas saber?** 🤝`
    };
  }

  // Thanks
  if (queryLower.match(/(gracias|muchas gracias|te agradezco|thanks)/)) {
    return {
      content: `¡De nada! 😊 Ha sido un gusto ayudarte.

Si tienes más dudas legales en el futuro, no dudes en consultarme. Estoy aquí 24/7 para orientarte.

**¿Hay algo más en lo que pueda ayudarte?**

---
*Recuerda: Para casos complejos, siempre es recomendable consultar con un abogado colegiado.*`
    };
  }

  // Labor related
  if (queryLower.match(/(despido|despidieron|liquidación|cts|trabajo|laboral|vacaciones|sueldo|empleador)/)) {
    return {
      content: `## 📌 Resumen

Según la legislación laboral peruana, en caso de despido tienes derecho a una liquidación completa que incluye varios conceptos.

## 📋 Explicación Detallada

El despido puede ser de diferentes tipos, cada uno con consecuencias distintas:

1. **Despido Arbitrario:**
   - Indemnización: 1.5 remuneraciones por cada año trabajado
   - Tope máximo: 12 remuneraciones

2. **Tu liquidación debe incluir:**
   - ✅ CTS (Compensación por Tiempo de Servicios)
   - ✅ Vacaciones truncas (no gozadas)
   - ✅ Gratificaciones proporcionales (julio/diciembre)
   - ✅ Indemnización (si aplica)

## ⚖️ Base Legal

- **D.S. 003-97-TR** - Ley de Productividad y Competitividad Laboral
- **D.S. 001-97-TR** - Ley de Compensación por Tiempo de Servicios

## ✅ Pasos a Seguir

1. Solicita tu carta de cese por escrito
2. Exige el pago de tu liquidación (plazo: 48 horas)
3. Si no te pagan, presenta denuncia en **SUNAFIL**
4. Considera demanda ante el Poder Judicial

## ⚠️ ¿Cuándo Necesitas un Abogado?

- Si el monto supera S/. 10,000
- Si hay indicios de discriminación
- Si la empresa niega el despido arbitrario

---
*¿Te gustaría que genere una carta de solicitud de liquidación?*`,
      sources: [
        {
          text: 'La indemnización por despido arbitrario es equivalente a una remuneración y media ordinaria mensual por cada año completo de servicios con un máximo de doce (12) remuneraciones.',
          law: 'D.S. 003-97-TR',
          article: 'Artículo 38',
          category: 'laboral',
        },
        {
          text: 'El trabajador tiene derecho a recibir su CTS dentro de las 48 horas de producido el cese.',
          law: 'D.S. 001-97-TR',
          article: 'Artículo 3',
          category: 'laboral',
        },
      ]
    };
  }

  // Consumer related
  if (queryLower.match(/(indecopi|reclamo|devol|garantía|producto|defectuoso|consumidor|tienda|compré)/)) {
    return {
      content: `## 📌 Resumen

Como consumidor en Perú, tienes derecho a la reparación, reposición o devolución de tu dinero cuando un producto es defectuoso.

## 📋 Explicación Detallada

El Código de Protección al Consumidor te protege:

1. **Tus derechos como consumidor:**
   - ✅ Productos de calidad e idóneos
   - ✅ Información veraz sobre productos
   - ✅ Reparación o cambio de productos defectuosos
   - ✅ Devolución del dinero si no hay solución

2. **Plazos de garantía:**
   - Garantía legal: mínimo 1 año para productos duraderos
   - La tienda debe responder, no solo la marca

## ⚖️ Base Legal

- **Ley 29571** - Código de Protección y Defensa del Consumidor
- **Artículo 97** - Derecho a reparación o reposición

## ✅ Pasos a Seguir

1. Presenta tu reclamo en el **Libro de Reclamaciones** de la tienda
2. Espera respuesta en máximo 30 días
3. Si no te responden, presenta queja en **INDECOPI**
4. Puedes hacerlo online en: reclamos.indecopi.gob.pe

## ⚠️ Importante

El reclamo en Indecopi es **gratuito** y puedes hacerlo tú mismo sin necesidad de abogado.

---
*¿Quieres que te ayude a redactar una carta de reclamo?*`,
      sources: [
        {
          text: 'El proveedor es responsable por la idoneidad y calidad de los productos y servicios que ofrece.',
          law: 'Código de Protección al Consumidor',
          article: 'Artículo 18',
          category: 'consumidor',
        },
      ]
    };
  }

  // Family law
  if (queryLower.match(/(pensión|alimentos|divorcio|tenencia|hijo|hija|separación|custodia|alimenticia)/)) {
    return {
      content: `## 📌 Resumen

En temas de familia, la ley peruana protege especialmente a los menores de edad y establece obligaciones claras para los padres.

## 📋 Explicación Detallada

**Sobre Pensión de Alimentos:**

1. **¿Quién debe pasar pensión?**
   - Ambos padres tienen la obligación de mantener a sus hijos
   - Normalmente, quien no tiene la tenencia pasa pensión

2. **¿Cuánto corresponde?**
   - No hay un porcentaje fijo por ley
   - Se calcula según las necesidades del menor y posibilidades del obligado
   - Generalmente oscila entre 20% y 40% de los ingresos

3. **¿Hasta cuándo?**
   - Hasta los 18 años
   - O hasta los 28 si estudia con éxito

## ⚖️ Base Legal

- **Código Civil** - Artículos 472 al 487
- **Código de Niños y Adolescentes** - Artículos 92 al 97

## ✅ Pasos a Seguir

1. Intenta un acuerdo amistoso (conciliación)
2. Si no hay acuerdo, presenta demanda en el Juzgado de Paz o de Familia
3. Puedes solicitar asignación anticipada mientras dura el proceso

## ⚠️ ¿Cuándo Necesitas Abogado?

- La demanda de alimentos **sí requiere abogado**
- Defensoría del Pueblo ofrece asesoría gratuita
- También puedes acudir al CEM (Centro Emergencia Mujer)

---
*¿Quieres que genere un modelo de demanda de alimentos?*`,
      sources: [
        {
          text: 'Los alimentos comprenden lo necesario para el sustento, habitación, vestido, educación, instrucción y capacitación para el trabajo.',
          law: 'Código Civil',
          article: 'Artículo 472',
          category: 'familia',
        },
      ]
    };
  }

  // Civil - Contracts, rent
  if (queryLower.match(/(contrato|alquiler|arrendamiento|inquilino|propietario|deuda|préstamo|pagar)/)) {
    return {
      content: `## 📌 Resumen

Los contratos en Perú están regulados por el Código Civil. Es importante que todo acuerdo importante quede por escrito.

## 📋 Explicación Detallada

**Sobre contratos de alquiler:**

1. **Requisitos básicos:**
   - Identificación de las partes (DNI)
   - Descripción del inmueble
   - Monto de la renta y forma de pago
   - Duración del contrato
   - Garantía (usualmente 1-2 meses)

2. **Derechos del inquilino:**
   - Uso pacífico del inmueble
   - Que le devuelvan la garantía al final
   - No ser desalojado sin proceso legal

3. **Derechos del propietario:**
   - Cobrar la renta puntualmente
   - Que mantengan el inmueble en buen estado
   - Recuperar el inmueble al final del contrato

## ⚖️ Base Legal

- **Código Civil** - Artículos 1666 al 1712
- **Ley 30201** - Ley del Desalojo Notarial

## ✅ Pasos a Seguir

1. Siempre firma un contrato escrito
2. Legaliza las firmas en notaría (recomendable)
3. Si hay incumplimiento, envía carta notarial
4. Como último recurso, proceso de desalojo

## ⚠️ Importante

- El contrato de alquiler debe inscribirse en SUNAT
- Guarda todos los recibos de pago

---
*¿Quieres que genere un modelo de contrato de alquiler?*`,
      sources: [
        {
          text: 'El arrendamiento es el contrato por el cual el arrendador se obliga a ceder temporalmente al arrendatario el uso de un bien.',
          law: 'Código Civil',
          article: 'Artículo 1666',
          category: 'civil',
        },
      ]
    };
  }

  // Traffic
  if (queryLower.match(/(papeleta|multa|tránsito|licencia|brevete|sat|accidente|choqu)/)) {
    return {
      content: `## 📌 Resumen

Las papeletas de tránsito pueden impugnarse si consideras que fueron mal puestas. Tienes plazos específicos para hacerlo.

## 📋 Explicación Detallada

**Sobre papeletas:**

1. **Tipos de infracciones:**
   - Leves: desde S/. 88
   - Graves: desde S/. 220
   - Muy graves: desde S/. 440 hasta S/. 2,200

2. **Plazos para impugnar:**
   - 7 días hábiles desde la notificación
   - Se presenta ante la Municipalidad o SAT

3. **Cómo pagar:**
   - SAT Lima: sat.gob.pe
   - Municipalidades provinciales: en sus portales web

## ⚖️ Base Legal

- **D.S. 016-2009-MTC** - Texto Único Ordenado del Reglamento Nacional de Tránsito
- **Ley 27181** - Ley General de Transporte

## ✅ Pasos para Impugnar

1. Verifica en SAT/Municipalidad el detalle de la papeleta
2. Reúne pruebas (fotos, testigos, GPS)
3. Presenta recurso de reconsideración en 7 días
4. Si te rechazan, presenta apelación en 15 días

## ⚠️ Consejo

Si pagas dentro de los 7 primeros días, tienes **descuento del 50%** en muchas municipalidades.

---
*¿Necesitas ayuda para redactar un recurso de impugnación?*`
    };
  }

  // Business
  if (queryLower.match(/(empresa|negocio|sac|eirl|ruc|sunat|constituir|emprender)/)) {
    return {
      content: `## 📌 Resumen

Para constituir una empresa en Perú, tienes varias opciones según tus necesidades. Las más comunes son SAC y EIRL.

## 📋 Explicación Detallada

**Comparación de tipos de empresa:**

| Tipo | Socios | Capital mínimo | Responsabilidad |
|------|--------|----------------|-----------------|
| **EIRL** | 1 persona | No hay mínimo | Limitada |
| **SAC** | 2-20 socios | No hay mínimo | Limitada |
| **SRL** | 2-20 socios | No hay mínimo | Limitada |

**Pasos para constituir:**

1. **Reserva de nombre** en SUNARP (S/. 20, 3 días)
2. **Elaborar minuta** con abogado
3. **Escritura pública** en notaría
4. **Inscripción en SUNARP** (~S/. 40)
5. **Obtener RUC** en SUNAT (gratis)

## ⚖️ Base Legal

- **Ley 26887** - Ley General de Sociedades
- **D.L. 21621** - Ley de EIRL

## ✅ Costos Aproximados

- Notaría: S/. 300-500
- SUNARP: S/. 50-100
- Licencia municipal: varía
- **Total aproximado: S/. 500-1,000**

## 💡 Alternativa Rápida

**Empresa en 72 horas** con el SID-SUNARP (Sistema de Intermediación Digital): más rápido pero mismos costos.

---
*¿Quieres que genere los estatutos para una SAC?*`
    };
  }

  // General questions
  if (queryLower.match(/(qué puedes|que puedes|ayuda|ayúdame|que haces|qué haces|cómo funciona)/)) {
    return {
      content: `## ¡Claro! Te cuento qué puedo hacer 🤖

Soy **LegalBot**, un asistente legal con inteligencia artificial especializado en leyes peruanas.

### Puedo ayudarte con:

🔍 **Consultas Legales**
- Respondo preguntas sobre tus derechos
- Te explico leyes en lenguaje simple
- Te oriento sobre qué pasos seguir

📄 **Generación de Documentos**
- Cartas de reclamo
- Contratos de alquiler
- Cartas notariales
- Y más...

📚 **Áreas que domino:**
- Derecho Laboral
- Protección al Consumidor
- Derecho de Familia
- Derecho Civil
- Tránsito y Transporte
- Constitución de Empresas

### ⚠️ Lo que NO hago:
- No reemplazo a un abogado
- No puedo representarte en juicio
- No doy asesoría sobre casos penales graves

### 💬 ¿Cómo empezar?

Simplemente **escríbeme tu duda** con el mayor detalle posible. Por ejemplo:

*"Me despidieron sin motivo después de 3 años, ¿qué me corresponde?"*

---
**¡Adelante, pregunta lo que necesites!** 😊`
    };
  }

  // Default response
  return {
    content: `## 📌 Entendido

Gracias por tu consulta. Para darte una orientación más precisa, necesitaría algunos detalles adicionales.

**Mientras tanto, te comento:**

Puedo ayudarte con temas como:
- 💼 Problemas laborales (despidos, liquidaciones, CTS)
- 🛒 Reclamos de consumidor (Indecopi, garantías)
- 👨‍👩‍👧 Derecho de familia (pensión alimenticia, divorcios)
- 📝 Contratos (alquiler, compraventa, servicios)
- 🚗 Temas de tránsito (papeletas, licencias)
- 🏢 Constitución de empresas (SAC, EIRL)

**¿Podrías darme más detalles sobre tu situación?**

Por ejemplo:
- ¿Cuál es el problema específico?
- ¿Cuándo ocurrió?
- ¿Qué has intentado hacer hasta ahora?

---
*Recuerda: Soy una herramienta informativa. Para casos complejos, te recomiendo consultar con un abogado.*`
  };
};

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([welcomeMessage]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<LegalCategory | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [conversations] = useState(mockConversations);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [authToken] = useState<string | null>(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  });
  const [userContext, setUserContext] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [chatMode, setChatMode] = useState<'advisor' | 'hearing'>('advisor');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      conversationId: currentConversationId || 'current',
      role: 'user',
      content: input.trim(),
      createdAt: new Date(),
    };

    const queryText = input.trim();
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Keep a local copy of context and mode for this specific send
    const activeContext = userContext || undefined;
    const activeMode = chatMode;

    try {
      let assistantMessage: Message;

      if (authToken) {
        // Authenticated User -> Full Chat API
        const response = await sendChatMessage(
          queryText,
          currentConversationId || undefined,
          authToken,
          activeContext,
          activeMode
        );

        // Update conversation ID for follow-up messages
        if (response.conversation?.id) {
          setCurrentConversationId(response.conversation.id);
        }

        assistantMessage = {
          id: response.message.id,
          conversationId: response.conversation.id,
          role: 'assistant',
          content: response.message.content,
          sources: response.message.sources as LegalSource[] | undefined,
          createdAt: new Date(response.message.created_at),
          mode: activeMode,
        };
      } else {
        // Guest User -> Demo API (Real AI, no DB saving)
        // This fixes the "Server Unavailable" error when testing without login
        const response = await sendDemoMessage(queryText, activeContext, activeMode);

        assistantMessage = {
          id: Date.now().toString(),
          conversationId: 'guest-demo',
          role: 'assistant',
          content: response.content,
          sources: response.sources as LegalSource[] | undefined,
          createdAt: new Date(),
          mode: activeMode,
        };
      }

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Error calling AI backend:', error);
      // Fallback to demo response if API fails
      const demoResponse = getDemoResponse(queryText);

      let errorMessage = 'Error de conexión con el servidor. (Intenta reiniciar el backend)';
      if (error?.message) {
        errorMessage = `Error: ${error.message}`;
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        conversationId: 'current',
        role: 'assistant',
        content: demoResponse.content + `\n\n---\n*⚠️ ${errorMessage}*`,
        sources: demoResponse.sources,
        createdAt: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      alert('Solo se admiten archivos PDF');
      return;
    }

    setIsUploading(true);
    try {
      const result = await uploadUserDocument(file, authToken || undefined);
      setUserContext(result.extracted_text);
      setUploadedFileName(result.filename || file.name);
    } catch (error: any) {
      console.error('Error uploading document:', error);
      alert(error.message || 'Error al subir el documento');
    } finally {
      setIsUploading(false);
    }
  };

  const removeDocument = () => {
    setUserContext(null);
    setUploadedFileName(null);
  };

  const handleCopy = async (content: string, id: string) => {
    await navigator.clipboard.writeText(content);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleCategoryClick = (categoryId: LegalCategory) => {
    setSelectedCategory(categoryId);
    const category = LEGAL_CATEGORIES.find(c => c.id === categoryId);
    if (category) {
      setInput(`Tengo una consulta sobre ${category.name.toLowerCase()}: `);
      textareaRef.current?.focus();
    }
  };

  const handleNewConversation = () => {
    setMessages([welcomeMessage]);
    setSelectedCategory(null);
    setInput('');
    setCurrentConversationId(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b">
        <Button onClick={handleNewConversation} className="w-full gradient-primary">
          <Plus className="w-4 h-4 mr-2" />
          Nueva Consulta
        </Button>
      </div>

      {/* Usage */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-muted-foreground">Consultas este mes</span>
          <Badge variant="secondary">2/3</Badge>
        </div>
        <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
          <div className="h-full w-2/3 bg-primary rounded-full" />
        </div>
        <Button variant="link" className="mt-2 p-0 h-auto text-sm" asChild>
          <a href="/precios">
            <CreditCard className="w-3 h-3 mr-1" />
            Obtener más consultas
          </a>
        </Button>
      </div>

      {/* Categories */}
      <div className="p-4 border-b">
        <h4 className="text-sm font-medium mb-3 text-muted-foreground">Categorías</h4>
        <div className="space-y-1">
          {LEGAL_CATEGORIES.map((cat) => {
            const Icon = categoryIcons[cat.id] || MessageSquare;
            return (
              <button
                key={cat.id}
                onClick={() => handleCategoryClick(cat.id)}
                className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors hover:bg-muted ${selectedCategory === cat.id ? 'bg-primary/10 text-primary' : 'text-muted-foreground'
                  }`}
              >
                <Icon className="w-4 h-4" />
                {cat.name}
              </button>
            );
          })}
        </div>
      </div>

      {/* History */}
      <div className="flex-1 overflow-hidden">
        <div className="p-4 pb-2">
          <h4 className="text-sm font-medium text-muted-foreground flex items-center gap-2">
            <History className="w-4 h-4" />
            Historial
          </h4>
        </div>
        <ScrollArea className="h-full px-4 pb-4">
          <div className="space-y-2">
            {conversations.map((conv) => {
              const Icon = categoryIcons[conv.category] || MessageSquare;
              return (
                <button
                  key={conv.id}
                  className="w-full text-left p-3 rounded-lg hover:bg-muted transition-colors group"
                >
                  <div className="flex items-start gap-2">
                    <Icon className="w-4 h-4 mt-0.5 text-muted-foreground" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium truncate group-hover:text-primary transition-colors">
                        {conv.title}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {conv.date.toLocaleDateString('es-PE')}
                      </p>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </ScrollArea>
      </div>
    </div>
  );

  return (
    <div className="h-[calc(100vh-4rem)] flex">
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex w-80 border-r bg-muted/30 flex-col">
        <SidebarContent />
      </aside>

      {/* Mobile Sidebar */}
      <Sheet open={sidebarOpen} onOpenChange={setSidebarOpen}>
        <SheetContent side="left" className="w-80 p-0">
          <SidebarContent />
        </SheetContent>
      </Sheet>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Chat Header */}
        <div className="h-14 border-b flex items-center justify-between px-4">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="w-5 h-5" />
            </Button>
            <div className="flex items-center gap-2">
              <Scale className={`w-5 h-5 ${chatMode === 'hearing' ? 'text-red-500' : 'text-primary'}`} />
              <span className="font-semibold">
                {chatMode === 'hearing' ? 'Simulación de Audiencia' : 'LegalBot'}
              </span>
              <AnimatePresence mode="wait">
                <motion.div
                  key={chatMode}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                >
                  <Badge variant={chatMode === 'hearing' ? 'destructive' : 'secondary'} className="text-xs">
                    {chatMode === 'hearing' ? <Gavel className="w-3 h-3 mr-1" /> : <Sparkles className="w-3 h-3 mr-1" />}
                    {chatMode === 'hearing' ? 'MODO JUEZ' : 'IA ASESOR'}
                  </Badge>
                </motion.div>
              </AnimatePresence>
            </div>
          </div>
          <Button variant="ghost" size="sm" asChild>
            <a href="/documentos">
              <FileText className="w-4 h-4 mr-2" />
              Generar Documento
            </a>
          </Button>
        </div>

        {/* Messages */}
        <ScrollArea className="flex-1 p-4">
          <div className="max-w-3xl mx-auto space-y-6">
            <AnimatePresence>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                  className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  {message.role === 'assistant' && (
                    <Avatar className={`w-8 h-8 shrink-0 ${message.mode === 'hearing' ? 'ring-2 ring-red-500' : ''}`}>
                      <AvatarFallback className={`${message.mode === 'hearing' ? 'bg-red-600' : 'bg-primary'} text-white`}>
                        {message.mode === 'hearing' ? <Gavel className="w-4 h-4" /> : <Scale className="w-4 h-4" />}
                      </AvatarFallback>
                    </Avatar>
                  )}

                  <div className={`max-w-[85%] ${message.role === 'user' ? 'order-1' : ''}`}>
                    <div
                      className={`rounded-2xl px-4 py-3 ${message.role === 'user'
                        ? 'bg-primary text-primary-foreground rounded-br-md'
                        : message.mode === 'hearing'
                          ? 'bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900/30 rounded-bl-md'
                          : 'bg-muted rounded-bl-md'
                        }`}
                    >
                      {message.role === 'assistant' && message.mode === 'hearing' && (
                        <div className="flex items-center gap-1.5 mb-1.5 text-red-600 dark:text-red-400 font-bold text-[10px] tracking-wider uppercase">
                          <Gavel className="w-3 h-3" />
                          Magistrado / Juez
                        </div>
                      )}
                      {message.role === 'assistant' ? (
                        <div className="markdown-content prose prose-sm dark:prose-invert max-w-none">
                          <ReactMarkdown>{message.content}</ReactMarkdown>
                        </div>
                      ) : (
                        <p>{message.content}</p>
                      )}
                    </div>

                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-2">
                        <Accordion type="single" collapsible className="w-full">
                          <AccordionItem value="sources" className="border-0">
                            <AccordionTrigger className="py-2 text-sm text-muted-foreground hover:no-underline">
                              <div className="flex items-center gap-2">
                                <BookOpen className="w-4 h-4" />
                                Ver fuentes legales ({message.sources.length})
                              </div>
                            </AccordionTrigger>
                            <AccordionContent>
                              <div className="space-y-2">
                                {message.sources.map((source, idx) => (
                                  <Card key={idx} className="bg-muted/50">
                                    <CardContent className="p-3">
                                      <div className="flex items-center gap-2 mb-2">
                                        <Badge variant="outline" className="text-xs">
                                          {source.law}
                                        </Badge>
                                        <Badge variant="secondary" className="text-xs">
                                          {source.article}
                                        </Badge>
                                      </div>
                                      <p className="text-sm text-muted-foreground italic">
                                        &ldquo;{source.text}&rdquo;
                                      </p>
                                    </CardContent>
                                  </Card>
                                ))}
                              </div>
                            </AccordionContent>
                          </AccordionItem>
                        </Accordion>
                      </div>
                    )}

                    {/* Actions */}
                    {message.role === 'assistant' && message.id !== 'welcome' && (
                      <div className="flex items-center gap-1 mt-2">
                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-8 w-8 text-muted-foreground hover:text-green-500"
                              >
                                <ThumbsUp className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Útil</TooltipContent>
                          </Tooltip>
                        </TooltipProvider>

                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-8 w-8 text-muted-foreground hover:text-red-500"
                              >
                                <ThumbsDown className="w-4 h-4" />
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>No útil</TooltipContent>
                          </Tooltip>
                        </TooltipProvider>

                        <TooltipProvider>
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button
                                variant="ghost"
                                size="icon"
                                className="h-8 w-8 text-muted-foreground"
                                onClick={() => handleCopy(message.content, message.id)}
                              >
                                {copiedId === message.id ? (
                                  <Check className="w-4 h-4 text-green-500" />
                                ) : (
                                  <Copy className="w-4 h-4" />
                                )}
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>Copiar</TooltipContent>
                          </Tooltip>
                        </TooltipProvider>
                      </div>
                    )}
                  </div>

                  {message.role === 'user' && (
                    <Avatar className="w-8 h-8 shrink-0 order-2">
                      <AvatarFallback className="bg-secondary text-secondary-foreground">
                        U
                      </AvatarFallback>
                    </Avatar>
                  )}
                </motion.div>
              ))}

              {/* Loading indicator */}
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3"
                >
                  <Avatar className="w-8 h-8 shrink-0">
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      <Scale className="w-4 h-4" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-muted rounded-2xl rounded-bl-md px-4 py-3">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">Analizando tu consulta...</span>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Quick category buttons on welcome */}
            {messages.length === 1 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="grid grid-cols-2 md:grid-cols-3 gap-3 mt-6"
              >
                {LEGAL_CATEGORIES.map((category) => {
                  const Icon = categoryIcons[category.id] || MessageSquare;
                  return (
                    <Card
                      key={category.id}
                      className="cursor-pointer hover:border-primary/50 hover:shadow-md transition-all group"
                      onClick={() => handleCategoryClick(category.id)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                            <Icon className="w-5 h-5" />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="font-medium text-sm truncate">{category.name}</p>
                          </div>
                          <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-primary transition-colors" />
                        </div>
                      </CardContent>
                    </Card>
                  );
                })}
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Disclaimer */}
        <div className="px-4 py-2 text-center">
          <p className="text-xs text-muted-foreground flex items-center justify-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            LegalBot proporciona información orientativa. Para casos complejos, consulta con un abogado.
          </p>
        </div>

        {/* Input Area */}
        <div className="border-t p-4 bg-background">
          <div className="max-w-3xl mx-auto">
            {/* File Info / User Context Badge */}
            <AnimatePresence>
              {uploadedFileName && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-2"
                >
                  <Badge variant="outline" className="flex items-center gap-2 py-1.5 px-3 bg-primary/5 border-primary/20">
                    <Paperclip className="w-3 h-3 text-primary" />
                    <span className="text-xs font-medium max-w-[200px] truncate">{uploadedFileName}</span>
                    <button onClick={removeDocument} className="hover:text-destructive transition-colors">
                      <X className="w-3 h-3" />
                    </button>
                  </Badge>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="relative flex items-end gap-2">
              {/* Hidden File Input */}
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept=".pdf"
                onChange={handleFileUpload}
              />

              <div className="flex flex-col gap-2">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="outline"
                        size="icon"
                        className={`shrink-0 transition-all duration-300 ${chatMode === 'hearing'
                          ? 'bg-red-600 text-white border-red-600 hover:bg-red-700 shadow-lg shadow-red-500/20 scale-110'
                          : 'hover:border-primary hover:text-primary'
                          }`}
                        onClick={() => {
                          const newMode = chatMode === 'advisor' ? 'hearing' : 'advisor';
                          setChatMode(newMode);
                        }}
                      >
                        <Gavel className="w-5 h-5" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      {chatMode === 'advisor' ? 'Activar Simulación de Audiencia' : 'Regresar a Modo Asesor'}
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="outline"
                        size="icon"
                        className="shrink-0"
                        disabled={isUploading || !!uploadedFileName}
                        onClick={() => fileInputRef.current?.click()}
                      >
                        {isUploading ? (
                          <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                          <Paperclip className="w-5 h-5" />
                        )}
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Documento de Contexto (PDF)</TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>

              <div className="flex-1 relative">
                <Textarea
                  ref={textareaRef}
                  placeholder="Escribe tu consulta legal aquí..."
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  className="min-h-[52px] max-h-32 pr-12 resize-none"
                  rows={1}
                />
                <div className="absolute right-2 bottom-2 text-xs text-muted-foreground">
                  {input.length}/2000
                </div>
              </div>
              <Button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                className="gradient-primary h-[52px] w-[52px] shrink-0"
              >
                {isLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <Send className="w-5 h-5" />
                )}
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mt-2 text-center">
              Presiona Enter para enviar, Shift + Enter para nueva línea
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

