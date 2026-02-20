import { Component, OnInit, ChangeDetectionStrategy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FinanzasService, Transaccion, Reporte } from '../core/services/finanzas.service';

@Component({
  selector: 'app-historial',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './historial.component.html',
  styleUrls: ['./historial.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class HistorialComponent implements OnInit {
  allTx: Transaccion[] = [];
  filtered: Transaccion[] = [];
  reports: Reporte[] = [];
  loading = true;
  error = '';
  searchTerm = '';
  filterTipo: 'todos' | 'ingreso' | 'gasto' = 'todos';

  get totalIngresos() {
    return this.filtered
      .filter(t => t.tipo === 'ingreso')
      .reduce((s, t) => s + t.monto, 0);
  }
  get totalGastos() {
    return this.filtered
      .filter(t => t.tipo === 'gasto')
      .reduce((s, t) => s + t.monto, 0);
  }
  get balance() { return this.totalIngresos - this.totalGastos; }

  constructor(private svc: FinanzasService, private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.load();
    this.loadReports();
  }

  load() {
    this.loading = true;
    this.error = '';
    this.svc.getHistorial().subscribe({
      next: r => {
        this.allTx = r.transacciones;
        this.applyFilter();
        this.loading = false;
        this.cdr.markForCheck();
      },
      error: () => {
        this.error = 'No se pudo cargar el historial. Verifica que el servidor esté activo.';
        this.loading = false;
        this.cdr.markForCheck();
      },
    });
  }

  loadReports() {
    this.svc.getReportes().subscribe({
      next: list => {
        this.reports = list;
        this.cdr.markForCheck();
      },
      error: () => console.warn('Could not load reports')
    });
  }

  applyFilter() {
    let tx = [...this.allTx];
    if (this.filterTipo !== 'todos')
      tx = tx.filter(t => t.tipo === this.filterTipo);
    if (this.searchTerm.trim())
      tx = tx.filter(t =>
        t.concepto.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        t.categoria.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
    this.filtered = tx;
  }

  downloadExcel() {
    this.svc.finalize().subscribe({
      next: blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = 'finanzas_export.xlsx'; a.click();
        URL.revokeObjectURL(url);

        // Refresh report list after export
        setTimeout(() => this.loadReports(), 1000);
      },
      error: () => {
        this.error = 'No se pudo generar el Excel. Verifica que haya transacciones registradas.';
        this.cdr.markForCheck();
      }
    });
  }

  downloadReport(r: Reporte) {
    this.svc.downloadReport(r.id).subscribe({
      next: blob => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = r.nombre; a.click();
        URL.revokeObjectURL(url);
      },
      error: () => {
        this.error = 'No se pudo descargar el reporte.';
        this.cdr.markForCheck();
      }
    });
  }
}
