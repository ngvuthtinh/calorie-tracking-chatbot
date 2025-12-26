import { API_ENDPOINTS } from '@/config/api';

export interface ChatMessage {
    user_id: number;
    entry_date: string; // YYYY-MM-DD
    text: string;
}

export interface ActionChip {
    label: string;
    command?: string;
}

export interface ChatResponse {
    success: boolean;
    message: string;
    data?: any;
    actions?: ActionChip[];
    frame?: any;
}

export class ChatService {
    /**
     * Send a chat message to the backend
     */
    static async sendMessage(
        userId: number,
        entryDate: string,
        text: string
    ): Promise<ChatResponse> {
        try {
            console.log('=== Sending message to backend ===');
            console.log('URL:', API_ENDPOINTS.CHAT);
            console.log('Payload:', { user_id: userId, entry_date: entryDate, text });

            // Add timeout to prevent infinite hanging
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

            const response = await fetch(API_ENDPOINTS.CHAT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    entry_date: entryDate,
                    text: text,
                }),
                signal: controller.signal,
            });

            clearTimeout(timeoutId);

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Error response:', errorText);
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data: ChatResponse = await response.json();
            console.log('Success response:', data);
            return data;
        } catch (error) {
            console.error('=== Chat API Error ===');
            if (error instanceof Error && error.name === 'AbortError') {
                console.error('Request timed out after 10 seconds');
                return {
                    success: false,
                    message: 'Request timed out. Cannot reach backend at ' + API_ENDPOINTS.CHAT,
                    data: { error: 'Timeout' },
                };
            }
            console.error('Error type:', error instanceof TypeError ? 'Network/CORS' : 'Other');
            console.error('Error details:', error);
            return {
                success: false,
                message: 'Failed to send message. Please check your connection.',
                data: { error: String(error) },
            };
        }
    }

    /**
     * Generate action chips from frame data
     */
    static generateActionChips(frame?: any): ActionChip[] {
        if (!frame) return [];

        const chips: ActionChip[] = [];
        const intent = frame.intent || '';

        // Generate contextual action chips based on intent
        if (intent.includes('food')) {
            chips.push(
                { label: 'breakfast: 2 eggs', command: 'breakfast: 2 eggs' },
                { label: 'lunch: chicken salad', command: 'lunch: chicken salad' },
                { label: 'show summary today', command: 'show summary today' }
            );
        } else if (intent.includes('exercise')) {
            chips.push(
                { label: 'exercise: run 20min', command: 'exercise: run 20min' },
                { label: 'exercise: 50 pushups', command: 'exercise: 50 pushups' },
                { label: 'show summary today', command: 'show summary today' }
            );
        } else {
            chips.push(
                { label: 'breakfast: 150g chicken', command: 'breakfast: 150g chicken' },
                { label: 'exercise: run 20min', command: 'exercise: run 20min' },
                { label: 'show summary today', command: 'show summary today' }
            );
        }

        return chips;
    }
}
