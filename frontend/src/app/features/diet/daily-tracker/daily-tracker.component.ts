import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { Store } from '@ngrx/store';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDividerModule } from '@angular/material/divider';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { selectTodayLog, selectDietLoading } from '../../../store/diet/diet.selectors';
import { selectUser } from '../../../store/auth/auth.selectors';
import * as DietActions from '../../../store/diet/diet.actions';
import { AddEntryDialogComponent } from './add-entry-dialog.component';

const MEAL_LABELS: Record<string, string> = {
  breakfast: 'Breakfast',
  lunch: 'Lunch',
  dinner: 'Dinner',
  snack: 'Snack',
  pre_workout: 'Pre-Workout',
  post_workout: 'Post-Workout',
};

@Component({
  selector: 'app-daily-tracker',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatCardModule, MatButtonModule, MatIconModule, MatProgressBarModule, MatDividerModule, MatDialogModule],
  template: `
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold">Daily Diet Tracker</h1>
        <p class="text-gray-500 text-sm">{{ today }}</p>
      </div>
      <button mat-raised-button color="primary" (click)="openAddEntry()">
        <mat-icon>add</mat-icon> Add Food
      </button>
    </div>

    <!-- Macro summary bar -->
    <mat-card class="p-4 mb-6" *ngIf="log$ | async as log">
      <div class="grid grid-cols-4 gap-4 text-center mb-3">
        <div>
          <div class="text-2xl font-bold text-orange-500">{{ log.total_calories | number:'1.0-0' }}</div>
          <div class="text-xs text-gray-500">kcal</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-red-500">{{ log.total_protein_g | number:'1.0-0' }}g</div>
          <div class="text-xs text-gray-500">Protein</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-yellow-500">{{ log.total_carbs_g | number:'1.0-0' }}g</div>
          <div class="text-xs text-gray-500">Carbs</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-green-500">{{ log.total_fat_g | number:'1.0-0' }}g</div>
          <div class="text-xs text-gray-500">Fat</div>
        </div>
      </div>
      <mat-progress-bar mode="determinate" [value]="caloriePercent(log)" color="primary"></mat-progress-bar>
      <p class="text-xs text-gray-400 mt-1">Calorie progress vs. 2000 kcal target</p>
    </mat-card>

    <!-- Meal sections -->
    <ng-container *ngIf="log$ | async as log">
      <ng-container *ngFor="let mealType of mealTypes">
        <ng-container *ngIf="entriesForMeal(log.entries, mealType) as entries">
          <mat-card class="p-4 mb-4" *ngIf="entries.length > 0">
            <h2 class="text-lg font-semibold mb-3">{{ mealLabel(mealType) }}</h2>
            <div *ngFor="let entry of entries" class="flex items-center justify-between py-2 border-b last:border-0">
              <div>
                <p class="font-medium text-gray-900">{{ entry.food_name }}</p>
                <p class="text-xs text-gray-500">{{ entry.quantity_g }}g · {{ entry.calories | number:'1.0-0' }} kcal</p>
              </div>
              <div class="flex items-center gap-3 text-xs text-gray-600">
                <span>P: {{ entry.protein_g | number:'1.0-0' }}g</span>
                <span>C: {{ entry.carbs_g | number:'1.0-0' }}g</span>
                <span>F: {{ entry.fat_g | number:'1.0-0' }}g</span>
                <button mat-icon-button color="warn" (click)="deleteEntry(entry.entry_id)">
                  <mat-icon>close</mat-icon>
                </button>
              </div>
            </div>
          </mat-card>
        </ng-container>
      </ng-container>

      <div *ngIf="log.entries.length === 0" class="text-center py-16 text-gray-500">
        <mat-icon class="text-5xl">restaurant</mat-icon>
        <p class="mt-3 text-lg">Nothing logged yet today.</p>
        <button mat-raised-button color="primary" class="mt-4" (click)="openAddEntry()">Add your first meal</button>
      </div>
    </ng-container>
  `,
})
export class DailyTrackerComponent implements OnInit {
  private store = inject(Store);
  private dialog = inject(MatDialog);
  today = new Date().toISOString().split('T')[0];
  log$ = this.store.select(selectTodayLog);
  loading$ = this.store.select(selectDietLoading);
  mealTypes = Object.keys(MEAL_LABELS);

  ngOnInit(): void {
    this.store.dispatch(DietActions.loadTodayLog({ date: this.today }));
    this.store.dispatch(DietActions.loadFoods({}));
  }

  mealLabel(type: string): string { return MEAL_LABELS[type] ?? type; }

  entriesForMeal(entries: any[], mealType: string): any[] {
    return entries?.filter((e) => e.meal_type === mealType) ?? [];
  }

  caloriePercent(log: any): number {
    return Math.min(((log.total_calories / 2000) * 100), 100);
  }

  openAddEntry(): void {
    const ref = this.dialog.open(AddEntryDialogComponent, { width: '480px' });
    ref.afterClosed().subscribe((result) => {
      if (result) this.store.dispatch(DietActions.addLogEntry({ date: this.today, payload: result }));
    });
  }

  deleteEntry(entryId: string): void {
    if (confirm('Remove this entry?')) {
      this.store.dispatch(DietActions.deleteLogEntry({ date: this.today, entryId }));
    }
  }
}
