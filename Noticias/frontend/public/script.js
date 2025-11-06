/**
 * Archivo: script.js
 * Descripción: Funciones JavaScript para conectar con el backend Flask
 * 
 * NOTA: Las funciones principales están en index.astro dentro de <script>
 * Este archivo puede usarse para funciones adicionales o compartidas
 */

// URL base del backend Flask
const API_BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Obtener configuración de la aplicación
 * @returns {Promise<Object>} Objeto con la configuración
 */
async function obtenerConfiguracion() {
	try {
		const response = await fetch(`${API_BASE_URL}/config`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		
		if (!response.ok) {
			throw new Error(`Error al obtener configuración: ${response.status}`);
		}
		
		const config = await response.json();
		return config;
	} catch (error) {
		console.error('Error al obtener configuración:', error);
		throw error;
	}
}

/**
 * Obtener URL de imagen desde Firebase Storage
 * Función preparada para cuando se implemente Firebase Storage
 * @param {string} nombreArchivo - Nombre del archivo en Firebase Storage
 * @returns {string} URL completa de la imagen
 */
function obtenerUrlImagenFirebase(nombreArchivo) {
	// TODO: Implementar lógica real de Firebase Storage
	const baseUrl = 'https://firebasestorage.googleapis.com/v0/b/noticias-ul.appspot.com/o/';
	return `${baseUrl}imagenes%2F${nombreArchivo}?alt=media`;
}

// Exportar funciones para uso global si es necesario
if (typeof window !== 'undefined') {
	window.obtenerConfiguracion = obtenerConfiguracion;
	window.obtenerUrlImagenFirebase = obtenerUrlImagenFirebase;
}
