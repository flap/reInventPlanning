<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
import AppNav from '@/components/layout/AppNav.vue'
import AppNavMobile from '@/components/layout/AppNavMobile.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-aws-light">
    <!-- Header -->
    <AppHeader />

    <!-- Body: Sidebar + Main Content -->
    <div class="flex flex-1">
      <!-- Desktop Sidebar -->
      <AppNav />

      <!-- Main Content -->
      <main class="flex-1 p-4 lg:p-6 pb-20 lg:pb-6">
        <router-view />
      </main>
    </div>

    <!-- Footer -->
    <AppFooter />

    <!-- Mobile Bottom Navigation -->
    <AppNavMobile />
  </div>
</template>
