export interface NewsItem {
	id: number;
	titulo: string;
	contenido: string;
	autor: string;
	nombre_autor?: string;  // Nombre completo del usuario desde usuarios_nul.nombre
	fecha: string;
	imagen?: string;
}
