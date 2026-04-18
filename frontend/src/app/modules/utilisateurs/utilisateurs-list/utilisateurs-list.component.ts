import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Utilisateur } from '../../../models/utilisateur.model';
import { UtilisateurService } from '../../../services/utilisateur.service';
import { ConfirmDialogComponent } from '../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-utilisateurs-list',
  standalone: true,
  imports: [CommonModule, RouterLink, ConfirmDialogComponent],
  templateUrl: './utilisateurs-list.component.html'
})
export class UtilisateursListComponent implements OnInit {
  utilisateurs: Utilisateur[] = [];
  loading = false;
  error = '';
  deleteTargetId: number | null = null;
  showConfirm = false;

  constructor(private utilisateurService: UtilisateurService) {}

  ngOnInit(): void {
    this.loadUtilisateurs();
  }

  loadUtilisateurs(): void {
    this.loading = true;
    this.utilisateurService.getAll().subscribe({
      next: (data) => {
        this.utilisateurs = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Erreur lors du chargement des utilisateurs.';
        this.loading = false;
      }
    });
  }

  confirmDelete(id: number): void {
    this.deleteTargetId = id;
    this.showConfirm = true;
  }

  onDeleteConfirmed(): void {
    if (this.deleteTargetId === null) return;
    this.utilisateurService.delete(this.deleteTargetId).subscribe({
      next: () => {
        this.utilisateurs = this.utilisateurs.filter(u => u.id !== this.deleteTargetId);
        this.showConfirm = false;
        this.deleteTargetId = null;
      },
      error: () => {
        this.error = 'Erreur lors de la suppression.';
        this.showConfirm = false;
      }
    });
  }

  onDeleteCancelled(): void {
    this.showConfirm = false;
    this.deleteTargetId = null;
  }
}
