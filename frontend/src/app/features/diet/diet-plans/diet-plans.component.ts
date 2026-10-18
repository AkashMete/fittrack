import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-diet-plans',
  standalone: true,
  imports: [CommonModule, RouterModule, MatCardModule, MatButtonModule, MatIconModule],
  template: `
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Diet Plans</h1>
      <button mat-raised-button color="primary">
        <mat-icon>add</mat-icon> New Plan
      </button>
    </div>
    <div class="text-center py-16 text-gray-500">
      <mat-icon class="text-5xl">event_note</mat-icon>
      <p class="mt-3 text-lg">No diet plans yet.</p>
      <p class="text-sm mt-1">Create a plan to define your daily meals as a template.</p>
    </div>
  `,
})
export class DietPlansComponent {}
