import {
  AfterViewChecked,
  Component,
  ElementRef,
  ViewChild,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FinanzasService, Transaccion } from '../core/services/finanzas.service';

interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
  time: string;
  transactions?: Transaccion[];
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ChatbotComponent implements AfterViewChecked {
  messages: ChatMessage[] = [
    {
      sender: 'bot',
      text: '¡Hola! 👋 Soy tu asistente financiero. Cuéntame tus ingresos y gastos de forma natural, como: "Gasté $500 en comida" o "Recibí $15,000 de sueldo". Iré registrándolos automáticamente.',
      time: this.now(),
    },
  ];
  chatHistory: any[] = [];
  userInput = '';
  loading = false;
  excelReady = false;

  @ViewChild('chatContainer') private chatRef!: ElementRef;

  constructor(private svc: FinanzasService, private cdr: ChangeDetectorRef) { }

  ngAfterViewChecked() {
    this.scrollBottom();
  }

  private scrollBottom() {
    try {
      this.chatRef.nativeElement.scrollTop =
        this.chatRef.nativeElement.scrollHeight;
    } catch (_) { }
  }

  private now(): string {
    return new Date().toLocaleTimeString('es-MX', {
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  sendMessage() {
    const text = this.userInput.trim();
    if (!text || this.loading) return;
    this.userInput = '';

    this.messages.push({ sender: 'user', text, time: this.now() });
    this.chatHistory.push({ role: 'user', content: text });
    this.loading = true;

    // Only send the new user message; the backend keeps its own full history
    const newMessage = [{ role: 'user', content: text }];

    this.svc.sendConversation(newMessage).subscribe({
      next: (res) => {
        this.loading = false;
        const msg: ChatMessage = {
          sender: 'bot',
          text: res.response,
          time: this.now(),
        };
        if (res.transacciones_detectadas?.length) {
          msg.transactions = res.transacciones_detectadas;
          this.excelReady = true;
        }
        this.messages.push(msg);
        this.chatHistory.push({ role: 'assistant', content: res.response });
        this.cdr.markForCheck();
      },
      error: () => {
        this.loading = false;
        this.messages.push({
          sender: 'bot',
          text: '⚠️ Error al conectar con el servidor. Verifica que el backend esté iniciado.',
          time: this.now(),
        });
        this.cdr.markForCheck();
      },
    });
  }

  downloadExcel() {
    this.svc.finalize().subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'finanzas.xlsx';
        a.click();
        URL.revokeObjectURL(url);
        this.cdr.markForCheck();
      },
      error: () => {
        this.messages.push({
          sender: 'bot',
          text: '⚠️ No se pudo generar el Excel. Asegúrate de haber registrado al menos una transacción.',
          time: this.now(),
        });
        this.cdr.markForCheck();
      },
    });
  }

  resetChat() {
    this.svc.resetChat().subscribe();
    this.chatHistory = [];
    this.excelReady = false;
    this.messages = [
      {
        sender: 'bot',
        text: '🔄 Conversación reiniciada. ¡Listo para registrar nuevas transacciones!',
        time: this.now(),
      },
    ];
    this.cdr.markForCheck();
  }

  trackByMessage(index: number, msg: ChatMessage): number {
    return index;
  }

  trackByTransaction(index: number, tx: Transaccion): number {
    return index;
  }
}
