export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const mockResponses = [
  "Olá! Sou o assistente virtual da Plataforma Cívica Digital. Como posso ajudá-lo hoje?",
  "Posso ajudá-lo com informações sobre denúncias, consulta de processos ou dúvidas sobre a plataforma.",
  "Para fazer uma denúncia, acesse a seção 'Fazer Denúncia' no menu principal.",
  "Você pode consultar o andamento de processos na área de 'Triagem' ou 'Protocolo'.",
  "O Banco de Normas contém toda a legislação relevante para sua consulta.",
  "Precisa de mais alguma informação? Estou aqui para ajudar!",
];

let messageIndex = 0;

export const sendMessage = async (message: string): Promise<string> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 800 + Math.random() * 1200));
  
  // Simple mock response logic
  if (message.toLowerCase().includes('olá') || message.toLowerCase().includes('oi')) {
    return mockResponses[0];
  }
  
  if (message.toLowerCase().includes('denúncia') || message.toLowerCase().includes('denuncia')) {
    return mockResponses[2];
  }
  
  if (message.toLowerCase().includes('processo') || message.toLowerCase().includes('protocolo')) {
    return mockResponses[3];
  }
  
  if (message.toLowerCase().includes('norma') || message.toLowerCase().includes('lei')) {
    return mockResponses[4];
  }
  
  // Cycle through responses for other messages
  const response = mockResponses[messageIndex % mockResponses.length];
  messageIndex++;
  return response;
};

export const generateId = (): string => {
  return `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};
