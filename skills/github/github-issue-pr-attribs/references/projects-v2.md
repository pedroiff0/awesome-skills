# Attaching a GitHub Projects V2 item (GraphQL)

`gh issue create --project` / `gh pr create --project` target **Projects (classic, v1)** via REST and return 404 for **Projects V2**. To attach an item to a V2 project, use the GraphQL `addProjectV2ItemById` mutation after creating the issue/PR.

## 1. Find the project and its owner node ID

```bash
gh api graphql -f query='query{
  user(login:"pedroiff0"){projectsV2(first:10){nodes{id title number}}}
}'
# For an org project: replace `user(login:...)` with `organization(login:...)`
```

Take the `id` of the target project (e.g. `PVT_kwHOCDc9HM4Bfzbo`).

## 2. Get the issue/PR node ID

```bash
# Issue
gh api graphql -f query='query{
  repository(owner:"pedroiff0",name:"financas-app"){
    issue(number:287){id}
  }
}'
# PR
gh api graphql -f query='query{
  repository(owner:"pedroiff0",name:"financas-app"){
    pullRequest(number:288){id}
  }
}'
```

## 3. Add the item to the project

```bash
gh api graphql -f query='mutation{
  addProjectV2ItemById(input:{
    projectId:"PVT_kwHOCDc9HM4Bfzbo"
    contentId:"<ISSUE_OR_PR_NODE_ID>"
  }){item{id}}
}'
```

## 4. Verify (REST shows projectCards:null for V2 — use GraphQL)

```bash
gh api graphql -f query='query{
  repository(owner:"pedroiff0",name:"financas-app"){
    pullRequest(number:288){
      projectItems(first:10){nodes{project{title}}}
    }
  }
}'
```

> Tip: create a small helper that resolves a project title → id and an issue/PR number → contentId, then calls the mutation. Keep the project id cached; it doesn't change.
