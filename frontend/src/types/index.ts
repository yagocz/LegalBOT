// User Types
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  plan: PlanType;
  createdAt: Date;
  updatedAt: Date;
}

export type PlanType = 'free' | 'basic' | 'premium' | 'enterprise';

// Subscription Types
export interface Subscription {
  id: string;
  userId: string;
  plan: PlanType;
  status: 'active' | 'cancelled' | 'expired';
  startDate: Date;
  endDate: Date;
  culqiSubscriptionId?: string;
}

// Chat Types
export interface Conversation {
  id: string;
  userId: string;
  title: string;
  category: LegalCategory;
  createdAt: Date;
  updatedAt: Date;
  messages: Message[];
}

export interface Message {
  id: string;
  conversationId: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: LegalSource[];
  createdAt: Date;
  mode?: string;
}

export interface LegalSource {
  text: string;
  law: string;
  article: string;
  category: LegalCategory;
}

export type LegalCategory =
  | 'laboral'
  | 'consumidor'
  | 'familia'
  | 'civil'
  | 'transito'
  | 'empresas'
  | 'general';

// Document Types
export interface DocumentTemplate {
  id: string;
  name: string;
  description: string;
  category: LegalCategory;
  price: number | 'free' | 'included';
  icon: string;
  fields: DocumentField[];
}

export interface DocumentField {
  name: string;
  label: string;
  type: 'text' | 'textarea' | 'date' | 'number' | 'select';
  required: boolean;
  placeholder?: string;
  options?: string[];
}

export interface GeneratedDocument {
  id: string;
  userId: string;
  templateId: string;
  data: Record<string, string>;
  pdfUrl?: string;
  paid: boolean;
  createdAt: Date;
}

// Usage Types
export interface Usage {
  id: string;
  userId: string;
  month: string;
  queriesCount: number;
  documentsCount: number;
}

// Plan Details
export interface PlanDetails {
  id: PlanType;
  name: string;
  price: number;
  yearlyPrice: number;
  features: string[];
  queriesLimit: number | 'unlimited';
  documentsLimit: number | 'unlimited';
  popular?: boolean;
}

// API Response Types
export interface ChatResponse {
  answer: string;
  category: LegalCategory;
  sources: LegalSource[];
  needsLawyer: boolean;
  confidence: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

