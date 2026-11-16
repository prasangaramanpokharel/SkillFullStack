# Automated Code Review Assignment Reference

GitHub allows teams to automatically route Pull Requests to team members using two primary algorithms:

## 1. Routing Algorithms
- **Round-Robin**: Alternates assignments sequentially through team members. Guarantees fair, equal distribution of review duties.
- **Load-Balancing**: Assigns reviews based on each member's current open review count. Prevents overloading busy developers.

## 2. API Configuration Pattern
```bash
# Configure team review assignment via GitHub API
gh api -X PATCH /orgs/:org/teams/:team_slug \
  -f review_request_delegation[enabled]=true \
  -f review_request_delegation[algorithm]="ROUND_ROBIN" \
  -f review_request_delegation[member_count]=1 \
  -f review_request_delegation[notify_team]=false
```
