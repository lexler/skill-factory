# Mermaid C4 Diagrams

Renders natively in GitHub, GitLab, and many markdown tools. Mermaid's C4 support is experimental but functional.

These illustrate the syntax. Consider what fits your context.

## Diagram Types

Each C4 diagram level has its own Mermaid diagram type:

- `C4Context` — System Context diagrams
- `C4Container` — Container diagrams
- `C4Component` — Component diagrams
- `C4Dynamic` — Dynamic diagrams
- `C4Deployment` — Deployment diagrams

## Elements

### People

```
Person(alias, "Label", "Description")
Person_Ext(alias, "Label", "Description")
```

### Software Systems

```
System(alias, "Label", "Description")
System_Ext(alias, "Label", "Description")
SystemDb(alias, "Label", "Description")
SystemQueue(alias, "Label", "Description")
SystemDb_Ext(alias, "Label", "Description")
SystemQueue_Ext(alias, "Label", "Description")
```

### Containers

```
Container(alias, "Label", "Technology", "Description")
Container_Ext(alias, "Label", "Technology", "Description")
ContainerDb(alias, "Label", "Technology", "Description")
ContainerQueue(alias, "Label", "Technology", "Description")
ContainerDb_Ext(alias, "Label", "Technology", "Description")
ContainerQueue_Ext(alias, "Label", "Technology", "Description")
```

### Components

```
Component(alias, "Label", "Technology", "Description")
Component_Ext(alias, "Label", "Technology", "Description")
ComponentDb(alias, "Label", "Technology", "Description")
ComponentQueue(alias, "Label", "Technology", "Description")
```

### Deployment Nodes

```
Deployment_Node(alias, "Label", "Type", "Description")
Node(alias, "Label", "Type", "Description")
Node_L(alias, "Label", "Type", "Description")
Node_R(alias, "Label", "Type", "Description")
```

## Boundaries

Group elements visually:

```
Boundary(alias, "Label", "Type")
Enterprise_Boundary(alias, "Label")
System_Boundary(alias, "Label")
Container_Boundary(alias, "Label")
```

Boundaries use block syntax — elements inside the boundary go between the boundary declaration and a closing `}`:

```
System_Boundary(b1, "Internet Banking System") {
    Container(spa, "SPA", "React", "Banking UI")
    Container(api, "API", "Spring Boot", "Banking logic")
    ContainerDb(db, "Database", "PostgreSQL", "Account data")
}
```

## Relationships

```
Rel(from, to, "Label", "Technology")
Rel(from, to, "Label")
BiRel(from, to, "Label", "Technology")
```

Directional hints (suggest layout positioning):

```
Rel_U(from, to, "Label")    %% or Rel_Up
Rel_D(from, to, "Label")    %% or Rel_Down
Rel_L(from, to, "Label")    %% or Rel_Left
Rel_R(from, to, "Label")    %% or Rel_Right
Rel_Back(from, to, "Label")
```

For Dynamic diagrams, use indexed relationships:

```
RelIndex(1, from, to, "Label")
RelIndex(2, from, to, "Label")
```

## Styling

Override element appearance:

```
UpdateElementStyle(alias, $bgColor="blue", $fontColor="white", $borderColor="darkblue")
```

Override relationship appearance:

```
UpdateRelStyle(from, to, $textColor="red", $lineColor="red", $offsetX="-40", $offsetY="60")
```

Control layout density:

```
UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

Parameters can be positional or named with `$` prefix.

## System Context Example

```mermaid
C4Context
    title System Context diagram for Internet Banking System

    Person(customer, "Customer", "A bank customer")
    
    System(bankSystem, "Internet Banking System", "Allows customers to manage accounts")
    
    System_Ext(mainframe, "Mainframe", "Core banking system")
    System_Ext(email, "E-mail System", "Sends notifications")

    Rel(customer, bankSystem, "Manages accounts using")
    Rel(bankSystem, mainframe, "Gets account data from", "XML/HTTPS")
    Rel(bankSystem, email, "Sends notifications via", "SMTP")

    UpdateLayoutConfig($c4ShapeInRow="3")
```

## Container Example

```mermaid
C4Container
    title Container diagram for Internet Banking System

    Person(customer, "Customer", "A bank customer")

    System_Boundary(b1, "Internet Banking System") {
        Container(spa, "Single-Page App", "React", "Banking UI")
        Container(api, "API Application", "Spring Boot", "Banking logic")
        ContainerDb(db, "Database", "PostgreSQL", "Stores accounts, transactions")
    }

    System_Ext(mainframe, "Mainframe", "Core banking system")
    System_Ext(email, "E-mail System", "Sends notifications")

    Rel(customer, spa, "Manages accounts using", "HTTPS")
    Rel(spa, api, "Makes API calls to", "JSON/HTTPS")
    Rel(api, db, "Reads/writes", "JDBC")
    Rel(api, mainframe, "Gets account data from", "XML/HTTPS")
    Rel(api, email, "Sends notifications via", "SMTP")
```

## Dynamic Example

```mermaid
C4Dynamic
    title Sign-in flow for Internet Banking System

    ContainerDb(db, "Database", "PostgreSQL", "Stores credentials")
    Container(spa, "SPA", "React", "Banking UI")
    Container(api, "API", "Spring Boot", "Banking logic")

    RelIndex(1, spa, api, "Submits credentials", "JSON/HTTPS")
    RelIndex(2, api, db, "Validates credentials", "JDBC")
    RelIndex(3, api, spa, "Returns session token", "JSON/HTTPS")
```

## Deployment Example

```mermaid
C4Deployment
    title Production deployment for Internet Banking System

    Deployment_Node(aws, "AWS", "Cloud") {
        Deployment_Node(ecs, "ECS Cluster", "Amazon ECS") {
            Container(api, "API Application", "Spring Boot", "Banking logic")
            Container(spa, "Single-Page App", "React", "Banking UI")
        }
        Deployment_Node(rds, "RDS", "Amazon RDS") {
            ContainerDb(db, "Database", "PostgreSQL", "Account data")
        }
    }

    Rel(spa, api, "Makes API calls to", "JSON/HTTPS")
    Rel(api, db, "Reads/writes", "JDBC")
```

## Limitations

Mermaid's C4 support does not include:
- Sprites/icons
- Tags
- Clickable links
- Layout directives (Lay_U, Lay_D, etc.)
- Custom stereotypes
- Legends (must be implied through consistent naming)

Layout control is limited — use `UpdateLayoutConfig` and directional `Rel_` hints for rough positioning, but expect less control than Structurizr.
