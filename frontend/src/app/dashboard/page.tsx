'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { 
  MessageSquare, 
  FileText, 
  Calendar, 
  TrendingUp,
  Clock,
  Download,
  ChevronRight,
  CreditCard,
  Star,
  ArrowUpRight,
  Search,
  Briefcase,
  ShoppingCart,
  Users,
  Car,
  Building,
  BarChart3,
  Zap
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { PLANS } from '@/lib/constants';
import { LegalCategory } from '@/types';

// Mock data for demo
const mockUser = {
  name: 'Juan Pérez',
  email: 'juan@example.com',
  plan: 'basic' as const,
  avatar: 'JP',
};

const mockUsage = {
  queries: 15,
  limit: 20 as number | 'unlimited',
  documents: 8,
  documentsLimit: 'unlimited' as number | 'unlimited',
};

const mockSubscription = {
  plan: 'Básico',
  price: 29,
  renewalDate: new Date(Date.now() + 15 * 24 * 60 * 60 * 1000),
  status: 'active',
};

const mockConsultations = [
  { id: '1', title: 'Consulta sobre despido laboral', category: 'laboral' as LegalCategory, date: new Date(), messages: 5 },
  { id: '2', title: 'Reclamo a empresa de telefonía', category: 'consumidor' as LegalCategory, date: new Date(Date.now() - 86400000), messages: 3 },
  { id: '3', title: 'Pensión alimenticia para mi hijo', category: 'familia' as LegalCategory, date: new Date(Date.now() - 172800000), messages: 8 },
  { id: '4', title: 'Contrato de alquiler', category: 'civil' as LegalCategory, date: new Date(Date.now() - 259200000), messages: 4 },
  { id: '5', title: 'Papeleta de tránsito injusta', category: 'transito' as LegalCategory, date: new Date(Date.now() - 345600000), messages: 2 },
];

const mockDocuments = [
  { id: '1', name: 'Carta de reclamo - Claro', type: 'carta-reclamo', date: new Date(), status: 'completed' },
  { id: '2', name: 'Contrato de alquiler - Dpto Miraflores', type: 'contrato-alquiler', date: new Date(Date.now() - 86400000), status: 'completed' },
  { id: '3', name: 'Carta notarial - Cobro deuda', type: 'carta-notarial', date: new Date(Date.now() - 172800000), status: 'completed' },
];

const categoryIcons: Record<string, React.ElementType> = {
  laboral: Briefcase,
  consumidor: ShoppingCart,
  familia: Users,
  civil: FileText,
  transito: Car,
  empresas: Building,
};

