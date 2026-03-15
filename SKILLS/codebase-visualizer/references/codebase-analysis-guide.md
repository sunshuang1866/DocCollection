# Codebase Analysis Guide

Use this guide during Step 1 to systematically extract information from the project.

## 1. Tech Stack Detection

Scan these files to identify languages, frameworks, and runtimes:
- `package.json` / `requirements.txt` / `go.mod` / `Cargo.toml` / `pom.xml` → dependencies
- `Dockerfile` / `docker-compose.yml` → container/service topology
- `.env.example` / `.env` / config files → external service keys and endpoints
- CI/CD files (`.github/workflows/`, `Jenkinsfile`) → build/deploy pipeline

## 2. Component Identification

Identify logical components (not files) by looking for:
- **Entry points:** `main.*`, `index.*`, `app.*`, `server.*`
- **Route/controller layers:** files in `routes/`, `controllers/`, `handlers/`, `api/`
- **Business logic:** files in `services/`, `use-cases/`, `domain/`, `core/`
- **Data access:** files in `repositories/`, `models/`, `db/`, `store/`
- **Background jobs:** files in `workers/`, `jobs/`, `tasks/`, `queue/`
- **Frontend:** files in `components/`, `pages/`, `views/`, `ui/`

Group these into 3–5 architecture layers. If uncertain, default to: Frontend → API Gateway → Services → Data → External.

## 3. Communication Pattern Detection

For each component, find how it communicates:
- **HTTP/REST calls:** look for `fetch(`, `axios`, `requests.get`, `http.Get`, `@GET`, `router.get`
- **Database queries:** look for `query(`, `find(`, `SELECT`, ORM method chains
- **Message queues:** look for `publish(`, `subscribe(`, `produce(`, `consume(`, queue/topic names
- **Event emitters:** look for `emit(`, `on(`, `EventEmitter`, `addEventListener`
- **Webhooks:** look for webhook URL patterns, `/webhook` routes
- **WebSocket:** look for `ws://`, `socket.on`, `io.emit`

Map the top 3–5 user-facing scenarios (e.g., "user signs up", "user places an order") as multi-step communication chains.

## 4. Third-Party Service Detection

Scan imports and config for known services:
- **Auth:** Auth0, Clerk, Firebase Auth, Supabase Auth, Cognito, NextAuth
- **Storage:** S3, GCS, Azure Blob, Cloudinary, Uploadthing
- **Database:** PostgreSQL, MySQL, MongoDB, Redis, Supabase, PlanetScale, Neon
- **Email:** SendGrid, Resend, Mailgun, SES, Postmark
- **Payments:** Stripe, PayPal, Paddle, LemonSqueezy
- **AI/ML:** OpenAI, Anthropic, Replicate, HuggingFace, Vertex AI
- **Monitoring:** Sentry, Datadog, LogRocket, PostHog, Amplitude
- **CDN/Edge:** Vercel, Cloudflare, Fastly
- **Messaging:** Twilio, Vonage, Slack API, Discord API

For each detected service, record: name, detected config key or import, and which component uses it.

## 5. Data Flow Scenarios (Top Priority Ranking)

Rank scenarios by user impact for the Communication Flow Panel:
1. Primary user action (the core thing the app does)
2. User authentication flow
3. Data creation/mutation flow
4. Notification/async flow
5. Error/fallback flow
