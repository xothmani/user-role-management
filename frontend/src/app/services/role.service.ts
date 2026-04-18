import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Role } from '../models/role.model';

@Injectable({ providedIn: 'root' })
export class RoleService {
  private readonly API = 'http://localhost:8080/api/roles';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Role[]> {
    return this.http.get<Role[]>(this.API);
  }

  getById(id: number): Observable<Role> {
    return this.http.get<Role>(`${this.API}/${id}`);
  }

  create(role: Role): Observable<Role> {
    return this.http.post<Role>(this.API, role);
  }

  update(id: number, role: Role): Observable<Role> {
    return this.http.put<Role>(`${this.API}/${id}`, role);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}`);
  }

  assignPermissions(roleId: number, permissionIds: number[]): Observable<Role> {
    return this.http.post<Role>(`${this.API}/${roleId}/permissions`, permissionIds);
  }
}
