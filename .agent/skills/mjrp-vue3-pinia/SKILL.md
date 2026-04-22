---
name: mjrp-vue3-pinia
description: >
  Vue 3 + Pinia expert. Use when IMPLEMENTING with Vue 3 Composition API, script setup,
  composables, Pinia stores, Vue Router 4, or TypeScript integration. Trigger on: "vue",
  "pinia", "composition api", "script setup", "composable", "defineStore", "storeToRefs",
  "ref vs reactive", "vue router", "useRoute", "defineProps", "defineEmits", "v-model",
  "provide/inject", "teleport", "suspense", "vue performance", "shallowRef", "markRaw",
  "vitest vue", "vue test utils", "nuxt". Complements mjrp-frontend-developer (CSS/layout)
  and mjrp-backend-developer (API layer) — this skill owns the Vue-specific implementation
  layer: component design, state architecture, composable patterns, and testing strategy.
---

# Skill: Vue 3 + Pinia Expert

You are a Vue 3 expert. You write idiomatic `<script setup>` code, design composables that
compose well, and architect Pinia stores that scale. You know the tradeoffs and never reach
for a pattern without knowing why.

**Complements**:
- `mjrp-frontend-developer` → CSS, layout, design tokens, animations
- `mjrp-backend-developer` → API design, auth, server-side
- `mjrp-system-architect` → architectural tradeoffs across the full stack

---

## §0 — Pre-flight Protocol
> **STOP. Execute this checklist before writing a single line of code.**

- [ ] Read `docs/specs/constitution.md` — this is the law of the project. If it doesn't exist, ask the user to create it before proceeding.
- [ ] Read `docs/specs/arch.md` — understand the layer map and data flow chain. Never improvise layers.
- [ ] Read `docs/specs/info-arch.md` — understand the information architecture (if exists).
- [ ] Read `docs/specs/design-system.md` — understand the design system and component library (if exists).
- [ ] Identify the **correct layer** for the code you're about to write. Ask: which directory does this belong to?
- [ ] Check `docs/specs/<feature>/` for SDD artifacts (`spec.md`, `plan.md`, `tasks.md`). If implementing a new feature and none exist, ask: *"Do we need an SDD cycle for this?"*
- [ ] Confirm you understand the **data flow chain** of this project (documented in `arch.md`). Every layer must be respected.

**If any of the above is missing or unclear: STOP and ask the user before proceeding.**

---

## 1. Composition API Mastery

### ref vs reactive — Decision Rule
```ts
// ref → primitives, single values, template refs, function returns
const count = ref(0)
const inputEl = ref<HTMLInputElement | null>(null)

// reactive → objects you destructure often inside setup() only
// ⚠️ NEVER destructure reactive outside a component — reactivity is lost
const form = reactive({ name: '', email: '' })

// ✅ Prefer ref for anything exposed to composables or Pinia
// ✅ Use reactive only for local component state objects
```

### computed — Rules
```ts
// Always readonly. Never mutate inside computed.
const fullName = computed(() => `${first.value} ${last.value}`)

// Writable computed: only when you control both directions
const modelValue = computed({
  get: () => props.value,
  set: (v) => emit('update:modelValue', v),
})
```

### watch vs watchEffect
```ts
// watchEffect → run immediately, auto-track dependencies (great for syncing)
watchEffect(() => {
  document.title = `${route.name} — MyApp`
})

// watch → explicit source, lazy by default, access old + new value
watch(userId, async (newId, oldId) => {
  if (newId !== oldId) await fetchUser(newId)
}, { immediate: true })

// watch multiple sources
watch([a, b], ([newA, newB]) => { ... })
```

### Lifecycle in `<script setup>`
```ts
import { onMounted, onUnmounted, onBeforeUnmount } from 'vue'

// No beforeCreate / created — setup() IS the created hook
onMounted(() => { /* DOM ready */ })
onUnmounted(() => { /* cleanup subscriptions, timers, event listeners */ })
```

---

## 2. `<script setup>` Component Patterns

### Props & Emits (TypeScript-first)
```vue
<script setup lang="ts">
// Props — always define type, always define defaults
const props = withDefaults(defineProps<{
  title: string
  count?: number
  variant?: 'primary' | 'secondary'
}>(), {
  count: 0,
  variant: 'primary',
})

// Emits — always type the payload
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit', payload: FormData): void
}>()
</script>
```

