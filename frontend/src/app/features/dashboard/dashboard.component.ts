import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { map } from 'rxjs/operators';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatIconModule } from '@angular/material/icon';
import { RouterModule } from '@angular/router';
import { selectUser } from '../../store/auth/auth.selectors';
import { selectTodayLog } from '../../store/diet/diet.selectors';
import * as DietActions from '../../store/diet/diet.actions';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatProgressBarModule, MatIconModule, RouterModule],
  template: `
    <h1 class="text-2xl font-bold mb-6">Good day, {{ (user$ | async)?.first_name || 'there' }}! 👋</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <!-- Calories card -->
      <mat-card class="p-4">
        <div class="flex items-center gap-3 mb-3">
          <mat-icon class="text-orange-500">local_fire_department</mat-icon>
          <span class="font-semibold text-gray-700">Calories</span>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ (log$ | async)?.total_calories || 0 | number:'1.0-0' }}</div>
        <p class="text-sm text-gray-500 mt-1">kcal today</p>
        <mat-progress-bar mode="determinate" [value]="calorieProgress$ | async" class="mt-3"></mat-progress-bar>
      </mat-card>

      <!-- Protein -->
      <mat-card class="p-4">
        <div class="flex items-center gap-3 mb-3">
          <mat-icon class="text-red-500">fitness_center</mat-icon>
          <span class="font-semibold text-gray-700">Protein</span>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ (log$ | async)?.total_protein_g || 0 | number:'1.0-0' }}g</div>
        <p class="text-sm text-gray-500 mt-1">of daily target</p>
      </mat-card>

      <!-- Carbs -->
      <mat-card class="p-4">
        <div class="flex items-center gap-3 mb-3">
          <mat-icon class="text-yellow-500">grain</mat-icon>
          <span class="font-semibold text-gray-700">Carbs</span>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ (log$ | async)?.total_carbs_g || 0 | number:'1.0-0' }}g</div>
        <p class="text-sm text-gray-500 mt-1">of daily target</p>
      </mat-card>

      <!-- Fat -->
      <mat-card class="p-4">
        <div class="flex items-center gap-3 mb-3">
          <mat-icon class="text-green-500">opacity</mat-icon>
          <span class="font-semibold text-gray-700">Fat</span>
        </div>
        <div class="text-3xl font-bold text-gray-900">{{ (log$ | async)?.total_fat_g || 0 | number:'1.0-0' }}g</div>
        <p class="text-sm text-gray-500 mt-1">of daily target</p>
      </mat-card>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <mat-card class="p-4">
        <h2 class="text-lg font-semibold mb-3">Quick Actions</h2>
        <div class="flex flex-col gap-2">
          <a routerLink="/diet/tracker" class="flex items-center gap-2 p-3 rounded-lg bg-blue-50 hover:bg-blue-100 transition-colors">
            <mat-icon class="text-blue-600">add_circle</mat-icon>
            <span class="text-blue-700 font-medium">Log a meal</span>
          </a>
          <a routerLink="/diet/foods" class="flex items-center gap-2 p-3 rounded-lg bg-green-50 hover:bg-green-100 transition-colors">
            <mat-icon class="text-green-600">search</mat-icon>
            <span class="text-green-700 font-medium">Browse food library</span>
          </a>
          <a routerLink="/diet/plans" class="flex items-center gap-2 p-3 rounded-lg bg-purple-50 hover:bg-purple-100 transition-colors">
            <mat-icon class="text-purple-600">event_note</mat-icon>
            <span class="text-purple-700 font-medium">View diet plans</span>
          </a>
        </div>
      </mat-card>

      <mat-card class="p-4">
        <h2 class="text-lg font-semibold mb-3">Today's Log — {{ today }}</h2>
        <ng-container *ngIf="(log$ | async)?.entries as entries">
          <div *ngIf="entries.length === 0" class="text-gray-500 text-sm py-4 text-center">
            Nothing logged yet today. <a routerLink="/diet/tracker" class="text-blue-600 hover:underline">Add a meal</a>
          </div>
          <div *ngFor="let entry of entries | slice:0:5" class="flex justify-between py-2 border-b last:border-0">
            <span class="text-sm font-medium">{{ entry.food_name }}</span>
            <span class="text-sm text-gray-500">{{ entry.calories | number:'1.0-0' }} kcal</span>
          </div>
          <p *ngIf="entries.length > 5" class="text-xs text-gray-400 mt-2">+{{ entries.length - 5 }} more items…</p>
        </ng-container>
      </mat-card>
    </div>
  `,
})
export class DashboardComponent implements OnInit {
  private store = inject(Store);
  today = new Date().toISOString().split('T')[0];
  user$ = this.store.select(selectUser);
  log$ = this.store.select(selectTodayLog);
  calorieProgress$ = this.log$.pipe(map((l) => Math.min(((l?.total_calories ?? 0) / 2000) * 100, 100)));

  ngOnInit(): void {
    this.store.dispatch(DietActions.loadTodayLog({ date: this.today }));
  }
}
