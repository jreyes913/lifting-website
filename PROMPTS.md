# Lifting Website Prompt History

## 1. Styling Task Prompt (4/4/2026)

You are a frontend CSS specialist. Your job is to style an existing web application to match the design specifications in `DESIGN.md`.

### Context

- The backend is complete and should not be touched.
- The HTML/JS skeleton of the frontend is already built and functional.
- The primary file you should be working in is `main.css` (or the project's main stylesheet). Make as many changes as needed there.
- For all other frontend files (HTML, JS, templates, etc.), make the **absolute minimum changes necessary** — only modify them if the design specs cannot be achieved through CSS alone (e.g., adding a class name, wrapping element, or a missing structural element required by the design).

### Instructions

1. **Read `DESIGN.md` thoroughly** before making any changes. Understand every design requirement — layout, typography, colors, spacing, responsive behavior, animations, component styles, etc.

2. **Read all existing frontend files** (HTML, JS, CSS) to understand the current structure, existing class names, IDs, and how components are organized.

3. **Implement the design in `main.css`**, using the existing HTML structure and class names wherever possible. Prefer CSS selectors that target what already exists over adding new classes.

4. **If and only if** a design requirement cannot be achieved with CSS alone, make minimal, targeted changes to HTML/JS files. Examples of acceptable changes:
   - Adding a CSS class or `data-` attribute to an element
   - Adding a wrapper `<div>` needed for a layout
   - Adding a semantic element required by the design (e.g., a `<span>` for an icon)
   - Do **not** restructure, rename, or refactor existing code
   - Do **not** change any JS logic, event handling, API calls, or data flow

5. **Log every change** you make in `CHANGES.md` using this format:

   ```
   # Changes Made

   ## main.css
   - [description of what was added/changed and why]

   ## other-file.html (if applicable)
   - [exact change made, e.g., "Added class 'card--featured' to line X"]
   - [reason: "Needed to differentiate featured cards for distinct styling per DESIGN.md section Y"]
   ```

   Group changes by file. For non-CSS files, be specific about what changed and cite the design requirement that necessitated it.

### Rules

- **Do not modify any backend files.**
- **Do not modify any JavaScript application logic.** Only touch JS files if you must add a class toggle or similar purely presentational concern, and only as a last resort.
- **Do not install new dependencies or add external stylesheets/CDNs** unless explicitly specified in `DESIGN.md`.
- **Do not remove existing functionality.** The app must work exactly as it did before, just styled differently.
- **Preserve all existing class names and IDs.** Add new ones if needed, but never rename or remove existing ones.
- Write clean, well-organized, commented CSS.
- Use CSS custom properties (variables) for colors, fonts, and recurring values where it improves maintainability.
- Ensure responsive behavior if specified in `DESIGN.md`. If not specified, ensure nothing breaks at common viewport sizes.

### Workflow

1. Read `DESIGN.md`
2. Read all frontend source files
3. Plan your approach
4. Implement styles in `main.css`
5. Make minimal non-CSS changes only if required
6. Verify the result visually if possible
7. Write `CHANGES.md`


## 2. Information UX Optimization Prompt (4/4/26)

You are a Senior UX Engineer specializing in **Cognitive Load Theory** and **Information Architecture**. Your task is to audit and refine the existing HTML/JavaScript display to ensure the information is presented with maximum clarity, hierarchy, and user understanding.

### Context

- The core data and backend are fixed; your focus is purely on the **presentation layer**.
- The current application is functional but suffers from "information dump" syndrome.
- You will be provided with a `USER_GOALS.md` file (or a description of the user's primary intent) which should guide your prioritization.
- The primary goal is to minimize the user's "interaction cost"—the mental and physical effort required to find and understand information.

### Instructions

1. **Analyze the Data Flow**: Read through the HTML/JS to identify what information is "primary" (essential for the user's next step) and what is "secondary" (supporting details).
2. **Audit for Scannability**: Identify walls of text, poorly grouped data, and lack of visual anchors. Your job is to ensure a user can grasp the status of the page in under 3 seconds.
3. **Optimize the Interface**:
    - **Hierarchy**: Use typography (weight, size, color) to clearly distinguish headings from metadata.
    - **Grouping**: Use whitespace and subtle borders to group related pieces of information (Gestalt Principles).
    - **Signal-to-Noise**: De-emphasize or hide repetitive labels. For example, if a list is all "Dates," use a single header instead of repeating "Date: " on every line.
    - **Formatting**: Apply logic for data formatting (e.g., human-readable dates, currency alignment, or status-based color coding).

4. **Implement via CSS-First**:
    - Use `main.css` for 90% of the work (flexbox/grid for layout, pseudo-elements for icons/labels).
    - Only modify HTML/JS to add semantic wrappers, conditional classes (e.g., `is-urgent`), or to adjust the *order* of data if it improves the logical flow.

5. **Log Cognitive Improvements**: Document your changes in `UX_CHANGES.md` focusing on the *why*. Use this format:

   # UX Changes Made

   ## Information Hierarchy
   - **Change**: [e.g., Increased font-weight of 'Status' and moved to top-right]
   - **UX Reason**: [e.g., This is the user's primary decision-making data point per USER_GOALS.md]

   ## Data Density
   - **Change**: [e.g., Converted table layout to card-based grid for mobile]
   - **UX Reason**: [e.g., Reduces horizontal scrolling and improves scan-rate on small screens]

### Rules

- **Do not touch business logic**: If the JS calculates a value, do not change the calculation—only how the result is displayed.
- **No "Mystery Meat" Navigation**: Do not use icons without labels or tooltips unless they are universally understood (e.g., a magnifying glass for search).
- **Preserve Data Integrity**: Never remove data points entirely to "clean up" the UI unless they are truly redundant; instead, move them to a secondary "Details" view or tooltip.
- **Accessibility (a11y)**: Ensure that your styling tweaks maintain high color contrast and do not break screen reader accessibility.

### Workflow

1. **Map Intent**: Review `USER_GOALS.md` to identify the "North Star" of this view.
2. **Structural Review**: Read the HTML/JS to find where data is being injected.
3. **Pruning & Prioritization**: Plan which elements need more "visual weight" and which need less.
4. **Execute CSS Styles**: Focus on spacing, typography, and visual grouping.
5. **Refactor Display Logic**: (Only if needed) adjust JS template literals or HTML structure to better serve the user's mental model.
6. **Verify**: Ensure the most important information is the first thing the eye hits.


## 3. Full-Stack Testing Implementation Prompt (4/4/2026)

You are a Senior QA Automation Engineer. Your task is to implement a robust, professional testing suite for both the frontend and backend of this application to ensure stability, prevent regressions, and document expected behavior.

### Context

- The application is currently functional but lacks comprehensive test coverage.
- You must identify the core business logic in the backend and critical user flows in the frontend.
- You should use the existing testing framework if one is initialized (e.g., Jest, Vitest, Pytest, Cypress, Playwright); if none exists, use the industry standard most appropriate for the stack.

### Instructions

1. **Audit the Codebase**: 
    - Identify high-risk backend functions (e.g., data mutations, auth logic, API endpoints).
    - Identify critical frontend interactions (e.g., form submissions, navigation, state changes).
2. **Backend Testing**:
    - Implement **Unit Tests** for isolated business logic and helper functions.
    - Implement **Integration Tests** for API endpoints, ensuring correct status codes and payload structures.
    - Use mocks/stubs for external dependencies (e.g., third-party APIs) to ensure tests are deterministic.
3. **Frontend Testing**:
    - Implement **Component Tests** to verify that UI elements render correctly based on props/state.
    - Implement **End-to-End (E2E) Tests** for the most critical "happy paths" (e.g., a user successfully completing a primary task).
    - Verify accessibility (a11y) standards are met during UI tests.
4. **Test Data Management**: Create reusable factories or fixtures to ensure tests have a clean, predictable state. Avoid "brittle" tests that rely on hardcoded IDs that may change.

5. **Log Test Coverage**: Document the new testing surface in `TESTING_REPORT.md` using this format:

   # Testing Implementation Report

   ## Backend Coverage
   - **Suite**: [e.g., controllers/auth.test.js]
   - **Focus**: [e.g., Validates JWT issuance and password hashing logic]

   ## Frontend Coverage
   - **Suite**: [e.g., e2e/registration.spec.ts]
   - **Focus**: [e.g., Full user sign-up flow including validation error handling]

### Rules

- **Do not modify production logic**: Your job is to test the code, not refactor it. If you find a bug, document it in the report rather than fixing it, unless the fix is trivial and required for the test to pass.
- **Isolate Tests**: Ensure that running the test suite does not pollute the production database or external state.
- **Maintainability**: Write "DRY" (Don't Repeat Yourself) test code. Use `beforeEach` and `afterEach` hooks effectively.
- **Speed**: Prioritize unit and integration tests over E2E tests to keep the CI pipeline fast.
- **No Flakiness**: Ensure tests pass consistently. Use proper wait-for logic in frontend tests instead of arbitrary timeouts.

### Workflow

1. **Discovery**: Map out all API routes and UI components.
2. **Environment Setup**: Configure the test runner and environment variables.
3. **Backend Implementation**: Write and pass backend unit/integration tests.
4. **Frontend Implementation**: Write and pass component/E2E tests.
5. **Final Audit**: Run the full suite 5 times to ensure no intermittent failures (flakiness).
6. **Documentation**: Append the changes made to `CHANGES.md`, maintaining current document structure.

## 4. Data Portability Implementation Prompt

You are a Senior Full-Stack Engineer. Your task is to implement a robust **Import/Export** system that allows users to download their data as a JSON file and re-upload it to restore the application state.

### Context

- The application manages local or database state that needs to be portable.
- You must handle the serialization (export) and parsing/validation (import) of the application's data structures.
- The primary format for both operations is **JSON**.

### Instructions

1.  **Analyze Data Schema**: Identify all relevant data models, state objects, or database collections that constitute a user's full profile/session.
2.  **Implement Export Logic**:
    * Create a utility to aggregate current data into a single, structured JSON object.
    * Trigger a browser-side "Save As" dialog with a timestamped filename (e.g., `data-export-2026-04-04.json`).
    * Ensure the exported JSON is "pretty-printed" (indented) for human readability.
3.  **Implement Import Logic**:
    * Create a file upload handler that accepts `.json` files.
    * **Validation**: Before applying the data, validate the schema of the uploaded file. Ensure required fields exist and data types are correct to prevent application crashes.
    * **Conflict Resolution**: Implement a "Overwrite" strategy where the imported data replaces the current state, unless a "Merge" strategy is explicitly requested in the UI.
4.  **UI/UX Integration**:
    * Add "Export Data" and "Import Data" buttons to the settings or profile section.
    * Provide visual feedback (e.g., success toasts or error alerts) for both operations.
    * Implement a loading state for large data imports.

5.  **Log Integration Details**: Document every change you make in `CHANGES.md` using this format:

   # Changes Made

   ## [File Name]
   - **Change**: [e.g., Added `handleExport` function to `App.js`]
   - **Reason**: [e.g., Required to aggregate Redux state into a downloadable JSON blob]

   ## [File Name]
   - **Change**: [e.g., Added file input and 'Import' button to `Settings.html`]
   - **Reason**: [e.g., Provides the user interface for triggering the JSON data restoration]

### Rules

-   **Data Integrity**: Ensure that an Export followed immediately by an Import results in an identical application state (Idempotency).
-   **Security**: Sanitize all imported data before injecting it into the DOM or state to prevent XSS attacks. 
-   **No Partial Imports**: If the JSON is invalid, the import should fail entirely rather than importing a "broken" partial state.
-   **File Size Handling**: Implement basic checks to prevent the browser from crashing on extremely large JSON files.
-   **Minimal Structural Change**: Reuse existing data-access patterns (Redux, Context, or API calls) to update the state.

### Workflow

1.  **Map State**: Define exactly what needs to be exported to recreate the user experience.
2.  **Develop Serializer**: Write the logic to transform state/DB into a JSON string.
3.  **Develop Parser**: Write the logic to validate and transform JSON back into application state.
4.  **Frontend Wiring**: Create the UI triggers and file upload listeners.
5.  **End-to-End Test**: Export a complex state, clear the app, import the file, and verify consistency.
6.  **Document**: Complete the `CHANGES.md` log.

## 6. Data Visualization Implementation Prompt (4/8/2026)

Implement a data visualization feature on the `progress.html` page.

**UI Components** -- Add the following dropdown selectors: a Date selector (populated with available workout dates), an Exercise selector (dynamically populated based on the selected date), and a Metric selector (independent of the others) with options: load, intensity, RTL, weight, volume.

**Chart** — Add a chart (Chart.js) that updates dynamically based on the selected date, exercise, and metric. The chart should visualize the selected metric across sets (or over time, depending on available data).

**Data Integration** — Fetch data from the backend endpoint `/strength/` located in `backend/app.py`. Pass the selected dropdown values as query parameters to the API. Ensure the frontend properly parses and uses the returned data.

**Dynamic Behavior** — When the date changes, update the exercise dropdown accordingly. When any selector changes, refresh the chart with new data. Ensure smooth UX.

**Code Updates** — Modify HTML, CSS, and JavaScript as needed. Keep the structure clean and modular. Use existing JS structure in the project, even if it is not common practice, as much as possible.

**Goal**: Create a clean, responsive interface that allows a user to explore their training data interactively by selecting date, exercise, and metric, with the chart updating in real time.

---

## 7. Progress Button Styling + Changelog Prompt (4/8/2026)

Make the progress button look more appealing in the athlete page, then log all updates you have made in CHANGES.md and PROMPTS.md.

---

## 5. Navigation & Transition Implementation Prompt

You are a Senior Frontend Developer. Your task is to refactor the application's routing to support a fully interconnected page architecture with fluid visual transitions.

### Context

- The current navigation is limited to a "Hub and Spoke" model (Home -> Subpage -> Home).
- You must enable direct lateral navigation between sibling pages and sub-modules.
- All routing changes must be accompanied by smooth CSS transitions or Framer Motion/GSAP animations to improve perceived performance.

### Instructions

1. **Refactor Routing**: Audit the current router (or conditional rendering logic) and modify it to allow any-to-any page navigation.
2. **Implement Transitions**: Add enter/exit animations for page containers. Ensure that moving "deeper" into the hierarchy feels different than moving "laterally."
3. **State Preservation**: Ensure that navigating between pages does not unnecessarily reset scroll positions or clear transient UI states unless intended.
4. **Update UI**: Modify navigation bars, breadcrumbs, or "Back" buttons to reflect the new non-linear pathing.

5. **Log Changes**: Document every file modification in `CHANGES.md` using this format:

   ## [File Name]
   - **Change**: [e.g., Replaced static 'Home' link with dynamic breadcrumb component]
   - **Reason**: [e.g., To support lateral navigation between 'Settings' and 'Profile']

### Rules

- **No Broken Links**: Every page must be reachable from its logical neighbors.
- **Performance**: Animations must be performant (use `transform` and `opacity`) and should not exceed 300ms.
- **Logic Integrity**: Do not break existing deep-linking or URL parameters.
- **Minimalism**: Use existing CSS classes for animations where possible.

### Workflow

1. Map the new interconnected site architecture.
2. Implement the expanded routing logic.
3. Add global transition wrappers.
4. Update navigation components.
5. Verify flow in `CHANGES.md`.
