'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Check, Sparkles, MessageSquare, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { PLANS, FAQ } from '@/lib/constants';

export default function PreciosPage() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <div className="min-h-screen">
      {/* Header */}
      <section className="py-20 bg-gradient-to-br from-primary/5 via-background to-secondary/5">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Badge variant="secondary" className="mb-4">
              <Sparkles className="w-4 h-4 mr-2" />
              Sin compromisos • Cancela cuando quieras
            </Badge>
            <h1 className="font-display text-4xl md:text-5xl font-bold text-primary mb-4">
              Planes y Precios
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
              Elige el plan que mejor se adapte a tus necesidades legales. 
              Todos incluyen acceso a nuestra IA legal especializada en legislación peruana.
            </p>

            {/* Toggle */}
            <div className="flex items-center justify-center gap-4 mb-12">
              <span className={`font-medium ${!isYearly ? 'text-primary' : 'text-muted-foreground'}`}>
                Mensual
              </span>
              <button
                onClick={() => setIsYearly(!isYearly)}
                className={`relative w-16 h-8 rounded-full transition-colors ${
                  isYearly ? 'bg-primary' : 'bg-muted'
                }`}
              >
                <span
                  className={`absolute top-1 w-6 h-6 rounded-full bg-white shadow transition-transform ${
                    isYearly ? 'translate-x-9' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className={`font-medium flex items-center gap-2 ${isYearly ? 'text-primary' : 'text-muted-foreground'}`}>
                Anual
                <Badge className="bg-green-100 text-green-700 hover:bg-green-100">
                  Ahorra 20%
                </Badge>
              </span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Plans Grid */}
      <section className="py-12 -mt-8">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
            {PLANS.map((plan, index) => (
              <motion.div
                key={plan.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className={`h-full relative flex flex-col ${
                  plan.popular 
                    ? 'border-2 border-primary shadow-xl scale-105 z-10' 
                    : 'hover:shadow-lg transition-shadow'
                }`}>
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                      <Badge className="gradient-primary px-4 py-1">
                        <Sparkles className="w-3 h-3 mr-1" />
                        Más Popular
                      </Badge>
                    </div>
                  )}
                  
                  <CardHeader className="text-center pt-8">
                    <CardTitle className="text-2xl font-sans">{plan.name}</CardTitle>
                    <div className="mt-4">
                      {plan.price === 0 ? (
                        <span className="text-4xl font-bold text-primary">Gratis</span>
                      ) : (
                        <>
                          <span className="text-4xl font-bold text-primary">
                            S/. {isYearly ? Math.round(plan.yearlyPrice / 12) : plan.price}
                          </span>
                          <span className="text-muted-foreground">/mes</span>
                        </>
                      )}
                    </div>
                    {isYearly && plan.price > 0 && (
                      <div className="mt-2">
                        <p className="text-sm text-muted-foreground">
                          S/. {plan.yearlyPrice} al año
                        </p>
                        <p className="text-sm text-green-600 font-medium">
                          Ahorras S/. {plan.price * 12 - plan.yearlyPrice}
                        </p>
                      </div>
                    )}
                  </CardHeader>
                  
                  <CardContent className="flex-1">
                    <div className="space-y-3 mb-6">
                      <div className="flex items-center gap-2 text-sm font-medium">
                        <MessageSquare className="w-4 h-4 text-primary" />
                        {plan.queriesLimit === 'unlimited' 
                          ? 'Consultas ilimitadas' 
                          : `${plan.queriesLimit} consultas/mes`}
                      </div>
                    </div>
                    
                    <ul className="space-y-3">
                      {plan.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-start gap-2">
                          <Check className="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
                          <span className="text-sm text-muted-foreground">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  
                  <CardFooter className="pt-0">
                    <Button 
                      className={`w-full ${plan.popular ? 'gradient-primary' : ''}`}
                      variant={plan.popular ? 'default' : 'outline'}
                      size="lg"
                      asChild
                    >
                      <Link href={`/registro${plan.price > 0 ? `?plan=${plan.id}` : ''}`}>
                        {plan.price === 0 ? 'Comenzar Gratis' : 'Elegir Plan'}
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </Link>
                    </Button>
                  </CardFooter>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Comparison Table */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-3xl font-bold text-center text-primary mb-12">
            Comparación Detallada
          </h2>
          
          <div className="max-w-5xl mx-auto overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-4 px-4 font-medium">Característica</th>
                  {PLANS.map((plan) => (
                    <th key={plan.id} className="text-center py-4 px-4 font-medium">
                      {plan.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr className="border-b">
                  <td className="py-4 px-4">Consultas por mes</td>
                  <td className="text-center py-4 px-4">3</td>
                  <td className="text-center py-4 px-4">20</td>
                  <td className="text-center py-4 px-4">Ilimitadas</td>
                  <td className="text-center py-4 px-4">Ilimitadas</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Documentos básicos</td>
                  <td className="text-center py-4 px-4">1</td>
                  <td className="text-center py-4 px-4">Ilimitados</td>
                  <td className="text-center py-4 px-4">Ilimitados</td>
                  <td className="text-center py-4 px-4">Ilimitados</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Documentos complejos</td>
                  <td className="text-center py-4 px-4">—</td>
                  <td className="text-center py-4 px-4">—</td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Historial guardado</td>
                  <td className="text-center py-4 px-4">—</td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Sin marca de agua</td>
                  <td className="text-center py-4 px-4">—</td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                  <td className="text-center py-4 px-4"><Check className="w-5 h-5 text-green-500 mx-auto" /></td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Videollamada con abogado</td>
                  <td className="text-center py-4 px-4">—</td>
                  <td className="text-center py-4 px-4">—</td>
                  <td className="text-center py-4 px-4">30 min/mes</td>
                  <td className="text-center py-4 px-4">60 min/mes</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Usuarios</td>
                  <td className="text-center py-4 px-4">1</td>
                  <td className="text-center py-4 px-4">1</td>
                  <td className="text-center py-4 px-4">1</td>
                  <td className="text-center py-4 px-4">Hasta 20</td>
                </tr>
                <tr className="border-b">
                  <td className="py-4 px-4">Soporte</td>
                  <td className="text-center py-4 px-4">Email</td>
                  <td className="text-center py-4 px-4">Email</td>
                  <td className="text-center py-4 px-4">Prioritario</td>
                  <td className="text-center py-4 px-4">24/7</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="font-display text-3xl font-bold text-center text-primary mb-4">
            Preguntas Frecuentes
          </h2>
          <p className="text-center text-muted-foreground mb-12 max-w-2xl mx-auto">
            ¿Tienes dudas sobre nuestros planes? Aquí respondemos las preguntas más comunes.
          </p>
          
          <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible className="w-full">
              {FAQ.map((faq, index) => (
                <AccordionItem key={index} value={`item-${index}`}>
                  <AccordionTrigger className="text-left font-medium hover:text-primary">
                    {faq.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-muted-foreground">
                    {faq.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="font-display text-3xl font-bold mb-4">
            ¿Listo para comenzar?
          </h2>
          <p className="text-xl text-primary-foreground/80 mb-8 max-w-2xl mx-auto">
            Únete a miles de peruanos que ya confían en LegalBot para sus consultas legales.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" asChild className="text-lg px-8">
              <Link href="/registro">
                Comenzar Gratis
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              asChild 
              className="text-lg px-8 bg-transparent border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary"
            >
              <Link href="/chat">
                Probar Chat
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}

