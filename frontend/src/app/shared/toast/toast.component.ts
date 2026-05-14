import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { Toast, ToastService } from '../../core/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './toast.component.html'
})
export class ToastComponent implements OnInit, OnDestroy {
  toasts: Toast[] = [];
  private sub!: Subscription;

  constructor(private toastService: ToastService) {}

  ngOnInit(): void {
    this.sub = this.toastService.toast$.subscribe(toast => {
      this.toasts.push(toast);
      setTimeout(() => this.dismiss(toast.id), 4500);
    });
  }

  ngOnDestroy(): void {
    this.sub.unsubscribe();
  }

  dismiss(id: number): void {
    this.toasts = this.toasts.filter(t => t.id !== id);
  }

  iconClass(type: Toast['type']): string {
    return type === 'error'   ? 'bi-exclamation-circle-fill'
         : type === 'warning' ? 'bi-exclamation-triangle-fill'
                              : 'bi-info-circle-fill';
  }

  alertClass(type: Toast['type']): string {
    return type === 'error'   ? 'alert-danger'
         : type === 'warning' ? 'alert-warning'
                              : 'alert-info';
  }
}