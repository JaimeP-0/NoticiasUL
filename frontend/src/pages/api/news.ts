import type { APIRoute } from 'astro';
import { getNews, postNews } from '../../controllers/newsController';
import { getCommentsByNewsId, postComment } from '../../controllers/commentController';

export const prerender = false;

export const GET: APIRoute = async ({ url }) => {
	try {
		const newsId = url.searchParams.get('noticiaId');
		if (newsId) {
			const comments = await getCommentsByNewsId(Number(newsId));
			return new Response(JSON.stringify(comments), {
				status: 200,
				headers: { 'Content-Type': 'application/json' },
			});
		}
		const data = await getNews();
		return new Response(JSON.stringify(data), {
			status: 200,
			headers: { 'Content-Type': 'application/json' },
		});
	} catch (err: any) {
		return new Response(JSON.stringify({ error: err?.message || 'Error' }), {
			status: 500,
			headers: { 'Content-Type': 'application/json' },
		});
	}
};

export const POST: APIRoute = async ({ request }) => {
	try {
		const body = await request.json();
		const type = body?.type || 'news';
		
		if (type === 'comment') {
			const created = await postComment(body);
			return new Response(JSON.stringify({ comentario: created }), {
				status: 201,
				headers: { 'Content-Type': 'application/json' },
			});
		}
		
		const created = await postNews(body);
		return new Response(JSON.stringify({ noticia: created }), {
			status: 201,
			headers: { 'Content-Type': 'application/json' },
		});
	} catch (err: any) {
		return new Response(JSON.stringify({ error: err?.message || 'Error' }), {
			status: 400,
			headers: { 'Content-Type': 'application/json' },
		});
	}
};
