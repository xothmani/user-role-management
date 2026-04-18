import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from '../shared/navbar/navbar.component';
import { SidebarComponent } from '../shared/sidebar/sidebar.component';

@Component({
  selector: 'app-layout',
  standalone: true,
  imports: [RouterOutlet, NavbarComponent, SidebarComponent],
  template: `
    <div class="app-layout">
      <app-sidebar />
      <div class="d-flex flex-column flex-grow-1">
        <app-navbar />
        <main class="main-content">
          <router-outlet />
        </main>
      </div>
    </div>
  `
})
export class LayoutComponent {}
