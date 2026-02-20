import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./chatbot/chatbot.component').then(m => m.ChatbotComponent)
  },
  {
    path: 'historial',
    loadComponent: () => import('./historial/historial.component').then(m => m.HistorialComponent)
  },
  {
    path: 'analisis',
    loadComponent: () => import('./analisis-gastos/analisis-gastos.component').then(m => m.AnalisisGastosComponent)
  },
  {
    path: 'metas',
    loadComponent: () => import('./metas-financieras/metas-financieras.component').then(m => m.MetasFinancierasComponent)
  },
  {
    path: 'contacto',
    loadComponent: () => import('./contacto/contacto.component').then(m => m.ContactoComponent)
  },
  { path: '**', redirectTo: '' },
];
