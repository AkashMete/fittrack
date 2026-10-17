import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { Store } from '@ngrx/store';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import * as AuthActions from '../../../store/auth/auth.actions';
import { selectAuthLoading, selectAuthError } from '../../../store/auth/auth.selectors';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule, MatProgressSpinnerModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-gray-50">
      <mat-card class="w-full max-w-md p-6 shadow-lg">
        <mat-card-header>
          <mat-card-title class="text-2xl font-bold mb-4">Create your account</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <form [formGroup]="form" (ngSubmit)="onSubmit()" class="flex flex-col gap-4">
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

            <mat-form-field class="w-full">
              <mat-label>Email</mat-label>
              <input matInput type="email" formControlName="email" autocomplete="email" />
              <mat-error *ngIf="form.get('email')?.hasError('email')">Enter a valid email</mat-error>
            </mat-form-field>

            <mat-form-field class="w-full">
              <mat-label>Password (min 8 characters)</mat-label>
              <input matInput type="password" formControlName="password" autocomplete="new-password" />
              <mat-error *ngIf="form.get('password')?.hasError('minlength')">At least 8 characters</mat-error>
            </mat-form-field>

            <p *ngIf="error$ | async as err" class="text-red-600 text-sm">{{ err }}</p>

            <button mat-raised-button color="primary" type="submit" [disabled]="form.invalid || (loading$ | async)">
              <mat-spinner *ngIf="loading$ | async" diameter="20" class="inline-block mr-2"></mat-spinner>
              Create Account
            </button>
          </form>
        </mat-card-content>
        <mat-card-footer class="text-center p-4">
          <a routerLink="/auth/login" class="text-blue-600 hover:underline">Already have an account? Sign in</a>
        </mat-card-footer>
      </mat-card>
    </div>
  `,
})
export class RegisterComponent {
  private store = inject(Store);
  form: FormGroup;
  loading$ = this.store.select(selectAuthLoading);
  error$ = this.store.select(selectAuthError);

  constructor(private fb: FormBuilder) {
    this.form = this.fb.group({
      first_name: [''],
      last_name: [''],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });
  }

  onSubmit(): void {
    if (this.form.valid) {
      this.store.dispatch(AuthActions.register(this.form.value));
    }
  }
}
