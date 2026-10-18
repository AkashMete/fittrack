import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Store } from '@ngrx/store';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { selectUser } from '../../store/auth/auth.selectors';
import { environment } from '../../../environments/environment';
import * as AuthActions from '../../store/auth/auth.actions';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatSnackBarModule],
  template: `
    <h1 class="text-2xl font-bold mb-6">My Profile</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <mat-card class="p-6">
        <h2 class="text-lg font-semibold mb-4">Personal Information</h2>
        <form [formGroup]="form" (ngSubmit)="save()" class="flex flex-col gap-4">
          <div class="flex gap-3">
            <mat-form-field class="flex-1">
              <mat-label>First name</mat-label>
              <input matInput formControlName="first_name" />
            </mat-form-field>
            <mat-form-field class="flex-1">
              <mat-label>Last name</mat-label>
              <input matInput formControlName="last_name" />
            </mat-form-field>
          </div>
          <mat-form-field>
            <mat-label>Height (cm)</mat-label>
            <input matInput type="number" formControlName="height_cm" />
          </mat-form-field>
          <button mat-raised-button color="primary" type="submit">Save Changes</button>
        </form>
      </mat-card>

      <mat-card class="p-6">
        <h2 class="text-lg font-semibold mb-4">Daily Targets</h2>
        <form [formGroup]="targetsForm" (ngSubmit)="saveTargets()" class="flex flex-col gap-4">
          <mat-form-field>
            <mat-label>Calorie target (kcal)</mat-label>
            <input matInput type="number" formControlName="daily_calorie_target" />
          </mat-form-field>
          <mat-form-field>
            <mat-label>Protein target (g)</mat-label>
            <input matInput type="number" formControlName="daily_protein_target_g" />
          </mat-form-field>
          <mat-form-field>
            <mat-label>Carbs target (g)</mat-label>
            <input matInput type="number" formControlName="daily_carbs_target_g" />
          </mat-form-field>
          <mat-form-field>
            <mat-label>Fat target (g)</mat-label>
            <input matInput type="number" formControlName="daily_fat_target_g" />
          </mat-form-field>
          <button mat-raised-button color="primary" type="submit">Save Targets</button>
        </form>
      </mat-card>
    </div>
  `,
})
export class ProfileComponent {
  form: FormGroup;
  targetsForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private store: Store,
    private snack: MatSnackBar
  ) {
    this.form = this.fb.group({ first_name: [''], last_name: [''], height_cm: [null] });
    this.targetsForm = this.fb.group({
      daily_calorie_target: [2000],
      daily_protein_target_g: [150],
      daily_carbs_target_g: [200],
      daily_fat_target_g: [65],
    });
    this.store.select(selectUser).subscribe((u) => {
      if (u) {
        this.form.patchValue(u as any);
        this.targetsForm.patchValue(u as any);
      }
    });
  }

  save(): void {
    this.http.patch(`${environment.apiUrl}/users/me`, this.form.value).subscribe({
      next: (res: any) => {
        this.store.dispatch(AuthActions.loadProfileSuccess({ user: res.data }));
        this.snack.open('Profile saved!', 'OK', { duration: 3000 });
      },
    });
  }

  saveTargets(): void {
    this.http.patch(`${environment.apiUrl}/users/me`, this.targetsForm.value).subscribe({
      next: (res: any) => {
        this.store.dispatch(AuthActions.loadProfileSuccess({ user: res.data }));
        this.snack.open('Targets saved!', 'OK', { duration: 3000 });
      },
    });
  }
}
