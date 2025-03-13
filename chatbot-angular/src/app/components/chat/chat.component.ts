import { Component } from '@angular/core';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {
  messages: { text: string, fromUser: boolean }[] = [];
  userInput: string = '';

  sendMessage() {
    if (!this.userInput.trim()) return;

    this.messages.push({ text: this.userInput, fromUser: true });

    setTimeout(() => {
      this.messages.push({ text: "Procesando tu mensaje...", fromUser: false });
      // Aquí se enviará la petición al backend
    }, 500);

    this.userInput = '';
  }
}
