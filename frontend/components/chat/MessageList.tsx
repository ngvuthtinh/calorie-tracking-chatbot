import React from 'react';
import { ScrollView, View, StyleSheet, ViewStyle } from 'react-native';
import { Spacing } from '@/constants/theme';
import ChatBubble from './ChatBubble';

interface Message {
    id: string;
    text: string;
    isUser: boolean;
}

interface MessageListProps {
    messages: Message[];
    style?: ViewStyle;
}

export default function MessageList({ messages, style }: MessageListProps) {
    return (
        <ScrollView
            style={[styles.container, style]}
            contentContainerStyle={styles.content}
            showsVerticalScrollIndicator={false}
        >
            {messages.map((message) => (
                <ChatBubble
                    key={message.id}
                    message={message.text}
                    isUser={message.isUser}
                />
            ))}
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
});
