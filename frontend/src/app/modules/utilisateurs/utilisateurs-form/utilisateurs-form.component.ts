import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Utilisateur } from '../../../models/utilisateur.model';
import { Role } from '../../../models/role.model';
import { UtilisateurService } from '../../../services/utilisateur.service';
import { RoleService } from '../../../services/role.service';

@Component({
  selector: 'app-utilisateurs-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './utilisateurs-form.component.html'
})
export class UtilisateursFormComponent implements OnInit {
  form!: FormGroup;
  roles: Role[] = [];
  loading = false;
  saving = false;
  error = '';
  isEditMode = false;
  utilisateurId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private utilisateurService: UtilisateurService,
    private roleService: RoleService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.utilisateurId = this.route.snapshot.params['id'] ? +this.route.snapshot.params['id'] : null;
    this.isEditMode = !!this.utilisateurId;

    this.form = this.fb.group({
      nom: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      motDePasse: ['', this.isEditMode ? [] : [Validators.required, Validators.minLength(6)]],
      roleId: [null],
      actif: [true]
    });

    this.roleService.getAll().subscribe({ next: (roles) => (this.roles = roles) });

    if (this.isEditMode) {
      this.loading = true;
      this.utilisateurService.getById(this.utilisateurId!).subscribe({
        next: (u) => {
          this.form.patchValue({
            nom: u.nom,
            email: u.email,
            roleId: u.roleId || null,
            actif: u.actif
          });
          this.loading = false;
        },
        error: () => {
          this.error = 'Utilisateur non trouvé.';
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
    const payload: Utilisateur = { ...this.form.value };

    const request$ = this.isEditMode
      ? this.utilisateurService.update(this.utilisateurId!, payload)
      : this.utilisateurService.create(payload);

    request$.subscribe({
      next: () => this.router.navigate(['/utilisateurs']),
      error: (err) => {
        this.error = err.error?.message || 'Erreur lors de l\'enregistrement.';
        this.saving = false;
      }
    });
  }
}
