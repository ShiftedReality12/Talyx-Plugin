# Connectors

Skills never name a product. They say *read from `sources`* or *find the intake email*, and
whatever you have connected in that category does the work. Nothing here is bundled or run
by Talyx; each connector is yours, authorized by you, and a skill only uses the ones you have.

`.mcp.json` lists the ones below so your AI app can show which are connected and offer to
connect the rest. A connector you do not use is simply ignored.

| Connector | Category | How it is reached |
|---|---|---|
| google drive | Files | your Claude connector |
| gmail | Email | your Claude connector |
| google calendar | Calendar | your Claude connector |
| microsoft 365 | Files, Email, Calendar (SharePoint · Outlook · Teams) | your Claude connector |
| quickbooks | Accounting | the vendor's own endpoint, your account |
| docusign | Signatures | the vendor's own endpoint, your account |
| box | Files | the vendor's own endpoint, your account |
| slack | Chat | the vendor's own endpoint, your account |

Systems without a connector (a land system, a portfolio platform, a regulator's portal)
are named in your config as `sources` and reached by export or upload.