export default function DashboardPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const currentPlan = PLANS.find(p => p.id === mockUser.plan);

  const getUsagePercentage = () => {
    if (mockUsage.limit === 'unlimited') return 0;
    return (mockUsage.queries / (mockUsage.limit as number)) * 100;
  };

  return (
    <div className="min-h-screen bg-muted/30">
      {/* Header */}
      <div className="bg-background border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-center gap-4">
              <Avatar className="h-16 w-16">
                <AvatarFallback className="bg-primary text-primary-foreground text-xl">
                  {mockUser.avatar}
                </AvatarFallback>
              </Avatar>
              <div>
                <h1 className="text-2xl font-bold">¡Hola, {mockUser.name.split(' ')[0]}!</h1>
                <p className="text-muted-foreground">Bienvenido a tu dashboard de LegalBot</p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" asChild>
                <Link href="/chat">
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Nueva Consulta
                </Link>
              </Button>
              <Button asChild className="gradient-primary">
                <Link href="/documentos">
                  <FileText className="w-4 h-4 mr-2" />
                  Generar Documento
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Queries Usage */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <MessageSquare className="w-4 h-4" />
                  Consultas este mes
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold">{mockUsage.queries}</span>
                  <span className="text-muted-foreground">/ {mockUsage.limit}</span>
                </div>
                <Progress value={getUsagePercentage()} className="mt-3 h-2" />
                <p className="text-xs text-muted-foreground mt-2">
                  Te quedan {(mockUsage.limit as number) - mockUsage.queries} consultas
                </p>
              </CardContent>
            </Card>
          </motion.div>

          {/* Documents */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <FileText className="w-4 h-4" />
                  Documentos generados
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-bold">{mockUsage.documents}</span>
                  <span className="text-muted-foreground">este mes</span>
                </div>
                <div className="flex items-center gap-2 mt-3 text-sm text-green-600">
                  <TrendingUp className="w-4 h-4" />
                  <span>+3 vs. mes anterior</span>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Plan */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <Star className="w-4 h-4" />
                  Tu plan actual
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center gap-2">
                  <span className="text-2xl font-bold">{currentPlan?.name}</span>
                  <Badge variant="secondary">S/. {currentPlan?.price}/mes</Badge>
                </div>
                <Button variant="link" className="p-0 h-auto mt-2" asChild>
                  <Link href="/precios" className="text-sm flex items-center gap-1">
                    <Zap className="w-3 h-3" />
                    Mejorar plan
                    <ArrowUpRight className="w-3 h-3" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Renewal */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardHeader className="pb-2">
                <CardDescription className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  Próxima renovación
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {mockSubscription.renewalDate.toLocaleDateString('es-PE', { 
                    day: 'numeric', 
                    month: 'short' 
                  })}
                </div>
                <p className="text-sm text-muted-foreground mt-1">
                  En {Math.ceil((mockSubscription.renewalDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24))} días
                </p>
                <Button variant="link" className="p-0 h-auto mt-2 text-sm" asChild>
                  <Link href="/configuracion/facturacion">
                    <CreditCard className="w-3 h-3 mr-1" />
                    Gestionar suscripción
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="consultations" className="space-y-6">
          <TabsList>
            <TabsTrigger value="consultations" className="gap-2">
              <MessageSquare className="w-4 h-4" />
              Consultas
            </TabsTrigger>
            <TabsTrigger value="documents" className="gap-2">
              <FileText className="w-4 h-4" />
              Documentos
            </TabsTrigger>
            <TabsTrigger value="stats" className="gap-2">
              <BarChart3 className="w-4 h-4" />
              Estadísticas
            </TabsTrigger>
          </TabsList>

          {/* Consultations Tab */}
          <TabsContent value="consultations">
            <Card>
              <CardHeader>
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div>
                    <CardTitle>Historial de Consultas</CardTitle>
                    <CardDescription>Tus conversaciones con LegalBot</CardDescription>
                  </div>
                  <div className="relative w-full md:w-64">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      placeholder="Buscar consultas..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockConsultations.map((consultation, index) => {
                    const Icon = categoryIcons[consultation.category] || MessageSquare;
                    return (
                      <motion.div
                        key={consultation.id}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.05 }}
                      >
                        <Link href={`/chat?id=${consultation.id}`}>
                          <div className="flex items-center gap-4 p-4 rounded-lg border hover:bg-muted/50 transition-colors group">
                            <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                              <Icon className="w-5 h-5 text-primary" />
                            </div>
                            <div className="flex-1 min-w-0">
                              <h4 className="font-medium truncate group-hover:text-primary transition-colors">
                                {consultation.title}
                              </h4>
                              <div className="flex items-center gap-3 text-sm text-muted-foreground">
                                <span>{consultation.date.toLocaleDateString('es-PE')}</span>
                                <span>•</span>
                                <span>{consultation.messages} mensajes</span>
                              </div>
                            </div>
                            <Badge variant="outline" className="hidden sm:flex">
                              {consultation.category}
                            </Badge>
                            <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                          </div>
                        </Link>
                      </motion.div>
                    );
                  })}
                </div>
              </CardContent>
              <CardFooter className="justify-center">
                <Button variant="ghost">
                  Ver todas las consultas
                  <ChevronRight className="w-4 h-4 ml-1" />
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>

          {/* Documents Tab */}
          <TabsContent value="documents">
            <Card>
              <CardHeader>
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div>
                    <CardTitle>Mis Documentos</CardTitle>
                    <CardDescription>Documentos legales generados</CardDescription>
                  </div>
                  <Button asChild>
                    <Link href="/documentos">
                      <FileText className="w-4 h-4 mr-2" />
                      Nuevo Documento
                    </Link>
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockDocuments.map((doc, index) => (
                    <motion.div
                      key={doc.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                      className="flex items-center gap-4 p-4 rounded-lg border"
                    >
                      <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
                        <FileText className="w-5 h-5 text-green-600" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-medium truncate">{doc.name}</h4>
                        <div className="flex items-center gap-3 text-sm text-muted-foreground">
                          <span>{doc.date.toLocaleDateString('es-PE')}</span>
                          <Badge variant="secondary" className="text-xs">
                            {doc.status === 'completed' ? 'Completado' : 'Pendiente'}
                          </Badge>
                        </div>
                      </div>
                      <Button variant="outline" size="sm">
                        <Download className="w-4 h-4 mr-2" />
                        Descargar
                      </Button>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Stats Tab */}
          <TabsContent value="stats">
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Categorías más consultadas</CardTitle>
                  <CardDescription>Distribución de tus consultas por área legal</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { category: 'Laboral', percentage: 45, color: 'bg-blue-500' },
                      { category: 'Consumidor', percentage: 28, color: 'bg-green-500' },
                      { category: 'Familia', percentage: 18, color: 'bg-purple-500' },
                      { category: 'Civil', percentage: 9, color: 'bg-orange-500' },
                    ].map((item) => (
                      <div key={item.category} className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                          <span>{item.category}</span>
                          <span className="font-medium">{item.percentage}%</span>
                        </div>
                        <div className="h-2 bg-muted rounded-full overflow-hidden">
                          <div 
                            className={`h-full ${item.color} rounded-full`}
                            style={{ width: `${item.percentage}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Actividad reciente</CardTitle>
                  <CardDescription>Tu uso de LegalBot en los últimos 30 días</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                          <MessageSquare className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium">Consultas realizadas</p>
                          <p className="text-sm text-muted-foreground">Últimos 30 días</p>
                        </div>
                      </div>
                      <span className="text-2xl font-bold">15</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
                          <FileText className="w-5 h-5 text-green-600" />
                        </div>
                        <div>
                          <p className="font-medium">Documentos generados</p>
                          <p className="text-sm text-muted-foreground">Últimos 30 días</p>
                        </div>
                      </div>
                      <span className="text-2xl font-bold">3</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-purple-100 flex items-center justify-center">
                          <Clock className="w-5 h-5 text-purple-600" />
                        </div>
                        <div>
                          <p className="font-medium">Tiempo promedio respuesta</p>
                          <p className="text-sm text-muted-foreground">Por consulta</p>
                        </div>
                      </div>
                      <span className="text-2xl font-bold">5s</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

