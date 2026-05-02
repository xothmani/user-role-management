import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Permission } from '../models/permission.model';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class PermissionService {
  private readonly API = `${environment.apiUrl}/api/permissions`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Permission[]> {
    return this.http.get<Permission[]>(this.API);
  }

  create(permission: Permission): Observable<Permission> {
    return this.http.post<Permission>(this.API, permission);
  }

  update(id: number, permission: Permission): Observable<Permission> {
    return this.http.put<Permission>(`${this.API}/${id}`, permission);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}`);
  }
}
