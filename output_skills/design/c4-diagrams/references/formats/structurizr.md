# Structurizr DSL

Structurizr DSL is a modeling language for C4 architecture. It defines the model (elements and relationships) separately from views (which diagrams to render). The user pastes the output into [playground.structurizr.com](https://playground.structurizr.com) to see rendered diagrams.

Always produce a complete, self-contained `workspace.dsl` file.

## Contents
- Structure — workspace/model/views hierarchy
- Model Elements — people, systems, containers, components
- Relationships — connecting elements
- Views — system context, container, component, dynamic, deployment
- Selective Include/Exclude — controlling what appears
- Layout — auto-layout options
- Styles — visual customization
- Complete Example — full banking system workspace
- Segmenting Large Systems — focused views for complex systems

## Structure

```
workspace "Name" "Description" {
    model {
        // elements and relationships
    }
    views {
        // which diagrams to render
    }
}
```

## Model Elements

Assign identifiers to reference elements later in relationships and views.

```
model {
    user = person "Customer" "Places and tracks orders"

    orderSystem = softwareSystem "Order System" "Handles order lifecycle" {
        webapp = container "Web Application" "Customer-facing UI" "React"
        api = container "API" "Order processing" "Node.js, Express"
        db = container "Database" "Stores orders and customers" "PostgreSQL"
        queue = container "Message Queue" "Async order events" "RabbitMQ"
    }

    emailSystem = softwareSystem "Email System" "Sends transactional email" "Existing"

    // Components go inside a container
    api2 = container "API" "Order processing" "Node.js" {
        orderController = component "Order Controller" "Handles HTTP requests" "Express Router"
        orderService = component "Order Service" "Business logic" "TypeScript"
        orderRepo = component "Order Repository" "Data access" "Knex"
    }
}
```

Element syntax: `identifier = elementType "Name" "Description" "Technology" "Tags"`
- Person: `person "Name" "Description"`
- Software System: `softwareSystem "Name" "Description"`
- Container: `container "Name" "Description" "Technology"`
- Component: `component "Name" "Description" "Technology"`

## Relationships

```
user -> webapp "Places orders" "HTTPS"
webapp -> api "Makes API calls" "REST/JSON"
api -> db "Reads/writes" "SQL/TCP"
api -> queue "Publishes order events" "AMQP"
orderSystem -> emailSystem "Sends order confirmations" "SMTP"
```

Syntax: `source -> destination "Description" "Technology"`

Within an element block, use `this`:
```
api = container "API" "Order processing" "Node.js" {
    this -> db "Reads/writes" "SQL"
}
```

## Views

Each view type selects which elements to show.

### System Context
```
views {
    systemContext orderSystem "SystemContext" "System Context for Order System" {
        include *
        autoLayout
    }
}
```
`include *` adds the system in scope plus all directly connected people and systems.

### Container
```
views {
    container orderSystem "Containers" "Container view of Order System" {
        include *
        autoLayout
    }
}
```
Shows all containers within the system plus connected people and external systems.

### Component
```
views {
    component api "Components" "API internals" {
        include *
        autoLayout
    }
}
```

### Multiple Views in One File
Produce multiple views to show different zoom levels:
```
views {
    systemContext orderSystem "Context" {
        include *
        autoLayout
    }
    container orderSystem "Containers" {
        include *
        autoLayout
    }
    component api "APIComponents" {
        include *
        autoLayout
    }
}
```

## Layout

`autoLayout` uses automatic layout. Options:
- `autoLayout` — top to bottom (default)
- `autoLayout lr` — left to right
- `autoLayout rl` — right to left
- `autoLayout bt` — bottom to top
- `autoLayout tb 300 200` — with rank and node separation

For most diagrams, `autoLayout` or `autoLayout lr` works well.

## Selective Include/Exclude

Control what appears in a view:
```
container orderSystem "Containers" {
    include *
    exclude queue
    autoLayout
}
```

Include specific elements:
```
container orderSystem "FrontendView" {
    include user
    include webapp
    include api
    autoLayout
}
```

## Styles

Add visual styling in the views block:
```
views {
    styles {
        element "Person" {
            shape Person
            background #08427B
            color #ffffff
        }
        element "Software System" {
            background #1168BD
            color #ffffff
        }
        element "Container" {
            background #438DD5
            color #ffffff
        }
        element "Component" {
            background #85BBF0
            color #000000
        }
        element "Existing" {
            background #999999
            color #ffffff
        }
        relationship "Relationship" {
            color #707070
        }
    }
}
```

Tag external systems with "Existing" to visually distinguish them:
```
emailSystem = softwareSystem "Email System" "Sends email" "Existing"
```

## Complete Example

A minimal but complete workspace showing System Context and Container levels:

```
workspace "Internet Banking System" "Architecture of the Internet Banking System" {

    model {
        customer = person "Personal Banking Customer" "A customer of the bank"

        bankingSystem = softwareSystem "Internet Banking System" "Allows customers to manage accounts and make payments" {
            webapp = container "Web Application" "Serves the static content and the single-page app" "Java, Spring Boot"
            spa = container "Single-Page Application" "Provides banking functionality via the browser" "JavaScript, React"
            api = container "API Application" "Provides banking functionality via a JSON API" "Java, Spring Boot"
            db = container "Database" "Stores user data, accounts, transactions" "PostgreSQL"
        }

        mainframe = softwareSystem "Mainframe Banking System" "Stores core banking data" "Existing"
        email = softwareSystem "Email System" "Sends emails to customers" "Existing"

        customer -> webapp "Visits" "HTTPS"
        customer -> spa "Manages accounts" "HTTPS"
        spa -> api "Makes API calls" "REST/JSON, HTTPS"
        api -> db "Reads/writes" "SQL/TCP"
        api -> mainframe "Gets account data" "XML/HTTPS"
        api -> email "Sends notifications" "SMTP"
    }

    views {
        systemContext bankingSystem "SystemContext" {
            include *
            autoLayout
        }

        container bankingSystem "Containers" {
            include *
            autoLayout
        }

        styles {
            element "Person" {
                shape Person
                background #08427B
                color #ffffff
            }
            element "Software System" {
                background #1168BD
                color #ffffff
            }
            element "Existing" {
                background #999999
                color #ffffff
            }
            element "Container" {
                background #438DD5
                color #ffffff
            }
        }
    }
}
```

## Segmenting Large Systems

When a system has many containers, create focused views instead of one massive diagram:

```
views {
    container bankingSystem "Frontend" "Frontend containers" {
        include customer
        include webapp
        include spa
        include api
        autoLayout
    }

    container bankingSystem "Backend" "Backend and data stores" {
        include api
        include db
        include mainframe
        include email
        autoLayout
    }
}
```

Group by user persona, use case, or logical boundary — whichever tells the clearest story.
