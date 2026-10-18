import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { switchMap, map, catchError } from 'rxjs/operators';
import { environment } from '../../../environments/environment';
import * as DietActions from './diet.actions';

@Injectable()
export class DietEffects {
  private readonly api = environment.apiUrl;

  constructor(private actions$: Actions, private http: HttpClient) {}

  loadFoods$ = createEffect(() =>
    this.actions$.pipe(
      ofType(DietActions.loadFoods),
      switchMap(({ q, category, page }) => {
        let params = new HttpParams().set('page', page ?? 1);
        if (q) params = params.set('q', q);
        if (category) params = params.set('category', category);
        return this.http.get<any>(`${this.api}/foods`, { params }).pipe(
          map((res) => DietActions.loadFoodsSuccess({ foods: res.data, meta: res.meta })),
          catchError((err) => of(DietActions.dietError({ error: err.error?.error?.message ?? 'Load failed' })))
        );
      })
    )
  );

  createFood$ = createEffect(() =>
    this.actions$.pipe(
      ofType(DietActions.createFood),
      switchMap(({ payload }) =>
        this.http.post<any>(`${this.api}/foods`, payload).pipe(
          map((res) => DietActions.createFoodSuccess({ food: res.data })),
          catchError((err) => of(DietActions.dietError({ error: err.error?.error?.message ?? 'Create failed' })))
        )
      )
    )
  );

  deleteFood$ = createEffect(() =>
    this.actions$.pipe(
      ofType(DietActions.deleteFood),
      switchMap(({ id }) =>
        this.http.delete<any>(`${this.api}/foods/${id}`).pipe(
          map(() => DietActions.deleteFoodSuccess({ id })),
          catchError((err) => of(DietActions.dietError({ error: err.error?.error?.message ?? 'Delete failed' })))
        )
      )
    )
  );

  loadTodayLog$ = createEffect(() =>
    this.actions$.pipe(
      ofType(DietActions.loadTodayLog),
      switchMap(({ date }) =>
        this.http.get<any>(`${this.api}/diet/logs/${date}`).pipe(
          map((res) => DietActions.loadTodayLogSuccess({ log: res.data })),
          catchError((err) => of(DietActions.dietError({ error: err.error?.error?.message ?? 'Load failed' })))
        )
      )
    )
  );

  addLogEntry$ = createEffect(() =>
    this.actions$.pipe(
      ofType(DietActions.addLogEntry),
      switchMap(({ date, payload }) =>
        this.http.post<any>(`${this.api}/diet/logs/${date}/entries`, payload).pipe(
          map((res) => DietActions.addLogEntrySuccess({ log: res.data })),
          catchError((err) => of(DietActions.dietError({ error: err.error?.error?.message ?? 'Add failed' })))
        )
      )
    )
  );

  deleteLogEntry$ = createEffect(() =>
    this.actions$.pipe(
      ofType(DietActions.deleteLogEntry),
      switchMap(({ date, entryId }) =>
        this.http.delete<any>(`${this.api}/diet/logs/${date}/entries/${entryId}`).pipe(
          map((res) => DietActions.deleteLogEntrySuccess({ log: res.data })),
          catchError((err) => of(DietActions.dietError({ error: err.error?.error?.message ?? 'Delete failed' })))
        )
      )
    )
  );
}
