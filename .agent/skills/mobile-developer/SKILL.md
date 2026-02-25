---
name: Mobile Developer
description: >
  Use when building MOBILE APPS (native or cross-platform, NOT mobile web):
  cross-platform vs native tradeoffs, offline-first architecture, performance
  on constrained devices, deep linking, push notifications, app lifecycle
  management, responsive vs adaptive UI, and app store submission guidelines.
  For mobile-responsive websites, see Frontend Developer instead.
---

# Skill: Mobile Developer

**Purpose**: Teach an AI agent mobile development best practices — covering the unique constraints and patterns that differ from web development.

**Related Workflows**: `sdd_task_protocol.md`, `code_quality_assessment_protocol.md`, `regression_protocol.md`

---

## 1. Platform Strategy

### Decision Framework

| Factor | Native | Cross-Platform (React Native, Flutter) | PWA |
|--------|--------|---------------------------------------|-----|
| **Performance** | Best | Good (near-native) | Acceptable for content apps |
| **Platform APIs** | Full access | Most APIs via bridges/plugins | Limited (no push on iOS Safari) |
| **Development speed** | Slower (2 codebases) | Faster (1 codebase) | Fastest (web tech) |
| **Team skills** | Swift/Kotlin specialists | JS/Dart generalists | Web developers |
| **App Store** | Required | Required | Optional |
| **Best for** | Games, AR, heavy computation | Business apps, MVPs, content apps | Simple apps, content, internal tools |

### When to Choose What
- **Go native** when: 60fps animations are critical, heavy platform API usage, long-term flagship app
- **Go cross-platform** when: Speed to market matters, team knows JS/Dart, feature parity across platforms
- **Go PWA** when: Content-first app, no need for platform APIs, want to avoid app store review

---

## 2. Offline-First Architecture

### The Principle
Mobile apps must work without network. Design for offline first, sync when online.

### Architecture Pattern

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   UI Layer   │ ──► │  Local Store │ ──► │  Sync Engine │
│              │ ◄── │  (SQLite /   │ ◄── │  (Queue +    │
│              │     │   AsyncStore)│     │   Conflict   │
│              │     │              │     │   Resolution)│
└──────────────┘     └──────────────┘     └──────┬───────┘
                                                  │
                                           ┌──────▼───────┐
                                           │  Remote API  │
                                           └──────────────┘
```

### Rules
- **UI always reads from local store** — never directly from API
- **Writes go to local store first**, then sync queue
- **Sync engine handles**: retry, conflict resolution, batching
- **Conflict strategy**: Last-write-wins (simple) or merge (complex) — decide per entity

### Sync Queue Pattern
```
1. User creates/edits data → Save locally + add to sync queue
2. When online → Process queue items in order
3. If sync fails → Retry with exponential backoff
4. If conflict → Apply resolution strategy, notify user if needed
5. When all synced → Mark queue items as completed
```

### Offline States to Handle
- **No network**: Show cached data, allow writes to queue
- **Slow network**: Timeout gracefully, don't block UI
- **Intermittent**: Retry silently, batch sync when stable
- **First launch (no cache)**: Show skeleton + "Loading for first time..." message

---

## 3. Performance on Mobile

### Constraints vs Web
- **Memory**: 2-4GB shared with OS and other apps (vs 8-16GB desktop)
- **CPU**: Efficient but thermal throttling under load
- **Battery**: Every computation costs battery life
- **Network**: Variable speeds, high latency, data caps

### Performance Budget

| Metric | Target |
|--------|--------|
| App launch (cold start) | < 2 seconds |
| Screen transition | < 300ms |
| List scrolling | 60fps (no dropped frames) |
| API response handling | < 100ms to show feedback |
| App size (download) | < 50MB (ideal), < 100MB (acceptable) |
| Memory usage | < 200MB baseline |

### Optimization Techniques

**Rendering**:
- Virtualize long lists (FlatList, RecyclerView, ListView.builder)
- Avoid re-renders: memoize components, use keys properly
- Offload heavy work to background threads (Web Workers, Isolates, WorkManager)
- Optimize images: resize to display size, cache aggressively, use WebP

**Network**:
- Compress API responses (gzip/brotli)
- Paginate everything (never load full datasets)
- Prefetch next-screen data during idle time
- Cache API responses locally with expiry

**Storage**:
- Use SQLite for structured data (not AsyncStorage for everything)
- Clean up old cache periodically
- Compress stored images and large blobs

---

## 4. Deep Linking

### Types

| Type | URL Example | Behavior |
|------|-------------|----------|
| **Standard deep link** | `myapp://books/123` | Opens app if installed, fails otherwise |
| **Universal/App Link** | `https://myapp.com/books/123` | Opens app if installed, falls back to web |
| **Deferred deep link** | `https://myapp.com/books/123` | Redirects to store if not installed, opens to correct screen after install |

### Implementation Checklist
```
[ ] Define URL scheme (myapp://) and/or universal links (https://domain/path)
[ ] Handle deep links at app entry point (route to correct screen)
[ ] Handle deep links when app is already open (navigate within app)
[ ] Test: link from browser, from another app, from notification, from email
[ ] Analytics: Track deep link sources and conversion
```

