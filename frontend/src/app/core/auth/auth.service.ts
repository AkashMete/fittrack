import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap, catchError } from 'rxjs/operators';
import { Observable, throwError } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface AuthUser {
  id: string;
  email: string;
  first_name: string | null;
  last_name: string | null;
}

export interface AuthState {
  user: AuthUser | null;
  accessToken: string | null;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly api = `${environment.apiUrl}/auth`;

  // Access token lives in memory only — never localStorage (XSS defence, ARCHITECTURE.md)
  private _accessToken = signal<string | null>(null);
  private _user = signal<AuthUser | null>(null);

  readonly accessToken = this._accessToken.asReadonly();
  readonly user = this._user.asReadonly();
  readonly isLoggedIn = computed(() => !!this._accessToken());

  constructor(private http: HttpClient, private router: Router) {}

  register(payload: { email: string; password: string; first_name?: string }): Observable<any> {
    return this.http.post(`${this.api}/register`, payload).pipe(
      tap((res: any) => this._handleAuthResponse(res))
    );
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post(`${this.api}/login`, { email, password }, { withCredentials: true }).pipe(
      tap((res: any) => this._handleAuthResponse(res))
    );
  }

  // Called by the auto-refresh interceptor on 401 — sends the httpOnly cookie automatically
  refresh(): Observable<any> {
    return this.http.post(`${this.api}/refresh`, {}, { withCredentials: true }).pipe(
      tap((res: any) => {
        this._accessToken.set(res.data.access_token);
      }),
      catchError((err) => {
        this.clearSession();
        return throwError(() => err);
      })
    );
  }

  logout(): void {
    this.http.post(`${this.api}/logout`, {}, { withCredentials: true }).subscribe({
      complete: () => this.clearSession(),
      error: () => this.clearSession(),
    });
  }

  clearSession(): void {
    this._accessToken.set(null);
    this._user.set(null);
    this.router.navigate(['/auth/login']);
  }

  private _handleAuthResponse(res: any): void {
    this._accessToken.set(res.data.access_token);
    this._user.set(res.data.user);
  }
}
