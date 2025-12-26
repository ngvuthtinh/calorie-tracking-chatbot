import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface ActionChipProps {
    label: string;
    onPress: () => void;
    style?: ViewStyle;
    textStyle?: TextStyle;
}

export default function ActionChip({ label, onPress, style, textStyle }: ActionChipProps) {
    return (
        <TouchableOpacity
            style={[styles.chip, style]}
            onPress={onPress}
            activeOpacity={0.8}
        >
            <Text style={[styles.text, textStyle]}>{label}</Text>
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    chip: {
        backgroundColor: AppColors.primaryYellow,
        paddingVertical: Spacing.sm,
        paddingHorizontal: Spacing.md,
        borderRadius: BorderRadius.pill,
        alignSelf: 'flex-start',
    },
    text: {
        ...Typography.bodySmall,
        color: AppColors.textDark,
        fontWeight: '500',
    },
});
