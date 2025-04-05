import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-historial',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './historial.component.html',
  styleUrls: ['./historial.component.css']
})
export class HistorialComponent {
  historialArchivos = [
    { nombre: 'Enero.xlsx', fecha: '2024-03-28', tamano: '2.4MB' },
    { nombre: 'Febrero.xlsx', fecha: '2024-03-29', tamano: '3.1MB' },
    { nombre: 'Marzo.xlsx', fecha: '2024-03-30', tamano: '1.9MB' }
  ];
}
