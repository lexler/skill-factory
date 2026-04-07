# ASCII C4 Diagrams

Text-based diagrams that work everywhere: inline documentation, chat, code review comments, terminals. No rendering tools needed.

These illustrate conventions. Adapt the layout to fit your specific diagram.

## Element Representation

### People

```
   .--.
   |  |
   '--'
  Person
 [Role/desc]
```

Or simplified:

```
[Person Name]
  (Role)
```

### Software Systems, Containers, Components

Use boxes with name, type, technology, and description:

```
+-----------------------------------+
|    Internet Banking System        |
|       [Software System]           |
|                                   |
|  Allows customers to manage       |
|  their bank accounts              |
+-----------------------------------+
```

```
+-----------------------------------+
|        API Application            |
|   [Container: Spring Boot]        |
|                                   |
|  Provides banking functionality   |
|  via JSON/HTTPS API               |
+-----------------------------------+
```

### External Elements

Distinguish external elements with dashed borders:

```
- - - - - - - - - - - - - - - - - -
:       Mainframe System            :
:     [Software System]             :
:                                   :
:  Core banking functionality       :
- - - - - - - - - - - - - - - - - -
```

### Databases

```
  +-----------------------+
 /                         \
|       Database            |
| [Container: PostgreSQL]   |
|                           |
| Stores account data       |
 \                         /
  +-----------------------+
```

Or simplified:

```
[(Database)]
[Container: PostgreSQL]
```

## Relationships

Use ASCII arrows with labels:

```
[Customer] ---"Manages accounts using"---> [Banking System]
```

For vertical layouts:

```
    [SPA]
      |
      | "JSON/HTTPS"
      v
    [API]
      |
      | "JDBC"
      v
  [(Database)]
```

## Boundaries

Use labeled borders to group elements:

```
+============================================+
|        Internet Banking System             |
|                                            |
|   +--------+    +--------+    +--------+   |
|   |  SPA   |--->|  API   |--->|   DB   |   |
|   | React  |    | Spring |    | PgSQL  |   |
|   +--------+    +--------+    +--------+   |
|                                            |
+============================================+
```

## System Context Example

```
                        +----------------------------------+
                        |    Internet Banking System       |
   .--.                 |      [Software System]           |
   |  |  --"Uses"-----> |                                  |
   '--'                 | Allows customers to manage       |
 Customer               | their bank accounts              |
                        +----------------------------------+
                              |                    |
                "Gets account |                    | "Sends
                 data from"   |                    |  emails via"
                 XML/HTTPS    |                    |  SMTP
                              v                    v
                  - - - - - - - - - -    - - - - - - - - - -
                  :    Mainframe    :    :  E-mail System  :
                  :  [Ext. System]  :    : [Ext. System]   :
                  - - - - - - - - - -    - - - - - - - - - -
```

## Container Example

```
   .--.
   |  | Customer
   '--'
     |
     | "Uses" / HTTPS
     v
+================================================================+
|                  Internet Banking System                        |
|                                                                |
|  +----------------+     +------------------+     +-----------+ |
|  | Single-Page    |     |  API Application |     | Database  | |
|  | App            |---->|                  |---->|           | |
|  | [Container:    |JSON/| [Container:      |JDBC | [Container| |
|  |  React]        |HTTPS|  Spring Boot]    |     |  PgSQL]   | |
|  +----------------+     +------------------+     +-----------+ |
|                                |                               |
+================================================================+
                                 |
                   "Gets account | XML/HTTPS
                    data from"   |
                                 v
                     - - - - - - - - - - -
                     :     Mainframe     :
                     :   [Ext. System]   :
                     - - - - - - - - - - -
```

## Layout Guidelines

- Place the primary element or initiator at the top or left
- Flow generally top-to-bottom or left-to-right
- Keep relationship labels close to the arrow they describe
- Align boxes for readability — exact pixel perfection isn't the goal, clarity is
- Use consistent box widths within a diagram where practical
- For complex diagrams, prioritize readable flow over compact layout

## Title and Legend

Always include at the top:

```
System Context diagram for Internet Banking System
===================================================

Legend:
  [---]  Internal system
  [- -]  External system
  --->   Relationship (direction of dependency/data flow)
```
