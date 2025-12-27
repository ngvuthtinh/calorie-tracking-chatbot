import { API_ENDPOINTS } from '@/config/api';

export interface LogEntry {
    id: number;
    name: string;
    calories: number;
    quantity: number;
    unit: string;
    logged_at: string;
    meal?: string;  // 'breakfast', 'lunch', 'dinner', 'snack'
    entry_code?: string;
}

export interface DaySummary {
    intake_kcal: number;
    burned_kcal: number;
    net_kcal: number;
    target_kcal: number;
    remaining_kcal: number;
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
