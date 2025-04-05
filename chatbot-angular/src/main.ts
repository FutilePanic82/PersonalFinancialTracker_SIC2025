import { CommonModule } from '@angular/common';
import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideHttpClient } from '@angular/common/http';
//import { provideForms } from '@angular/forms';
import { importProvidersFrom } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ChatbotComponent } from './app/chatbot/chatbot.component';
import { HistorialComponent } from './app/historial/historial.component';
import { ContactoComponent } from './app/contacto/contacto.component';
import { AnalisisGastosComponent } from './app/analisis-gastos/analisis-gastos.component';
import { MetasFinancierasComponent } from './app/metas-financieras/metas-financieras.component';

const appRoutes = [
  { path: '', component: ChatbotComponent },
  { path: 'historial', component: HistorialComponent },
  { path: 'contacto', component: ContactoComponent },
  { path: 'analisis', component: AnalisisGastosComponent },
  { path: 'metas', component:MetasFinancierasComponent }
];

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    //provideForms(),
    importProvidersFrom(RouterModule.forRoot(appRoutes)) // ✅ Asegura que RouterModule esté aquí
  ]
}).catch((err) => console.error(err));
