'use client';

import Link from 'next/link';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Scale, 
  Menu, 
  MessageSquare, 
  FileText, 
  LayoutDashboard,
  LogIn,
  UserPlus
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';

const navLinks = [
  { href: '/chat', label: 'Consultas', icon: MessageSquare },
  { href: '/documentos', label: 'Documentos', icon: FileText },
  { href: '/precios', label: 'Precios', icon: LayoutDashboard },
];

export function Header() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <nav className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <motion.div
            whileHover={{ rotate: 15 }}
            transition={{ type: 'spring', stiffness: 400 }}
          >
            <Scale className="h-8 w-8 text-primary" />
          </motion.div>
          <span className="font-display text-xl font-bold text-primary">
            Legal<span className="text-secondary">Bot</span>
          </span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center gap-6">
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors font-medium"
            >
              <link.icon className="h-4 w-4" />
              {link.label}
            </Link>
          ))}
        </div>

        {/* Desktop Auth Buttons */}
        <div className="hidden md:flex items-center gap-3">
          <Button variant="ghost" asChild>
            <Link href="/login" className="flex items-center gap-2">
              <LogIn className="h-4 w-4" />
              Ingresar
            </Link>
          </Button>
          <Button asChild className="gradient-primary">
            <Link href="/registro" className="flex items-center gap-2">
              <UserPlus className="h-4 w-4" />
              Registrarse
            </Link>
          </Button>
        </div>

        {/* Mobile Menu */}
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger asChild className="md:hidden">
            <Button variant="ghost" size="icon">
              <Menu className="h-6 w-6" />
              <span className="sr-only">Abrir menú</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="right" className="w-80">
            <div className="flex flex-col gap-6 mt-6">
              <Link href="/" className="flex items-center gap-2" onClick={() => setIsOpen(false)}>
                <Scale className="h-8 w-8 text-primary" />
                <span className="font-display text-xl font-bold text-primary">
                  Legal<span className="text-secondary">Bot</span>
                </span>
              </Link>

              <div className="flex flex-col gap-2">
                {navLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    onClick={() => setIsOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 rounded-lg text-muted-foreground hover:text-primary hover:bg-muted transition-colors"
                  >
                    <link.icon className="h-5 w-5" />
                    {link.label}
                  </Link>
                ))}
              </div>

              <div className="border-t pt-4 flex flex-col gap-2">
                <Button variant="outline" asChild className="w-full justify-start">
                  <Link href="/login" onClick={() => setIsOpen(false)} className="flex items-center gap-2">
                    <LogIn className="h-4 w-4" />
                    Ingresar
                  </Link>
                </Button>
                <Button asChild className="w-full justify-start gradient-primary">
                  <Link href="/registro" onClick={() => setIsOpen(false)} className="flex items-center gap-2">
                    <UserPlus className="h-4 w-4" />
                    Registrarse
                  </Link>
                </Button>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </nav>
    </header>
  );
}

