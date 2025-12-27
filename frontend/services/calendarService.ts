import { API_ENDPOINTS } from '@/config/api';

export interface LogEntry {
    id: number;
    name: string;
    calories: number;
    quantity: number;
    unit: string;
    logged_at: string;
}

export interface DaySummary {
    total_intake: number;
    total_burned: number;
    net_calories: number;
    target_calories: number;
    remaining_calories: number;
}

export interface DayViewResponse {
    date: string;
    summary: DaySummary;
    food_entries: LogEntry[];
    exercise_entries: LogEntry[];
    coach_advice?: string;
}

export class CalendarService {
    static async getDayView(userId: number, dateStr: string): Promise<DayViewResponse | null> {
        try {
            // dateStr format: YYYY-MM-DD
            const response = await fetch(`${API_ENDPOINTS.CALENDAR_DAY(dateStr)}?user_id=${userId}`);

            if (!response.ok) {
                console.error('Failed to fetch day view:', response.status);
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching day view:', error);
            return null;
        }
    }
}
