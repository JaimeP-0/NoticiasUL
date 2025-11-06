import type { APIRoute } from 'astro';
import type { NewsItem } from '../models/News';
import { fetchNews, createNews } from '../services/newsService';

export const getNews = async (): Promise<NewsItem[]> => {
    return await fetchNews();
};

export const postNews = async (body: any): Promise<NewsItem> => {
    const payload = {
        titulo: String(body?.titulo || ''),
        contenido: String(body?.contenido || ''),
        autor: String(body?.autor || ''),
        imagen: body?.imagen ? String(body.imagen) : '',
    };
    return await createNews(payload as any);
};


