import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-create-food-dialog',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatDialogModule, MatFormFieldModule, MatInputModule, MatSelectModule, MatButtonModule],
  template: `
    <h2 mat-dialog-title>Add Custom Food</h2>
    <mat-dialog-content class="flex flex-col gap-3 pt-2" style="min-width:400px">
      <form [formGroup]="form" id="foodForm" (ngSubmit)="submit()">
        <mat-form-field class="w-full">
          <mat-label>Name *</mat-label>
          <input matInput formControlName="name" />
        </mat-form-field>

        <mat-form-field class="w-full">
          <mat-label>Brand</mat-label>
          <input matInput formControlName="brand" />
        </mat-form-field>

        <mat-form-field class="w-full">
          <mat-label>Category</mat-label>
          <mat-select formControlName="category">
            <mat-option value="protein">Protein</mat-option>
            <mat-option value="carbs">Carbs</mat-option>
            <mat-option value="fats">Fats</mat-option>
            <mat-option value="vegetables">Vegetables</mat-option>
            <mat-option value="fruits">Fruits</mat-option>
            <mat-option value="dairy">Dairy</mat-option>
            <mat-option value="grains">Grains</mat-option>
            <mat-option value="supplements">Supplements</mat-option>
          </mat-select>
        </mat-form-field>

        <div class="grid grid-cols-2 gap-3">
          <mat-form-field>
            <mat-label>Calories / 100g *</mat-label>
            <input matInput type="number" formControlName="calories_per_100g" />
          </mat-form-field>
          <mat-form-field>
            <mat-label>Protein / 100g (g)</mat-label>
            <input matInput type="number" formControlName="protein_per_100g" />
          </mat-form-field>
          <mat-form-field>
            <mat-label>Carbs / 100g (g)</mat-label>
            <input matInput type="number" formControlName="carbs_per_100g" />
          </mat-form-field>
          <mat-form-field>
            <mat-label>Fat / 100g (g)</mat-label>
            <input matInput type="number" formControlName="fat_per_100g" />
          </mat-form-field>
        </div>

        <mat-form-field class="w-full">
          <mat-label>Default serving (g)</mat-label>
          <input matInput type="number" formControlName="default_serving_g" />
        </mat-form-field>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button mat-dialog-close>Cancel</button>
      <button mat-raised-button color="primary" form="foodForm" type="submit" [disabled]="form.invalid">Save</button>
    </mat-dialog-actions>
  `,
})
export class CreateFoodDialogComponent {
  form: FormGroup;

  constructor(private fb: FormBuilder, private dialogRef: MatDialogRef<CreateFoodDialogComponent>) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      brand: [''],
      category: [''],
      calories_per_100g: [0, [Validators.required, Validators.min(0)]],
      protein_per_100g: [0, Validators.min(0)],
      carbs_per_100g: [0, Validators.min(0)],
      fat_per_100g: [0, Validators.min(0)],
      default_serving_g: [100, Validators.min(0.1)],
    });
  }

  submit(): void {
    if (this.form.valid) this.dialogRef.close(this.form.value);
  }
}
