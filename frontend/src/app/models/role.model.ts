import { Permission } from './permission.model';

export interface Role {
  id?: number;
  nom: string;
  description: string;
  permissions?: Permission[];
  permissionIds?: number[];
}
