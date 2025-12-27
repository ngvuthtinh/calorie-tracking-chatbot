import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface ChatBubbleProps {
    message: string;
    isUser?: boolean;
    style?: ViewStyle;
    textStyle?: TextStyle;
}

export default function ChatBubble({
    message,
    isUser = false,
    style,
    textStyle,
}: ChatBubbleProps) {
    return (
        <View
            style={[
                styles.bubble,
                isUser ? styles.userBubble : styles.systemBubble,
                style,
            ]}
        >
            <Text
                style={[
                    styles.text,
                    isUser ? styles.userText : styles.systemText,
                    textStyle,
                ]}
            >
                {message}
            </Text>
        </View>
    );
}

const styles = StyleSheet.create({
    bubble: {
        maxWidth: '80%',
        paddingVertical: Spacing.sm,
        paddingHorizontal: Spacing.md,
        borderRadius: BorderRadius.medium,
        marginVertical: Spacing.xs,
    },
    userBubble: {
        backgroundColor: AppColors.primaryYellow,
        alignSelf: 'flex-end',
        borderBottomRightRadius: 4,
    },
    systemBubble: {
        backgroundColor: AppColors.backgroundLightGray,
        alignSelf: 'flex-start',
        borderBottomLeftRadius: 4,
    },
    text: {
        ...Typography.body,
    },
    userText: {
        color: AppColors.textDark,
    },
    systemText: {
        color: AppColors.textDark,
    },
});
