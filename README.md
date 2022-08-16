# Home Assistant Custom Components

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Discord](https://img.shields.io/discord/330944238910963714?label=discord)](https://discord.gg/AnNenrd2)

Custom Component for [Home Assistant](http://www.home-assistant.io).

## Microsoft Graph API Component

Component to interface with Microsoft's Graph API on your organization's tenant.
Currently only detects the authorized user's Microsoft Teams availability and activity but the possibilities are almost endless.

The Microsoft Graph integration allows Home Assistant to create sensors from various properties of your Office 365 tenant via Microsoft's Graph API. All queries are performed using the authenticated user's account and depend on the permissions granted when creating the Azure AD application.

Home Assistant authenticates with Microsoft through OAuth2. Set up your credentials by completing the steps in [Manual Configuration](#manual-configuration) and then add the integration in **Configuration -> Integrations -> Microsoft Graph**. Ensure you log in using a Microsoft account that belongs to your organization's tenant.

- [Home Assistant Custom Components](#home-assistant-custom-components)
  - [Microsoft Graph API Component](#microsoft-graph-api-component)
    - [Installation](#installation)
    - [Manual Configuration](#manual-configuration)
    - [Sensor](#sensor)
      - [Microsoft Teams](#microsoft-teams)

### Installation

- If it doesn't already exist, create a directory called `microsoft_graph` under `config/custom_components/`.
- Copy all files in `custom_components/microsoft_graph` to your `config/custom_components/microsoft_graph/` directory.
- Restart Home Assistant to pick up the new integration.
- Configure with config below.

### Manual Configuration

You will need to register an application in Azure AD and retrieve the client ID and client secret:


#### MS Azure account set up
- Register a new application in Azure AD, Click “New Registration”
  - URL: https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
  - Name your application
  - Select "Accounts in any organizational directory (Any Azure AD directory - Multitenant)" under supported account types
  - Ignore Redirect URI (for now), click “Register”
- You will now be on the “Overview” page for your app, copy the “Application (client) ID” value and save it for later
- In the left menu, select “Authentication”
  - Click “Add a platform”
  - Select “Web”
  - Add **https://<EXTERNAL_HOME_ASSISTANT_URL>:PORT/auth/external/callback**
  - Click the “Configure” button
  - Still In the Authentications Tab, select “Add URI” 
  - Paste in **https://my.home-assistant.io/redirect/oauth**
  - Scroll down and ticket “Access tokens” and “ID Tokens” check boxes
  - Scroll down further, select the “Accounts in any organizational directory (Any Azure AD directory - Multitenant)” radio button
  - Click the “Save” button
- In the left menu, select “Certificates & secrets”
  - Click “New client secret”
  - Set a description and expiration date (max 24 months), click the “add” button
  - You will now be presented a ‘value’ and ‘secret ID’. Copy the **"value"** field and save it for later
- In the left menu, select “API Permissions”
  - Click “Add a Permission”
  - Select “Microsoft Graph”
  - Select “Delegated Permissions”
  - Search for Presence.Read, expand “Presence” and select “Presence.Read” and “Presence.Read.All”
  - Search for User.Read, expand “User” and select “User.Read” and “User.ReadBasic.All”
  - Click the “Add permissions” button
- **You are done with Azure**



#### Home Assistant Setup
- Go to settings > Devices & services > Add Integration > Microsoft Graph
- Input your **ClientID** and **Secret Value** from earlier, click “next”
- A new tab will open with “Link account to Home Assistant?”, Click “Link account”


### Sensor

The Microsoft Graph sensor platform automatically tracks various resources from your Office 365 tenant.

#### Microsoft Teams

There are 2 sensors that are added, both of which are enabled by default.

| Entity ID | Default | Description                                                                                        |
| ---------------------------------| ------ | -----------------------------------------------------------------------------|
| `sensor.ms_teams_availability` | Enabled  | Shows your availability (e.g. Available, AvailableIdle, Away).               |
| `sensor.ms_teams_activity`     | Enabled  | Shows your activity (e.g. InACall, InAConferenceCall, Inactive, InAMeeting). |

See possible availability and activity values [here](https://docs.microsoft.com/en-us/graph/api/resources/presence?view=graph-rest-beta#properties).
