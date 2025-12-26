import React from 'react';
import { TouchableOpacity, StyleSheet, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Spacing } from '@/constants/theme';

interface IconButtonProps {
    icon: keyof typeof Ionicons.glyphMap;
    onPress: () => void;
    size?: number;
    color?: string;
    backgroundColor?: string;
    style?: ViewStyle;
    variant?: 'circular' | 'square';
}

export default function IconButton({
    icon,
    onPress,
    size = 24,
    color = AppColors.textDark,
    backgroundColor = 'transparent',
    style,
    variant = 'circular',
}: IconButtonProps) {
    return (
        <TouchableOpacity
            style={[
                styles.button,
                variant === 'circular' && styles.circular,
                { backgroundColor },
                style,
            ]}
            onPress={onPress}
            activeOpacity={0.7}
        >
            <Ionicons name={icon} size={size} color={color} />
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    button: {
        padding: Spacing.sm,
        alignItems: 'center',
        justifyContent: 'center',
        minWidth: 40,
        minHeight: 40,
    },
    circular: {
        borderRadius: 999,
    },
});
