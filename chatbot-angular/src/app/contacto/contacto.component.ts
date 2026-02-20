import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface ContactForm {
  nombre: string;
  email: string;
  asunto: string;
  mensaje: string;
}

@Component({
  selector: 'app-contacto',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './contacto.component.html',
  styleUrls: ['./contacto.component.css'],
})
export class ContactoComponent {
  form: ContactForm = { nombre: '', email: '', asunto: '', mensaje: '' };
  submitted = false;
  sending = false;

  send() {
    if (!this.form.nombre || !this.form.email || !this.form.mensaje) return;
    this.sending = true;
    // Simulate async send (no real backend endpoint needed)
    setTimeout(() => {
      this.sending = false;
      this.submitted = true;
      this.form = { nombre: '', email: '', asunto: '', mensaje: '' };
    }, 1200);
  }

  reset() { this.submitted = false; }
}
