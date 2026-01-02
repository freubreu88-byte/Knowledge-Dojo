---
created: 2026-01-02 13:07:31.054414
id: 01KDZ9P4ZE6MMDXJ0QZHK1TTGX
next_review: '2026-01-03'
prereqs: []
review_count: 0
source_id: 01KDZ88G6ZWHXK367H6888PJRH
status: failed
timebox_min: 20
topics:
- Payment Processing
- Stripe API
- Backend Development
- Claude Skills
- API Integration
type: drill
---

# Integrate Stripe Payments using Claude's Stripe Integration Skill

## Pattern
- Automate the integration of complex third-party payment gateways like Stripe.
- Understand how Claude Skills can handle multi-step processes including database setup, API routes, and frontend integration.
- Configure environment variables (API keys) for external service integrations.

## Drill
**Goal:** Implement a functional Stripe payment integration, including subscription tiers and a free trial, into a sample application using the Stripe Integration skill.

**Steps:**
1. Download the 'Stripe integration' skill folder (as described around 13:19).
2. Add the downloaded skill folder to your Claude project's 'skills' directory (see 13:22).
3. Restart your Claude session to ensure the new skill is recognized (see 13:26).
4. Prompt Claude to integrate Stripe payment into your application (see 13:29).
5. Answer Claude's clarifying questions regarding free trial duration, Stripe API keys availability, and plan upgrade/downgrade options (see 14:26).
6. Obtain your Stripe publishable key, secret key, webhook secret, and pricing IDs from your Stripe dashboard (see 14:46) and add them to your application's `.env.local` file (see 16:34).

## Snippet
```prompt
# Assumes the 'Stripe integration' skill folder has been added to your Claude project's skills directory and your Claude session has been restarted.
# Replace 'the application right now' with a brief description or context of your app.
Based on the application right now, please use the Stripe integration skill to integrate our Stripe payment inside of our application.
```

## Validation
- [ ] Claude generates a detailed plan for Stripe integration, including payment structure and database setup (see 15:13).
- [ ] The application's `.env.example` file is updated with necessary Stripe environment variables (see 16:34).
- [ ] The application's UI presents the new subscription tiers (e.g., Starter, Growth, Pro) (see 16:30).
- [ ] A test payment via the integrated Stripe checkout page is successful, leading to an active subscription in the application (see 17:34).
- [ ] The application's settings reflect the active growth tier subscription (see 17:39).

## Failure Modes
- Common pitfall 1
- Common pitfall 2

## Next Variation
- Try variation 1
- Try variation 2
