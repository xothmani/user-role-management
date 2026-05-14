import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export type ToastType = 'error' | 'warning' | 'info';

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

@Injectable({ providedIn: 'root' })
export class ToastService {
  private counter = 0;
  private subject = new Subject<Toast>();
  readonly toast$ = this.subject.asObservable();

  error(message: string): void {
    this.subject.next({ id: ++this.counter, message, type: 'error' });
  }

  warning(message: string): void {
    this.subject.next({ id: ++this.counter, message, type: 'warning' });
  }

  info(message: string): void {
    this.subject.next({ id: ++this.counter, message, type: 'info' });
  }
}