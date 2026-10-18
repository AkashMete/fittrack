import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Store } from '@ngrx/store';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import * as AuthActions from '../../store/auth/auth.actions';
import { selectUser } from '../../store/auth/auth.selectors';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [CommonModule, RouterModule, MatSidenavModule, MatToolbarModule, MatListModule, MatIconModule, MatButtonModule],
  template: `
    <mat-sidenav-container class="h-screen">
      <mat-sidenav mode="side" opened class="w-56 pt-4 bg-gray-900 text-white">
        <div class="px-4 py-3 mb-4">
          <span class="text-xl font-bold tracking-wide text-blue-400">FitTrack</span>
          <p class="text-xs text-gray-400 mt-1">{{ (user$ | async)?.first_name || 'My Account' }}</p>
        </div>
        <mat-nav-list>
          <a mat-list-item routerLink="/dashboard" routerLinkActive="bg-blue-800 rounded">
            <mat-icon matListItemIcon>dashboard</mat-icon>
            <span matListItemTitle>Dashboard</span>
          </a>
          <a mat-list-item routerLink="/diet/tracker" routerLinkActive="bg-blue-800 rounded">
            <mat-icon matListItemIcon>restaurant</mat-icon>
            <span matListItemTitle>Diet Tracker</span>
          </a>
          <a mat-list-item routerLink="/diet/foods" routerLinkActive="bg-blue-800 rounded">
            <mat-icon matListItemIcon>menu_book</mat-icon>
            <span matListItemTitle>Food Library</span>
          </a>
          <a mat-list-item routerLink="/diet/plans" routerLinkActive="bg-blue-800 rounded">
            <mat-icon matListItemIcon>event_note</mat-icon>
            <span matListItemTitle>Diet Plans</span>
          </a>
          <a mat-list-item routerLink="/profile" routerLinkActive="bg-blue-800 rounded">
            <mat-icon matListItemIcon>person</mat-icon>
            <span matListItemTitle>Profile</span>
          </a>
        </mat-nav-list>
        <div class="absolute bottom-4 left-0 right-0 px-4">
          <button mat-stroked-button class="w-full text-white border-gray-600" (click)="logout()">
            <mat-icon>logout</mat-icon> Sign out
          </button>
        </div>
      </mat-sidenav>

      <mat-sidenav-content class="overflow-auto">
        <mat-toolbar color="primary" class="shadow-md">
          <span class="flex-1">FitTrack</span>
        </mat-toolbar>
        <main class="p-6">
          <router-outlet />
        </main>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `,
})
export class AppShellComponent {
  private store = inject(Store);
  user$ = this.store.select(selectUser);
  logout(): void { this.store.dispatch(AuthActions.logout()); }
}
