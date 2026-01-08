/**
 * API Client for LegalBot Backend
 * Conecta el frontend con el backend FastAPI
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ═══════════════════════════════════════════════════════════════
// TIPOS
// ═══════════════════════════════════════════════════════════════

interface ChatMessageRequest {
  content: string;
  conversation_id?: string;
}

interface LegalSource {
  text: string;
  law: string;
  article: string;
  category: string;
}

interface ChatMessage {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: LegalSource[];
  created_at: string;
}

interface Conversation {
  id: string;
  title: string;
  category: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

interface ChatResponse {
  message: ChatMessage;
  conversation: Conversation;
  needs_lawyer: boolean;
  confidence: number;
}

interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    name: string;
    plan: string;
  };
}

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {},
  token?: string
): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new ApiError(response.status, error.detail || 'Error en la solicitud');
  }

  return response.json();
}

// ═══════════════════════════════════════════════════════════════
// AUTENTICACIÓN
// ═══════════════════════════════════════════════════════════════

export async function register(
  email: string,
  password: string,
  name: string
): Promise<AuthResponse> {
  return fetchApi<AuthResponse>('/api/users/register', {
    method: 'POST',
    body: JSON.stringify({ email, password, name }),
  });
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  return fetchApi<AuthResponse>('/api/users/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export async function getProfile(token: string) {
  return fetchApi('/api/users/me', {}, token);
}

export async function getUsage(token: string) {
  return fetchApi('/api/users/usage', {}, token);
}

// ═══════════════════════════════════════════════════════════════
// CHAT
// ═══════════════════════════════════════════════════════════════

export async function sendChatMessage(
  content: string,
  conversationId?: string,
  token?: string,
  userContext?: string,
  mode: string = 'advisor'
): Promise<ChatResponse> {
  const body: any = {
    content,
    user_context: userContext,
    mode: mode
  };
  if (conversationId) {
    body.conversation_id = conversationId;
  }

  return fetchApi<ChatResponse>(
    '/api/chat/message',
    {
      method: 'POST',
      body: JSON.stringify(body),
    },
    token
  );
}

/**
 * Upload a user PDF document for analysis
 */
export async function uploadUserDocument(file: File, token?: string) {
  const formData = new FormData();
  formData.append('file', file);

  const headers: any = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}/api/chat/upload-doc`, {
    method: 'POST',
    headers,
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Error al subir el documento');
  }

  return response.json();
}

export async function getConversations(token: string): Promise<Conversation[]> {
  return fetchApi<Conversation[]>('/api/chat/conversations', {}, token);
}

export async function getConversation(
  conversationId: string,
  token: string
): Promise<Conversation & { messages: ChatMessage[] }> {
  return fetchApi(`/api/chat/conversations/${conversationId}`, {}, token);
}

export async function deleteConversation(
  conversationId: string,
  token: string
): Promise<void> {
  await fetchApi(
    `/api/chat/conversations/${conversationId}`,
    { method: 'DELETE' },
    token
  );
}

export async function submitFeedback(
  messageId: string,
  feedback: 'positive' | 'negative',
  token: string
): Promise<void> {
  await fetchApi(
    '/api/chat/feedback',
    {
      method: 'POST',
      body: JSON.stringify({ message_id: messageId, feedback }),
    },
    token
  );
}

// ═══════════════════════════════════════════════════════════════
// DEMO CHAT (No authentication required)
// ═══════════════════════════════════════════════════════════════

interface DemoMessageResponse {
  content: string;
  sources?: LegalSource[];
  category: string;
  needs_lawyer: boolean;
  confidence: number;
}

export async function sendDemoMessage(
  content: string,
  userContext?: string,
  mode: string = 'advisor'
): Promise<DemoMessageResponse> {
  return fetchApi<DemoMessageResponse>('/api/chat/demo', {
    method: 'POST',
    body: JSON.stringify({
      content,
      user_context: userContext,
      mode: mode
    }),
  });
}

// ═══════════════════════════════════════════════════════════════
// DOCUMENTOS
// ═══════════════════════════════════════════════════════════════

export async function getDocumentTemplates() {
  return fetchApi('/api/documents/templates');
}

export async function generateDocument(
  templateId: string,
  data: Record<string, string>,
  token: string
) {
  return fetchApi(
    '/api/documents/generate',
    {
      method: 'POST',
      body: JSON.stringify({ template_id: templateId, data }),
    },
    token
  );
}

export async function getUserDocuments(token: string) {
  return fetchApi('/api/documents/', {}, token);
}

export function getDocumentDownloadUrl(documentId: string): string {
  return `${API_URL}/api/documents/${documentId}/download`;
}

// ═══════════════════════════════════════════════════════════════
// HEALTH CHECK
// ═══════════════════════════════════════════════════════════════

export async function checkHealth(): Promise<{ status: string }> {
  return fetchApi('/health');
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS
// ═══════════════════════════════════════════════════════════════

export { ApiError };
export type {
  ChatMessage,
  ChatResponse,
  Conversation,
  LegalSource,
  AuthResponse,
};

