import React, { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Text, ScrollView } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import {
    PageContainer,
    ScreenHeader,
    ChatBubble,
    TextInput,
} from '@/components';
import { AppColors, Spacing } from '@/constants/theme';
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

    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            text: `Hello! 👋 I'm your calorie tracking assistant.\n\nYou can:\n• Log food: "breakfast: 2 eggs"\n• Log exercise: "I ran for 30 minutes"\n• Check summary: "show summary today"\n\nWhat would you like to track today?`,
            isUser: false,
        }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);

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
            <Stack.Screen options={{ title: formattedDate }} />
            <PageContainer scrollable={false}>
                <KeyboardAvoidingView
                    style={styles.container}
                    behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                    keyboardVerticalOffset={100}
                >
                    {/* Messages */}
                    <ScrollView style={styles.messagesContainer} contentContainerStyle={styles.messagesContent}>
                        {messages.length === 0 && (
                            <View style={styles.emptyState}>
                                <Text style={styles.emptyText}>Start a conversation!</Text>
                                <Text style={styles.emptySubtext}>Try asking about your meals or exercises</Text>
                            </View>
                        )}

                        {messages.map((message) => (
                            <ChatBubble
                                key={message.id}
                                message={message.text}
                                isUser={message.isUser}
                            />
                        ))}

                        {isLoading && (
                            <View style={styles.loadingContainer}>
                                <ActivityIndicator size="small" color={AppColors.primaryYellow} />
                                <Text style={styles.loadingText}>Thinking...</Text>
                            </View>
                        )}
                    </ScrollView>

                    {/* Input */}
                    <View style={styles.inputContainer}>
                        <TextInput
                            placeholder="Ask me anything..."
                            value={inputText}
                            onChangeText={setInputText}
                            rightIcon="send"
                            onRightIconPress={() => handleSend()}
                            onSubmitEditing={() => handleSend()}
                            editable={!isLoading}
                        />
                    </View>
                </KeyboardAvoidingView>
            </PageContainer>
        </>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    messagesContainer: {
        flex: 1,
    },
    messagesContent: {
        paddingVertical: Spacing.md,
    },
    emptyState: {
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: Spacing.xl * 2,
    },
    emptyText: {
        fontSize: 18,
        fontWeight: '600',
        color: AppColors.textDark,
        marginBottom: Spacing.xs,
    },
    emptySubtext: {
        fontSize: 14,
        color: AppColors.textGray,
    },
    loadingContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
    },
    loadingText: {
        marginLeft: Spacing.sm,
        color: AppColors.textGray,
        fontSize: 14,
    },
    inputContainer: {
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
    },
});
