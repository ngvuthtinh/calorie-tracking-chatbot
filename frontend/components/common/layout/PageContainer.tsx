import React, { ReactNode } from 'react';
import { View, StyleSheet, ViewStyle, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { AppColors, Spacing } from '@/constants/theme';

interface PageContainerProps {
    children: ReactNode;
    scrollable?: boolean;
    style?: ViewStyle;
    contentContainerStyle?: ViewStyle;
}

export default function PageContainer({
    children,
    scrollable = true,
    style,
    contentContainerStyle,
}: PageContainerProps) {
    const content = (
        <View style={[styles.content, contentContainerStyle]}>
            {children}
        </View>
    );

    return (
        <SafeAreaView style={[styles.container, style]} edges={['top']}>
            {scrollable ? (
                <ScrollView
                    style={styles.scrollView}
                    contentContainerStyle={styles.scrollContent}
                    showsVerticalScrollIndicator={false}
                >
                    {content}
                </ScrollView>
            ) : (
                content
            )}
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: AppColors.backgroundWhite,
    },
    scrollView: {
        flex: 1,
    },
    scrollContent: {
        flexGrow: 1,
    },
    content: {
        flex: 1,
        paddingHorizontal: Spacing.md,
    },
});
