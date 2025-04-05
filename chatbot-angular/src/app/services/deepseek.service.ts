import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ChatbotService {
  private apiUrl = 'http://localhost:8000';  // URL de tu backend

  constructor(private http: HttpClient) {}

  // Envía el historial completo de la conversación al endpoint /conversation
  sendConversation(chatHistory: any[]): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/conversation`, { chat_history: chatHistory });
  }

  // Finaliza la conversación y genera el Excel enviando el historial real
  finalizeConversation(chatHistory: any[]): Observable<Blob> {
    return this.http.post(`${this.apiUrl}/finalize`, { chat_history: chatHistory }, { responseType: 'blob' });
  }
}
