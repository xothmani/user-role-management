import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { HistoriqueAction } from '../../../models/historique.model';
import { Utilisateur } from '../../../models/utilisateur.model';
import { HistoriqueService } from '../../../services/historique.service';
import { UtilisateurService } from '../../../services/utilisateur.service';

@Component({
  selector: 'app-historique-list',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './historique-list.component.html'
})
export class HistoriqueListComponent implements OnInit {
  historiques: HistoriqueAction[] = [];
  utilisateurs: Utilisateur[] = [];
  filterForm!: FormGroup;
  loading = false;
  error = '';

  constructor(
    private historiqueService: HistoriqueService,
    private utilisateurService: UtilisateurService,
    private fb: FormBuilder
  ) {}

  ngOnInit(): void {
    this.filterForm = this.fb.group({
      userId: [null],
      dateDebut: [''],
      dateFin: ['']
    });
    this.utilisateurService.getAll().subscribe({ next: (data) => (this.utilisateurs = data) });
    this.loadHistorique();
  }

  loadHistorique(): void {
    this.loading = true;
    const { userId, dateDebut, dateFin } = this.filterForm.value;
    this.historiqueService.getAll(
      userId || undefined,
      dateDebut || undefined,
      dateFin || undefined
    ).subscribe({
      next: (data) => {
        this.historiques = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Erreur lors du chargement de l\'historique.';
        this.loading = false;
      }
    });
  }

  onFilter(): void {
    this.loadHistorique();
  }

  resetFilters(): void {
    this.filterForm.reset();
    this.loadHistorique();
  }

  formatDate(dateStr: string): string {
    if (!dateStr) return '—';
    return new Date(dateStr).toLocaleString('fr-FR');
  }

  getActionBadgeClass(action: string): string {
    if (action.includes('create') || action.includes('Create')) return 'bg-success-subtle text-success';
    if (action.includes('update') || action.includes('Update')) return 'bg-warning-subtle text-warning';
    if (action.includes('delete') || action.includes('Delete')) return 'bg-danger-subtle text-danger';
    if (action.includes('assign') || action.includes('Assign')) return 'bg-info-subtle text-info';
    return 'bg-secondary-subtle text-secondary';
  }
}
