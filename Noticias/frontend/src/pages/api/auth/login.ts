import type { APIRoute } from 'astro';
import { login } from '../../../controllers/authController';

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
	try {
		const body = await request.json();
		const result = await login(body);
		
		if (!result.success) {
			return new Response(JSON.stringify(result), {
				status: 401,
				headers: { 'Content-Type': 'application/json' },
			});
		}

		return new Response(JSON.stringify(result), {
			status: 200,
			headers: { 'Content-Type': 'application/json' },
		});
	} catch (err: any) {
		return new Response(JSON.stringify({ success: false, error: err?.message || 'Error' }), {
			status: 500,
			headers: { 'Content-Type': 'application/json' },
		});
	}
};

