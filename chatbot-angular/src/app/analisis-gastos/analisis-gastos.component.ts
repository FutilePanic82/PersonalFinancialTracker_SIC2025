import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FinanzasService, Transaccion, PredictRequest, PredictResponse } from '../core/services/finanzas.service';

interface CategoryStat {
  categoria: string;
  total: number;
  pct: number;
}

@Component({
  selector: 'app-analisis-gastos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './analisis-gastos.component.html',
  styleUrls: ['./analisis-gastos.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AnalisisGastosComponent implements OnInit {
  /* ── Transaction summary from DB ── */
  txList: Transaccion[] = [];
  loadingTx = true;
  categoryStats: CategoryStat[] = [];
  totalGastos = 0;
  totalIngresos = 0;

  /* ── Polynomial regression form ── */
  form: PredictRequest = { ingresos: 15000, hijos: 0, edad: 28, educacion: 2 };
  prediction: PredictResponse | null = null;
  loadingPred = false;
  predError = '';

  educacionLabels = ['Primaria', 'Secundaria', 'Universidad', 'Posgrado'];
  adviceText = '';

  constructor(private svc: FinanzasService, private cdr: ChangeDetectorRef) { }

  ngOnInit() { this.loadTransactions(); }

  loadTransactions() {
    this.svc.getHistorial().subscribe({
      next: r => {
        this.txList = r.transacciones;
        this.computeStats();
        this.loadingTx = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.loadingTx = false;
        this.cdr.markForCheck();
      },
    });
  }

  computeStats() {
    this.totalGastos = this.txList.filter(t => t.tipo === 'gasto').reduce((s, t) => s + t.monto, 0);
    this.totalIngresos = this.txList.filter(t => t.tipo === 'ingreso').reduce((s, t) => s + t.monto, 0);

    const map = new Map<string, number>();
    this.txList.filter(t => t.tipo === 'gasto').forEach(t => {
      map.set(t.categoria, (map.get(t.categoria) ?? 0) + t.monto);
    });

    this.categoryStats = Array.from(map.entries())
      .map(([categoria, total]) => ({
        categoria,
        total,
        pct: this.totalGastos > 0 ? Math.round((total / this.totalGastos) * 100) : 0,
      }))
      .sort((a, b) => b.total - a.total);
  }

  runPrediction() {
    this.loadingPred = true;
    this.predError = '';
    this.prediction = null;
    this.adviceText = '';

    this.svc.predict(this.form).subscribe({
      next: res => {
        this.prediction = res;
        this.loadingPred = false;
        this.generateAdvice(res);
        this.cdr.markForCheck();
      },
      error: () => {
        this.predError = 'Error al obtener la predicción. Verifica que el servidor esté activo.';
        this.loadingPred = false;
        this.cdr.markForCheck();
      },
    });
  }

  private generateAdvice(res: PredictResponse) {
    const savingsPct = this.form.ingresos > 0
      ? Math.round((res.ahorro_estimado / this.form.ingresos) * 100)
      : 0;

    if (savingsPct >= 20)
      this.adviceText = `✅ Excelente perfil financiero. Ahorras el ${savingsPct}% de tus ingresos. Considera invertir parte del excedente.`;
    else if (savingsPct >= 10)
      this.adviceText = `🟡 Ahorro moderado (${savingsPct}%). Intenta reducir gastos no esenciales para llegar al 20% recomendado.`;
    else
      this.adviceText = `🔴 Ahorro bajo (${savingsPct}%). Tus gastos consumen la mayor parte de tus ingresos. Revisa categorías de mayor gasto.`;
  }

  get spendingRatio(): number {
    if (!this.prediction || this.form.ingresos === 0) return 0;
    return Math.round((this.prediction.gasto_predicho / this.form.ingresos) * 100);
  }
}
