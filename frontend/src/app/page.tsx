'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { 
  Scale, 
  MessageSquare, 
  FileText, 
  Clock, 
  Shield, 
  Sparkles,
  ArrowRight,
  Check,
  Star,
  ChevronRight,
  Briefcase,
  ShoppingCart,
  Users,
  Car,
  Building,
  Zap
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { PLANS, LEGAL_CATEGORIES, TESTIMONIALS, FAQ } from '@/lib/constants';
import { useState } from 'react';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

const categoryIcons: Record<string, React.ElementType> = {
  Briefcase: Briefcase,
  ShoppingCart: ShoppingCart,
  Users: Users,
  FileText: FileText,
  Car: Car,
  Building: Building,
};

export default function HomePage() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <div className="overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center bg-gradient-to-br from-primary/5 via-background to-secondary/5">
        {/* Background decoration */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full blur-3xl" />
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-secondary/20 rounded-full blur-3xl" />
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-primary/5 to-secondary/5 rounded-full blur-3xl" />
        </div>

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mb-6"
            >
              <Badge variant="secondary" className="px-4 py-2 text-sm font-medium">
                <Sparkles className="w-4 h-4 mr-2" />
                Potenciado por Inteligencia Artificial
              </Badge>
            </motion.div>

            <motion.h1 
              className="font-display text-4xl md:text-6xl lg:text-7xl font-bold text-primary mb-6 text-balance"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              Asesoría Legal Inteligente
              <span className="block text-secondary mt-2">Respuestas en Segundos</span>
            </motion.h1>

            <motion.p 
              className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-2xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              Consulta legal 24/7 con IA. Sin citas. Sin esperas. 
              <span className="text-primary font-semibold"> Desde S/. 29/mes</span>
            </motion.p>

            <motion.div 
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Button size="lg" asChild className="gradient-primary text-lg px-8 py-6 h-auto">
                <Link href="/chat">
                  <MessageSquare className="w-5 h-5 mr-2" />
                  Prueba Gratis
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild className="text-lg px-8 py-6 h-auto">
                <Link href="/precios">
                  Ver Planes
                </Link>
              </Button>
            </motion.div>

            {/* Trust badges */}
            <motion.div 
              className="mt-12 flex flex-wrap items-center justify-center gap-8 text-muted-foreground"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5 text-green-500" />
                <span className="text-sm">Datos Seguros</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-blue-500" />
                <span className="text-sm">Disponible 24/7</span>
              </div>
              <div className="flex items-center gap-2">
                <Scale className="w-5 h-5 text-primary" />
                <span className="text-sm">Legislación Peruana</span>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Floating elements */}
        <motion.div 
          className="absolute bottom-10 left-10 hidden lg:block"
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        >
          <div className="glass rounded-2xl p-4 shadow-lg">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                <Check className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p className="font-medium text-sm">Consulta respondida</p>
                <p className="text-xs text-muted-foreground">hace 2 minutos</p>
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div 
          className="absolute top-32 right-10 hidden lg:block"
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        >
          <div className="glass rounded-2xl p-4 shadow-lg">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                <FileText className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p className="font-medium text-sm">Documento generado</p>
                <p className="text-xs text-muted-foreground">Carta Notarial</p>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold text-primary mb-4">
              ¿Por qué elegir LegalBot?
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Democratizamos el acceso a la justicia en el Perú con tecnología de punta
            </p>
          </motion.div>

          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            {[
              {
                icon: Zap,
                title: 'Respuestas Instantáneas',
                description: 'Obtén orientación legal en segundos, no en días',
                color: 'bg-yellow-100 text-yellow-600'
              },
              {
                icon: Clock,
                title: 'Disponible 24/7',
                description: 'Consulta cuando lo necesites, sin horarios de oficina',
                color: 'bg-blue-100 text-blue-600'
              },
              {
                icon: FileText,
                title: 'Documentos en Minutos',
                description: 'Genera contratos y cartas legales profesionales',
                color: 'bg-green-100 text-green-600'
              },
              {
                icon: Shield,
                title: 'Información Confiable',
                description: 'Basado en la legislación peruana vigente',
                color: 'bg-purple-100 text-purple-600'
              },
            ].map((benefit, index) => (
              <motion.div key={index} variants={fadeInUp}>
                <Card className="h-full hover:shadow-lg transition-shadow border-0 bg-background">
                  <CardHeader>
                    <div className={`w-14 h-14 rounded-2xl ${benefit.color} flex items-center justify-center mb-4`}>
                      <benefit.icon className="w-7 h-7" />
                    </div>
                    <CardTitle className="text-xl font-sans">{benefit.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">{benefit.description}</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Legal Categories Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold text-primary mb-4">
              Áreas Legales que Cubrimos
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Especialistas en las áreas más demandadas del derecho peruano
            </p>
          </motion.div>

          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            {LEGAL_CATEGORIES.map((category) => {
              const IconComponent = categoryIcons[category.icon] || FileText;
              return (
                <motion.div key={category.id} variants={fadeInUp}>
                  <Link href={`/chat?categoria=${category.id}`}>
                    <Card className="h-full hover:shadow-lg hover:border-primary/50 transition-all cursor-pointer group">
                      <CardHeader>
                        <div className="flex items-center gap-4">
                          <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                            <IconComponent className="w-6 h-6" />
                          </div>
                          <div>
                            <CardTitle className="text-lg font-sans group-hover:text-primary transition-colors">
                              {category.name}
                            </CardTitle>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-muted-foreground">{category.description}</p>
                      </CardContent>
                      <CardFooter>
                        <span className="text-primary font-medium text-sm flex items-center gap-1 group-hover:gap-2 transition-all">
                          Consultar ahora
                          <ChevronRight className="w-4 h-4" />
                        </span>
                      </CardFooter>
                    </Card>
                  </Link>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>

      {/* How it Works Section */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
              ¿Cómo Funciona?
            </h2>
            <p className="text-lg text-primary-foreground/80 max-w-2xl mx-auto">
              Tres simples pasos para resolver tus dudas legales
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {
                step: '01',
                title: 'Haz tu Consulta',
                description: 'Escribe tu pregunta legal en lenguaje sencillo. No necesitas términos técnicos.'
              },
              {
                step: '02',
                title: 'Recibe Orientación',
                description: 'Nuestra IA analiza tu caso y te brinda información legal actualizada con referencias.'
              },
              {
                step: '03',
                title: 'Toma Acción',
                description: 'Sigue los pasos recomendados o genera documentos listos para usar.'
              },
            ].map((item, index) => (
              <motion.div
                key={index}
                className="text-center relative"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
              >
                <div className="relative inline-block mb-6">
                  <span className="text-6xl font-bold text-secondary/20">{item.step}</span>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-16 h-16 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center font-bold text-xl">
                      {index + 1}
                    </div>
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-3 font-sans">{item.title}</h3>
                <p className="text-primary-foreground/70">{item.description}</p>
                
                {index < 2 && (
                  <div className="hidden md:block absolute top-12 left-full w-full h-0.5 bg-secondary/30 -translate-x-1/2" />
                )}
              </motion.div>
            ))}
          </div>

          <motion.div 
            className="text-center mt-12"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <Button size="lg" variant="secondary" asChild className="text-lg px-8">
              <Link href="/chat">
                Comenzar Ahora
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </Button>
          </motion.div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold text-primary mb-4">
              Lo que Dicen Nuestros Usuarios
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Miles de peruanos ya confían en LegalBot
            </p>
          </motion.div>

          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            {TESTIMONIALS.map((testimonial, index) => (
              <motion.div key={index} variants={fadeInUp}>
                <Card className="h-full">
                  <CardHeader>
                    <div className="flex items-center gap-3">
                      <Avatar>
                        <AvatarFallback className="bg-primary text-primary-foreground">
                          {testimonial.avatar}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <CardTitle className="text-base font-sans">{testimonial.name}</CardTitle>
                        <CardDescription>{testimonial.role}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex gap-1 mb-3">
                      {Array.from({ length: testimonial.rating }).map((_, i) => (
                        <Star key={i} className="w-4 h-4 fill-secondary text-secondary" />
                      ))}
                    </div>
                    <p className="text-muted-foreground text-sm italic">&ldquo;{testimonial.content}&rdquo;</p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-muted/30" id="precios">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold text-primary mb-4">
              Planes y Precios
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto mb-8">
              Elige el plan que mejor se adapte a tus necesidades
            </p>

            {/* Toggle mensual/anual */}
            <div className="flex items-center justify-center gap-4">
              <span className={`font-medium ${!isYearly ? 'text-primary' : 'text-muted-foreground'}`}>
                Mensual
              </span>
              <button
                onClick={() => setIsYearly(!isYearly)}
                className={`relative w-14 h-7 rounded-full transition-colors ${
                  isYearly ? 'bg-primary' : 'bg-muted'
                }`}
              >
                <span
                  className={`absolute top-1 w-5 h-5 rounded-full bg-white transition-transform ${
                    isYearly ? 'translate-x-8' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className={`font-medium ${isYearly ? 'text-primary' : 'text-muted-foreground'}`}>
                Anual
                <Badge variant="secondary" className="ml-2">-20%</Badge>
              </span>
            </div>
          </motion.div>

          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            {PLANS.map((plan) => (
              <motion.div key={plan.id} variants={fadeInUp}>
                <Card className={`h-full relative ${plan.popular ? 'border-2 border-primary shadow-xl' : ''}`}>
                  {plan.popular && (
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                      <Badge className="gradient-primary">Más Popular</Badge>
                    </div>
                  )}
                  <CardHeader className="text-center pb-2">
                    <CardTitle className="text-xl font-sans">{plan.name}</CardTitle>
                    <div className="mt-4">
                      <span className="text-4xl font-bold text-primary">
                        S/. {isYearly ? Math.round(plan.yearlyPrice / 12) : plan.price}
                      </span>
                      {plan.price > 0 && (
                        <span className="text-muted-foreground">/mes</span>
                      )}
                    </div>
                    {isYearly && plan.price > 0 && (
                      <p className="text-sm text-muted-foreground mt-1">
                        S/. {plan.yearlyPrice} facturado anualmente
                      </p>
                    )}
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-3">
                      {plan.features.map((feature) => (
                        <li key={feature} className="flex items-start gap-2">
                          <Check className="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
                          <span className="text-sm text-muted-foreground">{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                  <CardFooter>
                    <Button 
                      className={`w-full ${plan.popular ? 'gradient-primary' : ''}`}
                      variant={plan.popular ? 'default' : 'outline'}
                      asChild
                    >
                      <Link href={plan.price === 0 ? '/registro' : '/registro?plan=' + plan.id}>
                        {plan.price === 0 ? 'Comenzar Gratis' : 'Elegir Plan'}
                      </Link>
                    </Button>
                  </CardFooter>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold text-primary mb-4">
              Preguntas Frecuentes
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Resolvemos tus dudas sobre LegalBot
            </p>
          </motion.div>

          <motion.div 
            className="max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
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
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary to-primary/90 text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
              ¿Listo para Resolver tus Dudas Legales?
            </h2>
            <p className="text-xl text-primary-foreground/80 mb-8 max-w-2xl mx-auto">
              Únete a miles de peruanos que ya confían en LegalBot para sus consultas legales
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button size="lg" variant="secondary" asChild className="text-lg px-8">
                <Link href="/chat">
                  <MessageSquare className="w-5 h-5 mr-2" />
                  Comenzar Ahora - Es Gratis
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild className="text-lg px-8 bg-transparent border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary">
                <Link href="/precios">
                  Ver Planes
                </Link>
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
