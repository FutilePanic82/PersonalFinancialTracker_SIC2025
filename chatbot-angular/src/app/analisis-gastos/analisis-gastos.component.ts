import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-analisis-gastos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analisis-gastos.component.html',
  styleUrls: ['./analisis-gastos.component.css']
})
export class AnalisisGastosComponent {
  gastos = [
    { categoria: 'Alquiler', monto: 2000 },
    { categoria: 'Servicios públicos (agua + luz + internet)', monto: 1000 },
    { categoria: 'Comida', monto: 2000 },
    { categoria: 'Transporte', monto: 300 },
    { categoria: 'Ocio y entretenimiento', monto: 500 },
    { categoria: 'Telecomunicaciones', monto: 1500 },
    { categoria: 'Salud y belleza', monto: 200 },
    { categoria: 'Ropa y accesorios', monto: 300 }
  ];

  ingresos = [
    { categoria: 'Ingreso fijo', monto: 15000 },
    { categoria: 'Ingreso extra', monto: 2000 }
  ];

  totalGasto: number = 0;
  totalIngreso: number = 0;
  categoriaMayorGasto: string = '';
  consejo: string = '';

  constructor() {
    this.analizarFinanzas();
  }

  analizarFinanzas() {
    this.totalGasto = this.gastos.reduce((acc, gasto) => acc + gasto.monto, 0);
    this.totalIngreso = this.ingresos.reduce((acc, ingreso) => acc + ingreso.monto, 0);

    const mayorGasto = this.gastos.reduce((max, gasto) => gasto.monto > max.monto ? gasto : max, this.gastos[0]);
    this.categoriaMayorGasto = mayorGasto.categoria;

    this.generarConsejo();
  }

  generarConsejo() {
    const balance = this.totalIngreso - this.totalGasto;

    if (balance < 0) {
      this.consejo = 'Tus gastos superan tus ingresos. Revisa tus gastos fijos y reduce lo innecesario.';
    } else if (this.categoriaMayorGasto === 'Supermercado') {
      this.consejo = 'Intenta optimizar tus compras en el supermercado aprovechando ofertas y evitando compras impulsivas.';
    } else if (this.totalGasto > this.totalIngreso * 0.8) {
      this.consejo = 'Estás gastando más del 80% de tus ingresos. Considera ahorrar una mayor proporción.';
    } else {
      this.consejo = 'Vas bien con tus finanzas. Considera crear un fondo de emergencia o invertir parte del ingreso.';
    }
  }
}
