import { Platform } from 'react-native';

const LOCALHOST = Platform.OS === 'android' ? '10.0.2.2' : '192.168.1.142';
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || `http://${LOCALHOST}:8000`;

export const API_ENDPOINTS = {
    CHAT: `${API_BASE_URL}/api/chat/`,
    CALENDAR_DAY: (date: string) => `${API_BASE_URL}/api/day/${date}`,
    OVERVIEW: `${API_BASE_URL}/api/overview/`,
    PROFILE: `${API_BASE_URL}/api/profile/`,
};

export default API_BASE_URL;
