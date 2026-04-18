import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.component.html'
})
export class LoginComponent {
  loginForm: FormGroup;
  loading = false;
  error = '';
  showPassword = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/utilisateurs']);
    }
    this.loginForm = this.fb.group({
      email: ['admin@app.com', [Validators.required, Validators.email]],
      motDePasse: ['Admin@123', [Validators.required, Validators.minLength(6)]]
    });
  }

  get f() {
    return this.loginForm.controls;
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }
    this.loading = true;
    this.error = '';
    const { email, motDePasse } = this.loginForm.value;
    this.authService.login(email, motDePasse).subscribe({
      next: () => {
        this.router.navigate(['/utilisateurs']);
      },
      error: (err) => {
        this.loading = false;
        this.error = err.status === 401
          ? 'Email ou mot de passe incorrect.'
          : 'Erreur de connexion. Vérifiez que le serveur est démarré.';
      }
    });
  }
}
