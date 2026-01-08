import type { Metadata } from 'next';
import './globals.css';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';

export const metadata: Metadata = {
  title: 'LegalBot - Asesoría Legal Inteligente | Perú',
  description: 'Consultas legales 24/7 con IA. Genera documentos legales en minutos. Especializado en legislación peruana. Sin citas, sin esperas.',
  keywords: 'abogado online, consulta legal, documentos legales, Perú, IA, chatbot legal, contrato, carta notarial',
  authors: [{ name: 'LegalBot' }],
  openGraph: {
    title: 'LegalBot - Asesoría Legal Inteligente',
    description: 'Consultas legales 24/7 con IA. Genera documentos legales en minutos.',
    type: 'website',
    locale: 'es_PE',
    siteName: 'LegalBot',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'LegalBot - Asesoría Legal Inteligente',
    description: 'Consultas legales 24/7 con IA. Genera documentos legales en minutos.',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="min-h-screen flex flex-col antialiased">
        <Header />
        <main className="flex-1">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
