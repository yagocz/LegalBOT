'use client';

import Link from 'next/link';
import { Scale, Mail, Phone, MapPin, Facebook, Instagram, Linkedin, Twitter } from 'lucide-react';
import { Separator } from '@/components/ui/separator';

const footerLinks = {
  producto: [
    { href: '/chat', label: 'Consultas Legales' },
    { href: '/documentos', label: 'Generar Documentos' },
    { href: '/precios', label: 'Planes y Precios' },
    { href: '/faq', label: 'Preguntas Frecuentes' },
  ],
  legal: [
    { href: '/terminos', label: 'Términos de Uso' },
    { href: '/privacidad', label: 'Política de Privacidad' },
    { href: '/cookies', label: 'Política de Cookies' },
  ],
  recursos: [
    { href: '/blog', label: 'Blog Legal' },
    { href: '/guias', label: 'Guías Legales' },
    { href: '/glosario', label: 'Glosario Jurídico' },
  ],
};

const socialLinks = [
  { href: 'https://facebook.com', icon: Facebook, label: 'Facebook' },
  { href: 'https://instagram.com', icon: Instagram, label: 'Instagram' },
  { href: 'https://linkedin.com', icon: Linkedin, label: 'LinkedIn' },
  { href: 'https://twitter.com', icon: Twitter, label: 'Twitter' },
];

export function Footer() {
  return (
    <footer className="bg-primary text-primary-foreground">
      {/* Disclaimer */}
      <div className="bg-secondary/10 border-b border-primary-foreground/10">
        <div className="container mx-auto px-4 py-4">
          <p className="text-sm text-primary-foreground/80 text-center">
            ⚠️ <strong>IMPORTANTE:</strong> LegalBot es una herramienta informativa basada en inteligencia artificial. 
            No reemplaza la asesoría de un abogado titulado y colegiado. Para casos complejos, penales o de alto riesgo, 
            recomendamos consultar con un profesional del derecho.
          </p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
          {/* Brand */}
          <div className="lg:col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <Scale className="h-8 w-8" />
              <span className="font-display text-2xl font-bold">
                Legal<span className="text-secondary">Bot</span>
              </span>
            </Link>
            <p className="text-primary-foreground/80 mb-6 max-w-md">
              Asesoría legal inteligente para todos los peruanos. Accede a información legal confiable 
              y genera documentos profesionales en minutos.
            </p>
            <div className="space-y-2 text-sm text-primary-foreground/70">
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4" />
                <span>contacto@legalbot.pe</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4" />
                <span>+51 1 234 5678</span>
              </div>
              <div className="flex items-center gap-2">
                <MapPin className="h-4 w-4" />
                <span>Lima, Perú</span>
              </div>
            </div>
          </div>

          {/* Producto */}
          <div>
            <h4 className="font-semibold mb-4">Producto</h4>
            <ul className="space-y-2">
              {footerLinks.producto.map((link) => (
                <li key={link.href}>
                  <Link 
                    href={link.href}
                    className="text-primary-foreground/70 hover:text-secondary transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold mb-4">Legal</h4>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.href}>
                  <Link 
                    href={link.href}
                    className="text-primary-foreground/70 hover:text-secondary transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Recursos */}
          <div>
            <h4 className="font-semibold mb-4">Recursos</h4>
            <ul className="space-y-2">
              {footerLinks.recursos.map((link) => (
                <li key={link.href}>
                  <Link 
                    href={link.href}
                    className="text-primary-foreground/70 hover:text-secondary transition-colors text-sm"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <Separator className="my-8 bg-primary-foreground/20" />

        {/* Bottom */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-primary-foreground/60">
            © {new Date().getFullYear()} LegalBot. Todos los derechos reservados.
          </p>
          
          <div className="flex items-center gap-4">
            {socialLinks.map((social) => (
              <a
                key={social.label}
                href={social.href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-foreground/60 hover:text-secondary transition-colors"
                aria-label={social.label}
              >
                <social.icon className="h-5 w-5" />
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}

