import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface FormFieldProps {
    label: string;
    value?: string;
    placeholder?: string;
    editable?: boolean;
    style?: ViewStyle;
    labelStyle?: TextStyle;
    valueStyle?: TextStyle;
}

export default function FormField({
    label,
    value,
    placeholder,
    editable = true,
    style,
    labelStyle,
    valueStyle,
}: FormFieldProps) {
    return (
        <View style={[styles.container, style]}>
            <Text style={[styles.label, labelStyle]}>{label}</Text>
            <View style={[styles.valueContainer, !editable && styles.disabled]}>
                <Text style={[styles.value, !value && styles.placeholder, valueStyle]}>
                    {value || placeholder}
                </Text>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        marginBottom: Spacing.md,
    },
    label: {
        ...Typography.bodySmall,
        color: AppColors.textGray,
        marginBottom: Spacing.xs,
    },
    valueContainer: {
        backgroundColor: AppColors.backgroundLightGray,
        borderRadius: BorderRadius.small,
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
        minHeight: 48,
        justifyContent: 'center',
    },
    disabled: {
        opacity: 0.6,
    },
    value: {
        ...Typography.body,
        color: AppColors.textDark,
    },
    placeholder: {
        color: AppColors.textLight,
    },
});
