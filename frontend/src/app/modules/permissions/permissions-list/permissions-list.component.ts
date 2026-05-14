import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Permission } from '../../../models/permission.model';
import { PermissionService } from '../../../services/permission.service';
import { ConfirmDialogComponent } from '../../../shared/confirm-dialog/confirm-dialog.component';

@Component({
  selector: 'app-permissions-list',
  standalone: true,
  imports: [CommonModule, RouterLink, ConfirmDialogComponent],
  templateUrl: './permissions-list.component.html'
})
export class PermissionsListComponent implements OnInit {
  permissions: Permission[] = [];
  loading = false;
  error = '';
  deleteTargetId: number | null = null;
  showConfirm = false;

  constructor(private permissionService: PermissionService) {}

  ngOnInit(): void {
    this.loadPermissions();
  }

  loadPermissions(): void {
    this.loading = true;
    this.permissionService.getAll().subscribe({
      next: (data) => {
        this.permissions = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Erreur lors du chargement des permissions.';
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
    this.permissionService.delete(this.deleteTargetId).subscribe({
      next: () => {
        this.permissions = this.permissions.filter(p => p.id !== this.deleteTargetId);
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