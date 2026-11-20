# Canva REST API Authentication & Scopes

Canva utilizes OAuth 2.0 with PKCE for user-authorized access tokens.

## Scopes Reference

| Scope | Description |
| :--- | :--- |
| `design:read` | Read user designs, slide contents, metadata, and export links |
| `design:content:write` | Mutate design canvas elements, text, styles, and layouts in editing sessions |
| `design:meta:write` | Update document titles and metadata |
| `brandkit:read` | Access organization brand kits, color palettes, and typography tokens |
| `asset:read` | List and inspect uploaded media items |
| `asset:write` | Upload new image and video assets to Canva library |
| `comment:read` | Inspect comment threads, mentions, and review feedback |
| `comment:write` | Reply to comments, resolve feedback threads |
| `brandtemplate:read` | Query brand template datasets and field schemas |
| `brandtemplate:meta:read`| Access brand template previews and configuration |

## CLI Profile Management
```bash
# Authenticate default profile
canva login

# Headless / CI/CD environment
canva login --mode manual

# Profile switching
canva login --profile production-team
canva api designs list --profile production-team
```
