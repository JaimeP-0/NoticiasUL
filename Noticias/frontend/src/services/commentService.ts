import type { CommentItem } from '../models/Comment';

// Simulación de base de datos de comentarios (en producción sería MySQL)
let commentsDB: CommentItem[] = [];

export async function fetchCommentsByNewsId(noticiaId: number): Promise<CommentItem[]> {
	return commentsDB.filter(c => c.noticiaId === noticiaId);
}

export async function createComment(payload: Omit<CommentItem, 'id' | 'fecha'>): Promise<CommentItem> {
	const newComment: CommentItem = {
		id: commentsDB.length + 1,
		...payload,
		fecha: new Date().toISOString(),
	};
	commentsDB.push(newComment);
	return newComment;
}

export async function getAllComments(): Promise<CommentItem[]> {
	return commentsDB;
}

