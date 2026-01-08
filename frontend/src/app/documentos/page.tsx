'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';
import { 
  FileText, 
  ScrollText, 
  Home, 
  Handshake, 
  UserMinus, 
  Building2, 
  FileCheck, 
  Baby,
  Search,
  Filter,
  ArrowLeft,
  ArrowRight,
  Download,
  Eye,
  Loader2,
  CreditCard,
  Lock,
  Sparkles,
  AlertTriangle
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { DOCUMENT_TEMPLATES, LEGAL_CATEGORIES } from '@/lib/constants';
import { DocumentTemplate, DocumentField } from '@/types';

const documentIcons: Record<string, React.ElementType> = {
  FileText: FileText,
  ScrollText: ScrollText,
  Home: Home,
  HandshakeIcon: Handshake,
  UserMinus: UserMinus,
  Building2: Building2,
  FileCheck: FileCheck,
  Baby: Baby,
};

export default function DocumentosPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedTemplate, setSelectedTemplate] = useState<DocumentTemplate | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<Record<string, string>>({});
  const [isGenerating, setIsGenerating] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [showPayment, setShowPayment] = useState(false);

  const filteredTemplates = DOCUMENT_TEMPLATES.filter((template) => {
    const matchesSearch = template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      template.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const handleTemplateSelect = (template: DocumentTemplate) => {
    setSelectedTemplate(template);
    setCurrentStep(1);
    setFormData({});
  };

  const handleInputChange = (fieldName: string, value: string) => {
    setFormData(prev => ({ ...prev, [fieldName]: value }));
  };

  const getFieldsForStep = (step: number): DocumentField[] => {
    if (!selectedTemplate) return [];
    const fieldsPerStep = 3;
    const startIndex = (step - 1) * fieldsPerStep;
    return selectedTemplate.fields.slice(startIndex, startIndex + fieldsPerStep);
  };

  const totalSteps = selectedTemplate ? Math.ceil(selectedTemplate.fields.length / 3) + 1 : 0;

  const canProceed = () => {
    if (currentStep === 0) return true;
    if (currentStep > totalSteps - 1) return true;
    
    const currentFields = getFieldsForStep(currentStep);
    return currentFields.every(field => !field.required || formData[field.name]?.trim());
  };

  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(prev => prev + 1);
    } else if (currentStep === totalSteps - 1) {
      // Preview step
      setShowPreview(true);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1);
    } else {
      setSelectedTemplate(null);
      setCurrentStep(0);
    }
  };

  const handleGenerate = () => {
    if (selectedTemplate?.price !== 'free' && selectedTemplate?.price !== 'included') {
      setShowPayment(true);
    } else {
      generateDocument();
    }
  };

  const generateDocument = () => {
    setIsGenerating(true);
    setShowPayment(false);
    
    // Simulate document generation
    setTimeout(() => {
      setIsGenerating(false);
      // In real app, this would trigger download
      alert('¡Documento generado exitosamente! En una implementación real, se descargaría el PDF.');
    }, 2000);
  };

  const getPriceDisplay = (price: number | 'free' | 'included') => {
    if (price === 'free') return { text: 'Gratis', color: 'bg-green-100 text-green-700' };
    if (price === 'included') return { text: 'Incluido', color: 'bg-blue-100 text-blue-700' };
    return { text: `S/. ${price}`, color: 'bg-secondary/20 text-secondary-foreground' };
  };

  const renderField = (field: DocumentField) => {
    const value = formData[field.name] || '';

    switch (field.type) {
      case 'textarea':
        return (
          <Textarea
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            rows={4}
          />
        );
      case 'select':
        return (
          <Select value={value} onValueChange={(v) => handleInputChange(field.name, v)}>
            <SelectTrigger>
              <SelectValue placeholder="Selecciona una opción" />
            </SelectTrigger>
            <SelectContent>
              {field.options?.map((option) => (
                <SelectItem key={option} value={option}>
                  {option}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        );
      case 'date':
        return (
          <Input
            type="date"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
          />
        );
      case 'number':
        return (
          <Input
            type="number"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={field.placeholder}
          />
        );
      default:
        return (
          <Input
            type="text"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={field.placeholder}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-muted/30">
      {/* Header */}
      <div className="bg-primary text-primary-foreground py-12">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl">
            <h1 className="font-display text-3xl md:text-4xl font-bold mb-4">
              Generador de Documentos Legales
            </h1>
            <p className="text-lg text-primary-foreground/80">
              Crea contratos, cartas notariales y documentos legales profesionales en minutos.
              Basados en la legislación peruana vigente.
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <AnimatePresence mode="wait">
          {!selectedTemplate ? (
            // Document Grid View
            <motion.div
              key="grid"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              {/* Filters */}
              <div className="flex flex-col md:flex-row gap-4 mb-8">
                <div className="relative flex-1">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Buscar documentos..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                  <SelectTrigger className="w-full md:w-[200px]">
                    <Filter className="w-4 h-4 mr-2" />
                    <SelectValue placeholder="Categoría" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todas las categorías</SelectItem>
                    {LEGAL_CATEGORIES.map((cat) => (
                      <SelectItem key={cat.id} value={cat.id}>
                        {cat.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Documents Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {filteredTemplates.map((template, index) => {
                  const Icon = documentIcons[template.icon] || FileText;
                  const priceInfo = getPriceDisplay(template.price);
                  const category = LEGAL_CATEGORIES.find(c => c.id === template.category);

                  return (
                    <motion.div
                      key={template.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.05 }}
                    >
                      <Card 
                        className="h-full cursor-pointer hover:shadow-lg hover:border-primary/50 transition-all group"
                        onClick={() => handleTemplateSelect(template)}
                      >
                        <CardHeader>
                          <div className="flex items-start justify-between mb-2">
                            <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                              <Icon className="w-6 h-6" />
                            </div>
                            <Badge className={priceInfo.color}>
                              {priceInfo.text}
                            </Badge>
                          </div>
                          <CardTitle className="text-lg font-sans group-hover:text-primary transition-colors">
                            {template.name}
                          </CardTitle>
                          <CardDescription className="line-clamp-2">
                            {template.description}
                          </CardDescription>
                        </CardHeader>
                        <CardFooter className="pt-0">
                          <Badge variant="outline" className="text-xs">
                            {category?.name}
                          </Badge>
                        </CardFooter>
                      </Card>
                    </motion.div>
                  );
                })}
              </div>

              {filteredTemplates.length === 0 && (
                <div className="text-center py-12">
                  <FileText className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                  <h3 className="text-lg font-medium mb-2">No se encontraron documentos</h3>
                  <p className="text-muted-foreground">
                    Prueba con otros términos de búsqueda o categoría.
                  </p>
                </div>
              )}
            </motion.div>
          ) : (
            // Document Wizard
            <motion.div
              key="wizard"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="max-w-2xl mx-auto"
            >
              {/* Wizard Header */}
              <div className="mb-8">
                <Button
                  variant="ghost"
                  onClick={handleBack}
                  className="mb-4"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  {currentStep === 1 ? 'Volver a documentos' : 'Paso anterior'}
                </Button>

                <div className="flex items-center gap-4 mb-4">
                  {(() => {
                    const Icon = documentIcons[selectedTemplate.icon] || FileText;
                    return (
                      <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center">
                        <Icon className="w-7 h-7 text-primary" />
                      </div>
                    );
                  })()}
                  <div>
                    <h2 className="text-2xl font-bold">{selectedTemplate.name}</h2>
                    <p className="text-muted-foreground">{selectedTemplate.description}</p>
                  </div>
                </div>

                {/* Progress */}
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">
                      Paso {currentStep} de {totalSteps}
                    </span>
                    <span className="font-medium">
                      {Math.round((currentStep / totalSteps) * 100)}%
                    </span>
                  </div>
                  <Progress value={(currentStep / totalSteps) * 100} className="h-2" />
                </div>
              </div>

              {/* Wizard Content */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg font-sans">
                    {currentStep === totalSteps
                      ? 'Revisar y Generar'
                      : `Datos del documento (${currentStep}/${totalSteps - 1})`}
                  </CardTitle>
                  <CardDescription>
                    {currentStep === totalSteps
                      ? 'Revisa la información antes de generar el documento.'
                      : 'Completa los campos requeridos para continuar.'}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {currentStep < totalSteps ? (
                    <div className="space-y-4">
                      {getFieldsForStep(currentStep).map((field) => (
                        <div key={field.name} className="space-y-2">
                          <Label htmlFor={field.name}>
                            {field.label}
                            {field.required && <span className="text-destructive ml-1">*</span>}
                          </Label>
                          {renderField(field)}
                        </div>
                      ))}
                    </div>
                  ) : (
                    // Summary step
                    <div className="space-y-4">
                      <div className="bg-muted rounded-lg p-4">
                        <h4 className="font-medium mb-3">Resumen de datos</h4>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {selectedTemplate.fields.map((field) => (
                            <div key={field.name}>
                              <span className="text-sm text-muted-foreground">{field.label}:</span>
                              <p className="font-medium truncate">
                                {formData[field.name] || '-'}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {selectedTemplate.price !== 'free' && selectedTemplate.price !== 'included' && (
                        <div className="flex items-center gap-3 p-4 bg-secondary/10 rounded-lg">
                          <CreditCard className="w-5 h-5 text-secondary" />
                          <div>
                            <p className="font-medium">Costo del documento</p>
                            <p className="text-2xl font-bold text-primary">
                              S/. {selectedTemplate.price}
                            </p>
                          </div>
                        </div>
                      )}

                      <div className="flex items-start gap-2 text-sm text-muted-foreground">
                        <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                        <p>
                          Este documento es un modelo referencial. Revísalo cuidadosamente 
                          antes de usarlo. Para casos complejos, consulta con un abogado.
                        </p>
                      </div>
                    </div>
                  )}
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button variant="outline" onClick={handleBack}>
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Anterior
                  </Button>
                  
                  {currentStep < totalSteps ? (
                    <Button onClick={handleNext} disabled={!canProceed()}>
                      Siguiente
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </Button>
                  ) : (
                    <div className="flex gap-2">
                      <Button variant="outline" onClick={() => setShowPreview(true)}>
                        <Eye className="w-4 h-4 mr-2" />
                        Vista Previa
                      </Button>
                      <Button onClick={handleGenerate} disabled={isGenerating} className="gradient-primary">
                        {isGenerating ? (
                          <>
                            <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                            Generando...
                          </>
                        ) : (
                          <>
                            <Download className="w-4 h-4 mr-2" />
                            Generar PDF
                          </>
                        )}
                      </Button>
                    </div>
                  )}
                </CardFooter>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Preview Dialog */}
      <Dialog open={showPreview} onOpenChange={setShowPreview}>
        <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Vista Previa del Documento</DialogTitle>
            <DialogDescription>
              Así se verá tu documento. Los datos de ejemplo serán reemplazados con tu información.
            </DialogDescription>
          </DialogHeader>
          
          <div className="bg-white border rounded-lg p-8 shadow-inner min-h-[400px]">
            {/* Mock document preview */}
            <div className="text-center mb-8">
              <h2 className="text-xl font-bold uppercase tracking-wide">
                {selectedTemplate?.name}
              </h2>
              <div className="w-20 h-1 bg-primary mx-auto mt-2" />
            </div>
            
            <div className="space-y-4 text-sm leading-relaxed">
              <p>
                <strong>Señor(a):</strong> {formData.destinatario || formData.arrendatario || formData.comprador || '[NOMBRE DESTINATARIO]'}
              </p>
              <p>
                <strong>De:</strong> {formData.nombreCompleto || formData.arrendador || formData.vendedor || '[TU NOMBRE]'}
              </p>
              <p>
                <strong>DNI:</strong> {formData.dni || formData.dniArrendador || formData.dniVendedor || '[DNI]'}
              </p>
              
              <div className="py-4">
                <p className="text-center font-medium mb-4">ASUNTO: {selectedTemplate?.name}</p>
                <p className="text-justify">
                  Por medio del presente documento, yo, {formData.nombreCompleto || '[NOMBRE]'}, 
                  identificado con DNI N° {formData.dni || '[DNI]'}, con domicilio en 
                  {formData.direccion || '[DIRECCIÓN]'}, me dirijo a usted para...
                </p>
                <p className="text-justify mt-4">
                  {formData.hechos || formData.motivo || '[Contenido del documento según los datos ingresados...]'}
                </p>
              </div>
              
              <div className="pt-8 text-right">
                <p>Lima, {new Date().toLocaleDateString('es-PE', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
                <div className="mt-12">
                  <div className="w-48 border-t border-gray-400 mx-auto" />
                  <p className="text-center mt-2">Firma</p>
                </div>
              </div>
            </div>
            
            {/* Watermark for preview */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-10">
              <span className="text-6xl font-bold text-gray-400 rotate-[-30deg]">
                VISTA PREVIA
              </span>
            </div>
          </div>
          
          <div className="flex justify-end gap-2 mt-4">
            <Button variant="outline" onClick={() => setShowPreview(false)}>
              Cerrar
            </Button>
            <Button onClick={handleGenerate} className="gradient-primary">
              <Download className="w-4 h-4 mr-2" />
              Generar Documento
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Payment Dialog */}
      <Dialog open={showPayment} onOpenChange={setShowPayment}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Confirmar Pago</DialogTitle>
            <DialogDescription>
              Para generar este documento necesitas realizar el pago.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-muted rounded-lg">
              <div>
                <p className="font-medium">{selectedTemplate?.name}</p>
                <p className="text-sm text-muted-foreground">Documento legal</p>
              </div>
              <p className="text-2xl font-bold text-primary">
                S/. {typeof selectedTemplate?.price === 'number' ? selectedTemplate.price : 0}
              </p>
            </div>

            <div className="flex items-start gap-2 text-sm text-muted-foreground">
              <Lock className="w-4 h-4 shrink-0 mt-0.5" />
              <p>
                Pago seguro procesado por Culqi. Tus datos están protegidos 
                con encriptación de grado bancario.
              </p>
            </div>

            <div className="grid gap-2">
              <Button onClick={generateDocument} className="gradient-primary">
                <CreditCard className="w-4 h-4 mr-2" />
                Pagar S/. {typeof selectedTemplate?.price === 'number' ? selectedTemplate.price : 0}
              </Button>
              <Button variant="outline" asChild>
                <Link href="/precios">
                  <Sparkles className="w-4 h-4 mr-2" />
                  Suscribirme y ahorrar
                </Link>
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

