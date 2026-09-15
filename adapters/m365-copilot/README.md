# Talyx Setup - Microsoft 365 Copilot Agent Builder

Use the instruction file below. The supplied provisional answer file contains the canonical questions and parameter reference.

## Agent instructions

Copy all of [copilot-agent-instructions.txt](copilot-agent-instructions.txt) into the agent Instructions. It collects provisional answers using the canonical free Setup questions. It does not handwrite or activate configuration.

## Create and use

1. In Microsoft 365 Copilot, choose **New agent → Skip to configure**. Name it **Talyx Setup**.
2. Paste the supplied instruction file into Instructions. Under **Configure → Knowledge → Upload**, add [talyx-company-setup.txt](talyx-company-setup.txt).
3. Test the agent, then use **Create** to save it when the app offers that action. Ask “Set up Talyx for my company.” A worksheet is optional.
4. Save the provisional answer file and replace its Knowledge copy. Use a supported local Talyx runtime to validate and save the actual configuration with the bundled writer.

[Microsoft knowledge instructions](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-knowledge)

## Status and acceptance

Prepared adaptation; live creation, question forms, validation, saving and reuse have not been verified in this host. Test with a company, input, output and reviewer already stated: it should ask only for missing facts, collect only evidenced parameters, label them provisional, then read the updated Knowledge copy in a new chat. Validated config generation requires the bundled local writer. This is separate from a repository plugin install.

Requires an eligible Microsoft 365 work tenant and Agent Builder access; this is not consumer Copilot or GitHub Copilot. Native skill ZIP import is a separate Frontier preview route with additional account requirements. Public ISV distribution of custom-skill agents is not assumed. [Microsoft skill preview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder-add-skills)
