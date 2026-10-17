import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { Store } from '@ngrx/store';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { selectFoods, selectDietLoading, selectFoodsMeta } from '../../../store/diet/diet.selectors';
import * as DietActions from '../../../store/diet/diet.actions';
import { CreateFoodDialogComponent } from './create-food-dialog.component';

const CATEGORIES = ['protein','carbs','fats','vegetables','fruits','dairy','grains','supplements'];

@Component({
  selector: 'app-food-library',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatCardModule, MatInputModule, MatFormFieldModule, MatButtonModule, MatIconModule, MatChipsModule, MatProgressSpinnerModule, MatSelectModule, MatDialogModule],
  template: `
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Food Library</h1>
      <button mat-raised-button color="primary" (click)="openCreateDialog()">
        <mat-icon>add</mat-icon> Add Food
      </button>
    </div>

    <div class="flex gap-4 mb-6">
      <mat-form-field class="flex-1">
        <mat-label>Search foods</mat-label>
        <mat-icon matPrefix>search</mat-icon>
        <input matInput [formControl]="searchCtrl" placeholder="e.g. Chicken Breast" />
      </mat-form-field>

      <mat-form-field class="w-48">
        <mat-label>Category</mat-label>
        <mat-select [formControl]="categoryCtrl">
          <mat-option value="">All categories</mat-option>
          <mat-option *ngFor="let c of categories" [value]="c">{{ c | titlecase }}</mat-option>
        </mat-select>
      </mat-form-field>
    </div>

    <div *ngIf="loading$ | async" class="flex justify-center py-12">
      <mat-spinner diameter="40"></mat-spinner>
    </div>

    <div *ngIf="!(loading$ | async)" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      <mat-card *ngFor="let food of foods$ | async" class="p-4 hover:shadow-md transition-shadow cursor-pointer">
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="font-semibold text-gray-900 leading-tight">{{ food.name }}</h3>
            <p *ngIf="food.brand" class="text-xs text-gray-500">{{ food.brand }}</p>
          </div>
          <span class="text-xs font-medium px-2 py-1 rounded-full bg-blue-100 text-blue-700 capitalize">
            {{ food.category || '—' }}
          </span>
        </div>
        <div class="grid grid-cols-2 gap-x-3 gap-y-1 text-xs text-gray-600 mt-3">
          <span><strong>{{ food.calories_per_100g }}</strong> kcal</span>
          <span><strong>{{ food.protein_per_100g }}g</strong> protein</span>
          <span><strong>{{ food.carbs_per_100g }}g</strong> carbs</span>
          <span><strong>{{ food.fat_per_100g }}g</strong> fat</span>
        </div>
        <p class="text-xs text-gray-400 mt-2">per 100g</p>
        <div class="flex gap-1 mt-2">
          <span *ngFor="let tag of (food.tags || []) | slice:0:2"
            class="text-xs px-1.5 py-0.5 bg-gray-100 rounded text-gray-500">{{ tag }}</span>
        </div>
        <div *ngIf="!food.is_global" class="mt-2 flex justify-end">
          <button mat-icon-button color="warn" (click)="deleteFood(food.id, $event)">
            <mat-icon>delete</mat-icon>
          </button>
        </div>
      </mat-card>
    </div>

    <div *ngIf="(foods$ | async)?.length === 0 && !(loading$ | async)" class="text-center py-16 text-gray-500">
      <mat-icon class="text-5xl">search_off</mat-icon>
      <p class="mt-3 text-lg">No foods found. Try a different search or add your own.</p>
    </div>
  `,
})
export class FoodLibraryComponent implements OnInit {
  private store = inject(Store);
  private dialog = inject(MatDialog);
  foods$ = this.store.select(selectFoods);
  loading$ = this.store.select(selectDietLoading);
  meta$ = this.store.select(selectFoodsMeta);
  categories = CATEGORIES;

  searchCtrl = new FormControl('');
  categoryCtrl = new FormControl('');

  ngOnInit(): void {
    this.loadFoods();
    this.searchCtrl.valueChanges.pipe(debounceTime(400), distinctUntilChanged())
      .subscribe(() => this.loadFoods());
    this.categoryCtrl.valueChanges.subscribe(() => this.loadFoods());
  }

  loadFoods(): void {
    this.store.dispatch(DietActions.loadFoods({
      q: this.searchCtrl.value || undefined,
      category: this.categoryCtrl.value || undefined,
    }));
  }

  openCreateDialog(): void {
    const ref = this.dialog.open(CreateFoodDialogComponent, { width: '560px' });
    ref.afterClosed().subscribe((result) => {
      if (result) this.store.dispatch(DietActions.createFood({ payload: result }));
    });
  }

  deleteFood(id: string, event: Event): void {
    event.stopPropagation();
    if (confirm('Delete this food item?')) {
      this.store.dispatch(DietActions.deleteFood({ id }));
    }
  }
}
