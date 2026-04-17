# VPN Access Setup

## Overview
All developers must connect to the TechCorp VPN to access internal systems, repositories, and databases. The VPN uses Cisco AnyConnect with MFA authentication.

## Prerequisites
- Active Directory account (provisioned on Day 1)
- Microsoft Authenticator app installed on your phone
- MFA enrollment completed (see Day 1 Checklist)

## Installation
1. Download Cisco AnyConnect from `software.techcorp.com/vpn`
2. Install with default settings. Administrator privileges required.
3. On macOS: grant Full Disk Access in System Preferences > Privacy & Security.

## Connection Steps
1. Open Cisco AnyConnect client.
2. Enter the VPN gateway: `vpn.techcorp.internal`
3. Select your region: US-East (default), US-West, EU-London, AP-Singapore.
4. Enter your AD credentials (same as laptop login).
5. Approve the MFA push notification on Microsoft Authenticator.
6. Connection establishes in 5-10 seconds.

## Split Tunnel Configuration
By default, only TechCorp traffic routes through the VPN. Internet traffic goes direct. This is the recommended configuration for performance. If you need full tunnel (e.g., for compliance testing), contact the Network team: network@techcorp.com.

## Troubleshooting
| Issue | Solution |
|-------|----------|
| "Connection attempt failed" | Restart the AnyConnect service. On Windows: `net stop vpnagent && net start vpnagent` |
| MFA prompt not received | Ensure Authenticator has notification permissions enabled. Try "I can't use the app" for SMS fallback. |
| Slow connection | Switch to a closer regional gateway. Check if you're on full tunnel accidentally. |
| "Certificate validation failure" | Update AnyConnect to the latest version from `software.techcorp.com/vpn` |

## Network Access After VPN
Once connected, you can access:
- GitHub Enterprise: `github.techcorp.com`
- Jenkins CI: `jenkins.techcorp.internal`
- Staging environment: `staging.techcorp.internal`
- Internal wikis: `confluence.techcorp.com`
- Databases: via connection strings in your team's `.env` files

## Support
For VPN issues not resolved by troubleshooting, contact IT Helpdesk: helpdesk@techcorp.com or #it-helpdesk on Slack.