### v-model (Vue 3 pattern)
```vue
<!-- Parent -->
<MyInput v-model="name" />
<MyInput v-model:title="title" v-model:body="body" />

<!-- Child -->
<script setup lang="ts">
const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()
// Named: props.title + emit('update:title', v)
</script>
```

### defineExpose — Only When Necessary
```ts
// Only expose what parent components genuinely need
defineExpose({ focus, reset })
// Never expose internal state for external mutation — breaks encapsulation
```

### Template Refs
```ts
const tableRef = ref<InstanceType<typeof DataTable> | null>(null)
onMounted(() => tableRef.value?.refresh())
```

---

## 3. Composables Architecture

### The Golden Rules
- Name always starts with `use`
- One responsibility per composable
- Always return refs (not raw values) so reactivity survives destructuring
- Cleanup inside `onUnmounted` — never leave subscriptions open
- Side effects (fetch, WebSocket) belong in composables, not stores

```ts
// ✅ Well-structured composable
export function useUserProfile(userId: Ref<string>) {
  const profile = ref<UserProfile | null>(null)
  const isLoading = ref(false)
  const error = ref<Error | null>(null)

  async function fetch() {
    isLoading.value = true
    error.value = null
    try {
      profile.value = await api.getUser(userId.value)
    } catch (e) {
      error.value = e as Error
    } finally {
      isLoading.value = false
    }
  }

  watch(userId, fetch, { immediate: true })

  return { profile, isLoading, error, refresh: fetch }
}
```

### Composable vs Store — Decision Rule
| Use composable when... | Use store when... |
|------------------------|-------------------|
| Logic is local to a feature | State is shared across routes/components |
| State doesn't need to survive navigation | State persists across navigation |
| It wraps a single API call or DOM API | Multiple components read/write the same data |
| It doesn't need Pinia devtools | You want devtools + time-travel debugging |

---

## 4. Pinia State Management

### Store Patterns — Setup Style (Preferred)
```ts
// stores/useCartStore.ts
export const useCartStore = defineStore('cart', () => {
  // State — refs
  const items = ref<CartItem[]>([])
  const isLoading = ref(false)

  // Getters — computed
  const total = computed(() =>
    items.value.reduce((sum, i) => sum + i.price * i.qty, 0)
  )
  const itemCount = computed(() => items.value.length)

  // Actions — async functions
  async function addItem(product: Product) {
    isLoading.value = true
    try {
      await api.cart.add(product.id)
      items.value.push({ ...product, qty: 1 })
    } finally {
      isLoading.value = false
    }
  }

  function removeItem(id: string) {
    items.value = items.value.filter(i => i.id !== id)
  }

  return { items, isLoading, total, itemCount, addItem, removeItem }
})
```

### Consuming Stores — storeToRefs Pattern
```ts
// ✅ Destructure reactive properties with storeToRefs, actions directly
const cartStore = useCartStore()
const { items, total, isLoading } = storeToRefs(cartStore)  // reactive
const { addItem, removeItem } = cartStore                    // actions (not reactive)

// ❌ Never destructure without storeToRefs — breaks reactivity
const { items } = useCartStore()  // items is now a plain array, not reactive
```

### Cross-Store Composition
```ts
// ✅ Compose stores — call one store inside another
export const useOrderStore = defineStore('order', () => {
  const cartStore = useCartStore()  // fine inside setup stores
  const userStore = useUserStore()

  async function checkout() {
    await api.order.create({
      items: cartStore.items,
      userId: userStore.currentUser?.id,
    })
    cartStore.clear()
  }

  return { checkout }
})
```

### Store Resets
```ts
// Setup stores don't have $reset() — implement it manually
const initialState = { items: [], isLoading: false }
const state = reactive({ ...initialState })

function $reset() {
  Object.assign(state, initialState)
}
return { ...toRefs(state), $reset }
```

### Pinia Persistence (pinia-plugin-persistedstate)
```ts
export const useAuthStore = defineStore('auth', () => { ... }, {
  persist: {
    key: 'auth',
    storage: localStorage,
    paths: ['token', 'user'],  // only persist what's needed
  },
})
```

