import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HistoriqueAction } from '../models/historique.model';

@Injectable({ providedIn: 'root' })
export class HistoriqueService {
  private readonly API = 'http://localhost:8080/api/historique';

  constructor(private http: HttpClient) {}

  getAll(userId?: number, dateDebut?: string, dateFin?: string): Observable<HistoriqueAction[]> {
    let params = new HttpParams();
    if (userId) params = params.set('userId', userId.toString());
    if (dateDebut) params = params.set('dateDebut', dateDebut);
    if (dateFin) params = params.set('dateFin', dateFin);
    return this.http.get<HistoriqueAction[]>(this.API, { params });
  }
}
