import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Utilisateur } from '../models/utilisateur.model';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class UtilisateurService {
  private readonly API = `${environment.apiUrl}/api/utilisateurs`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Utilisateur[]> {
    return this.http.get<Utilisateur[]>(this.API);
  }

  getById(id: number): Observable<Utilisateur> {
    return this.http.get<Utilisateur>(`${this.API}/${id}`);
  }

  create(utilisateur: Utilisateur): Observable<Utilisateur> {
    return this.http.post<Utilisateur>(this.API, utilisateur);
  }

  update(id: number, utilisateur: Utilisateur): Observable<Utilisateur> {
    return this.http.put<Utilisateur>(`${this.API}/${id}`, utilisateur);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}`);
  }

  assignRole(utilisateurId: number, roleId: number): Observable<Utilisateur> {
    return this.http.post<Utilisateur>(`${this.API}/${utilisateurId}/role/${roleId}`, {});
  }
}
