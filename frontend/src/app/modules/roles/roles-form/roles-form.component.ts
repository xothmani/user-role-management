import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Permission } from '../../../models/permission.model';
import { Role } from '../../../models/role.model';
import { RoleService } from '../../../services/role.service';
import { PermissionService } from '../../../services/permission.service';

@Component({
  selector: 'app-roles-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './roles-form.component.html'
})
export class RolesFormComponent implements OnInit {
  form!: FormGroup;
  allPermissions: Permission[] = [];
  selectedPermissionIds: Set<number> = new Set();
  loading = false;
  saving = false;
  error = '';
  isEditMode = false;
  roleId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private roleService: RoleService,
    private permissionService: PermissionService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.roleId = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    this.isEditMode = !!this.roleId;

    this.form = this.fb.group({
      nom: ['', [Validators.required, Validators.minLength(2)]],
      description: ['']
    });

    this.permissionService.getAll().subscribe({ next: (perms) => (this.allPermissions = perms) });

    if (this.isEditMode) {
      this.loading = true;
      this.roleService.getById(this.roleId!).subscribe({
        next: (role: Role) => {
          this.form.patchValue({ nom: role.nom, description: role.description });
          role.permissions?.forEach(p => { if (p.id) this.selectedPermissionIds.add(p.id); });
          this.loading = false;
        },
        error: () => {
          this.error = 'Rôle non trouvé.';
          this.loading = false;
        }
      });
    }
  }

  get f() {
    return this.form.controls;
  }

  isPermissionSelected(id: number): boolean {
    return this.selectedPermissionIds.has(id);
  }

  togglePermission(id: number): void {
    if (this.selectedPermissionIds.has(id)) {
      this.selectedPermissionIds.delete(id);
    } else {
      this.selectedPermissionIds.add(id);
    }
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.saving = true;
    this.error = '';
    const payload: Role = {
      ...this.form.value,
      permissionIds: Array.from(this.selectedPermissionIds)
    };

    const request$ = this.isEditMode
      ? this.roleService.update(this.roleId!, payload)
      : this.roleService.create(payload);

    request$.subscribe({
      next: () => this.router.navigate(['/roles']),
      error: (err) => {
        this.error = err.error?.message || 'Erreur lors de l\'enregistrement.';
        this.saving = false;
      }
    });
  }
}
