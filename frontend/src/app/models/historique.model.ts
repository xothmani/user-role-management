export interface HistoriqueAction {
  id?: number;
  utilisateurId?: number;
  utilisateurNom?: string;
  utilisateurEmail?: string;
  action: string;
  details?: string;
  date: string;
}
