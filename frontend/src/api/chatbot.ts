import { apiClient } from "./client";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  reply: string;
  model_used: string;
}

export const sendChatMessage = async (
  message: string,
  history: ChatMessage[]
): Promise<ChatResponse> => {
  const { data } = await apiClient.post<ChatResponse>("/chatbot/chat", {
    message,
    history,
  });
  return data;
};
