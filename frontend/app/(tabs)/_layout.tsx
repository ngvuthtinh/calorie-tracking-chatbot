import { Tabs } from 'expo-router';
import React from 'react';
import { Ionicons } from '@expo/vector-icons';
import { AppColors } from '@/constants/theme';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: AppColors.primaryYellow,
        tabBarInactiveTintColor: AppColors.textGray,
        headerShown: false,
        tabBarStyle: {
          borderTopWidth: 1,
          borderTopColor: AppColors.borderGray,
        },
      }}>
      <Tabs.Screen
        name="chat"
        options={{
          title: 'Chat',
          tabBarIcon: ({ color, size }) => <Ionicons name="chatbubble" size={size} color={color} />,
        }}
      />
    </Tabs>
  );
}