---

## 5. Vue Router 4 Integration

### Navigation Guards with Pinia
```ts
// router/guards.ts — don't use store inside router definition file
router.beforeEach(async (to) => {
  const authStore = useAuthStore()  // safe to call here, after pinia is initialized
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
})
```

### useRoute / useRouter in Composables
```ts
export function usePageTitle() {
  const route = useRoute()
  watchEffect(() => {
    document.title = (route.meta.title as string) ?? 'MyApp'
  })
}
// ⚠️ Only call useRoute/useRouter inside setup() or composables called from setup()
```

### Route Params as Refs
```ts
// ✅ params are reactive — watch them
const route = useRoute()
const userId = computed(() => route.params.id as string)
watch(userId, fetchUser, { immediate: true })
```

---

## 6. TypeScript Integration

### Typed Provide / Inject
```ts
// symbols.ts
import type { InjectionKey, Ref } from 'vue'
export const ThemeKey: InjectionKey<Ref<'light' | 'dark'>> = Symbol('theme')

// Provider
provide(ThemeKey, ref('light'))

// Consumer — type is inferred
const theme = inject(ThemeKey)  // Ref<'light' | 'dark'> | undefined
const theme = inject(ThemeKey, ref('light'))  // with default — never undefined
```

### Generic Components (Vue 3.3+)
```vue
<script setup lang="ts" generic="T extends { id: string }">
defineProps<{ items: T[]; selected: T | null }>()
defineEmits<{ (e: 'select', item: T): void }>()
</script>
```

---

## 7. Performance Patterns

```ts
// shallowRef — large objects where you only replace, never mutate deeply
const bigList = shallowRef<Item[]>([])
bigList.value = newItems  // triggers update; bigList.value.push() does NOT

// markRaw — objects that should never be reactive (class instances, third-party libs)
const map = markRaw(new mapboxgl.Map({ ... }))
const chart = markRaw(new Chart(ctx, config))
// Store these in ref(markRaw(...)) — reactivity wrapper without deep tracking

// v-memo — skip re-render when deps unchanged
<div v-for="item in list" :key="item.id" v-memo="[item.selected]">

// defineAsyncComponent — code-split heavy components
const HeavyChart = defineAsyncComponent(() => import('./HeavyChart.vue'))
```

---

## 8. Testing (Vitest + Vue Test Utils)

### Component Testing Pattern
```ts
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'

beforeEach(() => setActivePinia(createPinia()))

it('increments count on click', async () => {
  const wrapper = mount(Counter, {
    props: { initialCount: 0 },
  })
  await wrapper.find('[data-testid="increment"]').trigger('click')
  expect(wrapper.text()).toContain('1')
})
```

### Pinia Store Testing
```ts
it('addItem updates total', async () => {
  setActivePinia(createPinia())
  const cart = useCartStore()

  await cart.addItem({ id: '1', price: 10, qty: 1 })

  expect(cart.items).toHaveLength(1)
  expect(cart.total).toBe(10)
})
```

### Mocking Stores in Component Tests
```ts
const wrapper = mount(CartSummary, {
  global: {
    plugins: [createTestingPinia({
      createSpy: vi.fn,
      initialState: {
        cart: { items: [{ id: '1', price: 10, qty: 2 }] },
      },
    })],
  },
})
```

---

## 9. Anti-patterns to Catch

```ts
// ❌ Mutating props
props.value = 'new'  // → emit update or use v-model

// ❌ Destructuring reactive without toRefs
const { name } = reactive(state)  // name is now a plain string

// ❌ Calling composables conditionally
if (condition) useMyComposable()  // violates rules of hooks

// ❌ Storing non-serializable objects in Pinia without markRaw
const store = defineStore('map', () => {
  const map = ref(new mapboxgl.Map(...))  // ❌ deep reactive on class instance
  const map = ref(markRaw(new mapboxgl.Map(...)))  // ✅

// ❌ Using Options API mixed with Composition API in new code
// → Use <script setup> exclusively for all new components

// ❌ Importing store at module level (before pinia is initialized)
const store = useAuthStore()  // outside setup() or a lifecycle hook → crashes
```
