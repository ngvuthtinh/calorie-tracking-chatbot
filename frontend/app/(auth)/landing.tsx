import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

export default function LandingPage() {
    const router = useRouter();

    const handleGetStarted = () => {
        router.replace('/(tabs)/calendar');
    };

    return (
        <View
            style={styles.container}
        >
            <View style={styles.content}>
                {/* Logo Section */}
                <View style={styles.logoContainer}>
                    <View style={styles.logoCircle}>
                        <Ionicons name="nutrition" size={80} color={AppColors.primaryYellow} />
                    </View>
                </View>

                {/* Title Section */}
                <View style={styles.titleContainer}>
                    <Text style={styles.appName}>C:alo</Text>
                    <View style={styles.sloganContainer}>
                        <Text style={styles.slogan}>A Calorie Tracking Chatbot</Text>
                        <Text style={styles.slogan}>from Food and Activity</Text>
                    </View>
                </View>

                {/* Features Section */}
                <View style={styles.featuresContainer}>
                    <View style={styles.featureItem}>
                        <View style={styles.featureIcon}>
                            <Ionicons name="chatbubble-ellipses" size={24} color={AppColors.primaryYellow} />
                        </View>
                        <Text style={styles.featureText}>Smart Chat Assistant</Text>
                    </View>

                    <View style={styles.featureItem}>
                        <View style={styles.featureIcon}>
                            <Ionicons name="restaurant" size={24} color={AppColors.primaryYellow} />
                        </View>
                        <Text style={styles.featureText}>Track Your Meals</Text>
                    </View>

                    <View style={styles.featureItem}>
                        <View style={styles.featureIcon}>
                            <Ionicons name="fitness" size={24} color={AppColors.primaryYellow} />
                        </View>
                        <Text style={styles.featureText}>Log Activities</Text>
                    </View>
                </View>

                {/* CTA Button */}
                <View style={styles.buttonContainer}>
                    <TouchableOpacity
                        style={styles.button}
                        onPress={handleGetStarted}
                        activeOpacity={0.8}
                    >
                        <LinearGradient
                            colors={['#FFD700', '#FFA500']}
                            start={{ x: 0, y: 0 }}
                            end={{ x: 1, y: 0 }}
                            style={styles.buttonGradient}
                        >
                            <Text style={styles.buttonText}>Get Started</Text>
                            <Ionicons name="arrow-forward" size={24} color="#000" />
                        </LinearGradient>
                    </TouchableOpacity>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: 'white',
    },
    content: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: Spacing.xl,
        zIndex: 1,
    },
    logoContainer: {
        marginBottom: Spacing.xl,
    },
    logoCircle: {
        width: 160,
        height: 160,
        borderRadius: 80,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.2,
        shadowRadius: 16,
        elevation: 8,
    },
    titleContainer: {
        alignItems: 'center',
        marginBottom: Spacing.xxl,
    },
    appName: {
        fontSize: 64,
        fontWeight: '800',
        color: AppColors.textDark,
        marginBottom: Spacing.md,
        letterSpacing: -2,
    },
    sloganContainer: {
        alignItems: 'center',
    },
    slogan: {
        fontSize: 18,
        fontWeight: '500',
        color: AppColors.textGray,
        textAlign: 'center',
        lineHeight: 26,
    },
    featuresContainer: {
        width: '100%',
        marginBottom: Spacing.xxl,
        paddingHorizontal: Spacing.md,
    },
    featureItem: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: Spacing.md,
        backgroundColor: 'rgba(255, 255, 255, 0.7)',
        padding: Spacing.md,
        borderRadius: BorderRadius.medium,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 2,
    },
    featureIcon: {
        width: 48,
        height: 48,
        borderRadius: BorderRadius.medium,
        backgroundColor: 'rgba(255, 215, 0, 0.2)',
        justifyContent: 'center',
        alignItems: 'center',
        marginRight: Spacing.md,
    },
    featureText: {
        fontSize: 16,
        fontWeight: '600',
        color: AppColors.textDark,
    },
    buttonContainer: {
        width: '100%',
        paddingHorizontal: Spacing.md,
    },
    button: {
        width: '100%',
        borderRadius: BorderRadius.large,
        overflow: 'hidden',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 6,
    },
    buttonGradient: {
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        paddingVertical: Spacing.md + 4,
        paddingHorizontal: Spacing.xl,
    },
    buttonText: {
        fontSize: 20,
        fontWeight: '700',
        color: '#000',
        marginRight: Spacing.sm,
    },
});

