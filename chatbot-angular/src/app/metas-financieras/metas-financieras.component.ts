import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-metas-financieras',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './metas-financieras.component.html',
  styleUrls: ['./metas-financieras.component.css']
})
export class MetasFinancierasComponent {
  metas = [
    { nombre: 'Alimentación 🍽️', valor: 20, bloqueado: true },
    { nombre: 'Vivienda 🏡', valor: 20, bloqueado: true },
    { nombre: 'Transporte 🚗', valor: 10, bloqueado: true },
    { nombre: 'Salud 🏥', valor: 10, bloqueado: true },
    { nombre: 'Educación 📚', valor: 5, bloqueado: true },
    { nombre: 'Entretenimiento y ocio 🎮', valor: 10, bloqueado: true },
    { nombre: 'Ropa y accesorios 👕', valor: 5, bloqueado: true },
    { nombre: 'Ahorro personal 💰', valor: 10, bloqueado: true },
    { nombre: 'Inversiones 📊', valor: 10, bloqueado: true },
  ];

  respuestaLLM: string = '';

  ajustarValores(metaEditada: any) {
    let desbloqueadas = this.metas.filter(meta => !meta.bloqueado);
    let total = this.metas.reduce((sum, meta) => sum + meta.valor, 0);
    let exceso = total - 100;

    if (exceso !== 0 && desbloqueadas.length > 1) {
      let ajustePorMeta = Math.floor(exceso / (desbloqueadas.length - 1));

      desbloqueadas.forEach(meta => {
        if (meta !== metaEditada) {
          meta.valor = Math.max(0, Math.min(100, meta.valor - ajustePorMeta));
        }
      });
    }
  }

  isLastUnlocked(): boolean {
    return this.metas.filter(meta => !meta.bloqueado).length === 1;
  }

  guardarMetas() {
    this.normalizarValores(); // Normalizamos los valores antes de guardarlos
    localStorage.setItem('metasFinancieras', JSON.stringify(this.metas));
    this.enviarDatosALlm();
  }

  cargarMetas() {
    const datosGuardados = localStorage.getItem('metasFinancieras');
    if (datosGuardados) {
      this.metas = JSON.parse(datosGuardados);
    }
  }

  normalizarValores() {
    let total = this.metas.reduce((sum, meta) => sum + meta.valor, 0);
    if (total > 100) {
      const factor = 100 / total;
      this.metas.forEach(meta => meta.valor = Math.round(meta.valor * factor));
    }
  }

  async enviarDatosALlm() {
    const payload = {
      prompt: `Mis metas financieras son las siguientes:
      1. Alimentación 🍽️: ${this.metas[0].valor}%
      2. Vivienda 🏡: ${this.metas[1].valor}%
      3. Transporte 🚗: ${this.metas[2].valor}%
      4. Salud 🏥: ${this.metas[3].valor}%
      5. Educación 📚: ${this.metas[4].valor}%
      6. Entretenimiento y ocio 🎮: ${this.metas[5].valor}%
      7. Ropa y accesorios 👕: ${this.metas[6].valor}%
      8. Tecnología y gadgets 📱: ${this.metas[7].valor}%
      9. Viajes y vacaciones ✈️: ${this.metas[8].valor}%
      10. Ahorro personal 💰: ${this.metas[9].valor}%
      11. Inversiones 📊: ${this.metas[10].valor}%
      12. Donaciones y caridad ❤️: ${this.metas[11].valor}%.

      Los valores son porcentajes de distribución, y suman un total de 100%.`
    };

    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      this.respuestaLLM = data.response;
    } catch (error) {
      console.error('Error al enviar los datos al LLM:', error);
    }
  }

  ngOnInit() {
    this.cargarMetas();
  }
}
