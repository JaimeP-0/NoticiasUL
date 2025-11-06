import { getAuthHeaders } from './authService';

const BACKEND_BASE_URL = 'http://127.0.0.1:5000/api';

export interface User {
	idUsuario: number;
	usuario: string;
	nombre?: string;
	email?: string;
	rol: 'superadmin' | 'admin' | 'maestro' | 'usuario';
	fecha_creacion?: string;
}

export async function fetchUsers(): Promise<User[]> {
	const res = await fetch(`${BACKEND_BASE_URL}/users`, {
		method: 'GET',
		headers: getAuthHeaders(),
	});
	if (!res.ok) {
		let msg = `Error obteniendo usuarios: ${res.status}`;
		try {
			const d = await res.json();
			if (d?.error) msg = d.error;
		} catch {}
		throw new Error(msg);
	}
	return await res.json();
}

export async function createUser(payload: {
	usuario: string;
	password: string;
	nombre?: string;
	email?: string;
	rol: 'superadmin' | 'admin' | 'maestro' | 'usuario';
}): Promise<User> {
	const res = await fetch(`${BACKEND_BASE_URL}/users`, {
		method: 'POST',
		headers: getAuthHeaders(),
		body: JSON.stringify(payload),
	});
	if (!res.ok) {
		let msg = `Error creando usuario: ${res.status}`;
		try {
			const d = await res.json();
			if (d?.error) msg = d.error;
		} catch {}
		throw new Error(msg);
	}
	const data = await res.json();
	return data.usuario as User;
}

export async function updateUser(userId: number, payload: {
	rol?: 'superadmin' | 'admin' | 'maestro' | 'usuario';
	nombre?: string;
	email?: string;
}): Promise<User> {
	const res = await fetch(`${BACKEND_BASE_URL}/users/${userId}`, {
		method: 'PUT',
		headers: getAuthHeaders(),
		body: JSON.stringify(payload),
	});
	if (!res.ok) {
		let msg = `Error actualizando usuario: ${res.status}`;
		try {
			const d = await res.json();
			if (d?.error) msg = d.error;
		} catch {}
		throw new Error(msg);
	}
	const data = await res.json();
	return data.usuario as User;
}

