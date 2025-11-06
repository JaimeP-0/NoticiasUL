import type { LoginCredentials, RegisterCredentials, AuthResponse } from '../models/User';
import { login as authLogin, register as authRegister } from '../services/authService';

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
	return await authLogin(credentials);
};

export const register = async (credentials: RegisterCredentials): Promise<AuthResponse> => {
	return await authRegister(credentials);
};

