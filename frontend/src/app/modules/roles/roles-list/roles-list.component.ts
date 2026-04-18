import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Role } from '../../../models/role.model';
import { RoleService } from '../../../services/role.service';
import { ConfirmDialogComponent } from '../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-roles-list',
  standalone: true,
  imports: [CommonModule, RouterLink, ConfirmDialogComponent],
  templateUrl: './roles-list.component.html'
})
export class RolesListComponent implements OnInit {
  roles: Role[] = [];
  loading = false;
  error = '';
  deleteTargetId: number | null = null;
  showConfirm = false;

  constructor(private roleService: RoleService) {}

  ngOnInit(): void {
    this.loadRoles();
  }

  loadRoles(): void {
    this.loading = true;
    this.roleService.getAll().subscribe({
      next: (data) => {
        this.roles = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Erreur lors du chargement des rôles.';
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
    this.roleService.delete(this.deleteTargetId).subscribe({
      next: () => {
        this.roles = this.roles.filter(r => r.id !== this.deleteTargetId);
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
