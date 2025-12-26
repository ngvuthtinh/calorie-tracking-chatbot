import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface InfoCardProps {
    content: string;
    showCheckmark?: boolean;
    style?: ViewStyle;
    textStyle?: TextStyle;
}

export default function InfoCard({
    content,
    showCheckmark = false,
    style,
    textStyle,
}: InfoCardProps) {
    return (
        <View style={[styles.card, style]}>
            {showCheckmark && (
                <Ionicons
                    name="checkmark-circle"
                    size={20}
                    color={AppColors.textDark}
                    style={styles.checkmark}
                />
            )}
            <Text style={[styles.text, textStyle]}>{content}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        backgroundColor: AppColors.primaryYellow,
        borderRadius: BorderRadius.medium,
        padding: Spacing.md,
    },
    checkmark: {
        position: 'absolute',
        top: Spacing.sm,
        right: Spacing.sm,
    },
    text: {
        ...Typography.bodySmall,
        color: AppColors.textDark,
        lineHeight: 20,
    },
});
