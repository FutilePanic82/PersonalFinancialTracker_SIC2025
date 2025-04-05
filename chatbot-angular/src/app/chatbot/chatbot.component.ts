import { CommonModule } from '@angular/common';
import { Component, AfterViewChecked, ElementRef, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../services/deepseek.service';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements AfterViewChecked {
  userInput: string = '';
  messages: { sender: string; text: string }[] = [];
  chatHistory: any[] = [];
  excelDisponible: boolean = false;

  @ViewChild('chatContainer') private chatContainer!: ElementRef;

  constructor(private chatbotService: ChatbotService) {}

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  private scrollToBottom(): void {
    try {
      this.chatContainer.nativeElement.scrollTop = this.chatContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error(err);
    }
  }

  sendMessage(): void {
    if (!this.userInput.trim()) return;

    const userMessage = this.userInput;
    this.userInput = ''; // Limpiar el input inmediatamente

    // Agregar el mensaje del usuario con sender 'User'
    this.messages.push({ sender: 'User', text: userMessage });
    this.chatHistory.push({ role: 'user', content: userMessage });

    this.chatbotService.sendConversation(this.chatHistory).subscribe({
      next: (response) => {
        if (response && response.response) {
          this.messages.push({ sender: 'Bot', text: response.response });
          this.chatHistory.push({ role: 'assistant', content: response.response });
          // Si la respuesta contiene la palabra "descargalo", se habilita la descarga del Excel
          if (response.response.toLowerCase().includes('descargalo')) {
            this.excelDisponible = true;
          }
        }
      },
      error: (error) => {
        console.error('Error en la comunicación con el backend:', error);
        this.messages.push({ sender: 'Bot', text: 'Hubo un error, intenta nuevamente.' });
      }
    });
  }

  finalizeConversation(): void {
    this.chatbotService.finalizeConversation(this.chatHistory).subscribe({
      next: (response) => {
        const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'gastos_ingresos.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        console.error('Error al finalizar la conversación y descargar el Excel:', error);
        this.messages.push({ sender: 'Bot', text: 'Error al generar el archivo Excel.' });
      }
    });
  }
}
