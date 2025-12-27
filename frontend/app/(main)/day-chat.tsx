import React, { useState, useEffect } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Text, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import {
    PageContainer,
    ScreenHeader,
    TextInput,
    HelpModal,
    MessageList,
} from '@/components';
import { AppColors, Spacing } from '@/constants/theme';
import { CalendarService } from '@/services/calendarService';
import { ChatService } from '@/services/chatService';

interface Message {
    id: string;
    text: string;
    isUser: boolean;
}

export default function DayChatScreen() {
    const router = useRouter();
    const params = useLocalSearchParams();
    const dateParam = params.date as string;

    // Format date for display (e.g., "Dec 26, 2025")
    const formattedDate = dateParam ? new Date(dateParam + 'T00:00:00').toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit'
    }) : 'Chat';

    const [messages, setMessages] = useState<Message[]>([]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showHelpModal, setShowHelpModal] = useState(false);
    const [isLoadingSummary, setIsLoadingSummary] = useState(true);

    // Load day summary on mount
    useEffect(() => {
        const loadDaySummary = async () => {
            if (!dateParam) {
                setIsLoadingSummary(false);
                return;
            }

            try {
                console.log('Loading day summary for date:', dateParam);
                const dayView = await CalendarService.getDayView(1, dateParam); // TODO: Replace with actual user ID
                console.log('Day view response:', dayView);

                if (!dayView) {
                    console.error('getDayView returned null');
                    throw new Error('No data returned');
                }

                // Format summary message
                let summaryText = `Welcome back! Here's what you logged on ${formattedDate}:\n\n`;

                const foodCount = dayView.food_entries?.length || 0;
                const exerciseCount = dayView.exercise_entries?.length || 0;
                const netKcal = Math.round(dayView.summary?.net_kcal || 0);

                // Group food entries by entry_code for display
                if (foodCount > 0) {
                    summaryText += `Food:\n`;
                    const foodGroups: Record<string, any[]> = {};
                    dayView.food_entries.forEach((entry: any) => {
                        const code = entry.entry_code || 'fx';
                        if (!foodGroups[code]) foodGroups[code] = [];
                        foodGroups[code].push(entry);
                    });

                    Object.entries(foodGroups).forEach(([code, items]) => {
                        const meal = items[0].meal ? `${items[0].meal.charAt(0).toUpperCase()}${items[0].meal.slice(1)} - ` : '';
                        const itemDetails = items.map(it => `${it.name} (+${Math.round(it.calories || 0)} kcal)`).join(', ');
                        summaryText += `• ${code}: ${meal}${itemDetails}\n`;
                    });
                    summaryText += `\n`;
                }

                // Group exercise entries by entry_code for display
                if (exerciseCount > 0) {
                    summaryText += `Exercise:\n`;
                    const exerciseGroups: Record<string, any[]> = {};
                    dayView.exercise_entries.forEach((entry: any) => {
                        const code = entry.entry_code || 'xx';
                        if (!exerciseGroups[code]) exerciseGroups[code] = [];
                        exerciseGroups[code].push(entry);
                    });

                    Object.entries(exerciseGroups).forEach(([code, items]) => {
                        const itemDetails = items.map(it => `${it.name} (-${Math.round(it.calories || 0)} kcal)`).join(', ');
                        summaryText += `• ${code}: ${itemDetails}\n`;
                    });
                    summaryText += `\n`;
                }

                // Show total or no entries message
                if (foodCount > 0 || exerciseCount > 0) {
                    summaryText += `Total: ${netKcal} kcal net\n\n`;
                } else {
                    summaryText += `No entries logged yet.\n\n`;
                }

                summaryText += `What would you like to do?`;

                setMessages([{
                    id: 'summary',
                    text: summaryText,
                    isUser: false,
                }]);
            } catch (error) {
                console.error('Failed to load day summary:', error);
                setMessages([{
                    id: 'error',
                    text: `Hello! 👋\n\nCouldn't load summary for this day.\n\nWhat would you like to do?`,
                    isUser: false,
                }]);
            } finally {
                setIsLoadingSummary(false);
            }
        };

        loadDaySummary();
    }, [dateParam, formattedDate]);

    const handleSend = async () => {
        if (!inputText.trim()) return;

        // Add user message immediately
        const userMessage: Message = {
            id: Date.now().toString(),
            text: inputText,
            isUser: true,
        };
        setMessages(prev => [...prev, userMessage]);
        const messageToSend = inputText;
        setInputText('');
        setIsLoading(true);

        try {
            // Call backend API
            const response = await ChatService.sendMessage(
                1, // TODO: Replace with actual user ID from auth
                dateParam,
                messageToSend
            );

            // Add bot response
            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                text: response.message,
                isUser: false,
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            // Add error message
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                text: 'Sorry, something went wrong. Please try again.',
                isUser: false,
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <Stack.Screen options={{ headerShown: false }} />
            <PageContainer scrollable={false}>
                <ScreenHeader
                    title={formattedDate}
                    showBackButton={true}
                    onBackPress={() => router.back()}
                    rightIcon="help-circle"
                    onRightIconPress={() => setShowHelpModal(true)}
                />

                <KeyboardAvoidingView
                    style={styles.container}
                    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                    keyboardVerticalOffset={50}
                >
                    {/* Messages */}
                    <MessageList
                        messages={messages}
                        isLoading={isLoading}
                    />

                    {/* Input */}
                    <View style={styles.inputContainer}>
                        <TextInput
                            placeholder="Ask me anything..."
                            value={inputText}
                            onChangeText={setInputText}
                            rightIcon="paper-plane"
                            onRightIconPress={() => handleSend()}
                            onSubmitEditing={() => handleSend()}
                            editable={!isLoading}
                        />
                    </View>
                </KeyboardAvoidingView>

                <HelpModal visible={showHelpModal} onClose={() => setShowHelpModal(false)} />
            </PageContainer>
        </>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    inputContainer: {
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
    },
});
