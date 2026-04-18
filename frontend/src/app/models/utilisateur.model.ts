export interface Utilisateur {
  id?: number;
  nom: string;
  email: string;
  motDePasse?: string;
  roleId?: number;
  roleNom?: string;
  actif: boolean;
}
