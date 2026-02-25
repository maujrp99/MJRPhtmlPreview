# Design Patterns — Extended Reference

## Table of Contents
- [Creational Patterns](#creational-patterns)
- [Structural Patterns](#structural-patterns)
- [Behavioral Patterns](#behavioral-patterns)
- [Pattern Selection Guide](#pattern-selection-guide)
- [Common Anti-Patterns](#common-anti-patterns)

---

## Creational Patterns

### Factory Method
**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate.

**When to use:**
- A class can't anticipate which objects it must create
- A class wants its subclasses to specify the objects it creates
- You want to localize the knowledge of which class gets created

**Structure:**
```
Creator ---> FactoryMethod() (abstract)
    |
    └── ConcreteCreator ---> ConcreteProduct
```

**Real example in a Next.js/TypeScript context:**
```typescript
// Bad: hardcoded dependency
class BookRepository {
  fetch() { return new PostgresDB().query('SELECT * FROM books') }
}

// Good: Factory Method pattern
interface DataSource { query(sql: string): Promise<any[]> }
class BookRepository {
  constructor(private db: DataSource) {}
  fetch() { return this.db.query('SELECT * FROM books') }
}
// Tests use MockDataSource; prod uses PostgresDataSource
```

---

### Abstract Factory
**Intent:** Provide an interface for creating families of related objects without specifying their concrete classes.

**When to use:**
- System must be independent of how products are created
- System needs multiple families of products (e.g., Light theme + Dark theme components)
- You want to enforce product family constraints (don't mix dark buttons with light inputs)

---

### Builder
**Intent:** Separate construction of a complex object from its representation.

**When to use:**
- Creating complex objects with many optional parameters
- The same construction process should create different representations
- Avoid telescoping constructors (10-parameter constructors)

**Real example:**
```typescript
// Bad: 8-parameter constructor
new EmailNotification(to, from, subject, body, cc, bcc, attachments, priority)

// Good: Builder
new EmailNotificationBuilder()
  .to('user@example.com')
  .subject('Your order shipped')
  .body(renderTemplate('order-shipped', data))
  .build()
```

---

### Singleton
**Intent:** Ensure a class has only one instance and provide a global access point.

**Red flags:** Use Singleton only when you genuinely need one instance, not for convenience.
- Singletons make testing hard (shared state between tests)
- Often a sign that global state is being hidden
- In Next.js, module-level exports (`export const db = new Database()`) are a safer Singleton equivalent

---

## Structural Patterns

### Adapter
**Intent:** Convert the interface of a class into another interface clients expect.

**Clean Architecture connection:** This is the canonical pattern for the **Interface Adapters** layer. Every time you wrap a third-party library, you are implementing Adapter.

**Real example:**
```typescript
// Your system speaks: ContentSource interface
interface ContentSource {
  getBooks(): Promise<Book[]>
}

// Third-party Obsidian vault speaks differently
class ObsidianVaultAdapter implements ContentSource {
  constructor(private vault: ObsidianVault) {}
  async getBooks(): Promise<Book[]> {
    const files = await this.vault.getMarkdownFiles('books/')
    return files.map(this.parseBookFrontmatter)
  }
}
// Now your use cases talk to ContentSource, never to ObsidianVault
```

---

### Bridge
**Intent:** Decouple an abstraction from its implementation so both can vary independently.

**When to use:**
- You want to avoid permanent binding between abstraction and implementation
- Both abstraction and implementation should be extensible via subclassing
- Changes in implementation should not affect clients

**Distinction from Adapter:** Adapter makes unrelated classes work together; Bridge separates a class into two hierarchies that can evolve independently.

---

### Composite
**Intent:** Compose objects into tree structures to represent part-whole hierarchies.

**When to use:**
- You want clients to treat individual objects and compositions uniformly
- File system (File + Folder both implement FileSystemItem)
- UI component trees (Leaf + Container both implement Component)
- Menu items (MenuItem + MenuGroup both implement MenuElement)

---

### Decorator
**Intent:** Attach additional responsibilities to an object dynamically.

**Prefer over inheritance when:** You need to add behavior at runtime, or the number of feature combinations would cause a class explosion via inheritance.

**Real example in Next.js middleware:**
```typescript
// Each middleware "decorates" the request handler
withAuth(withLogging(withRateLimit(handler)))
```

---

### Facade
**Intent:** Provide a unified interface to a set of interfaces in a subsystem.

**Clean Architecture connection:** A Facade IS a Gateway in Clean Architecture terms. It hides the complexity of the data layer, external APIs, or any complex subsystem.

**Real example:**
```typescript
// Without Facade: use cases scatter calls across 4 services
// With Facade:
class BookEnrichmentService {
  constructor(
    private openLibrary: OpenLibraryClient,
    private coverFetcher: CoverFetcher,
    private llmSummarizer: LLMClient,
    private imageStore: ImageStore,
  ) {}

  async enrich(isbn: string): Promise<EnrichedBook> {
    // orchestrates all 4 services behind one clean interface
  }
}
```

---

### Proxy
**Intent:** Provide a surrogate or placeholder for another object to control access.

**Types:**
- **Virtual Proxy:** Lazy initialization (load heavy object only when needed)
- **Protection Proxy:** Access control (check permissions before delegating)
- **Remote Proxy:** Local representative for an object in a different address space
- **Caching Proxy:** Cache results of expensive operations
- **Logging Proxy:** Record all access for audit/debugging

---

## Behavioral Patterns

### Strategy
**Intent:** Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Clean Architecture connection:** This is how you keep conditionals out of use cases. Each "case" becomes a Strategy implementation injected from the outer layer.

**Real example:**
```typescript
// Bad: conditional in use case
function sortBooks(books: Book[], sortType: string) {
  if (sortType === 'title') return books.sort(byTitle)
  if (sortType === 'date') return books.sort(byDate)
  if (sortType === 'rating') return books.sort(byRating)
}

// Good: Strategy pattern
interface SortStrategy { sort(books: Book[]): Book[] }
class TitleSortStrategy implements SortStrategy { ... }
class DateSortStrategy implements SortStrategy { ... }

function sortBooks(books: Book[], strategy: SortStrategy) {
  return strategy.sort(books)
}
```

---

### Observer
**Intent:** Define a one-to-many dependency so that when one object changes state, all dependents are notified automatically.

**When to use:**
- When a change in one object requires changing others, and you don't know how many
- When an object should be able to notify other objects without assumptions about who they are
- UI event systems, domain events, webhooks, pub/sub

**In Next.js context:** React's `useState` + component re-renders IS Observer. Custom events and Zustand stores also implement Observer.

---

### Command
**Intent:** Encapsulate a request as an object, thereby letting you parameterize clients, queue or log requests, and support undoable operations.

**When to use:**
- Undo/redo functionality
- Request queuing, scheduling, or retry logic
- Logging all requests that change system state
- Transactional operations that need rollback

---

### Template Method
**Intent:** Define the skeleton of an algorithm in an operation, deferring some steps to subclasses.

**When to use:**
- Multiple classes share the same algorithm skeleton but differ in specific steps
- Migration scripts, report generators, data pipelines with fixed flow but variable steps

**Distinction from Strategy:** Template Method uses inheritance; Strategy uses composition. Prefer Strategy for flexibility.

---

### State
**Intent:** Allow an object to alter its behavior when its internal state changes.

**When to use:**
- Object behavior depends heavily on its state, and must change at runtime
- Replacing large conditional chains based on state
- Book status: Seed → Sprout → Evergreen (behavior changes at each stage)
- Order status: pending → processing → shipped → delivered

---

### Chain of Responsibility
**Intent:** Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request.

**In Next.js context:** Middleware stack is Chain of Responsibility. Each middleware either handles the request or passes it down the chain.

---

## Pattern Selection Guide

### "I have too many conditionals"
- Conditionals on **type/subtype** → Factory Method or Strategy
- Conditionals on **state** → State pattern
- Conditionals on **command type** → Command pattern

### "I need to add behavior without changing classes"
- At runtime, dynamically → Decorator
- At compile time, via new subclasses → Template Method

### "I need to isolate a third-party library"
- Single incompatible interface → Adapter
- Complex subsystem with many classes → Facade

### "I need to control object creation"
- Single class, deferred to subclass → Factory Method
- Families of related objects → Abstract Factory
- Complex object with many parts → Builder
- Only one instance ever → Singleton (use sparingly)

### "I need communication between objects"
- One sender, many receivers → Observer
- Decouple many-to-many → Mediator
- Request as object (undo, queue) → Command

---

## Common Anti-Patterns

### God Class
One class that knows too much and does too much. Violates SRP. Usually has vague names: `Manager`, `Handler`, `Processor`, `Service` with 50+ methods.

### Anemic Domain Model
Domain objects that are just data containers (no behavior). All behavior lives in service classes. This is the procedural style disguised as OO. Violates Tell, Don't Ask.

### Singleton Abuse
Using Singleton as a global variable store. Makes testing nearly impossible (can't reset state between tests). Prefer dependency injection.

### Premature Abstraction
Creating abstract interfaces for things that only have one implementation. "You Aren't Gonna Need It" (YAGNI). Add abstractions when you have two different implementations.

### Framework Coupling
Letting the framework's patterns invade your business logic. `useRouter()` in a business rule. ORM models in use cases. Database column names in domain entities.

### Magic Strings
`if (status === 'evergreen')` scattered across 15 files. When the value changes, you hunt. Use typed enums or constants in a single authoritative location.
