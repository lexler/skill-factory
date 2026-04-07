# Deployment Diagram

Shows how software system and container instances map to infrastructure in a specific environment.

## Scope

One or more software systems within a single deployment environment (production, staging, development, etc.).

## Elements

- **Primary**: Deployment nodes, software system instances, container instances
- **Supporting**: Infrastructure nodes (DNS, load balancers, firewalls, CDNs)

## Audience

Technical people — developers, architects, infrastructure engineers, operations staff. Answers: "How is this deployed, and where does each piece run?"

## What "Deployment Node" Means

A deployment node is where a container instance runs:
- Physical servers or devices
- Virtual machines (EC2, Azure VMs)
- Container orchestration (Kubernetes pods, ECS tasks)
- Platform services (Heroku dynos, App Engine instances)
- Database services (RDS, Cloud SQL)
- Serverless platforms (Lambda, Cloud Functions)

Deployment nodes can nest: a physical server contains a VM, which contains a Docker host, which contains container instances.

## Nesting Example

Deployment nodes form a containment hierarchy. A typical AWS-hosted system might nest like this:

```
AWS Region [us-east-1]
  └── VPC
       ├── Public Subnet
       │    └── Application Load Balancer
       │         └── Routes traffic to ECS Cluster
       └── Private Subnet
            ├── ECS Cluster
            │    ├── Web App Service [2x ECS Tasks]
            │    │    └── Web App Container [Node.js]
            │    └── API Service [3x ECS Tasks]
            │         └── API Container [Spring Boot]
            └── RDS Instance
                 └── Database [PostgreSQL 15]
```

The same nesting can be drawn with C4 boundary boxes in any format. The key is that the parent deployment node visually contains its children, and container instances live at the leaves.

## What to Include

- Deployment nodes with technology labels
- Container instances mapped to their deployment nodes
- Infrastructure nodes (load balancers, firewalls, DNS, CDNs)
- Communication paths between deployment nodes with protocols
- Instance counts where relevant (3x web servers, 2x read replicas)
- The specific environment being documented

## What NOT to Include

- Logical architecture (that's in Container/Component diagrams)
- Multiple environments in one diagram — create one per environment
- Application-level details (components, classes)

## When to Create

- When deployment topology matters for understanding (especially multi-environment setups)
- For operations runbooks
- When planning infrastructure changes
- To document auto-scaling, failover, or replication strategies

## Tips

- Create separate diagrams per environment when they differ significantly
- Use provider-specific icons (AWS, Azure, GCP) to make nodes recognizable — but explain them in the legend
- Show instance counts and scaling ranges where they matter

Source: https://c4model.com/diagrams/deployment
