import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { selectFoods } from '../../../store/diet/diet.selectors';
import { FoodItem } from '../../../store/diet/diet.actions';

@Component({
  selector: 'app-add-entry-dialog',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatDialogModule, MatFormFieldModule, MatInputModule, MatSelectModule, MatButtonModule, MatAutocompleteModule],
  template: `
    <h2 mat-dialog-title>Log Food Entry</h2>
    <mat-dialog-content style="min-width:380px;padding-top:12px">
      <form [formGroup]="form" id="entryForm" (ngSubmit)="submit()" class="flex flex-col gap-3">
        <mat-form-field class="w-full">
          <mat-label>Food item *</mat-label>
          <input matInput formControlName="food_name" [matAutocomplete]="auto" placeholder="Type to search..." />
          <mat-autocomplete #auto="matAutocomplete" (optionSelected)="onFoodSelected($event)">
            <mat-option *ngFor="let food of filteredFoods" [value]="food.name" [id]="food.id">
              {{ food.name }} <span class="text-gray-400 text-xs ml-2">{{ food.calories_per_100g }} kcal/100g</span>
            </mat-option>
          </mat-autocomplete>
        </mat-form-field>

        <mat-form-field class="w-full">
          <mat-label>Quantity (g) *</mat-label>
          <input matInput type="number" formControlName="quantity_g" />
        </mat-form-field>

        <mat-form-field class="w-full">
          <mat-label>Meal *</mat-label>
          <mat-select formControlName="meal_type">
            <mat-option value="breakfast">Breakfast</mat-option>
            <mat-option value="lunch">Lunch</mat-option>
            <mat-option value="dinner">Dinner</mat-option>
            <mat-option value="snack">Snack</mat-option>
            <mat-option value="pre_workout">Pre-Workout</mat-option>
            <mat-option value="post_workout">Post-Workout</mat-option>
          </mat-select>
        </mat-form-field>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" form="entryForm" type="submit" [disabled]="form.invalid">Log</button>
    </mat-dialog-actions>
  `,
})
export class AddEntryDialogComponent implements OnInit {
  form: FormGroup;
  allFoods: FoodItem[] = [];
  filteredFoods: FoodItem[] = [];
  selectedFoodId: string | null = null;

  constructor(
    private fb: FormBuilder,
    private dialogRef: MatDialogRef<AddEntryDialogComponent>,
    private store: Store
  ) {
    this.form = this.fb.group({
      food_name: ['', Validators.required],
      food_item_id: ['', Validators.required],
      quantity_g: [100, [Validators.required, Validators.min(0.1)]],
      meal_type: ['lunch', Validators.required],
    });
  }

  ngOnInit(): void {
    this.store.select(selectFoods).subscribe((foods) => {
      this.allFoods = foods;
      this.filteredFoods = foods;
    });
    this.form.get('food_name')!.valueChanges.subscribe((v) => {
      const q = (v ?? '').toLowerCase();
      this.filteredFoods = this.allFoods.filter((f) => f.name.toLowerCase().includes(q));
    });
  }

  onFoodSelected(event: any): void {
    const food = this.allFoods.find((f) => f.name === event.option.value);
    if (food) this.form.patchValue({ food_item_id: food.id });
  }

  submit(): void {
    if (this.form.valid) {
      const { food_name, ...rest } = this.form.value;
      this.dialogRef.close(rest);
    }
  }
}
