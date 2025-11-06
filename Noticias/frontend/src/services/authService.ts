import type { LoginCredentials, AuthResponse } from '../models/User';

const BACKEND_BASE_URL = 'http://127.0.0.1:5000/api';

export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
	try {
		// El backend espera "usuario" en lugar de "username"
		const res = await fetch(`${BACKEND_BASE_URL}/login`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				usuario: credentials.username,
				password: credentials.password
			}),
		});

		if (!res.ok) {
			const errorData = await res.json();
			return {
				success: false,
				message: errorData.error || 'Credenciales incorrectas',
			};
		}

		const data = await res.json();
		return {
			success: true,
			message: data.mensaje || 'Login exitoso',
			user: { username: data.usuario || credentials.username },
		};
	} catch (error: any) {
		return {
			success: false,
			message: error.message || 'Error al iniciar sesión',
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

