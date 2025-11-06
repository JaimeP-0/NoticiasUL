import type { NewsItem } from '../models/News';

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
		headers: { 'Content-Type': 'application/json' },
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

export async function getNewsById(id: number): Promise<NewsItem | null> {
	try {
		const allNews = await fetchNews();
		return allNews.find(n => n.id === id) || null;
	} catch {
		return null;
	}
}
