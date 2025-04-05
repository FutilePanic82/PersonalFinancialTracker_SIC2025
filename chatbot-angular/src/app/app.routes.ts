import { Routes } from '@angular/router';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { HistorialComponent } from './historial/historial.component';
import { ContactoComponent } from './contacto/contacto.component';
import { AnalisisGastosComponent } from './analisis-gastos/analisis-gastos.component';
import { MetasFinancierasComponent } from './metas-financieras/metas-financieras.component';

export const routes: Routes = [
  { path: '', component: ChatbotComponent },
  { path: 'historial', component: HistorialComponent },
  { path: 'contacto', component: ContactoComponent },
  { path: 'analisis', component: AnalisisGastosComponent },
  {path: 'metas', component:MetasFinancierasComponent}
];

