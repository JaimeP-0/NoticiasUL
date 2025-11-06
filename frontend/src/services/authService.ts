import type { LoginCredentials, RegisterCredentials, AuthResponse } from '../models/User';

const BACKEND_BASE_URL = 'http://127.0.0.1:5000/api';

export async function register(credentials: RegisterCredentials): Promise<AuthResponse> {
	try {
		console.log('Intentando registro con:', { username: credentials.username });
		
		const res = await fetch(`${BACKEND_BASE_URL}/register`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				usuario: credentials.username,
				password: credentials.password,
				nombre: credentials.nombre || '',
				email: credentials.email || ''
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
			
			console.error('Error en registro:', errorData);
			return {
				success: false,
				message: errorData.error || 'Error al registrar usuario',
			};
		}

		const data = await res.json();
		console.log('Registro exitoso:', data);
		return {
			success: true,
			message: data.mensaje || 'Registro exitoso',
			user: { 
				username: data.usuario || credentials.username,
				nombre: data.nombre,
				rol: data.rol || 'usuario'
			},
		};
	} catch (error: any) {
		console.error('Error al hacer registro:', error);
		return {
			success: false,
			message: error.message || 'Error al conectarse con el servidor. Verifica que el backend Flask esté corriendo.',
		};
	}
}

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
		const rol = data.rol || 'usuario';
		
		return {
			success: true,
			message: data.mensaje || 'Login exitoso',
			user: { 
				username: data.usuario || credentials.username,
				nombre: data.nombre,
				rol: rol
			},
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
	localStorage.removeItem('auth_role');
	localStorage.removeItem('auth_nombre');
}

export function isAuthenticated(): boolean {
	return !!localStorage.getItem('auth_user');
}

export function getCurrentUser(): string | null {
	return localStorage.getItem('auth_user');
}

export function getCurrentRole(): string {
	return localStorage.getItem('auth_role') || 'usuario';
}

export function getCurrentNombre(): string | null {
	return localStorage.getItem('auth_nombre');
}

export function hasPermission(permission: 'view' | 'create' | 'edit' | 'delete' | 'manage_users' | 'manage_admins'): boolean {
	const role = getCurrentRole();
	const permissions: Record<string, Record<string, boolean>> = {
		'superadmin': {
			'view': true,
			'create': true,
			'edit': true,
			'delete': true,
			'manage_users': true,
			'manage_admins': true
		},
		'admin': {
			'view': true,
			'create': true,
			'edit': true,
			'delete': true,
			'manage_users': false,
			'manage_admins': false
		},
		'maestro': {
			'view': true,
			'create': true,
			'edit': false,
			'delete': false,
			'manage_users': false,
			'manage_admins': false
		},
		'usuario': {
			'view': true,
			'create': false,
			'edit': false,
			'delete': false,
			'manage_users': false,
			'manage_admins': false
		}
	};
	
	return permissions[role]?.[permission] || false;
}

export function getAuthHeaders(): Record<string, string> {
	const role = getCurrentRole();
	return {
		'Content-Type': 'application/json',
		'X-User-Role': role
	};
}

