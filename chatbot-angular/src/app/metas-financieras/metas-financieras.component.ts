import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FinanzasService } from '../core/services/finanzas.service';

interface Meta {
  nombre: string;
  emoji: string;
  valor: number;   // percentage 0-100
  locked: boolean;
}

@Component({
  selector: 'app-metas-financieras',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './metas-financieras.component.html',
  styleUrls: ['./metas-financieras.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MetasFinancierasComponent implements OnInit {
  metas: Meta[] = [
    { nombre: 'Alimentación', emoji: '🍽️', valor: 20, locked: false },
    { nombre: 'Vivienda', emoji: '🏡', valor: 20, locked: false },
    { nombre: 'Transporte', emoji: '🚗', valor: 10, locked: false },
    { nombre: 'Salud', emoji: '🏥', valor: 10, locked: false },
    { nombre: 'Educación', emoji: '📚', valor: 5, locked: false },
    { nombre: 'Entretenimiento', emoji: '🎮', valor: 10, locked: false },
    { nombre: 'Ropa y accesorios', emoji: '👕', valor: 5, locked: false },
    { nombre: 'Ahorro personal', emoji: '💰', valor: 10, locked: false },
    { nombre: 'Inversiones', emoji: '📊', valor: 10, locked: false },
  ];

  llmAdvice = '';
  loadingAdvice = false;
  saved = false;

  constructor(private svc: FinanzasService, private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    const stored = localStorage.getItem('metasFinancieras');
    if (stored) this.metas = JSON.parse(stored);
  }

  get total(): number {
    return this.metas.reduce((s, m) => s + m.valor, 0);
  }
  get totalOk(): boolean { return this.total === 100; }

  onSliderChange(changed: Meta) {
    const unlocked = this.metas.filter(m => !m.locked && m !== changed);
    if (!unlocked.length) return;
    const excess = this.total - 100;
    if (excess === 0) return;
    const perItem = excess / unlocked.length;
    unlocked.forEach(m => {
      m.valor = Math.max(0, Math.min(100, Math.round(m.valor - perItem)));
    });
  }

  toggleLock(meta: Meta) { meta.locked = !meta.locked; }

  save() {
    this.normalise();
    localStorage.setItem('metasFinancieras', JSON.stringify(this.metas));
    this.saved = true;
    setTimeout(() => {
      this.saved = false;
      this.cdr.markForCheck();
    }, 2500);
    this.requestAdvice();
  }

  private normalise() {
    const t = this.total;
    if (t > 0 && t !== 100) {
      const factor = 100 / t;
      this.metas.forEach(m => (m.valor = Math.round(m.valor * factor)));
    }
  }

  private requestAdvice() {
    this.loadingAdvice = true;
    this.llmAdvice = '';
    const payload = this.metas.map(m => ({ nombre: m.nombre, valor: m.valor }));
    this.svc.metasAdvice(payload).subscribe({
      next: r => {
        this.llmAdvice = r.response;
        this.loadingAdvice = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.loadingAdvice = false;
        this.cdr.markForCheck();
      },
    });
  }
}
