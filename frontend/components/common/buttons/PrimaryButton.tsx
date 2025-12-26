import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator, ViewStyle, TextStyle } from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius, Shadows } from '@/constants/theme';

interface PrimaryButtonProps {
    title: string;
    onPress: () => void;
    fullWidth?: boolean;
    loading?: boolean;
    disabled?: boolean;
    style?: ViewStyle;
    textStyle?: TextStyle;
}

export default function PrimaryButton({
    title,
    onPress,
    fullWidth = true,
    loading = false,
    disabled = false,
    style,
    textStyle,
}: PrimaryButtonProps) {
    return (
        <TouchableOpacity
            style={[
                styles.button,
                fullWidth && styles.fullWidth,
                disabled && styles.disabled,
                style,
            ]}
            onPress={onPress}
            disabled={disabled || loading}
            activeOpacity={0.8}
        >
            {loading ? (
                <ActivityIndicator color={AppColors.textDark} />
            ) : (
                <Text style={[styles.text, textStyle]}>{title}</Text>
            )}
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    button: {
        backgroundColor: AppColors.primaryYellow,
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.lg,
        borderRadius: BorderRadius.medium,
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: 48,
        ...Shadows.small,
    },
    fullWidth: {
        width: '100%',
    },
    disabled: {
        opacity: 0.5,
    },
    text: {
        ...Typography.bodyBold,
        color: AppColors.textDark,
    },
});
