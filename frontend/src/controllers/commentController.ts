import type { CommentItem } from '../models/Comment';
import { fetchCommentsByNewsId, createComment } from '../services/commentService';

export const getCommentsByNewsId = async (noticiaId: number): Promise<CommentItem[]> => {
	return await fetchCommentsByNewsId(noticiaId);
};

export const postComment = async (body: any): Promise<CommentItem> => {
	const payload = {
		noticiaId: Number(body?.noticiaId || 0),
		autor: String(body?.autor || ''),
		contenido: String(body?.contenido || ''),
	};
	if (!payload.noticiaId || !payload.autor || !payload.contenido) {
		throw new Error('Faltan campos requeridos');
	}
	return await createComment(payload as any);
};

