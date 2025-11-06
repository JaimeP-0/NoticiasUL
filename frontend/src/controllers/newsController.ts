import type { NewsItem } from '../models/News';
import { fetchNews, createNews, getNewsById as fetchNewsById } from '../services/newsService';

export const getNews = async (): Promise<NewsItem[]> => {
	return await fetchNews();
};

export const getNewsById = async (id: number): Promise<NewsItem | null> => {
	return await fetchNewsById(id);
};

export const postNews = async (body: any): Promise<NewsItem> => {
	const payload = {
		titulo: String(body?.titulo || ''),
		contenido: String(body?.contenido || ''),
		autor: String(body?.autor || ''),
		imagen: body?.imagen ? String(body.imagen) : '',
	};
	if (!payload.titulo || !payload.contenido || !payload.autor) {
		throw new Error('Faltan campos requeridos');
	}
	return await createNews(payload as any);
};
