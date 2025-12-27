import React, { useRef } from 'react';
import { ScrollView, View, StyleSheet, Text, ActivityIndicator } from 'react-native';
import { Spacing, AppColors } from '@/constants/theme';
import ChatBubble from './ChatBubble';

export interface Message {
    id: string;
    text: string;
    isUser: boolean;
}

interface MessageListProps {
    messages: Message[];
    isLoading?: boolean;
    emptyText?: string;
    emptySubtext?: string;
}

export default function MessageList({
    messages,
    isLoading = false,
    emptyText = 'Start a conversation!',
    emptySubtext = 'Try asking about your meals or exercises',
}: MessageListProps) {
    const scrollViewRef = useRef<ScrollView>(null);

    return (
        <ScrollView
            ref={scrollViewRef}
            style={styles.container}
            contentContainerStyle={styles.content}
            onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
            showsVerticalScrollIndicator={false}
        >
            {messages.length === 0 && !isLoading && (
                <View style={styles.emptyState}>
                    <Text style={styles.emptyText}>{emptyText}</Text>
                    <Text style={styles.emptySubtext}>{emptySubtext}</Text>
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
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    content: {
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
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
    },
    loadingText: {
        marginLeft: Spacing.sm,
        color: AppColors.textGray,
        fontSize: 14,
    },
});
