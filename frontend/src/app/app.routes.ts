import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'auth',
    children: [
      { path: 'login',    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent) },
      { path: 'register', loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent) },
      { path: '', redirectTo: 'login', pathMatch: 'full' },
    ],
  },
  {
    path: '',
    loadComponent: () => import('./features/shell/app-shell.component').then(m => m.AppShellComponent),
    canActivate: [authGuard],
    children: [
      { path: 'dashboard', loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent) },
      { path: 'diet/tracker', loadComponent: () => import('./features/diet/daily-tracker/daily-tracker.component').then(m => m.DailyTrackerComponent) },
      { path: 'diet/foods',   loadComponent: () => import('./features/diet/food-library/food-library.component').then(m => m.FoodLibraryComponent) },
      { path: 'diet/plans',   loadComponent: () => import('./features/diet/diet-plans/diet-plans.component').then(m => m.DietPlansComponent) },
      { path: 'profile',      loadComponent: () => import('./features/profile/profile.component').then(m => m.ProfileComponent) },
    ],
  },
  { path: '**', redirectTo: 'dashboard' },
];
