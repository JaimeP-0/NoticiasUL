import type { LoginCredentials, AuthResponse } from '../models/User';

const BACKEND_BASE_URL = 'http://127.0.0.1:5000/api';

export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
	try {
		console.log('Intentando login con:', { username: credentials.username });
		
		// El backend espera "usuario" en lugar de "username"
		const res = await fetch(`${BACKEND_BASE_URL}/login`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				usuario: credentials.username,
				password: credentials.password
			}),
		});

		console.log('Respuesta del servidor:', res.status, res.statusText);

		if (!res.ok) {
			let errorData;
			try {
				errorData = await res.json();
			} catch {
				errorData = { error: `Error ${res.status}: ${res.statusText}` };
			}
			
			console.error('Error en login:', errorData);
			return {
				success: false,
				message: errorData.error || 'Credenciales incorrectas',
			};
		}

		const data = await res.json();
		console.log('Login exitoso:', data);
		return {
			success: true,
			message: data.mensaje || 'Login exitoso',
			user: { username: data.usuario || credentials.username },
		};
	} catch (error: any) {
		console.error('Error al hacer login:', error);
		return {
			success: false,
			message: error.message || 'Error al conectarse con el servidor. Verifica que el backend Flask esté corriendo.',
		};
	}
}

export function logout(): void {
	localStorage.removeItem('auth_user');
	localStorage.removeItem('auth_token');
}

export function isAuthenticated(): boolean {
	return !!localStorage.getItem('auth_user');
}

export function getCurrentUser(): string | null {
	return localStorage.getItem('auth_user');
}

