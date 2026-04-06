# Deployment Diagram

Source: https://c4model.com/diagrams/deployment

## Purpose
Shows how container instances from the static model map to infrastructure in a specific deployment environment (production, staging, dev).

## Scope
One or more software systems within a single deployment environment.

## Audience
Technical people: architects, developers, infrastructure architects, ops/SRE.

## Elements

**Deployment Nodes** — where things run. Can be nested to show layers:
- Physical infrastructure (servers, devices)
- Virtualized infrastructure (VMs, IaaS, PaaS)
- Containerized infrastructure (Docker, Kubernetes pods)
- Execution environments (JVM, application servers, database engines)

**Container Instances** — running instances of containers from the static model, placed inside deployment nodes.

**Software System Instances** — for external systems shown as black boxes in the deployment.

**Infrastructure Nodes** — supporting infrastructure: DNS, load balancers, firewalls, CDNs. Optional but recommended for a complete picture.

## What to Include
- The deployment environment name (production, staging, etc.)
- Deployment nodes nested to show the real infrastructure layers
- Container instances mapped to their deployment nodes
- Infrastructure nodes that affect the architecture (load balancers, firewalls)
- Communication paths between deployment nodes

## What to Exclude
- Application internals — components and code don't belong here
- Multiple environments in one diagram — create separate diagrams per environment

## Nesting Example
```
AWS Region
  └── VPC
       ├── Public Subnet
       │    └── ALB (load balancer)
       └── Private Subnet
            ├── ECS Cluster
            │    ├── API container instance
            │    └── Web App container instance
            └── RDS
                 └── Database container instance
```

## Common Mistakes
- Confusing Container diagrams with Deployment diagrams — Container shows what's inside the system; Deployment shows where it runs
- Showing one giant diagram for all environments — separate them
- Omitting infrastructure nodes — load balancers and firewalls are architecturally significant
