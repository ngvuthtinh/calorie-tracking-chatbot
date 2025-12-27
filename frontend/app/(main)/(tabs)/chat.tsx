import React, { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Text } from 'react-native';
import {
    PageContainer,
    ScreenHeader,
    TextInput,
    HelpModal,
    MessageList,
} from '@/components';
import { Spacing, AppColors } from '@/constants/theme';
import { ScrollView } from 'react-native';
import { ChatService } from '@/services/chatService';

interface Message {
    id: string;
    text: string;
    isUser: boolean;
}

export default function ChatScreen() {
    // Always show today's date
    const todayDate = new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit'
    });

    // Format date for API (YYYY-MM-DD) using local timezone
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const apiDate = `${year}-${month}-${day}`;

    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            text: `Hello! 👋 I'm your calorie tracking assistant.\n\nYou can:\n• Log food: "Breakfast: 2 eggs"\n• Log exercise: "Exercise: run 30 min"\n• Check summary: "Show summary today"\n\nWhat would you like to track today?`,
            isUser: false,
        }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showHelpModal, setShowHelpModal] = useState(false);

    const handleSend = async (text?: string) => {
        const messageText = text || inputText;
        if (!messageText.trim()) return;

        // Add user message immediately
        const userMessage: Message = {
            id: Date.now().toString(),
            text: messageText,
            isUser: true,
        };
        setMessages(prev => [...prev, userMessage]);
        setInputText('');
        setIsLoading(true);

        try {
            // Call backend API
            const response = await ChatService.sendMessage(
                1, // TODO: Replace with actual user ID from auth
                apiDate,
                messageText
            );

            // Add bot response (backend already formats the message with lists)
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
        <PageContainer scrollable={false}>
            <ScreenHeader
                title={`Today (${todayDate})`}
                showBackButton={false}
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
