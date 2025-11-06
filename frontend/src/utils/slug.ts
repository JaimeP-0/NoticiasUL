/**
 * Convierte un texto a formato slug (URL-friendly)
 * Ejemplo: "Mi Noticia Importante" -> "mi-noticia-importante"
 */
export function generarSlug(texto: string): string {
	if (!texto) return '';
	
	return texto
		.toString()
		.toLowerCase()
		.trim()
		// Reemplazar espacios y caracteres especiales con guiones
		.replace(/\s+/g, '-')
		// Reemplazar acentos y caracteres especiales
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		// Eliminar caracteres no alfanuméricos excepto guiones
		.replace(/[^a-z0-9-]/g, '')
		// Reemplazar múltiples guiones con uno solo
		.replace(/-+/g, '-')
		// Eliminar guiones al inicio y final
		.replace(/^-+|-+$/g, '')
		// Limitar longitud (máximo 100 caracteres)
		.substring(0, 100)
		.replace(/-+$/, ''); // Eliminar guión final si quedó
}

