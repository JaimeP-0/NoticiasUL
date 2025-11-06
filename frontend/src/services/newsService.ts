import type { NewsItem } from '../models/News';
import { getAuthHeaders } from './authService';

const BACKEND_BASE_URL = 'http://127.0.0.1:5000/api';

export async function fetchNews(): Promise<NewsItem[]> {
	const res = await fetch(`${BACKEND_BASE_URL}/news`, {
		method: 'GET',
		headers: { 'Content-Type': 'application/json' },
	});
	if (!res.ok) throw new Error(`Error obteniendo noticias: ${res.status}`);
	return await res.json();
}

export async function createNews(payload: Omit<NewsItem, 'id' | 'fecha'>): Promise<NewsItem> {
	const res = await fetch(`${BACKEND_BASE_URL}/news`, {
		method: 'POST',
		headers: getAuthHeaders(),
		body: JSON.stringify(payload),
	});
	if (!res.ok) {
		let msg = `Error creando noticia: ${res.status}`;
		try {
			const d = await res.json();
			if (d?.error) msg = d.error;
		} catch {}
		throw new Error(msg);
	}
	const data = await res.json();
	return data.noticia as NewsItem;
}

export async function updateNews(id: number, payload: Partial<Omit<NewsItem, 'id' | 'fecha'>>): Promise<NewsItem> {
	const res = await fetch(`${BACKEND_BASE_URL}/news/${id}`, {
		method: 'PUT',
		headers: getAuthHeaders(),
		body: JSON.stringify(payload),
	});
	if (!res.ok) {
		let msg = `Error actualizando noticia: ${res.status}`;
		try {
			const d = await res.json();
			if (d?.error) msg = d.error;
		} catch {}
		throw new Error(msg);
	}
	const data = await res.json();
	return data.noticia as NewsItem;
}

export async function deleteNews(id: number): Promise<void> {
	const res = await fetch(`${BACKEND_BASE_URL}/news/${id}`, {
		method: 'DELETE',
		headers: getAuthHeaders(),
	});
	if (!res.ok) {
		let msg = `Error eliminando noticia: ${res.status}`;
		try {
			const d = await res.json();
			if (d?.error) msg = d.error;
		} catch {}
		throw new Error(msg);
	}
}

export async function getNewsById(id: number): Promise<NewsItem | null> {
	try {
		const res = await fetch(`${BACKEND_BASE_URL}/news/${id}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' },
		});
		if (!res.ok) {
			if (res.status === 404) return null;
			throw new Error(`Error obteniendo noticia: ${res.status}`);
		}
		return await res.json();
	} catch (error) {
		console.error('Error en getNewsById:', error);
		return null;
	}
}
