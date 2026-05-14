import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Permission } from '../../../models/permission.model';
import { PermissionService } from '../../../services/permission.service';

@Component({
  selector: 'app-permissions-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './permissions-form.component.html'
})
export class PermissionsFormComponent implements OnInit {
  form!: FormGroup;
  loading = false;
  saving = false;
  error = '';
  isEditMode = false;
  permissionId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private permissionService: PermissionService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.permissionId = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    this.isEditMode = !!this.permissionId;

    this.form = this.fb.group({
      nom: ['', [Validators.required, Validators.minLength(2)]],
      description: ['']
    });

    if (this.isEditMode) {
      this.loading = true;
      this.permissionService.getById(this.permissionId!).subscribe({
        next: (permission: Permission) => {
          this.form.patchValue({ nom: permission.nom, description: permission.description });
          this.loading = false;
        },
        error: () => {
          this.error = 'Permission non trouvée.';
          this.loading = false;
        }
      });
    }
  }

  get f() {
    return this.form.controls;
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.saving = true;
    this.error = '';
    const payload: Permission = this.form.value;

    const request$ = this.isEditMode
      ? this.permissionService.update(this.permissionId!, payload)
      : this.permissionService.create(payload);

    request$.subscribe({
      next: () => this.router.navigate(['/permissions']),
      error: (err) => {
        this.error = err.error?.message || 'Erreur lors de l\'enregistrement.';
        this.saving = false;
      }
    });
  }
}