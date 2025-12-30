<template>
  <div class="btm-nav fixed bottom-0 bg-base-100 border-t">
    <RouterLink to="/dashboard" class="text-xs">
      📊
      <span class="btm-nav-label">Dashboard</span>
    </RouterLink>

    <RouterLink to="/transactions" class="text-xs">
      📄
      <span class="btm-nav-label">Transactions</span>
    </RouterLink>

    <RouterLink to="/upload" class="text-xs">
      ⬆️
      <span class="btm-nav-label">Upload</span>
    </RouterLink>

    <RouterLink to="/rules" class="text-xs">
      ⚙️
      <span class="btm-nav-label">Rules</span>
    </RouterLink>
  </div>
</template>
