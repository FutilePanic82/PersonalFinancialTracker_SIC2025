import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-contacto',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './contacto.component.html',
  styleUrls: ['./contacto.component.css']
})
export class ContactoComponent {
  contactos = [
    {
      nombre: 'David Alfredo Ramirez Silva',
      email: 'david.ramirez7093@alumnos.udg.mx',
      telefono: '+52 331 429 9105',
      foto: '../../assets/david.jpg'
    },
    {
      nombre: 'Ernesto castañeda Rubio',
      email: 'ernesto.castaneda1603@alumnos.udg.mx',
      telefono: '+52 322 199 7129',
      foto: '../../assets/ernesto.jpeg'
    },
    {
      nombre: 'César Imanol López Grave',
      email: 'lopezgravecesar@gmail.com',
      telefono: '+52 669 244 5503',
      foto: '../../assets/cesar.jpeg'
    }
  ];
}