### Route Mapping Pattern
```
URL: /books/:id         → Screen: BookDetailScreen(id)
URL: /books?filter=:cat → Screen: BookListScreen(filter=cat)
URL: /profile           → Screen: ProfileScreen (requires auth)
URL: /invite/:code      → Screen: OnboardingScreen(inviteCode)
```

---

## 5. Push Notifications

### Architecture
```
Server → Push Service (APNs / FCM) → Device → App → Handle
```

### Best Practices
- **Request permission at the right moment** — not on first launch, but when the user understands the value
- **Segment notifications**: Don't send everything to everyone
- **Rich notifications**: Include image, action buttons, deep link
- **Silent notifications**: Update data in background without alerting user
- **Respect the user**: Easy opt-out, clear notification preferences

### Notification Payload Design
```json
{
  "title": "New book added to your shelf",
  "body": "\"The Design of Everyday Things\" is now in your library",
  "data": {
    "type": "book_added",
    "book_id": "123",
    "deep_link": "/books/123"
  },
  "image": "https://covers.example.com/123.jpg"
}
```

---

## 6. App Lifecycle

### States
```
Not Running → Launching → Active → Background → Suspended → Terminated
```

### What to Do in Each State

| Transition | Action |
|-----------|--------|
| **Launch** | Restore last state, check auth, sync if online |
| **Active → Background** | Save state, pause timers, flush pending writes |
| **Background** | Process sync queue (if allowed), handle push notifications |
| **Background → Active** | Refresh data, check auth token expiry, resume timers |
| **Terminate** | Save critical state, clean up resources |

### State Persistence
- Save UI state (scroll position, form data, selected tab) to survive kills
- Use restoration keys / state preservation APIs
- Test: kill app from multitasking, reopen → should restore context

---

## 7. Responsive vs Adaptive UI

### Responsive (Fluid)
Same layout adjusts continuously to screen size. Best for simple layouts.
```
Phone: 1 column, full width cards
Tablet: 2 columns, cards resize
```

### Adaptive (Breakpoint-based)
Different layouts for different device classes. Best for complex layouts.
```
Phone:  Stack navigation, bottom tabs, compact cards
Tablet: Split view (list + detail side by side), larger touch targets
```

### Platform-Specific UI Patterns

| Pattern | iOS | Android |
|---------|-----|---------|
| **Navigation** | Tab bar (bottom), push/pop stack | Bottom nav, drawer, top tabs |
| **Back** | Swipe from left edge | Hardware/software back button |
| **Actions** | Action sheets from bottom | Dialogs, snackbars, FAB |
| **Lists** | Swipe to delete, pull to refresh | Long press context menu, swipe actions |

### Rule
Respect platform conventions — don't build iOS patterns on Android or vice versa. Cross-platform frameworks offer platform-adaptive components for this.

---

## 8. App Store Guidelines

### Common Rejection Reasons
- **Crashes and bugs**: Test on real devices before submission
- **Incomplete information**: Missing screenshots, unclear description
- **Privacy**: Not declaring data usage, missing privacy policy
- **Login wall**: Apple requires "Sign in with Apple" if you offer other social logins
- **Payments**: In-app purchases must use the store's payment system (iOS)
- **Performance**: App too slow, excessive battery drain

### Submission Checklist
```
[ ] Tested on minimum supported OS version
[ ] Tested on multiple screen sizes (including oldest supported device)
[ ] Privacy policy URL provided
[ ] App Store description, screenshots, and metadata complete
[ ] Data usage declarations accurate
[ ] No private API usage
[ ] App size within acceptable limits
[ ] Deep links and notifications tested
[ ] Analytics and crash reporting integrated
```

---

---

## Scope & Boundaries

This skill is for **mobile apps** (React Native, Flutter, Swift, Kotlin) — NOT mobile-responsive websites.

```
"Make the website work well on phones"       → Frontend Developer (responsive CSS)
"Build an iOS/Android app"                   → Mobile Developer (this skill)
"Design the mobile app UX"                   → UX/UI Designer (experience) + Mobile Developer (platform patterns)
"API for the mobile app to consume"          → Backend Developer
"Test strategy for the mobile app"           → QA Engineer (strategy) + Mobile Developer (device-specific testing)
```

### Decision Tree

```
Building a native/cross-platform mobile app?
  └─ YES → Mobile Developer
Making a website responsive for mobile browsers?
  └─ YES → Frontend Developer
Building a PWA (Progressive Web App)?
  └─ Mostly web tech? → Frontend Developer
  └─ Need app store distribution? → Mobile Developer
Designing how the app should feel on mobile?
  └─ UX patterns? → UX/UI Designer
  └─ Platform-specific conventions (iOS vs Android)? → Mobile Developer
```

---

## When to Apply This Skill

- During **Specify** phase: Define platform strategy, offline requirements, notification needs
- During **Plan** phase: Design offline architecture, data sync strategy, navigation structure
- During **Tasks** phase: Decompose by feature + platform layer (data, sync, UI, notifications)
- During **Implementation**: Follow performance budgets, test on real devices
- During **Review**: Validate offline behavior, check app store compliance
