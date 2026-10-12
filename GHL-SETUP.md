# Connecting the quote form to GoHighLevel

Every page uses the same form and script: `_build/ghl-form.js` (copied to `public/assets/ghl-form.js` on build).

## Option 1: Inbound Webhook (recommended, keeps the custom design)

1. GHL > Automation > Workflows > Create Workflow > Start from scratch.
2. Trigger: **Inbound Webhook**. Copy the URL.
3. Paste it in `_build/ghl-form.js` (copied to `public/assets/ghl-form.js` on build):
   ```js
   var GHL_WEBHOOK_URL = "https://services.leadconnectorhq.com/hooks/XXXX/webhook-trigger/YYYY";
   ```
   Or set it on one form only: `<form data-ghl-form data-ghl-webhook="...">`.
4. Submit one test lead from the site so GHL sees the payload.
5. Add action **Create/Update Contact** and map fields:

| Form field | GHL field |
|---|---|
| `first_name` | First Name |
| `phone` | Phone (sent as +1XXXXXXXXXX) |
| `email` | Email |
| `address1` | Street Address |
| `city` | City |
| `postal_code` | Postal Code |
| `service_needed` | Custom field: Service Needed |
| `page_city` | Custom field: Website Area (which city page the lead came from) |
| `sms_consent` | Custom field: SMS Consent (true/false) |
| `lead_source`, `page_url`, `utm_*`, `gclid` | Custom fields or contact source |
| `tags` | Add Tag (`website lead` + the service) |

6. Next actions: create an Opportunity in your pipeline, send the instant text back, notify the owner.

## Option 2: GHL native form embed

Sites > Forms > build the form > Integrate > copy the embed code.
Replace the form in `intake_form()` in `_build/build.py` with the embed and rebuild.
Easier to set up, but the form uses GHL styling.

## Notes

- Without a webhook URL, the form still validates and goes to `thank-you.html` so it can be demoed.
- `thank-you.html` is `noindex`. Point your Google Ads / GA4 conversion at it.
- The SMS consent checkbox language supports A2P 10DLC registration. Keep it.
