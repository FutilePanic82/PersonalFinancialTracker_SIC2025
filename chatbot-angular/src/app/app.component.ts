import { Component } from '@angular/core';
import { RouterModule } from '@angular/router'; // ✅ Importa RouterModule

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterModule], // ✅ Agrega RouterModule a imports
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'chatbot-angular';
  isSidebarOpen = false;

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }
  closeSidebar() {
    this.isSidebarOpen = false; // ✅ Cierra el sidebar al hacer clic en un enlace
  }
}
