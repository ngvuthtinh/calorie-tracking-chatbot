import React, { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform, ActivityIndicator, Text, Modal, TouchableOpacity, ScrollView as RNScrollView } from 'react-native';
import {
    PageContainer,
    ScreenHeader,
    ChatBubble,
    TextInput,
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
                        rightIcon="paper-plane"
                        onRightIconPress={() => handleSend()}
                        onSubmitEditing={() => handleSend()}
                        editable={!isLoading}
                    />
                </View>
            </KeyboardAvoidingView>

            {/* Help Modal */}
            <Modal
                visible={showHelpModal}
                animationType="slide"
                transparent={true}
                onRequestClose={() => setShowHelpModal(false)}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.modalContent}>
                        <View style={styles.modalHeader}>
                            <Text style={styles.modalTitle}>💡 How to Use</Text>
                            <TouchableOpacity onPress={() => setShowHelpModal(false)}>
                                <Text style={styles.closeButton}>✕</Text>
                            </TouchableOpacity>
                        </View>

                        <RNScrollView style={styles.modalScroll}>
                            <View style={styles.sectionContainer}>
                                <Text style={styles.sectionTitle}>🍎 Log Food</Text>
                                <Text style={styles.exampleText}>• "Breakfast: 2 eggs, 1 toast"</Text>
                                <Text style={styles.exampleText}>• "Lunch: chicken rice"</Text>
                                <Text style={styles.exampleText}>• "Dinner: 200g beef, salad"</Text>
                                <Text style={styles.exampleText}>• "Snack: apple"</Text>
                            </View>

                            <View style={styles.sectionContainer}>
                                <Text style={styles.sectionTitle}>🏃 Log Exercise</Text>
                                <Text style={styles.exampleText}>• "Exercise: run 30 min"</Text>
                                <Text style={styles.exampleText}>• "Exercise: gym 1 hour"</Text>
                                <Text style={styles.exampleText}>• "Exercise: swim 45 min"</Text>
                                <Text style={styles.exampleText}>• "Exercise: walk 2 km"</Text>
                            </View>

                            <View style={styles.sectionContainer}>
                                <Text style={styles.sectionTitle}>✏️ Edit Entries</Text>
                                <Text style={styles.exampleText}>• "Edit food f1: 3 eggs"</Text>
                                <Text style={styles.exampleText}>• "Edit exercise x2: run 45 min"</Text>
                                <Text style={styles.exampleText}>• "Add to f1: 1 banana"</Text>
                            </View>

                            <View style={styles.sectionContainer}>
                                <Text style={styles.sectionTitle}>🗑️ Delete Entries</Text>
                                <Text style={styles.exampleText}>• "Delete food f1"</Text>
                                <Text style={styles.exampleText}>• "Delete exercise x2"</Text>
                            </View>

                            <View style={styles.sectionContainer}>
                                <Text style={styles.sectionTitle}>📊 Check Stats</Text>
                                <Text style={styles.exampleText}>• "Show summary today"</Text>
                                <Text style={styles.exampleText}>• "Show summary 2025-12-25"</Text>
                                <Text style={styles.exampleText}>• "Show weekly stats"</Text>
                                <Text style={styles.exampleText}>• "Show stats this week"</Text>
                            </View>

                            <View style={styles.sectionContainer}>
                                <Text style={styles.sectionTitle}>🔄 Move Entries</Text>
                                <Text style={styles.exampleText}>• "Move f1 to lunch"</Text>
                                <Text style={styles.exampleText}>• "Move f2 to dinner"</Text>
                            </View>
                        </RNScrollView>

                        <TouchableOpacity
                            style={styles.modalButton}
                            onPress={() => setShowHelpModal(false)}
                        >
                            <Text style={styles.modalButtonText}>Got it!</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        </PageContainer>
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
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        backgroundColor: 'white',
        borderRadius: 16,
        padding: Spacing.lg,
        width: '90%',
        maxHeight: '80%',
    },
    modalHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Spacing.md,
    },
    modalTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: AppColors.textDark,
    },
    closeButton: {
        fontSize: 28,
        color: AppColors.textGray,
        fontWeight: '300',
    },
    modalScroll: {
        maxHeight: 400,
    },
    sectionContainer: {
        marginBottom: Spacing.lg,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: AppColors.textDark,
        marginBottom: Spacing.sm,
    },
    exampleText: {
        fontSize: 14,
        color: AppColors.textGray,
        marginBottom: 4,
        paddingLeft: Spacing.sm,
    },
    modalButton: {
        backgroundColor: AppColors.primaryYellow,
        paddingVertical: Spacing.md,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: Spacing.md,
    },
    modalButtonText: {
        fontSize: 16,
        fontWeight: '600',
        color: AppColors.textDark,
    },
});
