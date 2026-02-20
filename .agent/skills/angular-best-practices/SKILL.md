---
name: Angular Best Practices
description: Detailed guidelines and patterns for building scalable and performant Angular applications.
---

# Angular Frontend Development Skills

This skill provides a set of best practices and architectural patterns for developing Angular applications. These guidelines are synthesized from community-standard repositories and expert recommendations.

## 1. Project Structure & Architecture

### Modular Design
- **Core Module (`core/`)**: Place singleton services, static components (like navbar, footer), and interceptors here. Import `CoreModule` only once in the `AppModule`.
- **Shared Module (`shared/`)**: Place reusable components, directives, and pipes that are used across multiple feature modules. Import `SharedModule` in feature modules where needed.
- **Feature Modules (`features/`)**: Organize the application by domain features. Each feature should have its own module with its routing, components, and services.

### Component Architecture
- **Smart (Container) Components**: 
  - Responsible for fetching data, interacting with services, and managing state.
  - Pass data down to presentation components via `@Input()`.
  - Handle events from presentation components via `@Output()`.
- **Dumb (Presentational) Components**:
  - Focus purely on display logic.
  - Receive data via `@Input()` and emit events via `@Output()`.
  - Should not have dependencies producing side effects (e.g., HTTP services).

## 2. State Management & Data Flow

- **Unidirectional Data Flow**: Data flows down, events flow up. Avoid two-way binding (`[(ngModel)]`) unless absolutely necessary for forms.
- **Reactive Programming (RxJS)**:
  - Use `Observable` streams for data handling.
  - Avoid nested subscriptions. Use operators like `switchMap`, `catchError`, and `tap` to manage streams.
  - Prefer the `async` pipe in templates over manual `.subscribe()` in components to manage subscriptions automatically and prevent memory leaks.

## 3. Performance Optimization

- **Change Detection Strategy**: Set `changeDetection: ChangeDetectionStrategy.OnPush` for presentation components to improve performance by reducing checking cycles.
- **Lazy Loading**: Configure routes to lazy load feature modules. This reduces the initial bundle size and speeds up load time.
- **TrackBy Function**: Always use `trackBy` with `*ngFor` to minimize DOM manipulations when list items change.
- **Strict Typing**: Avoid `any`. Define interfaces/models for all data structures to leverage TypeScript's type safety.

## 4. Coding Standards

- **Naming Conventions**: Follow Angular style guide. 
  - Files: `feature-name.component.ts`, `data.service.ts`
  - Classes: `FeatureNameComponent`, `DataService`
- **Logic Separation**: Keep complex business logic out of components; delegate it to services.
- **Environment Configuration**: Use `environment.ts` for configuration variables (API endpoints, feature flags).

## 5. Testing

- Write unit tests for all components and services using Jasmine/Karma.
- Focus on testing component interaction (inputs/outputs) and service logic.

---
Source Inspiration:
- Angular Best Practices (GitHub)
- Angular Performance Checklist
